# -*- coding: utf-8 -*-
"""
Covenant Mobile v9.1 — core/event_bus.py

Tiny event bus with:
- topic-based pub/sub
- sync publish (default) + optional background worker
- simple middleware hooks (before/after)
- backpressure-safe queue when running the worker

Design goals: minimal deps, easy to test, no Django signals coupling.
"""

from __future__ import annotations
from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass, field
import threading
import queue
import time
import uuid
import logging

logger = logging.getLogger(__name__)

EventHandler = Callable[[Dict[str, Any]], None]
Middleware = Callable[[Dict[str, Any]], Dict[str, Any]]

@dataclass
class _Registry:
    subs: Dict[str, List[EventHandler]] = field(default_factory=dict)
    before_mw: List[Middleware] = field(default_factory=list)
    after_mw: List[Middleware] = field(default_factory=list)

class EventBus:
    """
    Usage:
        bus = EventBus()
        def on_ingest(evt): ...
        bus.subscribe("ingest.started", on_ingest)
        bus.publish("ingest.started", {"path": "/docs"})
    """

    def __init__(self) -> None:
        self._r = _Registry()
        self._lock = threading.RLock()
        self._q: "queue.Queue[Dict[str, Any]]" = queue.Queue(maxsize=1000)
        self._worker: Optional[threading.Thread] = None
        self._stop = threading.Event()

    # ---------- subscription ----------

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        with self._lock:
            self._r.subs.setdefault(topic, [])
            if handler not in self._r.subs[topic]:
                self._r.subs[topic].append(handler)
                logger.debug("Subscribed %s to %s", getattr(handler, "__name__", repr(handler)), topic)

    def unsubscribe(self, topic: str, handler: EventHandler) -> None:
        with self._lock:
            if topic in self._r.subs and handler in self._r.subs[topic]:
                self._r.subs[topic].remove(handler)
                logger.debug("Unsubscribed %s from %s", getattr(handler, "__name__", repr(handler)), topic)

    def clear(self) -> None:
        with self._lock:
            self._r.subs.clear()
            self._r.before_mw.clear()
            self._r.after_mw.clear()

    # ---------- middleware ----------

    def use_before(self, mw: Middleware) -> None:
        with self._lock:
            self._r.before_mw.append(mw)

    def use_after(self, mw: Middleware) -> None:
        with self._lock:
            self._r.after_mw.append(mw)

    # ---------- publish (sync) ----------

    def publish(self, topic: str, payload: Dict[str, Any] | None = None, meta: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Synchronous publish: calls handlers inline (good for tests / deterministic flows).
        Returns the final event dict after middleware.
        """
        evt = self._make_event(topic, payload, meta)
        evt = self._run_before(evt)
        for h in list(self._handlers_for(topic)):
            try:
                h(evt)
            except Exception as e:
                logger.exception("Handler error for %s: %s", topic, e)
        evt = self._run_after(evt)
        return evt

    # ---------- enqueue (async) ----------

    def enqueue(self, topic: str, payload: Dict[str, Any] | None = None, meta: Dict[str, Any] | None = None) -> None:
        """
        Enqueue event for background processing (requires start()).
        If queue is full, this blocks briefly and then drops with a warning (to avoid OOM).
        """
        evt = self._make_event(topic, payload, meta)
        try:
            self._q.put(evt, timeout=0.5)
        except queue.Full:
            logger.warning("Event queue full; dropping event: %s", topic)

    # ---------- worker lifecycle ----------

    def start(self) -> None:
        """
        Starts a single background worker thread that drains the queue and
        delivers events to subscribers. Idempotent.
        """
        with self._lock:
            if self._worker and self._worker.is_alive():
                return
            self._stop.clear()
            self._worker = threading.Thread(target=self._run, name="covenant-event-worker", daemon=True)
            self._worker.start()
            logger.info("EventBus worker started")

    def stop(self) -> None:
        with self._lock:
            self._stop.set()
        if self._worker:
            self._worker.join(timeout=2.0)
            logger.info("EventBus worker stopped")

    # ---------- internals ----------

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                evt = self._q.get(timeout=0.25)
            except queue.Empty:
                continue
            try:
                evt = self._run_before(evt)
                for h in list(self._handlers_for(evt["topic"])):
                    try:
                        h(evt)
                    except Exception as e:
                        logger.exception("Handler error for %s: %s", evt["topic"], e)
                evt = self._run_after(evt)
            finally:
                self._q.task_done()

    def _handlers_for(self, topic: str) -> List[EventHandler]:
        with self._lock:
            # exact topic and wildcard prefix (e.g., "ingest.*")
            handlers = list(self._r.subs.get(topic, []))
            prefix = topic.split(".")[0] + ".*"
            handlers += self._r.subs.get(prefix, [])
            return handlers

    def _make_event(self, topic: str, payload: Optional[Dict[str, Any]], meta: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "id": str(uuid.uuid4()),
            "ts": time.time(),
            "topic": topic,
            "payload": payload or {},
            "meta": meta or {},
        }

    def _run_before(self, evt: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            for mw in self._r.before_mw:
                try:
                    evt = mw(evt)
                except Exception as e:
                    logger.exception("before middleware error: %s", e)
        return evt

    def _run_after(self, evt: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            for mw in self._r.after_mw:
                try:
                    evt = mw(evt)
                except Exception as e:
                    logger.exception("after middleware error: %s", e)
        return evt


# Singleton bus for the app. Import as: from core.event_bus import bus
bus = EventBus()

# Example middleware (safe no-op; uncomment to use)
# def tag_source(evt):
#     evt["meta"]["source"] = evt["meta"].get("source","ui")
#     return evt
# bus.use_before(tag_source)

