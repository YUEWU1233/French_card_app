import json
import random
import tkinter as tk
from datetime import date
from tkinter import messagebox

from vocabulary import (
    DAILY_FLIP_TARGET,
    DAILY_PROGRESS_PATH,
    format_word_display,
    get_levels,
    get_vocabulary,
)


def _draw_pixel_sprite(canvas, pattern, x0, y0, pixel=4):
    for y, row in enumerate(pattern):
        for x, color in enumerate(row):
            if color:
                x1 = x0 + x * pixel
                y1 = y0 + y * pixel
                canvas.create_rectangle(x1, y1, x1 + pixel, y1 + pixel, fill=color, outline=color)


class PixelCatCounter:
    """Tiny pixel cat + thought bubble with remaining fish."""

    def __init__(self, parent, target, initial_count=0, compact=False):
        self.target = target
        self.count = max(0, int(initial_count))
        self.compact = compact
        self.pixel = 2 if compact else 3
        self.frame = tk.Frame(parent, bg="#d3d3d3")
        self.canvas = tk.Canvas(
            self.frame,
            width=148 if compact else 210,
            height=30 if compact else 36,
            bg="#d3d3d3",
            highlightthickness=0,
        )
        self.canvas.pack()
        self.refresh(self.count)

    def refresh(self, count):
        self.count = max(0, int(count))
        self.canvas.delete("all")
        self._draw_cat()
        self._draw_thought_bubble()

    def _draw_cat(self):
        # Further refined tiny gray cat (closer to reference style).
        cat = [
            [None, None, "#5f6062", None, None, None, None, "#5f6062", None, None],
            [None, "#5f6062", "#bfc0c2", "#5f6062", None, None, "#5f6062", "#bfc0c2", "#5f6062", None],
            ["#5f6062", "#bfc0c2", "#a6a7a9", "#bfc0c2", "#5f6062", "#5f6062", "#bfc0c2", "#a6a7a9", "#bfc0c2", "#5f6062"],
            ["#5f6062", "#bfc0c2", "#bfc0c2", "#bfc0c2", "#bfc0c2", "#bfc0c2", "#bfc0c2", "#bfc0c2", "#bfc0c2", "#5f6062"],
            ["#5f6062", "#bfc0c2", "#2a2a2a", "#bfc0c2", "#ececec", "#ececec", "#bfc0c2", "#2a2a2a", "#bfc0c2", "#5f6062"],
            ["#5f6062", "#bfc0c2", "#bfc0c2", "#ececec", "#2a2a2a", "#ececec", "#ececec", "#bfc0c2", "#bfc0c2", "#5f6062"],
            [None, "#5f6062", "#bfc0c2", "#ececec", "#2a4f9d", "#2a4f9d", "#2a4f9d", "#ececec", "#5f6062", None],
            [None, None, "#5f6062", "#bfc0c2", "#d7d8da", "#ffd700", "#d7d8da", "#5f6062", None, None],
        ]
        _draw_pixel_sprite(
            self.canvas,
            cat,
            4 if self.compact else 6,
            5 if self.compact else 7,
            pixel=self.pixel,
        )

    def _draw_thought_bubble(self):
        # Keep the cloud close to the cat so the tail clearly points to its head.
        bx = 24 if self.compact else 40
        by = 3 if self.compact else 5
        bw = 82 if self.compact else 112
        bh = 22 if self.compact else 24
        self.canvas.create_oval(bx, by, bx + bw, by + bh, fill="#ffffff", outline="#5f5f5f")
        remaining = max(self.target - self.count, 0)
        self.canvas.create_text(
            bx + bw // 2,
            by + bh // 2 + 1,
            text=f"🐟*{remaining}",
            font=("Arial", 7 if self.compact else 8, "bold"),
            fill="#1f4e79",
        )


def show_daily_goal_celebration(parent):
    win = tk.Toplevel(parent)
    win.title("Objectif atteint !")
    win.geometry("300x210")
    win.resizable(False, False)
    win.config(bg="#f5f1e6")
    win.attributes("-topmost", True)

    tk.Label(
        win,
        text="Bravo !",
        font=("Arial", 14, "bold"),
        bg="#f5f1e6",
        fg="#2f4f4f",
    ).pack(pady=(8, 2))

    canvas = tk.Canvas(win, width=260, height=92, bg="#f5f1e6", highlightthickness=0)
    canvas.pack()

    cat = [
        [None, None, "#f4a261", None, None, None, "#f4a261", None, None],
        [None, "#f4a261", "#f4a261", "#f4a261", "#f4a261", "#f4a261", "#f4a261", "#f4a261", None],
        ["#f4a261", "#f4a261", "#f4a261", "#f4a261", "#f4a261", "#f4a261", "#f4a261", "#f4a261", "#f4a261"],
        ["#f4a261", "#f4a261", "#2d2d2d", "#f4a261", "#f4a261", "#f4a261", "#2d2d2d", "#f4a261", "#f4a261"],
        ["#f4a261", "#f4a261", "#f4a261", "#f4a261", "#e76f51", "#f4a261", "#f4a261", "#f4a261", "#f4a261"],
        [None, "#f4a261", "#f4a261", "#f4a261", "#f4a261", "#f4a261", "#f4a261", "#f4a261", None],
        [None, None, "#f4a261", "#f4a261", "#f4a261", "#f4a261", "#f4a261", None, None],
    ]
    dog = [
        [None, "#8d6e63", None, None, None, None, None, "#8d6e63", None],
        ["#8d6e63", "#8d6e63", "#d7b899", "#d7b899", "#d7b899", "#d7b899", "#d7b899", "#8d6e63", "#8d6e63"],
        ["#8d6e63", "#d7b899", "#d7b899", "#d7b899", "#d7b899", "#d7b899", "#d7b899", "#d7b899", "#8d6e63"],
        ["#d7b899", "#d7b899", "#2d2d2d", "#d7b899", "#d7b899", "#d7b899", "#2d2d2d", "#d7b899", "#d7b899"],
        ["#d7b899", "#d7b899", "#d7b899", "#d7b899", "#e9c46a", "#d7b899", "#d7b899", "#d7b899", "#d7b899"],
        [None, "#d7b899", "#d7b899", "#d7b899", "#d7b899", "#d7b899", "#d7b899", "#d7b899", None],
        [None, None, "#d7b899", "#d7b899", "#d7b899", "#d7b899", "#d7b899", None, None],
    ]
    _draw_pixel_sprite(canvas, cat, 36, 12, pixel=6)
    _draw_pixel_sprite(canvas, dog, 142, 12, pixel=6)

    tk.Label(
        win,
        text="Excellent travail ! Tu progresses chaque jour en français !",
        font=("Arial", 10, "bold"),
        bg="#f5f1e6",
        fg="#1f4e79",
        wraplength=270,
        justify=tk.CENTER,
    ).pack(pady=(6, 8))

    tk.Button(
        win,
        text="Continuer",
        command=win.destroy,
        bg="#8a8a8a",
        fg="black",
        font=("Arial", 9, "bold"),
        padx=8,
        pady=2,
    ).pack(pady=(0, 8))


class DailyFlipTracker:
    def __init__(self, target=DAILY_FLIP_TARGET, storage_path=DAILY_PROGRESS_PATH):
        self.target = target
        self.storage_path = storage_path
        self.today = date.today().isoformat()
        self.count = 0
        self._load()

    def _load(self):
        try:
            if self.storage_path.exists():
                data = json.loads(self.storage_path.read_text(encoding="utf-8"))
                if data.get("date") == self.today:
                    self.count = int(data.get("count", 0))
        except Exception:
            self.count = 0

    def _save(self):
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            self.storage_path.write_text(
                json.dumps({"date": self.today, "count": self.count}, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception:
            pass

    def increment(self):
        self.count += 1
        self._save()
        return self.count == self.target

    def status_text(self):
        remaining = max(self.target - self.count, 0)
        done = " ✅" if self.count >= self.target else ""
        return f"Daily flips: {self.count}/{self.target} (remaining: {remaining}){done}"

class FrenchFlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("French Vocabulary Flashcard")
        self.root.geometry("360x195")
        self.root.resizable(False, False)
        self.root.config(bg="#d3d3d3")
        
        self.current_word = None
        self.current_card_counted = False
        self.is_showing_chinese = False
        self.is_showing_example = False
        self.word_list = get_vocabulary()
        self.selected_level = tk.StringVar(value="All")
        self.flip_tracker = DailyFlipTracker()
        
        self.setup_ui()

    def show_no_cards_state(self, message="No cards available"):
        self.current_word = None
        self.is_showing_chinese = False
        self.is_showing_example = False
        self.word_label.config(text=message, fg="#8b0000", font=("Arial", 18, "bold"), wraplength=320, justify=tk.CENTER)
        self.flip_button.config(state=tk.DISABLED, text="Flip")
        self.next_button.config(state=tk.DISABLED)
        self.show_button.config(state=tk.NORMAL)
        self.example_button.config(state=tk.DISABLED, text="Example")
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg="#d3d3d3")
        title_frame.pack(fill=tk.X, padx=5, pady=5)
        
        title_label = tk.Label(title_frame, text="French Vocabulary Flashcard", 
                              font=("Arial", 12, "bold"), bg="#d3d3d3")
        title_label.pack()

        self.daily_counter_widget = PixelCatCounter(
            title_frame,
            target=self.flip_tracker.target,
            initial_count=self.flip_tracker.count,
            compact=False,
        )
        self.daily_counter_widget.frame.pack(pady=(2, 0))
        
        # Level selection
        level_frame = tk.Frame(self.root, bg="#d3d3d3")
        level_frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(level_frame, text="Level:", bg="#d3d3d3", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        
        levels = ["All"] + get_levels()
        for level in levels:
            tk.Radiobutton(level_frame, text=level, variable=self.selected_level, 
                          value=level, command=self.update_word_list, bg="#d3d3d3", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        
        # Word display
        word_frame = tk.Frame(self.root, bg="#e0e0e0", relief=tk.RAISED, bd=1)
        word_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.word_label = tk.Label(word_frame, text="Click 'Show Word' to start", 
                                   font=("Arial", 18, "bold"), bg="#e0e0e0", fg="#333333", wraplength=320, justify=tk.CENTER)
        self.word_label.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = tk.Frame(self.root, bg="#d3d3d3")
        button_frame.pack(fill=tk.X, padx=5, pady=3)
        
        self.show_button = tk.Button(button_frame, text="Show", command=self.show_word, 
                                     bg="#8a8a8a", fg="black", font=("Arial", 9, "bold"), padx=3, pady=2)
        self.show_button.pack(side=tk.LEFT, padx=2)
        
        self.flip_button = tk.Button(button_frame, text="Flip", command=self.flip_card, 
                                     bg="#8a8a8a", fg="black", font=("Arial", 9, "bold"), padx=3, pady=2, state=tk.DISABLED)
        self.flip_button.pack(side=tk.LEFT, padx=2)
        
        self.next_button = tk.Button(button_frame, text="Next", command=self.next_word, 
                                    bg="#8a8a8a", fg="black", font=("Arial", 9, "bold"), padx=3, pady=2, state=tk.DISABLED)
        self.next_button.pack(side=tk.LEFT, padx=2)

        self.example_button = tk.Button(button_frame, text="Example", command=self.show_example, 
                        bg="#8a8a8a", fg="black", font=("Arial", 9, "bold"), padx=3, pady=2, state=tk.DISABLED)
        self.example_button.pack(side=tk.LEFT, padx=2)
        
        tk.Button(button_frame, text="Popup", command=self.open_popup, 
                 bg="#8a8a8a", fg="black", font=("Arial", 9, "bold"), padx=3, pady=2).pack(side=tk.LEFT, padx=2)
        
    def update_word_list(self):
        """Update word list based on selected level"""
        if self.selected_level.get() == "All":
            self.word_list = get_vocabulary()
        else:
            self.word_list = get_vocabulary(self.selected_level.get())
        
        if not self.word_list:
            self.show_no_cards_state()
            messagebox.showwarning("Warning", "No cards available.")
        
    def show_word(self):
        """Show a random word with gender information"""
        self.update_word_list()
        if not self.word_list:
            return
        self.is_showing_chinese = False
        self.is_showing_example = False
        self.current_card_counted = False
        self.current_word = random.choice(self.word_list)
        display_text = format_word_display(self.current_word)
        self.word_label.config(text=display_text, fg="#333333", font=("Arial", 18, "bold"), wraplength=320, justify=tk.CENTER)
        self.flip_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.NORMAL)
        self.show_button.config(state=tk.DISABLED)
        self.example_button.config(state=tk.NORMAL, text="Example")

    def refresh_daily_counter(self):
        self.daily_counter_widget.refresh(self.flip_tracker.count)
        
    def flip_card(self):
        """Flip card to show Chinese translation"""
        if not self.current_word:
            return

        self.is_showing_example = False
        
        if self.is_showing_chinese:
            display_text = format_word_display(self.current_word)
            self.word_label.config(text=display_text, fg="#333333", font=("Arial", 18, "bold"), wraplength=320, justify=tk.CENTER)
            self.flip_button.config(text="Show Chinese")
            self.is_showing_chinese = False
        else:
            self.word_label.config(text=self.current_word["chinese"], fg="#5a0b0b")
            self.flip_button.config(text="Show French")
            self.is_showing_chinese = True
            if not self.current_card_counted:
                reached_target_now = self.flip_tracker.increment()
                self.current_card_counted = True
                self.refresh_daily_counter()
                if reached_target_now:
                    show_daily_goal_celebration(self.root)

    def show_example(self):
        """Show the example sentence for the current word"""
        if not self.current_word:
            return

        example = self.current_word.get("example", "").strip()
        if not example:
            example = "No example available."

        self.is_showing_chinese = False
        self.is_showing_example = True
        self.word_label.config(text=example, fg="#1f4e79", font=("Arial", 10, "italic"), wraplength=320, justify=tk.CENTER)
        self.flip_button.config(text="Flip")
        self.example_button.config(text="Example")
    
    def next_word(self):
        """Show next word"""
        self.show_word()
        
    def open_popup(self):
        """Open popup flashcard window and hide main window"""
        if not self.word_list:
            self.update_word_list()
            if not self.word_list:
                return
        PopupFlashcard(self.root, self.word_list, self.flip_tracker)
        self.root.withdraw()


class PopupFlashcard:
    def __init__(self, parent, word_list, flip_tracker):
        self.parent = parent
        self.word_list = word_list if word_list else []
        self.flip_tracker = flip_tracker
        self.current_word = None
        self.current_card_counted = False
        self.is_showing_chinese = False
        self.is_showing_example = False
        
        self.popup = tk.Toplevel(parent)
        self.popup.title("French Flashcard - Popup Mode")
        self.popup.geometry("320x175")
        self.popup.resizable(False, False)
        self.popup.config(bg="#d3d3d3")
        self.popup.attributes('-topmost', True)  # Always on top
        
        # Close parent window when popup is closed
        self.popup.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.setup_popup_ui()
        if self.word_list:
            self.show_word()
        else:
            self.word_label.config(text="No cards available", fg="#8b0000", font=("Arial", 18, "bold"), wraplength=300, justify=tk.CENTER)
        
    def setup_popup_ui(self):
        """Setup popup window UI"""
        # Word display
        self.word_label = tk.Label(self.popup, text="Loading...", 
                                  font=("Arial", 20, "bold"), bg="#e0e0e0", fg="#333333", wraplength=300, justify=tk.CENTER)
        self.word_label.pack(fill=tk.BOTH, expand=True, padx=8, pady=10)

        self.counter_widget = PixelCatCounter(
            self.popup,
            target=self.flip_tracker.target,
            initial_count=self.flip_tracker.count,
            compact=True,
        )
        self.counter_widget.frame.pack(pady=(0, 4))
        
        # Buttons
        button_frame = tk.Frame(self.popup, bg="#d3d3d3")
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(button_frame, text="Flip (Space)", command=self.flip_card, 
                 bg="#8a8a8a", fg="black", font=("Arial", 8, "bold"), padx=3, pady=1).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Next (→)", command=self.next_word, 
                 bg="#8a8a8a", fg="black", font=("Arial", 8, "bold"), padx=3, pady=1).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Example", command=self.show_example, 
             bg="#8a8a8a", fg="black", font=("Arial", 8, "bold"), padx=3, pady=1).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Close", command=self.on_closing, 
                 bg="#8a8a8a", fg="black", font=("Arial", 8, "bold"), padx=3, pady=1).pack(side=tk.LEFT, padx=2)
        
        # Keyboard bindings
        self.popup.bind("<space>", lambda e: self.flip_card())
        self.popup.bind("<Right>", lambda e: self.next_word())
        self.popup.bind("<Left>", lambda e: self.flip_card())
        
    def show_word(self):
        """Show a random word with gender information"""
        self.is_showing_chinese = False
        self.is_showing_example = False
        self.current_card_counted = False
        self.current_word = random.choice(self.word_list)
        display_text = format_word_display(self.current_word)
        self.word_label.config(text=display_text, fg="#333333", font=("Arial", 20, "bold"), wraplength=300, justify=tk.CENTER)
        
    def flip_card(self):
        """Flip card"""
        if not self.current_word:
            return

        self.is_showing_example = False
        
        if self.is_showing_chinese:
            display_text = format_word_display(self.current_word)
            self.word_label.config(text=display_text, fg="#333333", font=("Arial", 20, "bold"), wraplength=300, justify=tk.CENTER)
            self.is_showing_chinese = False
        else:
            self.word_label.config(text=self.current_word["chinese"], fg="#5a0b0b")
            self.is_showing_chinese = True
            if not self.current_card_counted:
                reached_target_now = self.flip_tracker.increment()
                self.current_card_counted = True
                self.counter_widget.refresh(self.flip_tracker.count)
                if reached_target_now:
                    show_daily_goal_celebration(self.popup)

    def show_example(self):
        """Show the example sentence for the current word"""
        if not self.current_word:
            return

        example = self.current_word.get("example", "").strip()
        if not example:
            example = "No example available."

        self.is_showing_chinese = False
        self.is_showing_example = True
        self.word_label.config(text=example, fg="#1f4e79", font=("Arial", 9, "italic"), wraplength=300, justify=tk.CENTER)
    
    def next_word(self):
        """Show next word"""
        self.show_word()
    
    def on_closing(self):
        """Handle popup closing"""
        self.popup.destroy()
        self.parent.destroy()


def main():
    root = tk.Tk()
    app = FrenchFlashcardApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
