"""
Prompt builder that renders templates with data.
Mirrors the logic from gpt_handler.dart
"""
import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from .data_loader import StatisticsCalculation


class PromptBuilder:
    """Builds prompts from templates, mirroring Dart gpt_handler logic."""

    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = Path(prompts_dir)

    def load_template(self, template_path: str) -> str:
        """Load a prompt template file."""
        full_path = self.prompts_dir / template_path
        with open(full_path, 'r') as f:
            return f.read()

    def build_daily_prompt(
        self,
        statistic_name: str,
        statistic_id: str,
        statistic_explanation: str,
        daily_values: List[StatisticsCalculation],
        date: datetime,
        additional_guidelines: str,
        template_path: str
    ) -> str:
        """
        Build daily summary prompt.

        Mirrors: createPrompt in gpt_handler.dart (lines 50-107)

        Args:
            statistic_name: Behavior category (e.g., "bathroom")
            statistic_id: Specific stat (e.g., "hygiene usage")
            statistic_explanation: Human-readable explanation
            daily_values: List of StatisticsCalculation objects
            date: Date being summarized
            additional_guidelines: Extra context about stat types
            template_path: Path to prompt template

        Returns:
            Rendered prompt string
        """
        template = self.load_template(template_path)

        # Format date like Dart: "December 15, 2024"
        date_string = date.strftime("%B %d, %Y")

        # Convert daily_values to JSON (matching Dart's jsonEncode)
        daily_values_json = json.dumps(
            [stat.to_dict() for stat in daily_values],
            indent=2
        )

        # Render template (Python format strings match our {variable} syntax)
        prompt = template.format(
            statistic_id=statistic_id,
            statistic_name=statistic_name,
            statistic_explanation=statistic_explanation,
            date_string=date_string,
            daily_values_json=daily_values_json,
            additional_guidelines=additional_guidelines
        )

        return prompt

    def build_additional_guidelines(
        self,
        stat_explanation: str,
        stat_type: str
    ) -> str:
        """
        Build additional guidelines section.

        Mirrors: behavioral_statistics_summary_manager.dart lines 304-345
        """
        guidelines = {
            "Additional Guidelines": {
                "types": {
                    StatisticsCalculation.DAYS_IN_WEEK_TYPE:
                        "This calculation represents the values (averages, slopes etc'...) of the current statistics daily value over the last week. I.E - average of 20 would mean that the daily average over the past week was 20.",
                    StatisticsCalculation.DAYS_IN_MONTH_TYPE:
                        "This calculation is the same as the weekly calculation, but represents the daily values over the past month.",
                    StatisticsCalculation.DAYS_IN_YEAR_TYPE:
                        "This calculation is the same as the weekly calculation, but represents the daily values over the past year."
                }
            }
        }

        # Add stat-type specific guidance
        if stat_type == 'duration':
            stat_explanation += '\n  -  Notice that total and last duration values are provided in minutes, hours, etc..., make sure to use the most appropriate unit for the care giver who reads these summaries.'
        elif stat_type == 'quantitative':
            stat_explanation += '\n  -  Notice that the total and last values provided are the amount of occurrences of the statistic, not a duration.'

        return json.dumps(guidelines)

    def build_weekly_prompt(
        self,
        senior_id: str,
        week_start: datetime,
        week_end: datetime,
        daily_summaries: List[Dict],
        template_path: str
    ) -> str:
        """
        Build weekly summary prompt.

        Mirrors: createWeeklyPrompt in gpt_handler.dart (lines 134-187)

        Args:
            senior_id: Senior ID
            week_start: Start date of week
            week_end: End date of week
            daily_summaries: List of DailyDetailsSummary dicts
            template_path: Path to prompt template

        Returns:
            Rendered prompt string
        """
        template = self.load_template(template_path)

        # Format dates like Dart: "12/15/2024"
        start_str = week_start.strftime("%m/%d/%Y")
        end_str = week_end.strftime("%m/%d/%Y")

        # Convert daily summaries to JSON
        daily_summaries_json = json.dumps(daily_summaries, indent=2)

        # Render template
        prompt = template.format(
            week_start=start_str,
            week_end=end_str,
            daily_summaries_json=daily_summaries_json
        )

        return prompt
