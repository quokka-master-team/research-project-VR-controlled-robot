from src.di.module import Module
from src.core.infrastructure.database import SessionProvider

from src.stream.domain.ports import (
    StreamUnitCommandServiceInterface,
    StreamUnitQueryServiceInterface,
    StreamUnitUowInterface,
    StreamUnitListViewInterface,
    StreamUnitViewInterface,
    StreamingServiceInterface,
)
from src.stream.infrastructure.unit_of_work import StreamUnitUow
from src.stream.application.commands import (
    StreamUnitCommandService,
)
from src.stream.application.queries import StreamUnitQueryService
from src.stream.application.streaming import StreamingService
from src.stream.application.utils import (
    ConnectionManager,
    InMemoryConnectionManager,
)
from src.user_management.permissions.domain.ports import PermissionValidator
from src.stream.infrastructure.views import StreamUnitView, StreamUnitListView
from src.auth.ports import IAMTokenVerificationService


class StreamModule(Module):
    @classmethod
    def bootstrap(cls) -> None:
        cls.container[ConnectionManager] = InMemoryConnectionManager()

        # uow
        cls.container[StreamUnitUowInterface] = StreamUnitUow(
            cls.container[SessionProvider]
        )

        # views
        cls.container[StreamUnitViewInterface] = StreamUnitView(
            cls.container[SessionProvider]
        )
        cls.container[StreamUnitListViewInterface] = StreamUnitListView(
            cls.container[SessionProvider]
        )

        # services
        cls.container[
            StreamUnitCommandServiceInterface
        ] = StreamUnitCommandService(
            cls.container[StreamUnitUowInterface],  # type: ignore
            cls.container[PermissionValidator],  # type: ignore
        )
        cls.container[
            StreamUnitQueryServiceInterface
        ] = StreamUnitQueryService(
            cls.container[StreamUnitViewInterface],  # type: ignore
            cls.container[StreamUnitListViewInterface],  # type: ignore
            cls.container[PermissionValidator],  # type: ignore
        )
        cls.container[StreamingServiceInterface] = StreamingService(
            cls.container[StreamUnitUowInterface],  # type: ignore
            cls.container[ConnectionManager],  # type: ignore
            cls.container[PermissionValidator],  # type: ignore
            cls.container[IAMTokenVerificationService],  # type: ignore
        )
