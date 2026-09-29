from __future__ import annotations

import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier


MODEL_PATH = Path("models/snn_pipeline.pkl")


def _softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - np.max(logits, axis=1, keepdims=True)
    exp = np.exp(shifted)
    return exp / np.sum(exp, axis=1, keepdims=True)


def _sigmoid(values: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-values))


@dataclass
class DatasetBundle:
    x_train: np.ndarray
    x_test: np.ndarray
    y_train: np.ndarray
    y_test: np.ndarray


@dataclass
class PipelineArtifacts:
    ann: MLPClassifier
    snn_weights: dict[str, np.ndarray | float | int]
    generator: dict[str, np.ndarray | float | int]
    metrics: dict[str, float]
    dataset: DatasetBundle


class LightweightSNNPipeline:
    def __init__(self, artifacts: PipelineArtifacts):
        self.artifacts = artifacts
        self.ann = artifacts.ann
        self.snn = artifacts.snn_weights
        self.generator = artifacts.generator

    @staticmethod
    def load_digits_dataset(random_state: int = 42) -> DatasetBundle:
        digits = load_digits()
        x = digits.data.astype(np.float32) / 16.0
        y = digits.target.astype(np.int64)
        x_train, x_test, y_train, y_test = train_test_split(
            x,
            y,
            test_size=0.2,
            random_state=random_state,
            stratify=y,
        )
        return DatasetBundle(x_train=x_train, x_test=x_test, y_train=y_train, y_test=y_test)

    @classmethod
    def train(cls, random_state: int = 42) -> "LightweightSNNPipeline":
        dataset = cls.load_digits_dataset(random_state=random_state)
        ann = MLPClassifier(
            hidden_layer_sizes=(48,),
            activation="relu",
            solver="adam",
            learning_rate_init=0.003,
            max_iter=350,
            random_state=random_state,
            early_stopping=True,
            n_iter_no_change=20,
        )
        ann.fit(dataset.x_train, dataset.y_train)

        hidden_train = cls._hidden_activation(ann, dataset.x_train)
        hidden_test = cls._hidden_activation(ann, dataset.x_test)

        snn_weights = cls._convert_ann_to_snn(ann, hidden_train)
        generator = cls._fit_spiking_generator(hidden_train, dataset.y_train, dataset.x_train)

        ann_pred = ann.predict(dataset.x_test)
        snn_pred, _ = cls._predict_snn_batch(snn_weights, dataset.x_test, seed=random_state)

        metrics = {
            "ann_accuracy": float(accuracy_score(dataset.y_test, ann_pred)),
            "snn_accuracy": float(accuracy_score(dataset.y_test, snn_pred)),
        }

        artifacts = PipelineArtifacts(
            ann=ann,
            snn_weights=snn_weights,
            generator=generator,
            metrics=metrics,
            dataset=dataset,
        )
        return cls(artifacts)

    @staticmethod
    def _hidden_activation(ann: MLPClassifier, x: np.ndarray) -> np.ndarray:
        hidden_linear = x @ ann.coefs_[0] + ann.intercepts_[0]
        return np.maximum(hidden_linear, 0.0)

    @classmethod
    def _convert_ann_to_snn(
        cls,
        ann: MLPClassifier,
        hidden_activations: np.ndarray,
        time_steps: int = 24,
    ) -> dict[str, np.ndarray | float | int]:
        hidden_scale = float(np.percentile(hidden_activations, 95))
        hidden_scale = max(hidden_scale, 0.45)

        return {
            "w1": ann.coefs_[0].astype(np.float32),
            "b1": ann.intercepts_[0].astype(np.float32),
            "w2": ann.coefs_[1].astype(np.float32),
            "b2": ann.intercepts_[1].astype(np.float32),
            "time_steps": time_steps,
            "hidden_threshold": hidden_scale / max(time_steps * 0.35, 1.0),
            "hidden_scale": hidden_scale,
        }

    @classmethod
    def _fit_spiking_generator(
        cls,
        hidden_activations: np.ndarray,
        labels: np.ndarray,
        images: np.ndarray,
    ) -> dict[str, np.ndarray | float | int]:
        num_classes = 10
        one_hot = np.eye(num_classes, dtype=np.float32)[labels]
        features = np.concatenate([hidden_activations, one_hot], axis=1)
        bias = np.ones((features.shape[0], 1), dtype=np.float32)
        features = np.concatenate([features, bias], axis=1)
        decoder, *_ = np.linalg.lstsq(features, images, rcond=None)

        class_prototypes = np.zeros((num_classes, images.shape[1]), dtype=np.float32)
        for label in range(num_classes):
            class_prototypes[label] = images[labels == label].mean(axis=0)

        hidden_norm = np.percentile(hidden_activations, 90, axis=0)
        hidden_norm = np.where(hidden_norm < 1e-3, 1.0, hidden_norm)

        return {
            "decoder": decoder.astype(np.float32),
            "class_prototypes": class_prototypes,
            "hidden_norm": hidden_norm.astype(np.float32),
            "time_steps": 24,
        }

    @classmethod
    def _predict_snn_batch(
        cls,
        snn_weights: dict[str, np.ndarray | float | int],
        x: np.ndarray,
        seed: int = 42,
    ) -> tuple[np.ndarray, np.ndarray]:
        predictions = []
        logits = []
        rng = np.random.default_rng(seed)
        for sample in x:
            pred, details = cls._run_snn_single(snn_weights, sample, rng)
            predictions.append(pred)
            logits.append(details["logits"])
        return np.array(predictions), np.vstack(logits)

    @staticmethod
    def _run_snn_single(
        snn_weights: dict[str, np.ndarray | float | int],
        image: np.ndarray,
        rng: np.random.Generator,
    ) -> tuple[int, dict[str, Any]]:
        w1 = snn_weights["w1"]
        b1 = snn_weights["b1"]
        w2 = snn_weights["w2"]
        b2 = snn_weights["b2"]
        time_steps = int(snn_weights["time_steps"])
        hidden_threshold = float(snn_weights["hidden_threshold"])

        hidden_mem = np.zeros(w1.shape[1], dtype=np.float32)
        hidden_counts = np.zeros(w1.shape[1], dtype=np.float32)
        output_mem = np.zeros(w2.shape[1], dtype=np.float32)
        pixel_counts = np.zeros_like(image, dtype=np.float32)

        scaled_b1 = b1 / time_steps
        scaled_b2 = b2 / time_steps
        for _ in range(time_steps):
            input_spikes = (rng.random(image.shape[0]) < image).astype(np.float32)
            pixel_counts += input_spikes
            hidden_mem += (input_spikes @ w1) / time_steps + scaled_b1
            hidden_spikes = (hidden_mem >= hidden_threshold).astype(np.float32)
            hidden_mem -= hidden_spikes * hidden_threshold
            hidden_counts += hidden_spikes
            output_mem += (hidden_spikes * hidden_threshold) @ w2 + scaled_b2

        logits = output_mem
        prediction = int(np.argmax(logits))
        return prediction, {
            "logits": logits,
            "hidden_counts": hidden_counts,
            "pixel_counts": pixel_counts,
            "hidden_activation_estimate": hidden_counts * hidden_threshold,
        }

    @staticmethod
    def _generate_from_spikes(
        generator: dict[str, np.ndarray | float | int],
        hidden_signal: np.ndarray,
        predicted_class: int,
        rng: np.random.Generator,
    ) -> dict[str, np.ndarray]:
        decoder = generator["decoder"]
        class_prototypes = generator["class_prototypes"]
        hidden_norm = generator["hidden_norm"]
        time_steps = int(generator["time_steps"])

        hidden_rates = np.clip(hidden_signal / hidden_norm, 0.0, 1.0)
        hidden_spike_accumulator = np.zeros_like(hidden_signal, dtype=np.float32)
        for _ in range(time_steps):
            hidden_spike_accumulator += (rng.random(hidden_signal.shape[0]) < hidden_rates).astype(np.float32)

        hidden_features = (hidden_spike_accumulator / time_steps) * hidden_norm
        class_one_hot = np.zeros(10, dtype=np.float32)
        class_one_hot[predicted_class] = 1.0
        feature_vector = np.concatenate([hidden_features, class_one_hot, np.array([1.0], dtype=np.float32)])
        reconstruction = feature_vector @ decoder
        reconstruction = np.clip(0.65 * reconstruction + 0.35 * class_prototypes[predicted_class], 0.0, 1.0)

        pixel_rates = np.clip(reconstruction, 0.0, 1.0)
        pixel_spike_counts = np.zeros_like(pixel_rates, dtype=np.float32)
        for _ in range(time_steps):
            pixel_spike_counts += (rng.random(pixel_rates.shape[0]) < pixel_rates).astype(np.float32)
        synthesized = pixel_spike_counts / time_steps

        return {
            "reconstruction": reconstruction,
            "synthesized": synthesized,
            "pixel_spike_counts": pixel_spike_counts,
        }

    def evaluate(self) -> dict[str, float]:
        return self.artifacts.metrics

    def predict_with_pipeline(self, image: np.ndarray, seed: int = 123) -> dict[str, Any]:
        normalized = np.asarray(image, dtype=np.float32).reshape(-1)
        normalized = np.clip(normalized, 0.0, 1.0)
        ann_logits = self._ann_logits(normalized[None, :])[0]
        ann_probs = _softmax(ann_logits[None, :])[0]
        ann_prediction = int(np.argmax(ann_probs))

        rng = np.random.default_rng(seed)
        snn_prediction, snn_details = self._run_snn_single(self.snn, normalized, rng)
        generated = self._generate_from_spikes(
            self.generator,
            snn_details["hidden_activation_estimate"],
            snn_prediction,
            rng,
        )

        return {
            "ann_prediction": ann_prediction,
            "ann_probabilities": ann_probs,
            "snn_prediction": snn_prediction,
            "snn_logits": snn_details["logits"],
            "hidden_counts": snn_details["hidden_counts"],
            "input_spike_counts": snn_details["pixel_counts"],
            "generated_image": generated["synthesized"],
            "generator_reconstruction": generated["reconstruction"],
            "generator_pixel_spikes": generated["pixel_spike_counts"],
        }

    def random_test_sample(self, seed: int = 0) -> dict[str, Any]:
        rng = np.random.default_rng(seed)
        index = int(rng.integers(0, len(self.artifacts.dataset.x_test)))
        image = self.artifacts.dataset.x_test[index]
        label = int(self.artifacts.dataset.y_test[index])
        details = self.predict_with_pipeline(image, seed=seed + 999)
        details["image"] = image
        details["label"] = label
        details["index"] = index
        return details

    def _ann_logits(self, x: np.ndarray) -> np.ndarray:
        hidden = np.maximum(x @ self.ann.coefs_[0] + self.ann.intercepts_[0], 0.0)
        logits = hidden @ self.ann.coefs_[1] + self.ann.intercepts_[1]
        return logits

    def save(self, path: Path = MODEL_PATH) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as handle:
            pickle.dump(self.artifacts, handle)

    @classmethod
    def load(cls, path: Path = MODEL_PATH) -> "LightweightSNNPipeline":
        with path.open("rb") as handle:
            artifacts: PipelineArtifacts = pickle.load(handle)
        return cls(artifacts)

    @classmethod
    def load_or_train(cls, path: Path = MODEL_PATH) -> "LightweightSNNPipeline":
        if path.exists():
            return cls.load(path)
        pipeline = cls.train()
        pipeline.save(path)
        return pipeline
