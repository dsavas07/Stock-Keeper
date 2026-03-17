from typing import List

# Placeholder simple sentiment scoring by keyword counts
POSITIVE_WORDS = {"good", "great", "strong", "bull", "positive", "beat", "upgrade", "growth"}
NEGATIVE_WORDS = {"weak", "bad", "bear", "negative", "miss", "downgrade", "decline", "loss"}


def sentiment_score(headlines: List[str]) -> float:
    if not headlines:
        return 0.0
    score = 0
    for headline in headlines:
        tokens = [t.lower().strip(".,!?:;") for t in headline.split()]
        for token in tokens:
            if token in POSITIVE_WORDS:
                score += 1
            elif token in NEGATIVE_WORDS:
                score -= 1
    return float(score) / len(headlines)
