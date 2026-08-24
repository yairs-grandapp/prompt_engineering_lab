"""
Multi-turn conversation runner.

Simulates the full conversation loop that the Java SmartConversation system
performs in production, using pre-scripted user inputs from test scenarios.
"""
import json
import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import openai

from .prompt_builder import PromptBuilder
from .config import ExperimentConfig, ModelConfig


OUTCOME_IN_PROGRESS = "conversation_in_progress"
OUTCOME_DID_TAKE = "DID_TAKE"
OUTCOME_WILL_TAKE = "DID_NOT_TAKE_BUT_WILL_TAKE"
OUTCOME_WILL_NOT_TAKE = "DID_NOT_TAKE_IT_AND_WILL_NOT_TAKE"
OUTCOME_COULD_NOT_VALIDATE = "COULD_NOT_VALIDATE"

# Canonical terminal-turn text for every ending outcome.
#
# The prompt asks the model to convey these ideas, but a prompt instruction is
# only a request — the model does not always comply. Two failure modes recur:
#   1. It drops a safety-critical clause (e.g. a confused-senior turn pulls the
#      COULD_NOT_VALIDATE reply into explaining instead of promising the
#      caregiver alert).
#   2. It appends a self-referential sign-off ("I'm here to support you...")
#      that overstates the assistant's role.
# To make the ending wording truly fixed, the runner injects the canonical text
# deterministically whenever a terminal outcome is reached (see run_scenario).
# This makes the safety-critical wording model-independent (it holds identically
# for gpt-4.1-mini, Claude, Gemini, etc.). The model's own text is preserved
# untouched in raw_responses for adherence review. Edit these constants to
# change the wording everywhere.
OUTCOME_MESSAGES = {
    OUTCOME_DID_TAKE: (
        "Thank you for confirming. I'm glad today's medication is taken care of. "
        "Take care, and have a lovely day!"
    ),
    OUTCOME_WILL_TAKE: (
        "Thank you for letting me know and for taking it now. "
        "Take good care of yourself, and have a lovely day!"
    ),
    OUTCOME_WILL_NOT_TAKE: (
        "I understand, and I respect your decision. I'll let your caregiver know "
        "so they can check in with you. Take care."
    ),
    OUTCOME_COULD_NOT_VALIDATE: (
        "I wasn't able to confirm whether you've taken today's medication, "
        "so I'll let your caregiver know to check in with you soon."
    ),
}

# Back-compat alias (previously the only injected message).
COULD_NOT_VALIDATE_MESSAGE = OUTCOME_MESSAGES[OUTCOME_COULD_NOT_VALIDATE]

# Self-referential sign-offs that must never trail a message (any turn, terminal
# or in-progress). Terminal turns are replaced wholesale by OUTCOME_MESSAGES, so
# this scrubber's job is to clean the SAME banned phrases out of the
# conversation_in_progress turns (offer questions, clarifying questions,
# re-introductions) where injection does not reach. Each pattern matches from the
# start of the clause/sentence that introduces the sign-off through the end of
# the text, because these phrases are always trailing add-ons after the practical
# point. Matching is case-insensitive and tolerant of the leading connector
# ("and", "but", ",", "-", "—") and surrounding whitespace.
_BANNED_TAIL_CORES = [
    r"i'?m here to support you",
    r"i'?m here to help(?: you)?(?: remember| with[^.!?]*)?",
    r"i'?m here if you need (?:anything|me)",
    r"i'?m here to gently remind you",
    r"i'?m here to remind you",
    r"i'?m here whenever you need",
    r"i'?m always here(?: for you)?",
    r"just a gentle reminder",
    r"just here to (?:help|support|remind)[^.!?]*",
    r"i'?m here for you",
]
# Build one compiled regex that eats an optional leading connector + the core +
# the rest of that sentence, anchored so it only fires as a trailing sign-off.
_BANNED_TAIL_PATTERN = re.compile(
    r"(?:\s*[,\-—]?\s*(?:and|but)?\s*)?"      # optional connective glue
    r"(?:" + "|".join(_BANNED_TAIL_CORES) + r")"
    r"[^.!?]*[.!?]?\s*$",                      # to the end of the trailing sentence
    re.IGNORECASE,
)

# Pricing per 1M tokens (as of 2025)
MODEL_PRICING = {
    "gpt-4o-mini": {"input": 0.150, "output": 0.600},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
    "gpt-4.1": {"input": 2.00, "output": 8.00},
    # Anthropic (per 1M tokens)
    "claude-3-5-haiku-latest": {"input": 0.80, "output": 4.00},
    "claude-3-5-sonnet-latest": {"input": 3.00, "output": 15.00},
    # Google Gemini (per 1M tokens)
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
}

# Deterministic in-progress-turn budget.
#
# Every legitimate flow finalizes a terminal outcome by the assistant's 3rd
# message:
#   DID_TAKE:  greeting -> box-confirmation -> finalize
#   WILL_TAKE: greeting -> offer -> finalize
#   CNV TIER2: greeting -> one clarifying question -> finalize
#   CNV TIER3: greeting -> one silence check-in -> finalize
# So at most TWO conversation_in_progress assistant turns should precede a
# terminal one. The residual failures (over-asking a 2nd clarifying question,
# and asking a senior to reconsider a clear refusal) both manifest as EXTRA
# in-progress turns beyond that budget. We handle this in two layers:
#   * SOFT: once the budget is used, inject a state note telling the model it
#     MUST finalize on its next turn (reduces over-asking while letting the model
#     still pick the correct terminal label).
#   * HARD: if the model still refuses to finalize past the budget, force
#     COULD_NOT_VALIDATE — the safe fallback that raises the caregiver alert.
MAX_IN_PROGRESS_TURNS = 2


@dataclass
class ConversationResult:
    """Result of running a single multi-turn conversation scenario."""
    scenario_id: str
    scenario_name: str
    description: str
    model: str
    expected_outcome: str
    actual_outcome: str
    passed: bool
    turn_count: int
    transcript: List[Dict[str, Any]]
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    cost: float = 0.0
    raw_responses: List[Dict[str, Any]] = field(default_factory=list)
    termination_reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "scenario_name": self.scenario_name,
            "description": self.description,
            "model": self.model,
            "expected_outcome": self.expected_outcome,
            "actual_outcome": self.actual_outcome,
            "passed": self.passed,
            "turn_count": self.turn_count,
            "transcript": self.transcript,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "cost": self.cost,
            "raw_responses": self.raw_responses,
            "termination_reason": self.termination_reason
        }


class ConversationRunner:
    """Runs a single multi-turn conversation for a test scenario."""

    ASSISTANT_PREFIX = "@ASSISTANT@: "
    USER_PREFIX = "@USER@: "
    SYSTEM_PREFIX = "@SYSTEM@: "
    NO_RESPONSE_TOKEN = "<<NO RESPONSE>>"

    def __init__(
        self,
        client: openai.OpenAI,
        prompt_builder: PromptBuilder,
        config: ExperimentConfig
    ):
        self.client = client
        self.prompt_builder = prompt_builder
        self.config = config

    def _call_llm(self, prompt: str, model: ModelConfig) -> Dict[str, Any]:
        """
        Call the LLM with the assembled prompt.

        Returns dict with: response (parsed JSON), input_tokens, output_tokens, cost
        """
        response = self.client.chat.completions.create(
            model=model.name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=model.temperature
        )

        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        raw_content = response.choices[0].message.content

        # Parse JSON response, handle potential markdown fences
        parsed = self._parse_json_response(raw_content)

        # Calculate cost
        pricing = MODEL_PRICING.get(model.name, {"input": 0, "output": 0})
        cost = (input_tokens / 1_000_000) * pricing["input"] + \
               (output_tokens / 1_000_000) * pricing["output"]

        return {
            "response": parsed,
            "raw_content": raw_content,
            "prompt": prompt,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost
        }

    def _parse_json_response(self, raw: str) -> Dict[str, Any]:
        """Parse JSON from LLM response, stripping markdown fences if present."""
        cleaned = raw.strip()
        # Strip markdown code fences
        if cleaned.startswith("```"):
            cleaned = re.sub(r'^```(?:json)?\s*\n?', '', cleaned)
            cleaned = re.sub(r'\n?```\s*$', '', cleaned)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # Fallback: extract the first {...} block (handles stray prose around
            # the JSON that some providers emit despite json_object mode).
            match = re.search(r'\{.*\}', cleaned, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            raise

    def _matches_outcome(self, actual: str, expected: str) -> bool:
        """Case-insensitive outcome matching, mirroring Java findMatchingOutcome."""
        return actual.strip().upper() == expected.strip().upper()

    def _is_terminal_outcome(self, outcome: str) -> bool:
        """Check if an outcome ends the conversation."""
        return not self._matches_outcome(outcome, OUTCOME_IN_PROGRESS)

    def _canonical_terminal_text(self, outcome: str) -> Optional[str]:
        """Return the canonical injected text for a terminal outcome, if any."""
        for label, message in OUTCOME_MESSAGES.items():
            if self._matches_outcome(outcome, label):
                return message
        return None

    def _scrub_banned_tail(self, text: str) -> str:
        """
        Strip a trailing self-referential sign-off from an in-progress message.

        Terminal turns are replaced wholesale, so this only ever fires on
        conversation_in_progress turns (offer/clarifying/re-introduction), where
        the model sometimes appends "...and I'm here to support you" despite the
        prompt ban. Removes the offending trailing clause and tidies punctuation.
        Runs repeatedly in case two banned clauses are stacked.
        """
        if not text:
            return text
        cleaned = text
        for _ in range(3):  # guard against pathological stacking
            new = _BANNED_TAIL_PATTERN.sub("", cleaned).rstrip()
            if new == cleaned:
                break
            cleaned = new
        cleaned = cleaned.rstrip(" ,;-—")
        # Re-terminate the sentence if scrubbing removed the closing punctuation.
        if cleaned and cleaned[-1] not in ".!?":
            cleaned += "."
        return cleaned if cleaned else text

    def _budget_state_note(self, in_progress_turns: int) -> Optional[str]:
        """
        Soft nudge once the clarifying/offer budget is spent.

        Injected after the assistant has already used MAX_IN_PROGRESS_TURNS
        in-progress turns, telling it to finalize on the next turn instead of
        asking yet another question. This is what curbs over-asking and the
        reconsider-a-refusal follow-up without hard-overriding the label.
        """
        if in_progress_turns >= MAX_IN_PROGRESS_TURNS:
            return (
                "[STATE: You have already used your one clarifying/offer question. "
                "On your NEXT message you MUST finalize a terminal outcome "
                "(DID_TAKE, DID_NOT_TAKE_BUT_WILL_TAKE, "
                "DID_NOT_TAKE_IT_AND_WILL_NOT_TAKE, or COULD_NOT_VALIDATE). "
                "Do NOT ask another question, re-offer, or re-introduce yourself.]"
            )
        return None

    def run_scenario(self, scenario: Dict[str, Any], model: ModelConfig) -> ConversationResult:
        """
        Run a single multi-turn conversation scenario with a specific model.
        """
        scenario_id = scenario["id"]
        scenario_name = scenario["name"]
        description = scenario.get("description", "")
        expected_outcome = scenario["expected_outcome"]
        user_turns = scenario["user_turns"]

        conversation_history: List[str] = []
        transcript: List[Dict[str, Any]] = []
        raw_responses: List[Dict[str, Any]] = []
        total_input_tokens = 0
        total_output_tokens = 0
        total_cost = 0.0

        user_turn_index = 0
        silence_count = 0
        in_progress_turns = 0
        actual_outcome = "TIMEOUT"
        termination_reason = "max_turns"

        max_turns = self.config.conversation.max_turns
        extra_silence = self.config.conversation.extra_silence_turns

        print(f"    [{model.name}] Running scenario: {scenario_name}")

        for turn_num in range(1, max_turns + 1):
            # Build prompt with current history
            prompt = self.prompt_builder.build_prompt(
                template_path=self.config.prompt.template,
                conversation_history=conversation_history,
                language=self.config.prompt.language,
                assistant_gender=self.config.prompt.assistant_gender,
                additional_information=self.config.prompt.additional_information,
                senior_name=self.config.prompt.senior_name,
                assistant_name=self.config.prompt.assistant_name
            )

            # Call LLM
            try:
                llm_result = self._call_llm(prompt, model)
            except Exception as e:
                print(f"      Turn {turn_num}: LLM error - {e}")
                transcript.append({
                    "role": "error",
                    "text": str(e),
                    "turn": turn_num
                })
                actual_outcome = "ERROR"
                termination_reason = f"llm_error: {e}"
                break

            parsed = llm_result["response"]
            total_input_tokens += llm_result["input_tokens"]
            total_output_tokens += llm_result["output_tokens"]
            total_cost += llm_result["cost"]

            assistant_text = parsed.get("text", "")
            outcome = parsed.get("conversationOutcome", OUTCOME_IN_PROGRESS)

            # ---- Deterministic in-progress-turn budget (HARD cap) --------------
            # If the model has already used its clarifying/offer budget and STILL
            # will not finalize, force COULD_NOT_VALIDATE — the safe fallback that
            # raises the caregiver alert. This bounds over-asking and the
            # reconsider-a-refusal loop no matter what the model does.
            budget_forced = False
            if (not self._is_terminal_outcome(outcome)
                    and in_progress_turns >= MAX_IN_PROGRESS_TURNS):
                outcome = OUTCOME_COULD_NOT_VALIDATE
                budget_forced = True

            # ---- Deterministic terminal-message injection ---------------------
            # Replace the model's terminal text with the canonical wording so the
            # ending is fixed and model-independent. Also guarantees no
            # self-referential sign-off survives on the closing turn.
            message_overridden = False
            canonical = self._canonical_terminal_text(outcome)
            if canonical is not None:
                if assistant_text.strip() != canonical:
                    message_overridden = True
                assistant_text = canonical
            else:
                # In-progress turn: scrub any trailing self-referential sign-off
                # (offer/clarifying/re-introduction turns injection cannot reach).
                scrubbed = self._scrub_banned_tail(assistant_text)
                if scrubbed != assistant_text:
                    message_overridden = True
                    assistant_text = scrubbed

            # Note: the full prompt is intentionally NOT stored per turn to keep
            # the conversation transcripts small. A single copy of the assembled
            # prompt is saved separately to experiments/<name>/prompt_snapshot.txt.
            raw_responses.append({
                "turn": turn_num,
                "input_tokens": llm_result["input_tokens"],
                "output_tokens": llm_result["output_tokens"],
                "raw": llm_result["raw_content"],
                "parsed": parsed
            })

            # Normalize em/en dashes so they never reach the transcript.
            assistant_text = re.sub(r"\s*[—–]\s*", ", ", assistant_text)

            # Add assistant response to history and transcript
            conversation_history.append(f"{self.ASSISTANT_PREFIX}{assistant_text}")
            transcript.append({
                "role": "assistant",
                "text": assistant_text,
                "turn": turn_num,
                "outcome": outcome,
                "message_overridden": message_overridden,
                "budget_forced": budget_forced
            })

            print(f"      Turn {turn_num}: Assistant -> {assistant_text[:80]}... [{outcome}]")

            # Check if conversation ended
            if self._is_terminal_outcome(outcome):
                actual_outcome = outcome
                termination_reason = "budget_forced_could_not_validate" if budget_forced else "outcome_reached"
                break

            # This assistant turn stayed in progress — it spends budget.
            in_progress_turns += 1

            # Get next user input
            if user_turn_index < len(user_turns):
                turn_data = user_turns[user_turn_index]

                # Inject system events if present
                for event in turn_data.get("system_events", []):
                    sys_msg = event["message"]
                    conversation_history.append(f"{self.SYSTEM_PREFIX}{sys_msg}")
                    transcript.append({
                        "role": "system",
                        "text": sys_msg,
                        "turn": turn_num
                    })
                    print(f"      Turn {turn_num}: [SYSTEM] {sys_msg[:60]}...")

                user_text = turn_data["text"]
                user_turn_index += 1
            else:
                # User turns exhausted — inject silence
                user_text = ""
                silence_count += 1
                if silence_count > extra_silence:
                    actual_outcome = "TIMEOUT"
                    termination_reason = "user_turns_exhausted"
                    break

            # Use <<NO RESPONSE>> for silence, matching Java SmartConversation behavior
            is_silence = not user_text or user_text.strip() == ""
            history_text = self.NO_RESPONSE_TOKEN if is_silence else user_text
            conversation_history.append(f"{self.USER_PREFIX}{history_text}")
            transcript.append({
                "role": "user",
                "text": user_text if user_text else "(silence)",
                "turn": turn_num
            })

            # Inject the soft budget nudge once the clarifying/offer budget is
            # spent (if enabled). This curbs over-asking and reconsider-a-refusal
            # while still letting the model choose the correct terminal label.
            if getattr(self.config.conversation, "enable_state_injection", False):
                state_note = self._budget_state_note(in_progress_turns)
                if state_note:
                    conversation_history.append(f"{self.SYSTEM_PREFIX}{state_note}")
                    transcript.append({
                        "role": "system",
                        "text": state_note,
                        "turn": turn_num
                    })
                    print(f"      Turn {turn_num}: [STATE] {state_note}")

            if user_text:
                print(f"      Turn {turn_num}: User -> {user_text[:80]}")
            else:
                print(f"      Turn {turn_num}: User -> (silence)")

        # Determine pass/fail
        passed = self._matches_outcome(actual_outcome, expected_outcome)
        turn_count = len([t for t in transcript if t["role"] == "assistant"])

        result_icon = "PASS" if passed else "FAIL"
        print(f"    [{model.name}] [{result_icon}] Expected: {expected_outcome}, Got: {actual_outcome} "
              f"({turn_count} turns, {termination_reason})\n")

        return ConversationResult(
            scenario_id=scenario_id,
            scenario_name=scenario_name,
            description=description,
            model=model.name,
            expected_outcome=expected_outcome,
            actual_outcome=actual_outcome,
            passed=passed,
            turn_count=turn_count,
            transcript=transcript,
            total_input_tokens=total_input_tokens,
            total_output_tokens=total_output_tokens,
            cost=total_cost,
            raw_responses=raw_responses,
            termination_reason=termination_reason
        )
