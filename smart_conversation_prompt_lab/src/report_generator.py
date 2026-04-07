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
        summary = results['summary']
        total_cost = results['total_cost']

        lines = []

        # Header
        lines.append(f"# Experiment: {config['name']}\n")
        lines.append(f"**Date:** {config['date']}  ")
        lines.append(f"**Model:** {config['model']}  ")
        lines.append(f"**Temperature:** {config['temperature']}  ")
        lines.append(f"**Prompt Template:** {config['prompt_template']}  ")
        lines.append(f"**Language:** {config['language']}  ")
        lines.append(f"**Estimated Cost:** ${total_cost:.4f}\n")
        lines.append("---\n")

        # Summary table
        lines.append("## Summary\n")
        lines.append(f"**Pass Rate: {summary['passed']}/{summary['total']} "
                      f"({summary['pass_rate']})**\n")
        lines.append("| # | Scenario | Expected | Actual | Result | Turns | Reason |")
        lines.append("|---|----------|----------|--------|--------|-------|--------|")

        for s in scenarios:
            result_icon = "PASS" if s['passed'] else "FAIL"
            lines.append(
                f"| {s['scenario_id']} | {s['scenario_name']} | "
                f"{s['expected_outcome']} | {s['actual_outcome']} | "
                f"{result_icon} | {s['turn_count']} | {s['termination_reason']} |"
            )

        lines.append("")
        lines.append("---\n")

        # Full transcripts
        lines.append("## Conversation Transcripts\n")

        for s in scenarios:
            result_icon = "PASS" if s['passed'] else "FAIL"
            lines.append(f"### {s['scenario_id']}: {s['scenario_name']} [{result_icon}]\n")
            lines.append(f"**Description:** {s['description']}  ")
            lines.append(f"**Expected:** {s['expected_outcome']}  ")
            lines.append(f"**Actual:** {s['actual_outcome']}  ")
            lines.append(f"**Turns:** {s['turn_count']}  ")
            lines.append(f"**Tokens:** {s['total_input_tokens']} in / "
                          f"{s['total_output_tokens']} out\n")

            # Prompts sent to LLM per turn
            raw_responses = s.get('raw_responses', [])
            if raw_responses:
                lines.append("**Prompts Sent to LLM:**\n")
                for rr in raw_responses:
                    turn = rr['turn']
                    prompt_text = rr.get('prompt', '(not captured)')
                    lines.append(f"<details>\n<summary>Turn {turn} - Full Prompt</summary>\n")
                    lines.append(f"```\n{prompt_text}\n```\n")
                    lines.append(f"</details>\n")

            lines.append("**Transcript:**\n")
            for entry in s['transcript']:
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

            lines.append("---\n")

        return '\n'.join(lines)

    def save_report(self, results: Dict[str, Any]):
        """Generate and save markdown report."""
        report_content = self.generate_report(results)
        report_path = self.experiment_dir / "report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"Report saved to: {report_path}")
