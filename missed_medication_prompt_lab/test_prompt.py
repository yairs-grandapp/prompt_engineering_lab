#!/usr/bin/env python3
"""
Smart Conversation Prompt Lab - Entry Point

Usage:
    python test_prompt.py <experiment_name>

Example:
    python test_prompt.py exp_001_baseline
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.experiment_runner import ExperimentRunner
from src.report_generator import ReportGenerator


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_prompt.py <experiment_name>")
        print("\nExample: python test_prompt.py exp_001_baseline")
        print("\nThis will run the experiment defined in:")
        print("  experiments/<experiment_name>/config.yaml")
        print("\nResults will be saved to:")
        print("  experiments/<experiment_name>/outputs/")
        print("  experiments/<experiment_name>/report.md")
        sys.exit(1)

    experiment_name = sys.argv[1]
    config_path = f"experiments/{experiment_name}/config.yaml"

    if not Path(config_path).exists():
        print(f"Error: Config file not found: {config_path}")
        print(f"\nAvailable experiments:")
        experiments_dir = Path("experiments")
        if experiments_dir.exists():
            for exp_dir in sorted(experiments_dir.iterdir()):
                if exp_dir.is_dir() and (exp_dir / "config.yaml").exists():
                    print(f"  - {exp_dir.name}")
        sys.exit(1)

    try:
        print(f"Loading experiment configuration from: {config_path}\n")
        runner = ExperimentRunner(config_path)
        results = runner.run()

        # Generate report
        report_gen = ReportGenerator(Path(f"experiments/{experiment_name}"))
        report_gen.save_report(results)

        print("\nExperiment completed successfully!")

    except Exception as e:
        print(f"\nError running experiment: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
