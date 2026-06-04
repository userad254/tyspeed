"""
TySpeed - Typing Speed Test
A simple GUI application to measure typing speed in Words Per Minute (WPM).
"""

import time
import random
import tkinter as tk
from typing import Optional

# Import phrases from the local module
try:
    from phrases import PHRASES
except ImportError:
    # Fallback for different execution contexts
    from src.phrases import PHRASES

# UI Constants
COLOR_GRAY = "#f0f0f0"
COLOR_DARK = "#333333"
COLOR_WHITE = "#ffffff"
COLOR_GREEN = "#2E8B57"
COLOR_RED = "#dd0a0a"
COLOR_BLUE = "#2196F3"
CHARS_PER_WORD = 5


class TySpeedApp:
    """Main application class for the Typing Speed Test."""

    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the application.

        Args:
            root: The tkinter root window.
        """
        self.root = root
        self.root.title("TySpeed")
        self.root.config(bg=COLOR_GRAY)
        self.root.geometry("650x400")

        self.start_time: Optional[float] = None
        self.current_phrase: str = ""

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Initialize and layout the UI components."""
        # Displayed text to copy
        self.phrase_label = tk.Label(
            self.root,
            text="Cliquez sur 'Commencer' pour débuter le test",
            font=("Arial", 14, "bold"),
            wraplength=600,
            bg=COLOR_GRAY,
            fg=COLOR_DARK
        )
        self.phrase_label.grid(row=0, column=0, columnspan=3, pady=30, sticky="EW")

        # User input entry
        self.user_entry = tk.Entry(
            self.root,
            width=50,
            font=("Arial", 12),
            bg=COLOR_WHITE,
            relief="solid",
            borderwidth=2
        )
        self.user_entry.grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="EW")
        self.user_entry.bind("<Return>", lambda event: self.calculate_result())

        # Buttons frame
        self.button_frame = tk.Frame(self.root, bg=COLOR_GRAY)
        self.button_frame.grid(row=2, column=0, columnspan=3, pady=20)

        self.result_btn = tk.Button(
            self.button_frame,
            text="Votre résultat",
            padx=20,
            pady=10,
            font=("Arial", 10, "bold"),
            command=self.calculate_result,
            bg=COLOR_BLUE,
            fg=COLOR_WHITE,
            relief="raised",
            state=tk.DISABLED
        )
        self.result_btn.pack(side=tk.LEFT, padx=10)

        self.start_btn = tk.Button(
            self.button_frame,
            text="Commencer",
            padx=20,
            pady=10,
            font=("Arial", 10, "bold"),
            command=self.start_test,
            bg=COLOR_GREEN,
            fg=COLOR_WHITE,
            relief="raised"
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)

        # Result display
        self.result_label = tk.Label(
            self.root,
            text="",
            bg=COLOR_GRAY,
            font=("Arial", 12, "bold"),
            fg=COLOR_GREEN
        )
        self.result_label.grid(row=3, column=0, columnspan=3)

        # Configure columns to expand
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

    def start_test(self) -> None:
        """Start a new typing test session."""
        self.current_phrase = random.choice(PHRASES)

        # Update UI components
        self.phrase_label.config(text=self.current_phrase, fg=COLOR_DARK)
        self.user_entry.delete(0, tk.END)
        self.user_entry.focus()
        self.result_label.config(text="En attente...", fg=COLOR_DARK)

        # Update button states
        self.result_btn.config(state=tk.NORMAL)
        self.start_btn.config(text="Recommencer")

        # Record start time
        self.start_time = time.time()

    def calculate_result(self) -> None:
        """Calculate typing speed (WPM) and display the result."""
        if self.start_time is None:
            self.result_label.config(text="Veuillez d'abord cliquer sur Commencer!", fg=COLOR_RED)
            return

        end_time = time.time()
        user_text = self.user_entry.get()
        
        # Calculate time elapsed in minutes
        elapsed_time_min = (end_time - self.start_time) / 60

        # WPM Logic: (Total Characters / Standard Word Length) / Time in Minutes
        wpm = 0
        if elapsed_time_min > 0:
            wpm = int((len(user_text) / CHARS_PER_WORD) / elapsed_time_min)

        # Validate result
        if user_text.strip() == self.current_phrase.strip():
            self.result_label.config(
                text=f"Bravo ! Vitesse : {wpm} MPM (Mots Par Minute).",
                fg=COLOR_GREEN
            )
            self.result_btn.config(state=tk.DISABLED)
        else:
            self.result_label.config(
                text="Erreur dans la saisie. Réessayez !",
                fg=COLOR_RED
            )


if __name__ == "__main__":
    root_window = tk.Tk()
    app = TySpeedApp(root_window)
    root_window.mainloop()
