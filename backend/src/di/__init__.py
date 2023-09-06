from src.core.di import CoreModule
from src.di.container import Container, container
from src.auth.di import AuthModule
from src.user.di import UserModule

all_modules = [CoreModule, UserModule, AuthModule]


__all__ = ["all_modules", "Container", "container"]
