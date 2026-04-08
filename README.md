# French Vocabulary Flashcard
## 法语单词背诵应用

一个为学习B2-C2级法语词汇设计的桌面弹窗应用。

### Features (功能)

- 🎴 **Interactive Flashcards** - 交互式闪卡，点击翻转显示中文
- 📚 **Multiple Difficulty Levels** - 支持B2, C1, C2三个难度级别
- 🎯 **Popup Mode** - 弹窗模式，支持快速学习
- ⌨️ **Keyboard Shortcuts** - 键盘快捷键支持
  - **Space** - 翻转卡片
  - **Right Arrow (→)** - 下一单词
  - **Left Arrow (←)** - 翻转卡片
- 📊 **Vocabulary Database** - 包含100+个B2-C2级词汇，每个词都附有中文翻译和例句

### Project Structure (项目结构)

```
french_card/
├── main.py              # 主程序入口
├── gui.py              # GUI界面（主窗口和弹窗）
├── vocabulary.py       # 词汇数据库
├── requirements.txt    # 依赖（无额外依赖）
└── README.md          # 本文件
```

### Requirements (要求)

- Python 3.6+
- tkinter (comes with Python)

### Installation (安装)

1. Clone or download this project
   ```bash
   git clone <repository>
   cd french_card
   ```

### Usage (使用方法)

**方式 1: 无命令行窗口（推荐）**
直接双击运行：
```
run.pyw
```

**方式 2: 通过 Python 命令运行**
```bash
python main.py
```

或直接运行 GUI：
```bash
python gui.py
```

### How to Use (使用说明)

1. **Select Difficulty Level** - 选择难度级别（All, B2, C1, C2）
2. **Click "Show Word"** - 点击"Show Word"显示法语单词
3. **Click "Show Chinese" to flip** - 点击"Show Chinese"翻转显示中文翻译
4. **Click "Next Word"** - 点击"Next Word"显示下一个单词
5. **Popup Mode** - 点击"Popup Mode"打开弹窗模式

### Features in Popup Mode (弹窗模式功能)

- Always-on-top window for uninterrupted learning
- 保持窗口在最前面，不中断学习
- Keyboard shortcuts for quick navigation
- 支持键盘快捷键快速导航
- Display vocabulary with French word and Chinese translation
- 显示法语单词和中文翻译

### Vocabulary Levels (词汇级别)

- **B2**: Upper-Intermediate level - 中高级词汇
- **C1**: Advanced level - 高级词汇
- **C2**: Mastery level - 精通级词汇

### Word Example (词汇示例)

```
French: "ambiguïté"
Chinese: "模糊，歧义"
Level: B2
Example: "Il y a une ambiguïté dans cette phrase." (There is an ambiguity in this sentence.)
```

### Future Enhancements (未来改进)

- [ ] Add pronunciation audio
- [ ] Add word statistics and progress tracking
- [ ] Export vocabulary to Anki format
- [ ] Add more vocabulary items
- [ ] Support for custom vocabulary lists
- [ ] Dark mode theme

### Author (作者)

Created for French language learners at B2-C2 levels

---

**Enjoy learning! Bon apprentissage! 祝你学习愉快！**
