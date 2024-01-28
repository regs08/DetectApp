from ClassModels.ResultClasses.results_base import ResultsBase
from abc import ABC


class PayloadFilter(ABC):
    """
    Abstract base class for payload filtering.

    This class serves as a foundation for all payload filter implementations. It provides
    a structure to ensure that the filter is applied to an appropriate type of results.
    Subclasses should implement specific filtering logic as per their requirements.
    """

    def __init__(self, results: ResultsBase):
        """
        Initialize the payload filter with results.

        This constructor ensures that the provided results are an instance of ResultsBase.
        If the results are not of the expected type, a TypeError is raised. This type check
        ensures that subclasses of PayloadFilter work with the correct type of results.

        Parameters:
        - results (ResultsBase): The results to be filtered. Must be an instance of ResultsBase.

        Raises:
        - TypeError: If 'results' is not an instance of ResultsBase.
        """
        if not isinstance(results, ResultsBase):
            raise TypeError("Results not of results base!")
        self.results = results
