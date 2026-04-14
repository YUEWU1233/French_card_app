# French Vocabulary Database (B2-C2 Level)
# 法语词汇库（B2-C2难度）
# gender: m=阳性, f=阴性, -=动词/形容词

import csv
import json
from pathlib import Path


TARGET_WORDS_PER_LEVEL = 200
DAILY_FLIP_TARGET = 200
SUPPORTED_LEVELS = ("B2", "C1", "C2")
WORKSPACE_ROOT = Path(__file__).resolve().parent
DELF_JSON_PATH = WORKSPACE_ROOT / "data" / "delf_b2_c2.json"
DELF_CSV_PATH = WORKSPACE_ROOT / "data" / "delf_b2_c2.csv"
DAILY_PROGRESS_PATH = WORKSPACE_ROOT / "data" / "daily_flip_progress.json"


def _normalize_level(level):
    if not level:
        return None
    value = str(level).strip().upper()
    if value in SUPPORTED_LEVELS:
        return value
    return None


def _normalize_gender(gender):
    value = str(gender or "-").strip().lower()
    if value in {"m", "f", "m/f", "-"}:
        return value
    return "-"


def _normalize_entry(raw):
    french = str(raw.get("french", "")).strip()
    chinese = str(raw.get("chinese", "")).strip()
    level = _normalize_level(raw.get("level"))
    if not french or not chinese or level is None:
        return None
    return {
        "french": french,
        "chinese": chinese,
        "level": level,
        "gender": _normalize_gender(raw.get("gender")),
        "example": str(raw.get("example", "")).strip(),
    }


def _read_external_json(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        return []
    out = []
    for item in data:
        if isinstance(item, dict):
            normalized = _normalize_entry(item)
            if normalized is not None:
                out.append(normalized)
    return out


def _read_external_csv(path):
    out = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            normalized = _normalize_entry(row)
            if normalized is not None:
                out.append(normalized)
    return out


def _load_external_delf_vocabulary():
    """Load external DELF B2-C2 vocabulary from data/delf_b2_c2.json or .csv if present."""
    try:
        if DELF_JSON_PATH.exists():
            return _read_external_json(DELF_JSON_PATH)
        if DELF_CSV_PATH.exists():
            return _read_external_csv(DELF_CSV_PATH)
    except Exception:
        # Keep app usable even if external file format is invalid.
        return []
    return []


# Load vocabulary from JSON file only (no hardcoded seed vocabulary)
BASE_VOCABULARY_SEED = _load_external_delf_vocabulary()


def _expand_level_words(level_words, level, target_count=TARGET_WORDS_PER_LEVEL):
    """Expand one level to target_count by generating unique extension entries."""
    if len(level_words) >= target_count:
        return level_words[:target_count]

    if not level_words:
        # Fallback placeholders in case a level has no base words.
        return [
            {
                "french": f"{level.lower()}_mot_{i + 1:03d}",
                "chinese": "待补充词义",
                "level": level,
                "gender": "-",
                "example": "Exemple a completer.",
            }
            for i in range(target_count)
        ]

    expanded = list(level_words)
    idx = 0
    while len(expanded) < target_count:
        base = level_words[idx % len(level_words)]
        n = len(expanded) - len(level_words) + 1
        expanded.append(
            {
                "french": f"{base['french']}-{level.lower()}-{n:03d}",
                "chinese": f"{base['chinese']}（扩展）",
                "level": level,
                "gender": base.get("gender", "-"),
                "example": base.get("example", ""),
            }
        )
        idx += 1

    return expanded


def _get_base_level_words(level, source=None):
    src = BASE_VOCABULARY_SEED if source is None else source
    return [v for v in src if v["level"].upper() == level.upper()]


# Build full base vocabulary from JSON file only (no expansion)
BASE_VOCABULARY = BASE_VOCABULARY_SEED


def get_vocabulary(level=None):
    """Get vocabulary by level (B2, C1, C2) or all."""
    if level is None:
        return BASE_VOCABULARY_SEED

    level_upper = level.upper()
    return _get_base_level_words(level_upper)


# Visible vocabulary data from JSON file
LEVEL_VOCABULARY = {
    lv: _get_base_level_words(lv)
    for lv in SUPPORTED_LEVELS
}
B2_VOCABULARY = LEVEL_VOCABULARY["B2"]
C1_VOCABULARY = LEVEL_VOCABULARY["C1"]
C2_VOCABULARY = LEVEL_VOCABULARY["C2"]
VOCABULARY = BASE_VOCABULARY_SEED

def get_levels():
    """Get all available levels"""
    return sorted(list(SUPPORTED_LEVELS))

def get_random_word(level=None):
    """Get a random word from the vocabulary"""
    import random
    words = get_vocabulary(level)
    return random.choice(words) if words else None

def format_word_display(word):
    """Format word with article (le/la) based on gender
    Returns: "le word" for masculine, "la word" for feminine, "word" for verbs/adjectives"""
    gender = word.get("gender", "-")
    french_word = word.get("french", "")

    # Hide generated suffixes like "-b2-001", "-c1-179", "-c2-045" in UI display.
    for marker in ("-b2-", "-c1-", "-c2-"):
        if marker in french_word:
            french_word = french_word.split(marker, 1)[0]
            break
    
    if gender == "m":
        return f"le {french_word}"
    elif gender == "f":
        return f"la {french_word}"
    elif gender == "m/f":
        return f"le/la {french_word}"
    else:
        # For verbs and adjectives, no article
        return french_word

def get_word_stats():
    """Get statistics about vocabulary"""
    stats = {
        "total": len(VOCABULARY),
        "B2": len(LEVEL_VOCABULARY["B2"]),
        "C1": len(LEVEL_VOCABULARY["C1"]),
        "C2": len(LEVEL_VOCABULARY["C2"]),
    }
    return stats
