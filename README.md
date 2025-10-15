# Prompt Engineering Lab

A Python-based experimentation environment for iterating on prompts for senior behavioral statistics summaries. This lab mirrors the logic from the Dart production code, allowing rapid prompt iteration with real data.

## Features

- **Dart-Compatible Templates**: Prompts use `{variable}` syntax that can be easily copied back to Dart
- **Real Data**: Uses actual monthly regression calculations from the production system
- **Fast Iteration**: No compilation needed, instant feedback
- **Experiment Tracking**: All results documented with prompts, outputs, and costs
- **Report Generation**: Auto-generated markdown reports for easy comparison

## Setup

### 1. Install Python Dependencies

```bash
cd prompt_engineering_lab
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

Get your API key from: https://platform.openai.com/api-keys

### 3. Verify Data Files

Check that the following data files exist:
- `data/statistics_explanations.json`
- `data/available_stats.json`
- `data/monthly_regressions/` (5 behavior folders)

## Usage

### Running an Experiment

```bash
python run_experiment.py exp_001_baseline
```

This will:
1. Load configuration from `experiments/exp_001_baseline/config.yaml`
2. Generate 35 daily summaries (5 behaviors × 7 days)
3. Generate 1 weekly summary
4. Save all outputs to `experiments/exp_001_baseline/outputs/`
5. Generate a report at `experiments/exp_001_baseline/report.md`

### Creating a New Experiment

1. Copy an existing experiment:
   ```bash
   cp -r experiments/exp_001_baseline experiments/exp_002_my_experiment
   ```

2. Edit the config:
   ```yaml
   # experiments/exp_002_my_experiment/config.yaml
   experiment:
     name: "My Experiment - Testing Warmer Tone"
     date: "2025-10-14"

   prompts:
     daily_template: "daily_summary_v2.txt"  # Use new template
     weekly_template: "weekly_summary_v1.txt"
   ```

3. Create your new prompt template:
   ```bash
   cp prompts/daily_summary_v1.txt prompts/daily_summary_v2.txt
   # Edit daily_summary_v2.txt with your improvements
   ```

4. Run the experiment:
   ```bash
   python run_experiment.py exp_002_my_experiment
   ```

## Project Structure

```
prompt_engineering_lab/
├── data/                          # Test data from production
│   ├── statistics_explanations.json
│   ├── available_stats.json
│   └── monthly_regressions/
│       ├── bathroom_hygiene_usage_10-2025/
│       ├── bathroom_Shower_usage_10-2025/
│       ├── toilet_Toilet_usage_urination_10-2025/
│       ├── sleep_Sleep_duration_10-2025/
│       └── movement_Movements_duration_10-2025/
├── prompts/
│   ├── daily_summary_v1.txt      # Baseline daily prompt
│   ├── daily_summary_v2.txt      # Your improved version
│   └── weekly_summary_v1.txt     # Baseline weekly prompt
├── experiments/
│   └── exp_001_baseline/
│       ├── config.yaml            # Experiment configuration
│       ├── outputs/               # Generated summaries (JSON)
│       └── report.md             # Auto-generated report
├── src/
│   ├── config.py                 # Configuration loader
│   ├── data_loader.py            # Data loading (mirrors Dart file_handler)
│   ├── prompt_builder.py         # Prompt rendering (mirrors Dart gpt_handler)
│   ├── experiment_runner.py      # Orchestrates experiments
│   └── report_generator.py       # Generates markdown reports
└── run_experiment.py             # Main entry point
```

## Workflow: Iterating on Prompts

### 1. Baseline Run
```bash
python run_experiment.py exp_001_baseline
```
Review `experiments/exp_001_baseline/report.md` to see current outputs.

### 2. Create Improved Version
```bash
# Copy template
cp prompts/daily_summary_v1.txt prompts/daily_summary_v2.txt

# Edit prompts/daily_summary_v2.txt
# Example: Make tone warmer, add more context, etc.
```

### 3. Run New Experiment
```bash
# Create new experiment
cp -r experiments/exp_001_baseline experiments/exp_002_warmer_tone

# Update config to use v2 template
# Edit experiments/exp_002_warmer_tone/config.yaml

# Run
python run_experiment.py exp_002_warmer_tone
```

### 4. Compare Results
Open both reports side-by-side:
- `experiments/exp_001_baseline/report.md`
- `experiments/exp_002_warmer_tone/report.md`

### 5. Copy Winner Back to Dart
Once you find the best prompt:
1. Open the winning template (e.g., `prompts/daily_summary_v3.txt`)
2. Copy the content
3. Open `picmein_device/lib/managers/.../gpt_handler.dart`
4. Paste into `createPrompt()` method
5. Replace Python `{variables}` with Dart `$variables`

## Configuration Options

### Experiment Config (`config.yaml`)

```yaml
experiment:
  name: "Descriptive experiment name"
  date: "YYYY-MM-DD"

model:
  name: "gpt-4o-mini"  # or "gpt-4o"
  temperature: 0.7      # 0.0 to 1.0

prompts:
  daily_template: "daily_summary_v1.txt"
  weekly_template: "weekly_summary_v1.txt"

test_data:
  senior_id: "A_LK611111SGPD_senior_1744703199152"

  behaviors:
    - category: "bathroom"
      stat_id: "hygiene usage"
    # Add more behaviors...

  date_range:
    start: "2025-10-01"
    end: "2025-10-07"  # 7 days = 1 week
```

### Prompt Template Variables

Daily templates support:
- `{statistic_id}`: e.g., "hygiene usage"
- `{statistic_name}`: e.g., "bathroom"
- `{statistic_explanation}`: Human-readable description
- `{date_string}`: e.g., "October 1, 2025"
- `{daily_values_json}`: JSON array of StatisticsCalculation objects
- `{additional_guidelines}`: Extra context about stat types

Weekly templates support:
- `{week_start}`: e.g., "10/01/2025"
- `{week_end}`: e.g., "10/07/2025"
- `{daily_summaries_json}`: JSON array of all daily summaries

## Cost Tracking

The lab tracks approximate costs for each experiment:
- **gpt-4o-mini**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- **Typical cost per experiment** (5 behaviors × 7 days + 1 weekly): ~$0.10-0.30

Costs are displayed at the end of each run and included in the report.

## Tips

1. **Start Small**: Test on 1-2 behaviors first before running full experiments
2. **Version Everything**: Name templates with versions (v1, v2, v3)
3. **Document Changes**: Note what you changed in experiment names
4. **Compare Side-by-Side**: Open reports in split view for easy comparison
5. **Iterate Quickly**: The goal is fast cycles - don't overthink it!

## Troubleshooting

**Error: OPENAI_API_KEY not found**
- Make sure `.env` file exists (copy from `.env.example`)
- Add your actual API key to `.env`

**Error: No JSON file found in data/monthly_regressions/...**
- Check that data files were copied correctly
- Verify file structure matches expected format

**Import Errors**
- Make sure you're running from the `prompt_engineering_lab/` directory
- Check that all dependencies are installed: `pip install -r requirements.txt`

## What We Learned

This lab demonstrates several key software engineering principles:

1. **Separation of Concerns**: Data loading, prompt building, API calling, and reporting are separate modules
2. **Configuration as Code**: YAML configs make experiments reproducible
3. **Rapid Iteration**: Python's interpreted nature allows instant feedback
4. **Cross-Language Compatibility**: Template variable syntax designed for easy Dart translation
5. **Real Data Testing**: Using production data ensures prompts work in real scenarios
# prompt_engineering_lab
