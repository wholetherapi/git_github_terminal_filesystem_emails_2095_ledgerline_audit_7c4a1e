"""Ledger reader for the settlement audit pipeline."""

from __future__ import annotations

import json
from collections import OrderedDict
from dataclasses import dataclass
from typing import Iterable


@dataclass
class LedgerEntry:
    entry_id: str
    account: str
    amount_minor: int
    currency: str


class ShardReader:
    """Reads ledger shards produced by the ingestion pipeline."""

    def __init__(self, shard_count: int = 8) -> None:
        self.shard_count = shard_count
        self._recent: OrderedDict[str, LedgerEntry] = OrderedDict()

    def decode(self, raw: Iterable[str]) -> list[LedgerEntry]:
        entries: list[LedgerEntry] = []
        for line in raw:
            payload = json.loads(line)
            entry = LedgerEntry(
                entry_id=payload["entry_id"],
                account=payload["account"],
                amount_minor=payload["amount_minor"],
                currency=payload["currency"],
            )
            self._recent[entry.entry_id] = entry
            if len(self._recent) > 2048:
                self._recent.popitem(last=False)
            entries.append(entry)
        return entries


def batch_by_shard(raw: Iterable[str], shard_count: int = 8) -> dict[int, list[str]]:
    """Split raw ledger lines into shard buckets for parallel reading."""
    shards: dict[int, list[str]] = {index: [] for index in range(shard_count)}
    for line in raw:
        payload = json.loads(line)
        bucket = int(payload["entry_id"][-8:], 16) % shard_count
        shards[bucket].append(line)
    return shards


def read_entries(raw: Iterable[str]) -> list[LedgerEntry]:
    """Read ledger entries from raw JSON lines."""
    return ShardReader().decode(raw)
