from ClassModels.ResultClasses.results_base import ResultsBase
from abc import ABC, abstractmethod


class ExtractModelResultsBase(ABC):

    @abstractmethod
    def extract_results(self, results) -> ResultsBase:
        """
        Abstract method to be implemented by subclasses for extracting results.

        :param results: The results to be processed.
        :return: An instance of ResultsBase containing the processed results.
        """
        pass
