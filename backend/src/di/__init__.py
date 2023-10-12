from src.core.di import CoreModule
from src.auth.di import AuthModule
from src.user_management.di import UserModule
from src.stream.di import StreamModule

all_modules = [CoreModule, UserModule, StreamModule, AuthModule]


__all__ = ["all_modules"]
