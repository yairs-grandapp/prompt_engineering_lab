"""
Configuration loader for experiments.
"""
import yaml
from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path
from datetime import datetime


@dataclass
class BehaviorConfig:
    """Configuration for a single behavior to test."""
    category: str
    stat_id: str


@dataclass
class ModelConfig:
    """Configuration for the LLM model."""
    name: str
    temperature: float = 0.7


@dataclass
class PromptConfig:
    """Configuration for prompt templates."""
    daily_template: str
    weekly_template: str


@dataclass
class TestDataConfig:
    """Configuration for test data selection."""
    senior_id: str
    behaviors: List[BehaviorConfig]
    start_date: datetime
    end_date: datetime


@dataclass
class ExperimentConfig:
    """Main experiment configuration."""
    name: str
    date: str
    model: ModelConfig
    prompts: PromptConfig
    test_data: TestDataConfig

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'ExperimentConfig':
        """Load configuration from YAML file."""
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)

        # Parse experiment info
        exp_info = data['experiment']

        # Parse model config
        model_data = data['model']
        model = ModelConfig(
            name=model_data['name'],
            temperature=model_data.get('temperature', 0.7)
        )

        # Parse prompt config
        prompt_data = data['prompts']
        prompts = PromptConfig(
            daily_template=prompt_data['daily_template'],
            weekly_template=prompt_data['weekly_template']
        )

        # Parse test data config
        test_data_raw = data['test_data']
        behaviors = [
            BehaviorConfig(category=b['category'], stat_id=b['stat_id'])
            for b in test_data_raw['behaviors']
        ]

        date_range = test_data_raw['date_range']
        test_data = TestDataConfig(
            senior_id=test_data_raw['senior_id'],
            behaviors=behaviors,
            start_date=datetime.strptime(date_range['start'], '%Y-%m-%d'),
            end_date=datetime.strptime(date_range['end'], '%Y-%m-%d')
        )

        # Auto-generate date if not provided
        date = exp_info.get('date', datetime.now().strftime('%Y-%m-%d'))

        return cls(
            name=exp_info['name'],
            date=date,
            model=model,
            prompts=prompts,
            test_data=test_data
        )
