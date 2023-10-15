from src.di.module import Module
from src.core.infrastructure.database import SessionProvider

from src.stream.domain.ports import (
    StreamUnitCommandServiceInterface,
    StreamUnitQueryServiceInterface,
    StreamUnitUowInterface,
    StreamUnitListViewInterface,
    StreamUnitViewInterface,
)
from src.stream.infrastructure.unit_of_work import StreamUnitUow
from src.stream.application.services import (
    StreamUnitCommandService,
    StreamUnitQueryService,
)
from src.user_management.permissions.domain.ports import PermissionValidator
from src.stream.infrastructure.views import StreamUnitView, StreamUnitListView


class StreamModule(Module):
    @classmethod
    def bootstrap(cls) -> None:
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
