"""
Data loader for monthly regression files and statistic explanations.
Mirrors the logic from behavioral_statistics_summary_manager.dart
"""
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class StatisticsCalculation:
    """Python representation of Dart StatisticsCalculation class."""

    # Constants from StatisticsCalculation.dart
    DAYS_IN_WEEK_TYPE = "DaysInWeek"
    DAYS_IN_MONTH_TYPE = "DaysInMonth"
    DAYS_IN_YEAR_TYPE = "DaysInYear"

    def __init__(self, data: Dict):
        self.statistic_name = data.get('statisticName', '')
        self.statistic_id = data.get('statisticId', '')
        self.type = data.get('type', '')
        self.slope = data.get('slope', 0.0)
        self.average = data.get('average', 0.0)
        self.total = data.get('total', 0.0)
        self.number_of_values = data.get('numberOfValues', 0)
        self.last_value = data.get('lastValue', 0.0)
        self.additional_values = data.get('additionalValues', {})

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'statisticName': self.statistic_name,
            'statisticId': self.statistic_id,
            'type': self.type,
            'slope': self.slope,
            'average': self.average,
            'total': self.total,
            'numberOfValues': self.number_of_values,
            'lastValue': self.last_value,
            'additionalValues': self.additional_values
        }


class DataLoader:
    """Loads and processes behavioral statistics data."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.explanations = self._load_explanations()

    def _load_explanations(self) -> Dict:
        """Load statistic explanations from JSON file."""
        explanations_path = self.data_dir / "statistics_explanations.json"
        with open(explanations_path, 'r') as f:
            return json.load(f)

    def _sanitize_for_filename(self, text: str) -> str:
        """
        Sanitize stat_id for use in filename.
        Replaces spaces with underscores and removes parentheses.
        """
        # Replace spaces with underscores
        sanitized = text.replace(' ', '_')
        # Remove parentheses
        sanitized = sanitized.replace('(', '').replace(')', '')
        return sanitized

    def load_monthly_regression(
        self,
        behavior_category: str,
        stat_id: str,
        month: int,
        year: int
    ) -> List[Dict[str, Dict]]:
        """
        Load monthly regression calculations.
        Returns list of daily calculations (31 days).

        Mirrors: getMonthlyRegressionCalculationsStatisticsJson in file_handler.dart
        """
        # Sanitize stat_id for filename (spaces → underscores, remove parentheses)
        sanitized_stat_id = self._sanitize_for_filename(stat_id)

        # Format filename to match our copied structure
        filename = f"{behavior_category}_{sanitized_stat_id}_{month}-{year}"
        regression_dir = self.data_dir / "monthly_regressions" / filename

        # Find the versioned JSON file
        json_files = list(regression_dir.glob("*.json"))
        if not json_files:
            raise FileNotFoundError(f"No JSON file found in {regression_dir}")

        json_path = json_files[0]  # Take the first (should be only one)

        with open(json_path, 'r') as f:
            data = json.load(f)

        all_stats = data.get('allStatisticsCalculation', {})
        calculations = all_stats.get('calculations', [])

        return calculations

    def extract_daily_stats(
        self,
        monthly_data: List[Dict[str, Dict]],
        day: int
    ) -> List[StatisticsCalculation]:
        """
        Extract DaysInWeek, DaysInMonth, DaysInYear stats for a specific day.

        Mirrors: _generateDailySummaryForDay in behavioral_statistics_summary_manager.dart (lines 292-303)

        Args:
            monthly_data: List of 31 day calculations
            day: Day of month (1-31)

        Returns:
            List of StatisticsCalculation objects
        """
        day_index = day - 1  # Convert to 0-based index

        if day_index >= len(monthly_data):
            raise ValueError(f"Day {day} not found in monthly data (only {len(monthly_data)} days)")

        day_data = monthly_data[day_index]

        # Extract the specific types we need (matching Dart code line 296)
        types_to_extract = [
            StatisticsCalculation.DAYS_IN_WEEK_TYPE,
            StatisticsCalculation.DAYS_IN_MONTH_TYPE,
            StatisticsCalculation.DAYS_IN_YEAR_TYPE
        ]

        daily_stats = []
        for stat_type in types_to_extract:
            if stat_type in day_data:
                daily_stats.append(StatisticsCalculation(day_data[stat_type]))

        return daily_stats

    def get_statistic_explanation(
        self,
        behavior_category: str,
        stat_id: str
    ) -> tuple[str, Optional[str]]:
        """
        Get explanation and type for a statistic.

        Mirrors: getStatisticIdExplanations and _isStatisticExplanationExists
        in behavioral_statistics_summary_manager.dart (lines 314-345)

        Returns:
            Tuple of (explanation, statistic_type)
            statistic_type is either 'duration', 'quantitative', or None
        """
        data = self.explanations.get('data', {})

        if behavior_category not in data:
            return f"No explanation was available for {behavior_category}:{stat_id}", None

        category_data = data[behavior_category]

        if stat_id not in category_data:
            return f"No explanation was available for {behavior_category}:{stat_id}", None

        stat_data = category_data[stat_id]

        explanation = stat_data.get('explanation', f"No explanation was available for {behavior_category}:{stat_id}")
        stat_type = stat_data.get('statisticType', None)

        return explanation, stat_type

    def enhance_stats_with_duration_conversions(
        self,
        stats: List[StatisticsCalculation],
        stat_type: Optional[str]
    ) -> List[StatisticsCalculation]:
        """
        Add duration conversions and trend classification.

        For duration stats:
        - Converts average and lastValue from milliseconds to hours
        - Keeps raw values in additional_values for reference

        For all stats:
        - Classifies slope into trend: "increasing", "stable", or "decreasing"

        Mirrors: behavioral_statistics_summary_manager.dart lines 323-335 (enhanced)
        """
        for stat in stats:
            # Classify trend based on slope threshold
            slope_threshold = 0.05  # Same threshold used in prompt
            if stat.slope > slope_threshold:
                trend = "increasing"
            elif stat.slope < -slope_threshold:
                trend = "decreasing"
            else:
                trend = "stable"

            if stat_type == 'duration':
                # Store raw millisecond values for reference
                raw_average = stat.average
                raw_last_value = stat.last_value
                raw_total = stat.total
                raw_slope = stat.slope

                # Convert main fields from milliseconds to hours
                stat.average = stat.average / 1000 / 60 / 60  # ms → hours
                stat.last_value = stat.last_value / 1000 / 60 / 60  # ms → hours
                stat.total = stat.total / 1000 / 60 / 60  # ms → hours
                stat.slope = stat.slope / 1000 / 60 / 60  # ms/day → hours/day

                # Keep raw values and add trend in additional_values
                stat.additional_values = {
                    'averageMs': raw_average,
                    'lastValueMs': raw_last_value,
                    'totalMs': raw_total,
                    'slopeMs': raw_slope,
                    'trend': trend,
                    'unit': 'hours'
                }
            else:
                # For count-based stats, just add trend
                stat.additional_values = {
                    'trend': trend,
                    'unit': 'count'
                }

        return stats
