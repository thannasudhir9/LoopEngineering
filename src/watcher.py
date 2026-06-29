"""
Filesystem watcher — watches registered project folders for changes.
Emits events to state store so dashboard reflects live activity.
"""
import asyncio
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from . import state


class _Handler(FileSystemEventHandler):
    def __init__(self, project_id: str, loop: asyncio.AbstractEventLoop):
        self._project_id = project_id
        self._loop = loop

    def _emit(self, event_type: str, path: str):
        asyncio.run_coroutine_threadsafe(
            state._broadcast({
                "type": "fs_event",
                "project_id": self._project_id,
                "event_type": event_type,
                "path": path,
            }),
            self._loop,
        )

    def on_modified(self, event: FileSystemEvent):
        if not event.is_directory:
            self._emit("modified", event.src_path)

    def on_created(self, event: FileSystemEvent):
        self._emit("created", event.src_path)

    def on_deleted(self, event: FileSystemEvent):
        self._emit("deleted", event.src_path)


_observer: Observer | None = None
_watched: dict[str, _Handler] = {}


def start_watcher(event_loop: asyncio.AbstractEventLoop):
    global _observer
    _observer = Observer()
    _observer.start()


def watch_project(project_id: str, folder: str, event_loop: asyncio.AbstractEventLoop):
    global _observer
    if not _observer:
        start_watcher(event_loop)
    if project_id in _watched:
        return
    handler = _Handler(project_id, event_loop)
    _watched[project_id] = handler
    _observer.schedule(handler, str(Path(folder).resolve()), recursive=True)


def stop_watcher():
    global _observer
    if _observer:
        _observer.stop()
        _observer.join()
        _observer = None
