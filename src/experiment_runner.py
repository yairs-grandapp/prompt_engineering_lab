"""
Experiment runner that orchestrates the entire experiment workflow.
"""
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
import openai
from dotenv import load_dotenv

from .config import ExperimentConfig, BehaviorConfig
from .data_loader import DataLoader, StatisticsCalculation
from .prompt_builder import PromptBuilder


class ExperimentRunner:
    """Runs experiments by coordinating data loading, prompt building, and API calls."""

    def __init__(self, config_path: str):
        """
        Initialize runner with experiment configuration.

        Args:
            config_path: Path to experiment config YAML file
        """
        self.config = ExperimentConfig.from_yaml(config_path)
        self.config_path = Path(config_path)
        self.experiment_dir = self.config_path.parent
        self.outputs_dir = self.experiment_dir / "outputs"
        self.outputs_dir.mkdir(exist_ok=True)

        # Load environment variables (API key)
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=api_key)

        # Initialize our modules
        self.data_loader = DataLoader()
        self.prompt_builder = PromptBuilder()

        # Track results
        self.daily_results = []
        self.weekly_result = None
        self.total_cost = 0.0

    def call_openai_api(self, prompt: str) -> str:
        """
        Call OpenAI API with the given prompt.

        Mirrors: callApi in gpt4o_api.dart

        Returns:
            JSON string response
        """
        response = self.client.chat.completions.create(
            model=self.config.model.name,
            messages=[
                {"role": "system", "content": "You are a Senior Care Expert."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=self.config.model.temperature
        )

        # Track costs (approximate)
        # gpt-4o-mini: $0.150/1M input tokens, $0.600/1M output tokens
        if self.config.model.name == "gpt-4o-mini":
            input_cost = (response.usage.prompt_tokens / 1_000_000) * 0.150
            output_cost = (response.usage.completion_tokens / 1_000_000) * 0.600
            self.total_cost += input_cost + output_cost

        return response.choices[0].message.content

    def generate_daily_summary(
        self,
        behavior: BehaviorConfig,
        date: datetime
    ) -> Dict:
        """
        Generate a daily summary for one behavior on one date.

        Args:
            behavior: Behavior configuration
            date: Date to summarize

        Returns:
            Dictionary with summary and metadata
        """
        print(f"Generating summary for {behavior.category}/{behavior.stat_id} on {date.strftime('%Y-%m-%d')}")

        # Load monthly regression data
        monthly_data = self.data_loader.load_monthly_regression(
            behavior.category,
            behavior.stat_id,
            date.month,
            date.year
        )

        # Extract daily stats for this specific day
        daily_stats = self.data_loader.extract_daily_stats(monthly_data, date.day)

        if not daily_stats:
            print(f"  Warning: No daily stats found for this date")
            return None

        # Get explanation and type
        explanation, stat_type = self.data_loader.get_statistic_explanation(
            behavior.category,
            behavior.stat_id
        )

        # Enhance stats with duration conversions if needed
        daily_stats = self.data_loader.enhance_stats_with_duration_conversions(
            daily_stats,
            stat_type
        )

        # Build additional guidelines
        additional_guidelines = self.prompt_builder.build_additional_guidelines(
            explanation,
            stat_type or 'unknown'
        )

        # Build prompt
        prompt = self.prompt_builder.build_daily_prompt(
            statistic_name=behavior.category,
            statistic_id=behavior.stat_id,
            statistic_explanation=explanation,
            daily_values=daily_stats,
            date=date,
            additional_guidelines=additional_guidelines,
            template_path=self.config.prompts.daily_template
        )

        # Call API
        response_json = self.call_openai_api(prompt)
        response = json.loads(response_json)

        # Build result
        result = {
            "behaviorCategory": behavior.category,
            "behaviorName": behavior.stat_id,
            "date": date.isoformat(),
            "summary": response.get("summary", ""),
            "inputData": {
                "explanation": explanation,
                "statisticType": stat_type,
                "dailyStats": [stat.to_dict() for stat in daily_stats]
            }
        }

        print(f"  ✓ Generated: {result['summary'][:80]}...")

        return result

    def run_daily_summaries(self) -> List[Dict]:
        """
        Run daily summary generation for all behaviors and dates.

        Returns:
            List of daily summary results
        """
        print(f"\n{'='*70}")
        print(f"Running Daily Summaries")
        print(f"{'='*70}\n")

        results = []

        # Iterate over date range
        current_date = self.config.test_data.start_date
        while current_date <= self.config.test_data.end_date:
            # Generate summary for each behavior on this date
            for behavior in self.config.test_data.behaviors:
                try:
                    result = self.generate_daily_summary(behavior, current_date)
                    if result:
                        results.append(result)

                        # Save individual result
                        filename = f"{behavior.category}_{behavior.stat_id}_{current_date.strftime('%Y-%m-%d')}.json"
                        output_path = self.outputs_dir / filename
                        with open(output_path, 'w') as f:
                            json.dump(result, f, indent=2)

                except Exception as e:
                    print(f"  ✗ Error: {e}")

            current_date += timedelta(days=1)

        return results

    def run_weekly_summary(self, daily_results: List[Dict]) -> Dict:
        """
        Generate weekly summary from daily results.

        Args:
            daily_results: List of daily summary dictionaries

        Returns:
            Weekly summary result
        """
        print(f"\n{'='*70}")
        print(f"Running Weekly Summary")
        print(f"{'='*70}\n")

        # Build prompt
        prompt = self.prompt_builder.build_weekly_prompt(
            senior_id=self.config.test_data.senior_id,
            week_start=self.config.test_data.start_date,
            week_end=self.config.test_data.end_date,
            daily_summaries=daily_results,
            template_path=self.config.prompts.weekly_template
        )

        # Call API
        response_json = self.call_openai_api(prompt)
        response = json.loads(response_json)

        # Build result
        result = {
            "seniorId": self.config.test_data.senior_id,
            "weekStart": self.config.test_data.start_date.strftime("%Y-%m-%d"),
            "weekEnd": self.config.test_data.end_date.strftime("%Y-%m-%d"),
            "summary": response.get("summary", ""),
            "dailySummaries": daily_results
        }

        print(f"✓ Generated weekly summary")
        print(f"  {result['summary'][:200]}...")

        # Save result
        filename = f"weekly_summary_{result['weekStart']}_to_{result['weekEnd']}.json"
        output_path = self.outputs_dir / filename
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)

        return result

    def run(self) -> Dict:
        """
        Run complete experiment: daily summaries + weekly summary.

        Returns:
            Dictionary with all results
        """
        print(f"\n{'#'*70}")
        print(f"# Experiment: {self.config.name}")
        print(f"# Date: {self.config.date}")
        print(f"# Model: {self.config.model.name}")
        print(f"{'#'*70}\n")

        # Run daily summaries
        self.daily_results = self.run_daily_summaries()

        # Run weekly summary
        self.weekly_result = self.run_weekly_summary(self.daily_results)

        print(f"\n{'='*70}")
        print(f"Experiment Complete")
        print(f"{'='*70}")
        print(f"Daily summaries generated: {len(self.daily_results)}")
        print(f"Estimated cost: ${self.total_cost:.4f}")
        print(f"Results saved to: {self.outputs_dir}")
        print(f"{'='*70}\n")

        return {
            "config": {
                "name": self.config.name,
                "date": self.config.date,
                "model": self.config.model.name,
                "temperature": self.config.model.temperature,
            },
            "daily_results": self.daily_results,
            "weekly_result": self.weekly_result,
            "total_cost": self.total_cost
        }
