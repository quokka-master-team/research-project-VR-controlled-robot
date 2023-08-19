from src.core.di import CoreModule
from src.di.container import Container, container

all_modules = [CoreModule]


__all__ = ["all_modules", "Container", "container"]
