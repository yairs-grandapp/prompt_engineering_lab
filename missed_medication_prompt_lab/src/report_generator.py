"""
Report generator that creates markdown reports from experiment results.
"""
from pathlib import Path
from typing import Dict, Any, List


class ReportGenerator:
    """Generates markdown reports from conversation experiment results."""

    def __init__(self, experiment_dir: Path):
        self.experiment_dir = experiment_dir

    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a markdown report from experiment results."""
        config = results['config']
        scenarios = results['results']
        model_summaries = results['model_summaries']
        models = config['models']

        lines = []

        # Header
        lines.append(f"# Experiment: {config['name']}\n")
        lines.append(f"**Date:** {config['date']}  ")
        lines.append(f"**Models:** {', '.join(models)}  ")
        lines.append(f"**Prompt Template:** {config['prompt_template']}\n")
        lines.append("---\n")

        # Full prompt template
        prompt_snapshot_path = self.experiment_dir / "prompt_snapshot.txt"
        if prompt_snapshot_path.exists():
            with open(prompt_snapshot_path, 'r', encoding='utf-8') as f:
                prompt_text = f.read()
            lines.append("## Prompt Template\n")
            lines.append("The full prompt sent to the LLM (with conversation history placeholder):\n")
            lines.append(f"```\n{prompt_text}\n```\n")
            lines.append("---\n")

        # Summary per model
        lines.append("## Summary\n")
        for model_name, summary in model_summaries.items():
            lines.append(f"**{model_name}:** {summary['passed']}/{summary['total']} "
                          f"passed ({summary['pass_rate']})  ")
        lines.append("")

        # Summary table with columns for each model
        header = "| # | Scenario | Expected |"
        separator = "|---|----------|----------|"
        for m in models:
            header += f" {m} Outcome | {m} Result | {m} Turns |"
            separator += "--------|--------|-------|"
        lines.append(header)
        lines.append(separator)

        for s in scenarios:
            row = f"| {s['scenario_id']} | {s['scenario_name']} | {s['expected_outcome']} |"
            for m in models:
                r = s['model_results'][m]
                result_icon = "PASS" if r['passed'] else "FAIL"
                row += f" {r['actual_outcome']} | {result_icon} | {r['turn_count']} |"
            lines.append(row)

        lines.append("")
        lines.append("---\n")

        # Full transcripts per scenario, side by side per model
        lines.append("## Conversation Transcripts\n")

        for s in scenarios:
            lines.append(f"### {s['scenario_id']}: {s['scenario_name']}\n")
            lines.append(f"**Description:** {s['description']}  ")
            lines.append(f"**Expected:** {s['expected_outcome']}\n")

            for m in models:
                r = s['model_results'][m]
                result_icon = "PASS" if r['passed'] else "FAIL"
                lines.append(f"#### {m} [{result_icon}]\n")
                lines.append(f"**Actual:** {r['actual_outcome']}  ")
                lines.append(f"**Turns:** {r['turn_count']}  ")
                lines.append(f"**Tokens:** {r['total_input_tokens']} in / "
                              f"{r['total_output_tokens']} out\n")

                # The full assembled prompt is shown once at the top of this
                # report (from prompt_snapshot.txt); it is intentionally not
                # repeated per turn here or in the conversation transcripts.

                lines.append("**Transcript:**\n")
                for entry in r['transcript']:
                    role = entry['role'].upper()
                    text = entry['text']
                    turn = entry['turn']

                    if role == "ASSISTANT":
                        outcome = entry.get('outcome', '')
                        lines.append(f"> **[Turn {turn}] ASSISTANT** [{outcome}]:  ")
                        lines.append(f"> {text}\n")
                    elif role == "USER":
                        lines.append(f"> **[Turn {turn}] USER:**  ")
                        lines.append(f"> {text}\n")
                    elif role == "SYSTEM":
                        lines.append(f"> **[Turn {turn}] SYSTEM:**  ")
                        lines.append(f"> _{text}_\n")
                    elif role == "ERROR":
                        lines.append(f"> **[Turn {turn}] ERROR:**  ")
                        lines.append(f"> {text}\n")

                lines.append("")

            lines.append("---\n")

        return '\n'.join(lines)

    def save_report(self, results: Dict[str, Any]):
        """Generate and save markdown report."""
        report_content = self.generate_report(results)
        report_path = self.experiment_dir / "report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"Report saved to: {report_path}")
