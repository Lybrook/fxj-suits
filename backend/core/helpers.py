import re
from typing import Any


def camel_to_snake(value: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()


def snake_to_camel(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(part.title() for part in parts[1:])


def payload_id(payload: dict[str, Any]) -> str | None:
    raw = payload.get("id") or payload.get("uuid")
    return str(raw) if raw is not None else None


def get_value(payload: dict[str, Any], key: str, default: Any = None) -> Any:
    if key in payload:
        return payload[key]
    snake = camel_to_snake(key)
    if snake in payload:
        return payload[snake]
    camel = snake_to_camel(key)
    if camel in payload:
        return payload[camel]
    return default


def normalize_payload(payload: dict[str, Any], record_id: str | None = None) -> dict[str, Any]:
    normalized = dict(payload)
    if record_id:
        normalized["id"] = record_id
    elif payload_id(normalized):
        normalized["id"] = payload_id(normalized)
    return normalized
