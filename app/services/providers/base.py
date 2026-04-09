"""
Abstract base class for translation provider adapters.

All provider implementations must inherit from BaseProvider and implement
the `translate` method.
"""

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """Interface every provider adapter must satisfy."""

    @abstractmethod
    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        model_id: str,
        endpoint: str | None = None,
    ) -> dict:
        """
        Translate *text* from *source_lang* to *target_lang* using *model_id*.

        Must return a dict with at least:
          - translated_text: str
          - confidence: float  (0-1)
        """
        raise NotImplementedError
