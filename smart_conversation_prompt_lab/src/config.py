"""
Configuration loader for smart conversation prompt experiments.
"""
import yaml
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime


@dataclass
class ModelConfig:
    """Configuration for a single LLM model."""
    name: str
    temperature: float = 0.7


@dataclass
class PromptConfig:
    """Configuration for the prompt template and its variables."""
    template: str
    language: Optional[str] = None
    assistant_gender: Optional[str] = None
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
    models: List[ModelConfig]
    prompt: PromptConfig
    conversation: ConversationConfig
    inputs_file: str

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'ExperimentConfig':
        """Load configuration from YAML file."""
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        exp_info = data['experiment']

        # Support both 'models' (list) and 'model' (single) in config
        models = []
        if 'models' in data:
            for m in data['models']:
                models.append(ModelConfig(
                    name=m['name'],
                    temperature=m.get('temperature', 0.7)
                ))
        elif 'model' in data:
            m = data['model']
            models.append(ModelConfig(
                name=m['name'],
                temperature=m.get('temperature', 0.7)
            ))

        prompt_data = data['prompt']
        prompt = PromptConfig(
            template=prompt_data['template'],
            language=prompt_data.get('language', None),
            assistant_gender=prompt_data.get('assistant_gender', None),
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
            models=models,
            prompt=prompt,
            conversation=conversation,
            inputs_file=data['inputs_file']
        )
