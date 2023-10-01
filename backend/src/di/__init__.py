from src.core.di import CoreModule
from src.auth.di import AuthModule
from src.user_management.di import UserModule

all_modules = [CoreModule, UserModule, AuthModule]


__all__ = ["all_modules"]
