"""A small, deterministic YAML-frontmatter subset (stdlib only).

Supported, and nothing else:

* ``key: value`` scalars on one line (empty value -> ``""``),
* inline lists ``key: [a, b, "c, d"]``,
* double-quoted strings with ``\\"`` and ``\\\\`` escapes, single-quoted strings,
* ``# comment`` lines and trailing `` # comment`` after an unquoted value.

Values stay strings (``true``/``false``/dates are not converted), so a parse -> dump round trip is
lossless and a second dump produces no diff. That is the property the generated indexes rely on.
"""

from __future__ import annotations

import re
from typing import Union

# typing.Union on purpose: the hooks run this module with any Python >= 3.9 (the stock macOS
# python3), where ``str | list[str]`` fails at runtime.
Value = Union[str, list[str]]  # noqa: UP007
Meta = dict[str, Value]

_FENCE = "---"
_NEEDS_QUOTES = re.compile(r"""^[\s\[\]{}"'&*!|>%@`#,-]|:\s|\s#|\s$|^$|^[?:]""")


class FrontmatterError(ValueError):
    """Raised when a frontmatter block cannot be parsed."""


_OPEN = re.compile(r"---[ \t]*\n")
_CLOSE = re.compile(r"\n---[ \t]*(?:\n|$)")


def split(text: str) -> tuple[str | None, str]:
    """Split ``text`` into (raw frontmatter without fences, body). ``None`` if there is none.

    A leading UTF-8 BOM and trailing blanks after a fence are tolerated.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    opening = _OPEN.match(text)
    if not opening:
        return None, text
    closing = _CLOSE.search(text, opening.end() - 1)
    if not closing:
        return None, text
    return text[opening.end() : closing.start()], text[closing.end() :]


def _unquote(raw: str) -> str:
    if len(raw) >= 2 and raw[0] == raw[-1] == '"':
        out, i = [], 1
        while i < len(raw) - 1:
            ch = raw[i]
            if ch == "\\" and i + 1 < len(raw) - 1:
                out.append(raw[i + 1])
                i += 2
                continue
            out.append(ch)
            i += 1
        return "".join(out)
    if len(raw) >= 2 and raw[0] == raw[-1] == "'":
        return raw[1:-1].replace("''", "'")
    return raw


def _strip_comment(raw: str) -> str:
    """Drop a trailing `` # comment`` outside quotes."""
    quote, esc = "", False
    for i, ch in enumerate(raw):
        if esc:
            esc = False
        elif quote:
            if ch == "\\" and quote == '"':
                esc = True
            elif ch == quote:
                quote = ""
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or raw[i - 1].isspace()):
            return raw[:i].strip()
    return raw.strip()


def _split_list(inner: str) -> list[str]:
    items, buf, quote, esc = [], [], "", False
    for ch in inner:
        if esc:
            buf.append(ch)
            esc = False
            continue
        if quote:
            buf.append(ch)
            if ch == "\\" and quote == '"':
                esc = True
            elif ch == quote:
                quote = ""
            continue
        if ch in "\"'":
            quote = ch
            buf.append(ch)
        elif ch == ",":
            items.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    tail = "".join(buf).strip()
    if tail or items:
        items.append(tail)
    return [_unquote(i) for i in items if i != ""]


def parse_meta(raw: str) -> Meta:
    """Parse the inside of a frontmatter block."""
    meta: Meta = {}
    for n, line in enumerate(raw.split("\n"), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line[0].isspace() or ":" not in line:
            raise FrontmatterError(f"line {n}: only flat key: value lines allowed: {line!r}")
        key, _, rest = line.partition(":")
        key = key.strip()
        if key in meta:
            raise FrontmatterError(f"line {n}: duplicate key {key!r}")
        value = _strip_comment(rest)
        if value.startswith("[") and value.endswith("]"):
            meta[key] = _split_list(value[1:-1])
        else:
            meta[key] = _unquote(value)
    return meta


def parse(text: str) -> tuple[Meta | None, str]:
    """Return (metadata, body). Metadata is ``None`` when the text has no frontmatter."""
    raw, body = split(text)
    if raw is None:
        return None, body
    return parse_meta(raw), body


def _single_line(value: str) -> str:
    if "\n" in value or "\r" in value:
        raise FrontmatterError(f"line breaks are not allowed in frontmatter values: {value!r}")
    return value


def _scalar(value: str) -> str:
    _single_line(value)
    if value == "":
        return ""
    if _NEEDS_QUOTES.search(value) or value == "[]":
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return value


def _item(value: str) -> str:
    _single_line(value)
    if value == "" or re.search(r"""[,\[\]"'#]|^\s|\s$""", value):
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return value


def dump_meta(meta: Meta, order: list[str] | None = None) -> str:
    """Serialize ``meta`` deterministically. Keys in ``order`` first, then the rest sorted."""
    keys = [k for k in (order or []) if k in meta]
    keys += sorted(k for k in meta if k not in keys)
    lines = []
    for key in keys:
        value = meta[key]
        if isinstance(value, list):
            lines.append(f"{key}: [" + ", ".join(_item(v) for v in value) + "]")
        else:
            rendered = _scalar(value)
            lines.append(f"{key}: {rendered}" if rendered else f"{key}:")
    return "\n".join(lines)


def dump(meta: Meta, body: str, order: list[str] | None = None) -> str:
    """Render a full document: fenced frontmatter plus body."""
    return f"{_FENCE}\n{dump_meta(meta, order)}\n{_FENCE}\n{body}"


def set_scalar(text: str, key: str, value: str) -> str:
    """Set one scalar key inside an existing frontmatter block, leaving every other line as is.

    Used for the few permitted in-place edits (for example ``konsolidiert: true`` on a journal), so
    hand-written formatting and comments in the block survive.
    """
    raw, body = split(text)
    if raw is None:
        raise FrontmatterError("document has no frontmatter")
    lines = raw.split("\n")
    rendered = _scalar(value)
    new = f"{key}: {rendered}" if rendered else f"{key}:"
    for i, line in enumerate(lines):
        if line.partition(":")[0].strip() == key and not line[:1].isspace():
            lines[i] = new
            break
    else:
        lines.append(new)
    return f"{_FENCE}\n" + "\n".join(lines) + f"\n{_FENCE}\n{body}"
