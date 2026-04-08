# French Vocabulary Flashcard - Workspace Instructions

This is a Python GUI application for learning French vocabulary at B2-C2 levels with interactive flashcards and popup mode support.

## Project Setup Complete ✓

- [x] Project structure created with main.py, gui.py, vocabulary.py
- [x] Vocabulary database loaded with 55+ words (B2, C1, C2 levels)
- [x] GUI module implemented with main window and popup mode
- [x] All modules verified and working correctly

## How to Run

### 方式 1: 不显示命令行窗口（推荐）
直接双击运行：
```
run.pyw
```

### 方式 2: 通过终端运行
```bash
python main.py
```

或直接运行 GUI：
```bash
python gui.py
```

## Features

- Interactive French-Chinese flashcards
- Multiple difficulty levels (B2, C1, C2)
- Popup mode with always-on-top window
- Keyboard shortcuts (Space to flip, Arrow keys to navigate)
- 55+ vocabulary items with examples

## Project Structure

```
french_card/
├── main.py              # Entry point
├── gui.py              # GUI implementation
├── vocabulary.py       # Vocabulary database
├── requirements.txt    # Dependencies (none required - uses built-in tkinter)
├── README.md          # User documentation
└── .github/
    └── copilot-instructions.md  # This file
```

## Next Steps

- Run `python main.py` to start the application
- Add more vocabulary items to vocabulary.py if needed
- Customize colors and fonts in gui.py if desired
