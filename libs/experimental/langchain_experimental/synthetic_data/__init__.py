from typing import TYPE_CHECKING, Any, Dict, List, Optional

from langchain.chains.llm import LLMChain

from langchain_experimental.synthetic_data.prompts import SENTENCE_PROMPT

if TYPE_CHECKING:
    from langchain.chains.base import Chain
    from langchain.prompts import PromptTemplate
    from langchain.schema.language_model import BaseLanguageModel


def create_data_generation_chain(
    llm: BaseLanguageModel,
    prompt: Optional[PromptTemplate] = None,
) -> Chain:
    """Creates a chain that generates synthetic sentences with
     provided fields.

    Args:
        llm: The language model to use.
        prompt: Prompt to feed the language model with.
        If not provided, the default one will be used.
    """
    prompt = prompt or SENTENCE_PROMPT
    return LLMChain(
        llm=llm,
        prompt=prompt,
    )


class DatasetGenerator:
    """Generates synthetic dataset with a given language model."""

    def __init__(
        self,
        llm: BaseLanguageModel,
        sentence_preferences: Optional[Dict[str, Any]] = None,
    ):
        self.generator = create_data_generation_chain(llm)
        self.sentence_preferences = sentence_preferences or {}

    def __call__(self, fields_collection: List[List[Any]]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for fields in fields_collection:
            results.append(
                self.generator(
                    {"fields": fields, "preferences": self.sentence_preferences}
                )
            )
        return results
