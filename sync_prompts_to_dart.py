#!/usr/bin/env python3
"""
Sync prompt templates from Python lab to Dart production code.

This script reads prompt templates from prompts/ directory,
converts {variable} syntax to Dart $variable syntax,
and generates properly formatted Dart functions.

Usage:
    python sync_prompts_to_dart.py

Configuration:
    Edit SYNC_CONFIG below to change source/target mappings
"""
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple


# Configuration: Map Python template files to Dart output files
SYNC_CONFIG = [
    {
        "source": "prompts/daily_summary_v4.txt",
        "target": "../grandappflutter/picmein/picmein_device_apps/picmein_device/lib/managers/senior_behaviors_managers/behavioral_statistics_summary_manager/utils/prompts/daily_prompt.dart",
        "function_name": "getDailySummaryPrompt",
        "description": "Daily summary prompt for behavioral statistics.",
        "variable_mappings": {
            # Python template -> Dart parameter (camelCase conversion)
            "date_string": "dateString",
            "statistic_id": "statisticId",
            "statistic_explanation": "statisticExplanation",
            "additional_guidelines": "additionalGuidelines",
            "daily_values_json": "dailyValuesJson",
        }
    },
    {
        "source": "prompts/weekly_summary_v2.txt",
        "target": "../grandappflutter/picmein/picmein_device_apps/picmein_device/lib/managers/senior_behaviors_managers/behavioral_statistics_summary_manager/utils/prompts/weekly_prompt.dart",
        "function_name": "getWeeklySummaryPrompt",
        "description": "Weekly summary prompt for behavioral statistics.",
        "variable_mappings": {
            "start_date": "startDate",
            "end_date": "endDate",
            "daily_summaries_json": "dailySummariesJson",
        }
    }
]


class PromptSyncer:
    """Syncs prompt templates from Python to Dart."""

    def __init__(self, lab_root: Path):
        self.lab_root = lab_root

    def extract_variables(self, template_content: str) -> List[str]:
        """
        Extract all {variable} placeholders from template.

        Returns:
            List of variable names (without braces)
        """
        pattern = r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}'
        variables = re.findall(pattern, template_content)
        # Remove duplicates while preserving order
        seen = set()
        unique_vars = []
        for var in variables:
            if var not in seen:
                seen.add(var)
                unique_vars.append(var)
        return unique_vars

    def python_to_dart_template(self, template_content: str, variable_mappings: Dict[str, str]) -> str:
        """
        Convert Python {variable} syntax to Dart $variable syntax.

        Args:
            template_content: Original template with {variable}
            variable_mappings: Dict mapping Python var names to Dart param names

        Returns:
            Dart-compatible template string
        """
        dart_template = template_content

        # Replace each {variable} with $dartVariable
        for python_var, dart_var in variable_mappings.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\{' + python_var + r'\}'
            dart_template = re.sub(pattern, f'${dart_var}', dart_template)

        # Escape any remaining curly braces that aren't part of variables
        # (these would be literal braces in the prompt)
        # Handle double braces {{ and }} which are used for literal braces in JSON examples
        dart_template = dart_template.replace('{{', '{')
        dart_template = dart_template.replace('}}', '}')

        return dart_template

    def generate_dart_function_signature(
        self,
        function_name: str,
        variable_mappings: Dict[str, str]
    ) -> str:
        """
        Generate Dart function signature with named parameters.

        Args:
            function_name: Name of the Dart function
            variable_mappings: Dict of Python vars to Dart params

        Returns:
            Dart function signature string
        """
        params = []
        for dart_param in variable_mappings.values():
            params.append(f"  required String {dart_param},")

        params_str = "\n".join(params)

        return f"""String {function_name}({{
{params_str}
}})"""

    def generate_dart_file(
        self,
        source_file: str,
        template_content: str,
        function_name: str,
        description: str,
        variable_mappings: Dict[str, str]
    ) -> str:
        """
        Generate complete Dart file content.

        Returns:
            Complete Dart file as string
        """
        # Convert template
        dart_template = self.python_to_dart_template(template_content, variable_mappings)

        # Generate function signature
        signature = self.generate_dart_function_signature(function_name, variable_mappings)

        # Get current date
        today = datetime.now().strftime("%Y-%m-%d")

        # Build complete file
        dart_file = f'''/// {description}
///
/// This file is AUTO-GENERATED from the prompt engineering lab.
/// DO NOT EDIT MANUALLY - use sync_prompts_to_dart.py instead.
///
/// Source: {source_file}
/// Last synced: {today}

{signature} {{
  return \'\'\'
{dart_template}\'\'\'.trim();
}}
'''

        return dart_file

    def sync_prompt(self, config: Dict) -> bool:
        """
        Sync a single prompt template to Dart.

        Args:
            config: Configuration dict for this sync

        Returns:
            True if successful, False otherwise
        """
        source_path = self.lab_root / config["source"]
        target_path = self.lab_root / config["target"]

        print(f"\n{'='*70}")
        print(f"Syncing: {config['source']}")
        print(f"Target:  {config['target']}")
        print(f"{'='*70}")

        # Read source template
        if not source_path.exists():
            print(f"❌ ERROR: Source file not found: {source_path}")
            return False

        with open(source_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        print(f"✓ Read source template ({len(template_content)} chars)")

        # Extract variables
        extracted_vars = self.extract_variables(template_content)
        print(f"✓ Extracted variables: {extracted_vars}")

        # Verify all variables are mapped
        missing_mappings = [v for v in extracted_vars if v not in config["variable_mappings"]]
        if missing_mappings:
            print(f"⚠️  WARNING: Variables without mappings: {missing_mappings}")
            print(f"   These will remain as {{variable}} in the output.")

        # Generate Dart file
        dart_content = self.generate_dart_file(
            source_file=config["source"],
            template_content=template_content,
            function_name=config["function_name"],
            description=config["description"],
            variable_mappings=config["variable_mappings"]
        )

        # Ensure target directory exists
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Write Dart file
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(dart_content)

        print(f"✓ Written to: {target_path}")
        print(f"✓ Function: {config['function_name']}")
        print(f"✓ Parameters: {list(config['variable_mappings'].values())}")

        return True

    def sync_all(self) -> bool:
        """
        Sync all configured prompts.

        Returns:
            True if all syncs successful, False otherwise
        """
        print(f"\n{'#'*70}")
        print(f"# Prompt Engineering Lab → Dart Production Sync")
        print(f"# {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'#'*70}")

        results = []
        for config in SYNC_CONFIG:
            success = self.sync_prompt(config)
            results.append(success)

        print(f"\n{'='*70}")
        if all(results):
            print(f"✅ All {len(results)} prompts synced successfully!")
        else:
            failed_count = sum(1 for r in results if not r)
            print(f"⚠️  {failed_count}/{len(results)} prompts failed to sync")
        print(f"{'='*70}\n")

        return all(results)


def main():
    """Main entry point."""
    # Determine lab root (script is in lab root)
    script_dir = Path(__file__).parent.absolute()

    syncer = PromptSyncer(lab_root=script_dir)
    success = syncer.sync_all()

    if not success:
        exit(1)


if __name__ == "__main__":
    main()
