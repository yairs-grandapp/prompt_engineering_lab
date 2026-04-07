"""
Configuration loader for smart conversation prompt experiments.
"""
import yaml
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from pathlib import Path
from datetime import datetime


@dataclass
class ModelConfig:
    """Configuration for the LLM model."""
    name: str
    temperature: float = 0.7


@dataclass
class PromptConfig:
    """Configuration for the prompt template and its variables."""
    template: str
    language: str = "Hebrew"
    assistant_gender: str = "female"
    additional_information: Optional[Dict[str, Any]] = None


@dataclass
class ConversationConfig:
    """Configuration for conversation behavior."""
    max_turns: int = 10
    extra_silence_turns: int = 2


@dataclass
class ExperimentConfig:
    """Main experiment configuration."""
    name: str
    date: str
    model: ModelConfig
    prompt: PromptConfig
    conversation: ConversationConfig
    inputs_file: str

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'ExperimentConfig':
        """Load configuration from YAML file."""
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        exp_info = data['experiment']

        model_data = data['model']
        model = ModelConfig(
            name=model_data['name'],
            temperature=model_data.get('temperature', 0.7)
        )

        prompt_data = data['prompt']
        prompt = PromptConfig(
            template=prompt_data['template'],
            language=prompt_data.get('language', 'Hebrew'),
            assistant_gender=prompt_data.get('assistant_gender', 'female'),
            additional_information=prompt_data.get('additional_information', None)
        )

        conv_data = data.get('conversation', {})
        conversation = ConversationConfig(
            max_turns=conv_data.get('max_turns', 10),
            extra_silence_turns=conv_data.get('extra_silence_turns', 2)
        )

        date = exp_info.get('date', datetime.now().strftime('%Y-%m-%d'))

        return cls(
            name=exp_info['name'],
            date=date,
            model=model,
            prompt=prompt,
            conversation=conversation,
            inputs_file=data['inputs_file']
        )
