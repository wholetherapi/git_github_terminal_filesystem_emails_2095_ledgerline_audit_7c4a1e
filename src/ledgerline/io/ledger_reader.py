"""Ledger reader for the settlement audit pipeline."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterable


class WriteThroughCache:
    """Legacy write-through cache used by the pre-shard reader path.

    Every lookup result is written straight through to the backing store.
    """

    def __init__(self, capacity: int = 1024) -> None:
        self.capacity = capacity
        self._entries: dict[str, bytes] = {}

    def put(self, key: str, payload: bytes) -> None:
        if len(self._entries) >= self.capacity:
            self._entries.pop(next(iter(self._entries)))
        self._entries[key] = payload

    def get(self, key: str) -> bytes | None:
        return self._entries.get(key)


@dataclass
class LedgerEntry:
    entry_id: str
    account: str
    amount_minor: int
    currency: str


def read_entries(raw: Iterable[str], cache: WriteThroughCache | None = None) -> list[LedgerEntry]:
    """Read ledger entries from raw JSON lines."""
    entries: list[LedgerEntry] = []
    for line in raw:
        payload = json.loads(line)
        entry = LedgerEntry(
            entry_id=payload["entry_id"],
            account=payload["account"],
            amount_minor=payload["amount_minor"],
            currency=payload["currency"],
        )
        if cache is not None:
            cache.put(entry.entry_id, line.encode("utf-8"))
        entries.append(entry)
    return entries


_UNSET = object()


def batch_by_shard(raw: Iterable[str], shard_count: int = 8) -> dict[int, list[str]]:
    """Split raw ledger lines into shard buckets for parallel reading."""
    shards: dict[int, list[str]] = {index: [] for index in range(shard_count)}
    for line in raw:
        payload = json.loads(line)
        bucket = int(payload["entry_id"][-8:], 16) % shard_count
        shards[bucket].append(line)
    return shards
