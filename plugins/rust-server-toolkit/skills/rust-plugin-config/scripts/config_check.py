#!/usr/bin/env python3
"""Read-only strict JSON validation and value-free structural comparison."""

import argparse
import json
from decimal import Decimal
from pathlib import Path


class InvalidConfig(ValueError):
    pass


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InvalidConfig("Duplicate object key (name omitted)")
        result[key] = value
    return result


def reject_constant(_value):
    raise InvalidConfig("Non-finite number is not valid JSON")


def load_config(path):
    try:
        value = json.loads(
            Path(path).read_text(encoding="utf-8-sig"),
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
            parse_float=Decimal,
        )
        pending = [(value, 0)]
        while pending:
            node, depth = pending.pop()
            if depth > 128:
                raise InvalidConfig("JSON nesting exceeds 128 levels")
            if isinstance(node, dict):
                pending.extend((child, depth + 1) for child in node.values())
            elif isinstance(node, list):
                pending.extend((child, depth + 1) for child in node)
        return value
    except json.JSONDecodeError as error:
        raise InvalidConfig(
            f"Invalid JSON at line {error.lineno}, column {error.colno}"
        ) from None
    except (OSError, UnicodeError):
        raise InvalidConfig("Cannot read input as UTF-8 JSON") from None
    except RecursionError:
        raise InvalidConfig("JSON nesting exceeds supported depth") from None
    except ValueError as error:
        if isinstance(error, InvalidConfig):
            raise
        raise InvalidConfig("Unsupported JSON number") from None


def pointer_token(key):
    return key.replace("~", "~0").replace("/", "~1")


def differences(before, after, path=""):
    if type(before) is not type(after):
        return [{"kind": "type_changed", "path": path}]
    if isinstance(before, dict):
        result = []
        for key in sorted(before.keys() | after.keys()):
            child = path + "/" + pointer_token(key)
            if key not in before:
                result.append({"kind": "added", "path": child})
            elif key not in after:
                result.append({"kind": "removed", "path": child})
            else:
                result.extend(differences(before[key], after[key], child))
        return result
    if isinstance(before, list):
        # Python considers True == 1, including inside nested lists. Use the
        # same type-sensitive comparison recursively before collapsing arrays.
        changed = len(before) != len(after) or any(
            differences(left, right) for left, right in zip(before, after)
        )
    else:
        changed = before != after
    return [{"kind": "changed", "path": path}] if changed else []


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check")
    check.add_argument("input")
    diff = commands.add_parser("diff")
    diff.add_argument("before")
    diff.add_argument("after")
    args = parser.parse_args(argv)
    try:
        if args.command == "check":
            value = load_config(args.input)
            result = {"valid": True, "root_type": type(value).__name__}
        else:
            changes = differences(load_config(args.before), load_config(args.after))
            result = {"valid": True, "changes": changes, "count": len(changes)}
    except (InvalidConfig, RecursionError) as error:
        message = str(error) if isinstance(error, InvalidConfig) else "Comparison nesting exceeds supported depth"
        print(json.dumps({"valid": False, "error": message}))
        return 2
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
