from kink import Container as BaseContainer
from typing import Any


class Container(BaseContainer):
    """
    Dependency injection container.
    Extends default with the ability to add factories.
    """

    def add_factory(self, key: str | type, value: Any) -> None:
        """
        Adds factory to dependency injection container.
        Args:
            key (str, type): type of factory
            value (Any): factory function/class
        """
        self._factories[key] = value

        if key in self._memoized_services:
            del self._memoized_services[key]


container: Container = Container()
