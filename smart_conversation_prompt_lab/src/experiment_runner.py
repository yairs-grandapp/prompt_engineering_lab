"""
Experiment runner that orchestrates running all scenarios in an experiment.
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Any
import openai
from dotenv import load_dotenv

from .config import ExperimentConfig
from .prompt_builder import PromptBuilder
from .conversation_runner import ConversationRunner, ConversationResult


class ExperimentRunner:
    """Runs all scenarios in an experiment configuration."""

    def __init__(self, config_path: str):
        self.config = ExperimentConfig.from_yaml(config_path)
        self.config_path = Path(config_path)
        self.experiment_dir = self.config_path.parent
        self.outputs_dir = self.experiment_dir / "outputs"
        self.outputs_dir.mkdir(exist_ok=True)

        # Load environment variables
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables. "
                             "Create a .env file with OPENAI_API_KEY=sk-...")

        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=api_key)

        # Initialize modules
        self.prompt_builder = PromptBuilder()
        self.conversation_runner = ConversationRunner(
            self.client, self.prompt_builder, self.config
        )

        # Load scenarios
        self.scenarios = self._load_scenarios()

    def _load_scenarios(self) -> List[Dict[str, Any]]:
        """Load test scenarios from the inputs JSON file."""
        inputs_path = Path("data/inputs") / self.config.inputs_file
        with open(inputs_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data["scenarios"]

    def run(self) -> Dict[str, Any]:
        """
        Run all scenarios with all models and collect results.

        Each scenario is run independently with each model.
        Results are grouped by scenario, with each scenario containing
        results from all models for side-by-side comparison.
        """
        model_names = [m.name for m in self.config.models]

        print(f"\n{'#' * 70}")
        print(f"# Experiment: {self.config.name}")
        print(f"# Date: {self.config.date}")
        print(f"# Models: {', '.join(model_names)}")
        print(f"# Prompt: {self.config.prompt.template}")
        print(f"# Scenarios: {len(self.scenarios)}")
        print(f"{'#' * 70}\n")

        # results_by_scenario[scenario_id][model_name] = ConversationResult
        all_results: List[Dict[str, Any]] = []

        for i, scenario in enumerate(self.scenarios, 1):
            print(f"[{i}/{len(self.scenarios)}] {scenario['id']}")

            scenario_results = {}
            for model in self.config.models:
                result = self.conversation_runner.run_scenario(scenario, model)
                scenario_results[model.name] = result

            # Save per-scenario output with all model results
            output_data = {
                "scenario_id": scenario["id"],
                "scenario_name": scenario["name"],
                "description": scenario.get("description", ""),
                "expected_outcome": scenario["expected_outcome"],
                "model_results": {
                    model_name: r.to_dict()
                    for model_name, r in scenario_results.items()
                }
            }
            output_path = self.outputs_dir / f"{scenario['id']}.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)

            all_results.append(output_data)

        # Build summary per model
        model_summaries = {}
        for model in self.config.models:
            model_results = [
                r["model_results"][model.name] for r in all_results
            ]
            passed = sum(1 for r in model_results if r["passed"])
            failed = len(model_results) - passed
            model_summaries[model.name] = {
                "total": len(model_results),
                "passed": passed,
                "failed": failed,
                "pass_rate": f"{100 * passed / len(model_results):.0f}%"
            }

        print(f"\n{'=' * 70}")
        print(f"Experiment Complete")
        print(f"{'=' * 70}")
        for model_name, summary in model_summaries.items():
            print(f"  [{model_name}] {summary['passed']}/{summary['total']} passed "
                  f"({summary['pass_rate']})")
        print(f"Results saved to: {self.outputs_dir}")
        print(f"{'=' * 70}\n")

        return {
            "config": {
                "name": self.config.name,
                "date": self.config.date,
                "models": model_names,
                "prompt_template": self.config.prompt.template,
            },
            "results": all_results,
            "model_summaries": model_summaries,
        }
