from abc import abstractmethod
from kink import Container, di


class Module:
    """Contains dependency injection configuration for the container."""

    container: Container = di

    @classmethod
    @abstractmethod
    def bootstrap(cls) -> None:
        """
        Initiates injections.
        """
        pass
