from abc import abstractmethod
from src.di.container import Container, container


class Module:
    """Contains dependency injection configuration for the container."""

    container: Container = container

    @abstractmethod
    def bootstrap(self) -> None:
        """
        Initiates injections.
        """
        pass
