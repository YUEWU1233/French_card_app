import tkinter as tk
from tkinter import messagebox
import random
from vocabulary import get_vocabulary, get_levels, get_random_word, format_word_display

class FrenchFlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("French Vocabulary Flashcard")
        self.root.geometry("360x195")
        self.root.resizable(False, False)
        self.root.config(bg="#d3d3d3")
        
        self.current_word = None
        self.is_showing_chinese = False
        self.is_showing_example = False
        self.word_list = get_vocabulary()
        self.selected_level = tk.StringVar(value="All")
        
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
        self.current_word = random.choice(self.word_list)
        display_text = format_word_display(self.current_word)
        self.word_label.config(text=display_text, fg="#333333", font=("Arial", 18, "bold"), wraplength=320, justify=tk.CENTER)
        self.flip_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.NORMAL)
        self.show_button.config(state=tk.DISABLED)
        self.example_button.config(state=tk.NORMAL, text="Example")
        
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
        PopupFlashcard(self.root, self.word_list)
        self.root.withdraw()


class PopupFlashcard:
    def __init__(self, parent, word_list):
        self.parent = parent
        self.word_list = word_list if word_list else []
        self.current_word = None
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
