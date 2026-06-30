"""
Module: plugins.registry

Purpose:
In-memory registry of loaded plugins.

Responsibilities:
- Maintain a thread-safe registry of active plugin instances.
- Allow retrieval of plugins by name.

Dependencies:
- backend.plugins.base
- backend.plugins.exceptions

Owner:
SentinelVision
"""

import threading

from backend.plugins.base import BasePlugin
from backend.plugins.exceptions import PluginError


class PluginRegistry:
    """Thread-safe registry for loaded plugins."""

    def __init__(self) -> None:
        self._plugins: dict[str, BasePlugin] = {}
        self._lock = threading.RLock()

    def register(self, plugin: BasePlugin) -> None:
        """Register a plugin instance.
        
        Raises:
            PluginError: If a plugin with the same name is already registered.
        """
        name = plugin.manifest.name
        with self._lock:
            if name in self._plugins:
                raise PluginError(f"Plugin '{name}' is already registered.")
            self._plugins[name] = plugin

    def unregister(self, plugin_name: str) -> None:
        """Remove a plugin from the registry."""
        with self._lock:
            if plugin_name in self._plugins:
                del self._plugins[plugin_name]

    def get(self, plugin_name: str) -> BasePlugin | None:
        """Retrieve a plugin by name."""
        with self._lock:
            return self._plugins.get(plugin_name)

    def get_all(self) -> list[BasePlugin]:
        """Retrieve all registered plugins."""
        with self._lock:
            return list(self._plugins.values())

    def clear(self) -> None:
        """Clear all registered plugins."""
        with self._lock:
            self._plugins.clear()

# Global registry instance
registry = PluginRegistry()
