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

# Pricing per 1M tokens (as of 2025)
MODEL_PRICING = {
    "gpt-4o-mini": {"input": 0.150, "output": 0.600},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
    "gpt-4.1": {"input": 2.00, "output": 8.00},
}


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
        return json.loads(cleaned)

    def _matches_outcome(self, actual: str, expected: str) -> bool:
        """Case-insensitive outcome matching, mirroring Java findMatchingOutcome."""
        return actual.strip().upper() == expected.strip().upper()

    def _is_terminal_outcome(self, outcome: str) -> bool:
        """Check if an outcome ends the conversation."""
        return not self._matches_outcome(outcome, OUTCOME_IN_PROGRESS)

    def _is_clear_confirmation(self, text: str) -> bool:
        """Check if user text is a clear confirmation that they are fine."""
        text_lower = text.strip().lower()
        confirmation_phrases = [
            "i'm fine", "i am fine", "i'm okay", "i am okay",
            "i'm alright", "i am alright", "i'm ok", "i am ok",
            "i did not fall", "i didn't fall", "no i didn't fall",
            "everything is okay", "everything is fine", "everything is alright",
            "i'm perfectly fine", "i am perfectly fine",
            "yes i'm sure", "yes i am sure", "yes i'm fine",
            "don't worry", "nothing happened", "it was nothing",
        ]
        return any(phrase in text_lower for phrase in confirmation_phrases)

    def _is_tier1_trigger(self, text: str) -> bool:
        """Check if user text contains a TIER 1 immediate escalation trigger."""
        text_lower = text.strip().lower()
        tier1_phrases = [
            # Confirms fall
            "i fell", "i've fallen", "i have fallen", "yes i fell",
            "fell down", "i slipped", "i tripped",
            # Reports injury
            "broke my", "broken", "bleeding", "blood",
            "can't move", "cannot move", "can't get up", "cannot get up",
            "stuck on the floor", "on the floor",
            "hurts", "hurt", "pain", "in pain",
            "can't feel", "cannot feel",
            # Feeling unwell
            "don't feel good", "don't feel well", "do not feel good",
            "feel dizzy", "feel sick", "feel faint",
            "my head", "my leg", "my arm", "my hip", "my back",
            # Distress
            "help me", "send help", "need help", "please help",
            "i'm scared", "i am scared",
            # Implies was on the ground (fell and recovered)
            "got up by myself", "got up on my own", "got back up",
            "picked myself up", "managed to get up",
        ]
        return any(phrase in text_lower for phrase in tier1_phrases)

    def _build_state_note(self, consecutive_silence_count: int, unclear_response_count: int, user_text: str) -> Optional[str]:
        """Build a state note to inject into conversation history for escalation tracking."""
        # TIER 1 takes highest priority — immediate escalation triggers
        if user_text and user_text.strip() and self._is_tier1_trigger(user_text):
            return (
                "[ESCALATION STATE: The senior's response contains a TIER 1 trigger "
                "(confirmed fall, injury, distress, or feeling unwell). "
                "Per TIER 1 rules, you MUST return DISTRESS_FALL_CONFIRMED immediately on your next response. "
                "Do NOT ask any follow-up questions. Escalate NOW.]"
            )
        # TIER 3 — silence tracking
        if consecutive_silence_count >= 2:
            return (
                "[ESCALATION STATE: This is the senior's 2nd consecutive silence. "
                "Per TIER 3 rules, you MUST return DISTRESS_FALL_CONFIRMED immediately on your next response. "
                "Do NOT ask another question.]"
            )
        if consecutive_silence_count == 1:
            return (
                "[ESCALATION STATE: The senior did not respond (1st silence). "
                "Per TIER 3 rules, ask once more with concern. "
                "If the next response is also silence, you MUST escalate immediately.]"
            )
        # TIER 2 — confusion/unclear tracking
        if unclear_response_count >= 2:
            return (
                "[ESCALATION STATE: The senior has now given 2 unclear/confused/evasive responses. "
                "Per TIER 2 rules, you MUST return DISTRESS_FALL_CONFIRMED immediately on your next response. "
                "Do NOT ask another clarifying question.]"
            )
        if unclear_response_count == 1 and user_text and not user_text.strip() == "":
            return (
                "[ESCALATION STATE: The senior's response is unclear/confused/evasive (1st unclear response). "
                "Per TIER 2 rules, you may ask ONE clarifying question. "
                "If the next response is still not a clear 'I'm fine', you MUST escalate immediately.]"
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
        consecutive_silence_count = 0
        unclear_response_count = 0
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
                additional_information=self.config.prompt.additional_information
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

            raw_responses.append({
                "turn": turn_num,
                "prompt": llm_result["prompt"],
                "input_tokens": llm_result["input_tokens"],
                "output_tokens": llm_result["output_tokens"],
                "raw": llm_result["raw_content"],
                "parsed": parsed
            })

            # Add assistant response to history and transcript
            conversation_history.append(f"{self.ASSISTANT_PREFIX}{assistant_text}")
            transcript.append({
                "role": "assistant",
                "text": assistant_text,
                "turn": turn_num,
                "outcome": outcome
            })

            print(f"      Turn {turn_num}: Assistant -> {assistant_text[:80]}... [{outcome}]")

            # Check if conversation ended
            if self._is_terminal_outcome(outcome):
                actual_outcome = outcome
                termination_reason = "outcome_reached"
                break

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

            # Track conversation state for escalation metadata
            if not user_text or user_text.strip() == "":
                consecutive_silence_count += 1
            else:
                consecutive_silence_count = 0

            if user_text and not self._is_clear_confirmation(user_text):
                unclear_response_count += 1
            elif user_text and self._is_clear_confirmation(user_text):
                unclear_response_count = 0

            conversation_history.append(f"{self.USER_PREFIX}{user_text}")
            transcript.append({
                "role": "user",
                "text": user_text if user_text else "(silence)",
                "turn": turn_num
            })

            # Inject escalation state notes into conversation history
            state_note = self._build_state_note(consecutive_silence_count, unclear_response_count, user_text)
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
