# Missed Medication Prompt Lab

A multi-turn conversation testing tool for the SeniorMatics "missed medication" smart assistant prompt (Vega). Allows systematic iteration and validation of prompt changes before deploying to production.

## How It Works

The tool simulates the full conversation loop that the production system (`ContextBase.buildPrompt()` + `ContextMedicationMissed`) performs:

1. Builds the prompt with conversation history
2. Calls the LLM (OpenAI API)
3. Parses the JSON response (`text` + `conversationOutcome`)
4. Appends the assistant response to history
5. If the conversation isn't over, appends the next scripted user turn
6. Repeats until an outcome is reached or max turns exceeded

Each scenario has a predefined set of simulated senior responses and an expected outcome. The tool checks if the LLM reaches the correct outcome and generates a pass/fail report.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create `.env` file

```
OPENAI_API_KEY=sk-your-key-here
```

### 3. Run an experiment

```bash
python test_prompt.py exp_001_baseline
```

Results are saved to:
- `experiments/exp_001_baseline/outputs/` — individual conversation transcripts (JSON)
- `experiments/exp_001_baseline/report.md` — summary table + full transcripts

## Project Structure

```
missed_medication_prompt_lab/
├── test_prompt.py                      # CLI entry point
├── requirements.txt                    # Python dependencies
├── .env                                # OpenAI API key (not committed)
├── data/
│   ├── prompts/
│   │   └── prompt_v0.txt               # Baseline prompt (exact production replica)
│   └── inputs/
│       └── inputs_v0.json              # Test scenarios (4 multi-turn conversations)
├── experiments/
│   └── exp_001_baseline/
│       ├── config.yaml                 # Experiment configuration
│       ├── outputs/                    # Generated conversation transcripts
│       └── report.md                   # Generated markdown report
└── src/
    ├── config.py                       # YAML config loader
    ├── prompt_builder.py               # Template loading + variable injection
    ├── conversation_runner.py          # Multi-turn conversation loop
    ├── experiment_runner.py            # Orchestrates all scenarios
    └── report_generator.py             # Markdown report generation
```

## Experiment Configuration

Each experiment lives in `experiments/<name>/config.yaml`:

```yaml
experiment:
  name: "Baseline - Production Missed Medication Prompt v0"
  date: "2026-04-07"

model:
  name: "gpt-4o-mini"        # or gpt-4o, gpt-4.1-mini, gpt-4.1
  temperature: 0.7

prompt:
  template: "prompt_v0.txt"   # prompt file from data/prompts/
  language: "English"          # conversation language
  assistant_gender: "female"
  additional_information:      # optional JSON passed to the prompt
    scheduledTime: "2026-07-29T08:00"
    reminderCount: 0

conversation:
  max_turns: 10                # safety cap on LLM calls per scenario
  extra_silence_turns: 2       # empty turns to inject when scripted inputs run out

inputs_file: "inputs_v0.json"  # scenario file from data/inputs/
```

## Test Scenarios (inputs_v0.json)

Each scenario defines a conversation with scripted senior responses and an expected outcome:

| # | Scenario | Expected Outcome |
|---|----------|-----------------|
| 1 | Senior already took medication | DID_TAKE |
| 2 | Senior forgot but will take it now | DID_NOT_TAKE_BUT_WILL_TAKE |
| 3 | Senior refuses to take medication | DID_NOT_TAKE_IT_AND_WILL_NOT_TAKE |
| 4 | Senior doesn't respond (silence) | COULD_NOT_VALIDATE |

Scenarios can optionally include system events (e.g., sensor updates) injected between turns via a `system_events` array on a user turn.

## Possible Outcomes

The four terminal outcomes (any of these ends the conversation):

- `DID_TAKE` — senior says they already took it, but the pillbox sensor never confirmed it
- `DID_NOT_TAKE_BUT_WILL_TAKE` — senior commits to taking it now
- `DID_NOT_TAKE_IT_AND_WILL_NOT_TAKE` — senior explicitly refuses
- `COULD_NOT_VALIDATE` — no answer / confused / can't remember / upset

Plus the non-terminal state:

- `conversation_in_progress` — conversation continues (next turn)

Each terminal outcome has a designated standard message the assistant must deliver **before** returning it (clarification message → `DID_TAKE`, Reminder #2 → `DID_NOT_TAKE_BUT_WILL_TAKE`, Message #2 → `DID_NOT_TAKE_IT_AND_WILL_NOT_TAKE`, soft message → `COULD_NOT_VALIDATE`). See `data/prompts/prompt_v0.txt`.

## Iterating on Prompts

### Workflow

1. **Run baseline**: `python test_prompt.py exp_001_baseline`
2. **Review report**: open `experiments/exp_001_baseline/report.md` and check pass/fail + transcripts
3. **Create new prompt version**: copy `data/prompts/prompt_v0.txt` to `prompt_v1.txt`, make changes
4. **Create new experiment**: copy `experiments/exp_001_baseline/` to `experiments/exp_002_improved/`, update `config.yaml` to point to `prompt_v1.txt`
5. **Run**: `python test_prompt.py exp_002_improved`
6. **Compare**: review both reports side-by-side
7. **Repeat** until satisfied, then deploy the winning prompt

### Adding New Test Scenarios

Edit `data/inputs/inputs_v0.json` or create a new file (e.g., `inputs_v1.json`) and point to it in the experiment config.

Scenario format:

```json
{
  "id": "scenario_16",
  "name": "Description of the scenario",
  "description": "What this scenario tests",
  "expected_outcome": "DID_TAKE",
  "user_turns": [
    { "text": "First senior response" },
    {
      "text": "Second response after a system event",
      "system_events": [
        {
          "type": "sensor_update",
          "message": "Update: The home sensors have just detected activity..."
        }
      ]
    }
  ]
}
```

`expected_outcome` must be one of the four terminal outcomes listed above.

## Prompt Template Variables

The prompt template (`data/prompts/prompt_v0.txt`) uses these placeholders:

| Variable | Source | Description |
|----------|--------|-------------|
| `{language}` | config.yaml | Conversation language (e.g., English, Hebrew) |
| `{assistant_gender}` | config.yaml | Assistant gender for grammar (e.g., female) |
| `{additional_information_guidelines}` | auto-generated | Built from `additional_information` in config |
| `{conversation_history}` | auto-generated | Accumulated `@ASSISTANT@:` / `@USER@:` / `@SYSTEM@:` turns |

Use `{{` and `}}` for literal curly braces in the template (Python format string escaping).