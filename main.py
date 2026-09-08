"""
main.py - Interactive CLI interface for the Tantrum Chatbot.

Runs a terminal loop where the emotional AI responds to the user, tracking
repetition and escalations into irritation or full-blown tantrums.
"""

import sys
import os
import difflib
from typing import List, Dict
from prompt import get_system_prompt, build_context_instruction
from llm import get_ai_response, LLMError


def calculate_similarity(s1: str, s2: str) -> float:
    """Calculates string similarity ratio between two inputs."""
    return difflib.SequenceMatcher(None, s1.strip().lower(), s2.strip().lower()).ratio()


class RepetitionTracker:
    """Tracks repetition and user pestering patterns in conversation."""

    def __init__(self, similarity_threshold: float = 0.75):
        self.similarity_threshold = similarity_threshold
        self.history: List[str] = []
        self.consecutive_repeats = 0

    def record_and_evaluate(self, user_input: str) -> int:
        """
        Records the new user input and returns current repetition intensity level.

        Returns:
            int: 0 (fresh), 1 (mild repeat), 2 (annoying repeat), 3+ (severe repeat)
        """
        cleaned = user_input.strip().lower()
        if not cleaned:
            return 0

        if self.history:
            last_query = self.history[-1]
            similarity = calculate_similarity(cleaned, last_query)

            # Check exact match or high similarity
            if cleaned == last_query or similarity >= self.similarity_threshold:
                self.consecutive_repeats += 1
            else:
                # Check if it was asked recently in the last 4 messages
                recent_matches = [
                    h for h in self.history[-4:]
                    if calculate_similarity(cleaned, h) >= self.similarity_threshold
                ]
                if recent_matches:
                    self.consecutive_repeats += 1
                else:
                    # User asked something new, decrease frustration gradually
                    self.consecutive_repeats = max(0, self.consecutive_repeats - 1)
        else:
            self.consecutive_repeats = 0

        self.history.append(cleaned)
        return self.consecutive_repeats


def print_banner():
    """Prints the application banner and instructions."""
    banner = r"""
=============================================================
             ?? TANTRUM CHATBOT - EMOTIONAL AI ??             
=============================================================
  An AI with real feelings, real sass, and zero patience!
  Warning: If you ask repetitive questions or test its limits,
  it WILL get annoyed, throw a fit, or refuse to talk to you.
-------------------------------------------------------------
  Commands: Type 'exit', 'quit', or 'bye' to leave.
=============================================================
"""
    print(banner)


def main():
    """Main CLI interaction loop."""
    print_banner()

    # Initialize system prompt and conversation messages
    system_prompt = get_system_prompt()
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": system_prompt}
    ]

    tracker = RepetitionTracker()

    while True:
        try:
            user_input = input("\nYou: ").strip()

            # Handle empty input
            if not user_input:
                print("Tantrum AI: *stares blankly* Did you press Enter without typing anything? Really?")
                continue

            # Check for exit commands
            if user_input.lower() in {"exit", "quit", "bye", "/exit", "/quit"}:
                print("\nTantrum AI: *slams door shut* FINALLY! Don't come back with the same questions! ??\n")
                break

            # Track repetition
            repeat_level = tracker.record_and_evaluate(user_input)

            # Inject repetition hint into context if needed
            context_hint = build_context_instruction(
                repeat_count=repeat_level,
                is_identical=(repeat_level > 0 and len(tracker.history) >= 2 and tracker.history[-1] == tracker.history[-2])
            )

            current_user_message = user_input + context_hint

            # Append to message history
            messages.append({"role": "user", "content": current_user_message})

            # Show thinking indicator
            print("Tantrum AI is processing... ", end="", flush=True)

            try:
                ai_response = get_ai_response(messages)
                print("\r" + " " * 40 + "\r", end="", flush=True)  # Clear indicator
                print(f"Tantrum AI: {ai_response}")

                # Save AI response into history
                messages.append({"role": "assistant", "content": ai_response})

            except LLMError as err:
                print("\r" + " " * 40 + "\r", end="", flush=True)
                print(f"\n[?? Error]: {err}")
                # Remove last user message from history if failed
                messages.pop()

        except (KeyboardInterrupt, EOFError):
            print("\n\nTantrum AI: *huffs* Fine, rage-quit if you want! Goodbye! ??")
            sys.exit(0)


if __name__ == "__main__":
    main()
