from __future__ import annotations

from snn_pipeline import LightweightSNNPipeline


def main() -> None:
    pipeline = LightweightSNNPipeline.train()
    pipeline.save()
    metrics = pipeline.evaluate()
    print("Training complete.")
    print(f"ANN accuracy: {metrics['ann_accuracy']:.3f}")
    print(f"SNN accuracy: {metrics['snn_accuracy']:.3f}")
    print("Model saved to models/snn_pipeline.pkl")


if __name__ == "__main__":
    main()
