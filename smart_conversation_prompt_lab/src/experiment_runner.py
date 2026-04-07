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
        Run all scenarios and collect results.

        Returns dict with config, results list, summary, and total cost.
        """
        print(f"\n{'#' * 70}")
        print(f"# Experiment: {self.config.name}")
        print(f"# Date: {self.config.date}")
        print(f"# Model: {self.config.model.name} (temp={self.config.model.temperature})")
        print(f"# Prompt: {self.config.prompt.template}")
        print(f"# Language: {self.config.prompt.language}")
        print(f"# Scenarios: {len(self.scenarios)}")
        print(f"{'#' * 70}\n")

        results: List[ConversationResult] = []

        for i, scenario in enumerate(self.scenarios, 1):
            print(f"[{i}/{len(self.scenarios)}] {scenario['id']}")
            result = self.conversation_runner.run_scenario(scenario)
            results.append(result)

            # Save individual transcript
            output_path = self.outputs_dir / f"{scenario['id']}.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)

        # Summary
        passed = sum(1 for r in results if r.passed)
        failed = len(results) - passed
        total_cost = sum(r.cost for r in results)

        print(f"\n{'=' * 70}")
        print(f"Experiment Complete")
        print(f"{'=' * 70}")
        print(f"Scenarios: {len(results)} total, {passed} passed, {failed} failed")
        print(f"Pass rate: {passed}/{len(results)} ({100 * passed / len(results):.0f}%)")
        print(f"Estimated cost: ${total_cost:.4f}")
        print(f"Results saved to: {self.outputs_dir}")
        print(f"{'=' * 70}\n")

        return {
            "config": {
                "name": self.config.name,
                "date": self.config.date,
                "model": self.config.model.name,
                "temperature": self.config.model.temperature,
                "prompt_template": self.config.prompt.template,
                "language": self.config.prompt.language,
                "assistant_gender": self.config.prompt.assistant_gender,
            },
            "results": [r.to_dict() for r in results],
            "summary": {
                "total": len(results),
                "passed": passed,
                "failed": failed,
                "pass_rate": f"{100 * passed / len(results):.0f}%"
            },
            "total_cost": total_cost
        }
