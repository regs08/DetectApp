from abc import ABC, abstractmethod
from ClassModels.ResultClasses.results_base import ResultsBase
from ClassModels.payload import Payload
from typing import Optional


class PayloadProcessorBase(ABC):
    """
    Abstract base class for payload processing.

    This class serves as a template for all payload processor implementations.
    It defines a common interface for extracting log payloads from various types
    of results. Subclasses are required to implement the abstract methods defined here.

    TODO: Consider integrating a separate method for extracting photo payloads,
    or alternatively, handle it as an optional argument in the existing method.
    """

    def __init__(self):
        """
        Constructor for PayloadProcessorBase.

        Currently, this constructor doesn't perform any specific initialization.
        This can be extended in subclasses as needed.
        """
        pass

    @abstractmethod
    def extract_log_payload(self, results: ResultsBase) -> Optional[Payload]:
        """
        Abstract method to extract a log payload from the results.

        This method needs to be implemented by all subclasses, providing a specific
        mechanism for extracting a payload from given results.

        Parameters:
        - results (ResultsBase): An instance of ResultsBase or its subclass, representing
                                 the results from which the payload is to be extracted.

        Returns:
        - Optional[Payload]: The extracted payload object or None if no payload
                             could be extracted.
        """
        pass
