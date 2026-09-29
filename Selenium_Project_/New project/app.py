from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import numpy as np

from snn_pipeline import LightweightSNNPipeline


CELL_SIZE = 34
GRID_SIZE = 8


class PixelBoard(tk.Canvas):
    def __init__(self, master: tk.Misc, title: str, editable: bool = False):
        width = GRID_SIZE * CELL_SIZE
        height = GRID_SIZE * CELL_SIZE
        super().__init__(master, width=width, height=height, bg="#f4efe6", highlightthickness=0)
        self.title = title
        self.editable = editable
        self.values = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.float32)
        self.rectangles: dict[tuple[int, int], int] = {}
        self._build_grid()
        if editable:
            self.bind("<Button-1>", self._paint)
            self.bind("<B1-Motion>", self._paint)
            self.bind("<Button-3>", self._erase)
            self.bind("<B3-Motion>", self._erase)

    def _build_grid(self) -> None:
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                rect = self.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=self._color_for_value(0.0),
                    outline="#d8cfc0",
                    width=1,
                )
                self.rectangles[(row, col)] = rect

    @staticmethod
    def _color_for_value(value: float) -> str:
        value = float(np.clip(value, 0.0, 1.0))
        low = np.array([244, 239, 230], dtype=np.float32)
        high = np.array([34, 61, 89], dtype=np.float32)
        rgb = (low + (high - low) * value).astype(int)
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    def set_values(self, values: np.ndarray) -> None:
        self.values = np.asarray(values, dtype=np.float32).reshape(GRID_SIZE, GRID_SIZE)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self.itemconfig(self.rectangles[(row, col)], fill=self._color_for_value(self.values[row, col]))

    def clear(self) -> None:
        self.set_values(np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.float32))

    def get_values(self) -> np.ndarray:
        return self.values.copy()

    def _paint(self, event: tk.Event) -> None:
        if not self.editable:
            return
        row = max(0, min(GRID_SIZE - 1, event.y // CELL_SIZE))
        col = max(0, min(GRID_SIZE - 1, event.x // CELL_SIZE))
        self.values[row, col] = min(1.0, self.values[row, col] + 0.4)
        self.itemconfig(self.rectangles[(row, col)], fill=self._color_for_value(self.values[row, col]))

    def _erase(self, event: tk.Event) -> None:
        if not self.editable:
            return
        row = max(0, min(GRID_SIZE - 1, event.y // CELL_SIZE))
        col = max(0, min(GRID_SIZE - 1, event.x // CELL_SIZE))
        self.values[row, col] = max(0.0, self.values[row, col] - 0.5)
        self.itemconfig(self.rectangles[(row, col)], fill=self._color_for_value(self.values[row, col]))


class DemoApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.pipeline = LightweightSNNPipeline.load_or_train()
        self.current_seed = 1

        self.root.title("SNN Image Classifier -> Generator Pipeline Demo")
        self.root.configure(bg="#f7f3ea")
        self.root.minsize(1180, 720)

        self.title_var = tk.StringVar(
            value="ANN-to-SNN classifier with a lightweight spiking image generator"
        )
        metrics = self.pipeline.evaluate()
        self.metrics_var = tk.StringVar(
            value=(
                f"ANN test accuracy: {metrics['ann_accuracy']:.2%}   |   "
                f"SNN test accuracy: {metrics['snn_accuracy']:.2%}"
            )
        )
        self.status_var = tk.StringVar(
            value="Draw a digit on the left or load a random test sample, then run the pipeline."
        )
        self.prediction_var = tk.StringVar(value="Predictions will appear here.")
        self.generator_var = tk.StringVar(value="The generator output will appear after SNN inference.")

        self._build_layout()
        self.load_random_sample()

    def _build_layout(self) -> None:
        header = tk.Frame(self.root, bg="#f7f3ea")
        header.pack(fill="x", padx=24, pady=(18, 12))
        tk.Label(
            header,
            textvariable=self.title_var,
            font=("Georgia", 20, "bold"),
            bg="#f7f3ea",
            fg="#1e364d",
        ).pack(anchor="w")
        tk.Label(
            header,
            textvariable=self.metrics_var,
            font=("Segoe UI", 11),
            bg="#f7f3ea",
            fg="#5d5247",
        ).pack(anchor="w", pady=(4, 0))

        main = tk.Frame(self.root, bg="#f7f3ea")
        main.pack(fill="both", expand=True, padx=24, pady=10)

        left_panel = tk.Frame(main, bg="#fffaf1", bd=0, highlightthickness=1, highlightbackground="#ded2c3")
        center_panel = tk.Frame(main, bg="#fffaf1", bd=0, highlightthickness=1, highlightbackground="#ded2c3")
        right_panel = tk.Frame(main, bg="#fffaf1", bd=0, highlightthickness=1, highlightbackground="#ded2c3")
        left_panel.pack(side="left", fill="y", padx=(0, 12))
        center_panel.pack(side="left", fill="both", expand=True, padx=6)
        right_panel.pack(side="left", fill="both", expand=True, padx=(12, 0))

        self._section_label(left_panel, "Input Digit")
        tk.Label(
            left_panel,
            text="Left click to paint, right click to erase.",
            font=("Segoe UI", 10),
            bg="#fffaf1",
            fg="#6a5e53",
        ).pack(anchor="w", padx=16)
        self.input_board = PixelBoard(left_panel, "Input", editable=True)
        self.input_board.pack(padx=16, pady=12)

        controls = tk.Frame(left_panel, bg="#fffaf1")
        controls.pack(fill="x", padx=16, pady=(0, 14))
        self._button(controls, "Random Test Sample", self.load_random_sample).pack(fill="x", pady=4)
        self._button(controls, "Clear Drawing", self.clear_input).pack(fill="x", pady=4)
        self._button(controls, "Run ANN -> SNN -> Generator", self.run_pipeline).pack(fill="x", pady=4)

        self._section_label(center_panel, "Classifier Views")
        board_row = tk.Frame(center_panel, bg="#fffaf1")
        board_row.pack(fill="x", padx=16, pady=12)
        self.spike_input_board = self._labeled_board(board_row, "Input Spike Rates")
        self.hidden_board = self._labeled_board(board_row, "Hidden Spike Activity")
        self.original_board = self._labeled_board(board_row, "Current Input")
        self.prediction_label = tk.Label(
            center_panel,
            textvariable=self.prediction_var,
            justify="left",
            anchor="w",
            wraplength=360,
            font=("Segoe UI", 11),
            bg="#fffaf1",
            fg="#1f2a35",
        )
        self.prediction_label.pack(fill="x", padx=16, pady=(2, 10))

        self._section_label(right_panel, "Spiking Generator")
        gen_row = tk.Frame(right_panel, bg="#fffaf1")
        gen_row.pack(fill="x", padx=16, pady=12)
        self.reconstruction_board = self._labeled_board(gen_row, "Decoder Reconstruction")
        self.generated_board = self._labeled_board(gen_row, "Spiking Synthesis")
        self.generator_spike_board = self._labeled_board(gen_row, "Pixel Spike Counts")
        self.generator_label = tk.Label(
            right_panel,
            textvariable=self.generator_var,
            justify="left",
            anchor="w",
            wraplength=360,
            font=("Segoe UI", 11),
            bg="#fffaf1",
            fg="#1f2a35",
        )
        self.generator_label.pack(fill="x", padx=16, pady=(2, 10))

        footer = tk.Frame(self.root, bg="#ede4d7")
        footer.pack(fill="x", side="bottom")
        tk.Label(
            footer,
            textvariable=self.status_var,
            font=("Segoe UI", 10),
            bg="#ede4d7",
            fg="#4f463d",
            padx=16,
            pady=10,
            anchor="w",
        ).pack(fill="x")

    def _section_label(self, parent: tk.Misc, text: str) -> None:
        tk.Label(
            parent,
            text=text,
            font=("Georgia", 16, "bold"),
            bg="#fffaf1",
            fg="#1e364d",
            pady=16,
            padx=16,
        ).pack(anchor="w")

    def _button(self, parent: tk.Misc, text: str, command) -> ttk.Button:
        style = ttk.Style()
        style.configure("Accent.TButton", padding=8, font=("Segoe UI", 10, "bold"))
        return ttk.Button(parent, text=text, command=command, style="Accent.TButton")

    def _labeled_board(self, parent: tk.Misc, title: str) -> PixelBoard:
        frame = tk.Frame(parent, bg="#fffaf1")
        frame.pack(side="left", padx=8)
        tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 11, "bold"),
            bg="#fffaf1",
            fg="#5a4e41",
        ).pack()
        board = PixelBoard(frame, title, editable=False)
        board.pack(pady=8)
        return board

    def clear_input(self) -> None:
        self.input_board.clear()
        self.status_var.set("Input board cleared. Draw a digit and run the pipeline.")

    def load_random_sample(self) -> None:
        sample = self.pipeline.random_test_sample(seed=self.current_seed)
        self.current_seed += 1
        image = sample["image"].reshape(GRID_SIZE, GRID_SIZE)
        self.input_board.set_values(image)
        self.status_var.set(
            f"Loaded test sample #{sample['index']} with true label {sample['label']}. "
            "You can classify it directly or modify it before running."
        )
        self.run_pipeline()

    def run_pipeline(self) -> None:
        image = self.input_board.get_values().reshape(-1)
        details = self.pipeline.predict_with_pipeline(image)

        self.original_board.set_values(image.reshape(GRID_SIZE, GRID_SIZE))
        self.spike_input_board.set_values(
            (details["input_spike_counts"] / np.max([1.0, details["input_spike_counts"].max()])).reshape(GRID_SIZE, GRID_SIZE)
        )

        hidden = details["hidden_counts"]
        hidden_grid = np.zeros(GRID_SIZE * GRID_SIZE, dtype=np.float32)
        hidden_grid[: min(len(hidden), GRID_SIZE * GRID_SIZE)] = hidden[: GRID_SIZE * GRID_SIZE]
        hidden_grid = hidden_grid / np.max([1.0, hidden_grid.max()])
        self.hidden_board.set_values(hidden_grid.reshape(GRID_SIZE, GRID_SIZE))

        self.reconstruction_board.set_values(details["generator_reconstruction"].reshape(GRID_SIZE, GRID_SIZE))
        self.generated_board.set_values(details["generated_image"].reshape(GRID_SIZE, GRID_SIZE))
        pixel_spikes = details["generator_pixel_spikes"]
        self.generator_spike_board.set_values(
            (pixel_spikes / np.max([1.0, pixel_spikes.max()])).reshape(GRID_SIZE, GRID_SIZE)
        )

        ann_top = int(details["ann_prediction"])
        snn_top = int(details["snn_prediction"])
        ann_conf = float(np.max(details["ann_probabilities"]))
        self.prediction_var.set(
            f"ANN prediction: {ann_top} with confidence {ann_conf:.1%}\n"
            f"SNN prediction: {snn_top} using rate-coded spikes over {self.pipeline.snn['time_steps']} steps\n"
            f"Hidden spiking neurons fired {int(details['hidden_counts'].sum())} times in total."
        )
        self.generator_var.set(
            f"The spiking generator used the SNN hidden activity and class {snn_top} to synthesize a compact "
            "digit-like reconstruction. This is the classifier -> generator pipeline output."
        )
        self.status_var.set(
            "Pipeline executed successfully. Left: input, middle: classifier spike views, right: generated image."
        )


def main() -> None:
    root = tk.Tk()
    app = DemoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
