"""Strict JSON and hashing primitives: duplicate keys and NaN are refusals, not data."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, NoReturn

from .errors import ContractError


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value = {}
    for key, item in pairs:
        if key in value:
            raise ContractError("duplicate JSON object key")
        value[key] = item
    return value


def reject_constant(_value: str) -> NoReturn:
    raise ContractError("non-finite JSON value")


def parse_json(text: str) -> Any:
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def records(path: Path) -> list[Any]:
    result = []
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = parse_json(line)
        except ValueError as exc:
            raise ContractError(f"{path.name}:{number}: invalid JSON") from exc
        if not isinstance(value, dict):
            raise ContractError(f"{path.name}:{number}: expected object")
        result.append(value)
    return result
