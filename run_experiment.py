#!/usr/bin/env python3
"""
Main script to run experiments.

Usage:
    python run_experiment.py exp_001_baseline
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.experiment_runner import ExperimentRunner
from src.report_generator import ReportGenerator


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_experiment.py <experiment_name>")
        print("\nExample: python run_experiment.py exp_001_baseline")
        sys.exit(1)

    experiment_name = sys.argv[1]
    config_path = f"experiments/{experiment_name}/config.yaml"

    if not Path(config_path).exists():
        print(f"Error: Config file not found: {config_path}")
        sys.exit(1)

    try:
        # Run experiment
        print(f"Loading experiment configuration from: {config_path}\n")
        runner = ExperimentRunner(config_path)
        results = runner.run()

        # Generate report
        report_gen = ReportGenerator(Path(f"experiments/{experiment_name}"))
        report_gen.save_report(results)

        print("\n✓ Experiment completed successfully!")

    except Exception as e:
        print(f"\n✗ Error running experiment: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
