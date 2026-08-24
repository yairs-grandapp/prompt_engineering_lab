"""
Prompt builder that loads templates and renders them with conversation history
and configuration variables.

Mirrors the Java ContextBase.buildPrompt() assembly logic.
"""
import json
from pathlib import Path
from typing import Optional, Dict, Any, List


class PromptBuilder:
    """Builds prompts from templates, mirroring Java ContextBase.buildPrompt()."""

    def __init__(self, prompts_dir: str = "data/prompts"):
        self.prompts_dir = Path(prompts_dir)

    def load_template(self, template_path: str) -> str:
        """Load a prompt template file."""
        full_path = self.prompts_dir / template_path
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()

    def build_additional_info_guidelines(
        self, additional_information: Optional[Dict[str, Any]]
    ) -> str:
        """
        Build the additional information guidelines section.
        Mirrors ContextBase.initializeGuidelines() additionalInformationGuidelines.
        """
        if not additional_information:
            return ""
        info_json = json.dumps(additional_information, ensure_ascii=False)
        return (
            "* The additional information is a JSON object that contains additional "
            "information that can be used to help the assistant generate a response. \n"
            " * The additional information might contain the reminderCount which is "
            "the number of times the assistant has reminded the user about the task. \n"
            " * Make sure to show empathy and understanding, while using the information "
            "in the additional information.\n"
            f" The additional information is as follows: {info_json}\n"
        )

    def build_prompt(
        self,
        template_path: str,
        conversation_history: List[str],
        language: Optional[str] = None,
        assistant_gender: Optional[str] = None,
        additional_information: Optional[Dict[str, Any]] = None,
        senior_name: Optional[str] = None,
        assistant_name: Optional[str] = None
    ) -> str:
        """
        Load template and render with conversation history and variables.

        The template contains the full prompt structure (task definition, JSON format,
        outcomes, guidelines, context guidelines). Only the placeholders present
        in the template are injected.
        """
        template = self.load_template(template_path)
        history_str = "\n".join(conversation_history)

        format_vars = {"conversation_history": history_str}

        if language is not None:
            format_vars["language"] = language
        if assistant_gender is not None:
            format_vars["assistant_gender"] = assistant_gender
        if senior_name is not None:
            format_vars["senior_name"] = senior_name
        if assistant_name is not None:
            format_vars["assistant_name"] = assistant_name
        if additional_information is not None or "{additional_information_guidelines}" in template:
            format_vars["additional_information_guidelines"] = (
                self.build_additional_info_guidelines(additional_information)
            )

        return template.format(**format_vars)
