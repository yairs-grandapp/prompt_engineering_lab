"""
Report generator that creates markdown reports from experiment results.
"""
import json
from pathlib import Path
from typing import Dict, List


class ReportGenerator:
    """Generates markdown reports from experiment results."""

    def __init__(self, experiment_dir: Path):
        self.experiment_dir = experiment_dir
        self.outputs_dir = experiment_dir / "outputs"

    def generate_report(self, results: Dict) -> str:
        """
        Generate a markdown report from experiment results.

        Args:
            results: Dictionary with experiment results

        Returns:
            Markdown report string
        """
        config = results['config']
        daily_results = results['daily_results']
        weekly_result = results['weekly_result']
        total_cost = results['total_cost']

        report = []

        # Header
        report.append(f"# Experiment: {config['name']}\n")
        report.append(f"**Date:** {config['date']}  ")
        report.append(f"**Model:** {config['model']}  ")
        report.append(f"**Temperature:** {config['temperature']}  ")
        report.append(f"**Estimated Cost:** ${total_cost:.4f}\n")
        report.append("---\n")

        # Daily Results Summary
        report.append("## Daily Summaries\n")
        report.append(f"**Total Generated:** {len(daily_results)}\n")

        # Group by behavior
        behaviors = {}
        for result in daily_results:
            behavior_key = f"{result['behaviorCategory']} - {result['behaviorName']}"
            if behavior_key not in behaviors:
                behaviors[behavior_key] = []
            behaviors[behavior_key].append(result)

        for behavior_key, summaries in behaviors.items():
            report.append(f"\n### {behavior_key}\n")

            for summary in summaries:
                date = summary['date'].split('T')[0]  # Extract just date part
                report.append(f"#### {date}\n")

                # Input data summary
                input_data = summary['inputData']
                report.append(f"**Explanation:** {input_data['explanation']}\n")
                report.append(f"**Type:** {input_data.get('statisticType', 'N/A')}\n")

                # Show key stats
                if input_data['dailyStats']:
                    report.append("\n**Statistics:**\n")
                    for stat in input_data['dailyStats']:
                        report.append(f"- **{stat['type']}:** ")
                        report.append(f"avg={stat['average']:.2f}, ")
                        report.append(f"slope={stat['slope']:.3f}, ")
                        report.append(f"last={stat['lastValue']:.1f}\n")

                # Generated summary
                report.append(f"\n**Generated Summary:**  \n")
                report.append(f"> {summary['summary']}\n\n")
                report.append("---\n")

        # Weekly Summary
        report.append("\n## Weekly Summary\n")
        report.append(f"**Period:** {weekly_result['weekStart']} to {weekly_result['weekEnd']}\n")
        report.append(f"\n**Generated Summary:**  \n")
        report.append(f"> {weekly_result['summary']}\n")

        return '\n'.join(report)

    def save_report(self, results: Dict):
        """
        Generate and save markdown report.

        Args:
            results: Dictionary with experiment results
        """
        report_content = self.generate_report(results)

        report_path = self.experiment_dir / "report.md"
        with open(report_path, 'w') as f:
            f.write(report_content)

        print(f"Report saved to: {report_path}")
