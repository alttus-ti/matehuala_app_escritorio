from collections.abc import Callable
from typing import Protocol

from PySide6.QtWidgets import QWidget

from core.ui_loader import load_ui


class RoutableController(Protocol):
    def show(self) -> None: ...

    def close(self) -> None: ...


class UiRoute:
    def __init__(self, ui_relative_path: str):
        self.window: QWidget = load_ui(ui_relative_path)

    def show(self) -> None:
        self.window.show()

    def close(self) -> None:
        self.window.close()


class RouteController:
    def __init__(self):
        self._routes: dict[str, Callable[[], RoutableController]] = {}
        self._controllers: dict[str, RoutableController] = {}
        self._current_route: str | None = None

    def register(self, route: str, controller_factory: Callable[[], RoutableController]) -> None:
        if route in self._routes:
            raise ValueError(f"La ruta '{route}' ya fue registrada.")

        self._routes[route] = controller_factory

    def register_ui(self, route: str, ui_relative_path: str) -> None:
        self.register(route, lambda: UiRoute(ui_relative_path))

    def go(self, route: str) -> None:
        if route not in self._routes:
            raise KeyError(f"La ruta '{route}' no existe.")

        if self._current_route is not None and self._current_route != route:
            self._controllers[self._current_route].close()

        controller = self._get_or_create_controller(route)
        controller.show()
        self._current_route = route

    def _get_or_create_controller(self, route: str) -> RoutableController:
        if route not in self._controllers:
            self._controllers[route] = self._routes[route]()

        return self._controllers[route]
