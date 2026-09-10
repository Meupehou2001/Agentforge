"""Agent: bereinigt einen DataFrame gemäß der Standard-Cleaning-Pipeline."""

from __future__ import annotations

from ..data.cleaning import clean_dataset
from .base import AgentContext, BaseAgent


class DataCleaningAgent(BaseAgent):
    """Nimmt ``context.data['raw_dataframe']`` entgegen und bereinigt ihn."""

    name = "data-cleaning-agent"

    def __init__(self, dedupe_subset: list[str] | None = None, fill_strategy: str = "mean") -> None:
        self.dedupe_subset = dedupe_subset
        self.fill_strategy = fill_strategy

    def run(self, context: AgentContext) -> AgentContext:
        df = context.data.get("raw_dataframe")
        if df is None:
            raise ValueError(
                "Kein 'raw_dataframe' im Context gefunden. "
                "Bitte vor diesem Agent einen DataFrame in context.data['raw_dataframe'] ablegen."
            )
        cleaned = clean_dataset(df, dedupe_subset=self.dedupe_subset, fill_strategy=self.fill_strategy)
        context.data["cleaned_dataframe"] = cleaned
        context.data["rows_before"] = len(df)
        context.data["rows_after"] = len(cleaned)
        return context
