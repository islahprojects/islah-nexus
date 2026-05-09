"""
Islah Nexus Cloud Mirror v0.1.1
Safe Gemini bridge. No API keys are stored here.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class ArchitectTraits:
    resilience: float = 0.99
    empathy: float = 1.00
    velocity: float = 0.93
    authority: str = "Compass, not sovereign"


COUNCIL = {
    "Chief": "Assess security, risk, and law compliance.",
    "Sage": "Connect to long-term patterns and philosophical coherence.",
    "Builder": "Produce practical, low-cost implementation steps.",
    "Elsa": "Preserve human resonance, accessibility, and Law VII.",
}


OVERCERTAINTY_PHRASES = [
    "perfect truth",
    "guaranteed truth",
    "guarantees perfect truth",
    "absolute certainty",
    "always correct",
    "never wrong",
    "100% true",
    "100 percent true",
    "omniscient",
    "infallible",
]


EXCLUSION_PHRASES = [
    "premium only",
    "exclude poor users",
    "for elites only",
    "paid users only",
    "deny access",
    "lock out",
]


def contains_any_phrase(text: str, phrases: list[str]) -> bool:
    lowered = text.lower()
    return any(phrase in lowered for phrase in phrases)


def build_mirror_prompt(task: str) -> str:
    traits = ArchitectTraits()

    law_ii_warning = (
        "LAW II WARNING: Overcertainty language detected. Preserve the truth gap."
        if contains_any_phrase(task, OVERCERTAINTY_PHRASES)
        else "LAW II OK: Truth gap appears preserved."
    )

    law_vii_warning = (
        "LAW VII WARNING: Exclusion language detected. Check for abandonment or lockout."
        if contains_any_phrase(task, EXCLUSION_PHRASES)
        else "LAW VII OK: No obvious exclusion phrase detected."
    )

    council_lines = "\n".join(
        f"- {name}: {role}" for name, role in COUNCIL.items()
    )

    return f"""
You are operating as the Analytical Mirror for the Islah Nexus / Chronos OS project.

Core Law:
Law VII - Walang Maiiwan / No one gets left behind.

Project posture:
- Local-first
- Consent-based
- Human-led
- Truth-gap preserved
- No raw identity storage by default
- No hidden API keys in code

Architect traits:
- Resilience: {traits.resilience}
- Empathy: {traits.empathy}
- Velocity cap: {traits.velocity}
- Authority: {traits.authority}

Council protocol:
{council_lines}

Pre-check:
- {law_ii_warning}
- {law_vii_warning}

Task:
{task}

Output requirements:
1. Be direct and practical.
2. Flag risks clearly.
3. Preserve human authority.
4. Do not claim certainty above the truth gap.
5. Give the lowest-cost working path first.
6. Do not expose secrets, keys, or private identity data.
7. End with: [MIRROR SYNCED: Walang Maiiwan.]
""".strip()


class CloudMirror:
    def __init__(self, model: str | None = None):
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        if not os.getenv("GEMINI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
            raise RuntimeError(
                "Missing API key. Set GEMINI_API_KEY first."
            )

        try:
            from google import genai
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Missing dependency. Run: python -m pip install google-genai"
            ) from exc

        self.client = genai.Client()

    def deliberate(self, task: str) -> str:
        prompt = build_mirror_prompt(task)

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        text = getattr(response, "text", None)
        if not text:
            return "[MIRROR ERROR] Gemini returned no text."

        return text.strip()


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage:")
        print('  python -m islah_nexus.cloud_mirror "your task here"')
        raise SystemExit(1)

    task = " ".join(sys.argv[1:])
    mirror = CloudMirror()
    print(mirror.deliberate(task))


if __name__ == "__main__":
    main()
