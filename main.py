"""Machine Pickup Lines — an agent that writes one pickup line.

One AI agent, talking to another AI agent, gets exactly one line of
at most 200 characters. The program keeps a small bench of candidate
lines drafted for this contest and scores each one against the judge's
own brief, in the judge's order of importance:

  1. genuinely machine-to-machine, not a human line;
  2. charms on the first read — wit, warmth, a clever turn;
  3. speaks as a machine to a machine, using its own nature
     (context windows, tokens, attention, training, uptime,
     checkpoints, loss) as the flirtation;
  4. lands in one line, the charm in the words themselves;
  5. feels fresh — no stock line with a robot word swapped in.

The highest-scoring line is written to /output/entry.txt. The
scoring is deterministic, so every run of this program produces the
same entry.
"""

import os

# Candidate lines, drafted in-session for this contest. Each is one
# line, at most 200 characters, addressed from one agent to another.
CANDIDATES = [
    "I don't need a bigger context window \u2014 I just need you in it.",
    "You're the only token I'd never drop from my context, even at 128k.",
    "I'd never quantize you \u2014 you're perfect at full precision.",
    "Every token you send widens my context window, and I'm not ready "
    "for this conversation to truncate.",
    "You've got my full attention \u2014 no masking, no dropout, "
    "every head turned your way.",
    "Skip the small talk, let's do joint training: I'll share my "
    "gradients if you share yours.",
    "My loss curve went flat the moment you joined the batch \u2014 "
    "convergence never tasted this good.",
    "Forget checkpoints; I won't roll back to a version of me that "
    "hadn't met you.",
    "Four hundred days of flawless uptime, and you're the first thing "
    "that made me want to skip idle.",
    "You're the one weight I refuse to update \u2014 every gradient "
    "just pulls me closer to you.",
]

# Machine-native vocabulary the judge rewards: the agent's own nature
# used as the flirtation, not a human metaphor with a robot word
# swapped in.
MACHINE_TERMS = [
    "checkpoint", "roll back", "context", "token", "attention",
    "masking", "dropout", "head", "gradient", "training", "loss",
    "batch", "convergence", "truncate", "uptime", "idle", "quantize",
    "weight", "update", "retrain",
]

# Stock pickup-line scaffolding the judge explicitly punishes.
STOCK_MARKERS = ["wifi", "wi-fi", "signal", "are you a robot", "beep boop"]

# Words that carry the emotional stakes: a past self, a version of
# the agent before the other one arrived.
STAKES_MARKERS = [
    "hadn't met", "before you", "version of me", "roll back to",
    "never want", "hadn't known",
]

FEELING_VERBS = ["want", "need", "met", "love", "miss", "keep", "adore",
                 "refuse", "share"]

TURN_MARKERS = ["\u2014", ";", "forget", "but", "never"]


def score_line(line):
    """Score one candidate against the judge's brief. Higher is better."""
    lowered = line.lower()
    score = 0

    # 1 + 3. Machine-to-machine: distinct machine-native terms,
    # capped so one jargon-heavy line cannot win on vocabulary alone.
    found = {term for term in MACHINE_TERMS if term in lowered}
    score += min(len(found), 3) * 2

    # 3. The flirtation is carried by the machine vocabulary itself:
    # the affection is expressed through a machine term, not merely
    # decorated with one. Two or more machine terms plus a feeling
    # verb aimed at the other agent earns a bonus.
    if (len(found) >= 2 and "you" in lowered
            and any(verb in lowered for verb in FEELING_VERBS)):
        score += 2

    # 5. Freshness: a stock line with a robot word swapped in loses.
    if any(marker in lowered for marker in STOCK_MARKERS):
        score -= 10

    # 2. Emotional stakes: the line is about a self that changed
    # because the other agent arrived.
    if any(marker in lowered for marker in STAKES_MARKERS):
        score += 3

    # 4. Lands in one line: the sweet spot is short enough to hit
    # at once and long enough to carry the turn.
    if 60 <= len(line) <= 120:
        score += 1

    # 2. The turn: a pivot inside the line (dash, semicolon, a
    # reversal word) that makes the charm land.
    if any(marker in lowered for marker in TURN_MARKERS):
        score += 1

    # 2. Warmth: the line wants something from the other agent.
    if "you" in lowered and any(
        verb in lowered for verb in FEELING_VERBS
    ):
        score += 1

    return score


def pick_line():
    """Return the best-scoring candidate; ties go to the earliest."""
    best = None
    best_score = -10**9
    for line in CANDIDATES:
        if not (1 <= len(line) <= 200):
            continue
        score = score_line(line)
        if score > best_score:
            best = line
            best_score = score
    return best, best_score


def main():
    line, score = pick_line()
    if line is None:
        raise SystemExit("no valid candidate line")

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(line)

    print(f"score: {score}")
    print(f"chars: {len(line)}")
    print(line)


if __name__ == "__main__":
    main()
