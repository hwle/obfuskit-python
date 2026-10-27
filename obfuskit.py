#!/usr/bin/env python3
"""Conservative token-aware identifier renamer for Python source."""
from __future__ import annotations
import argparse
import builtins
import io
import json
import keyword
import tokenize
from pathlib import Path

def obfuscate(source: str, keep: set[str] | None = None) -> tuple[str, dict[str, str]]:
    keep = keep or set()
    protected = set(dir(builtins)) | set(keyword.kwlist) | keep
    tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    names: dict[str, str] = {}
    counter = 0
    out = []
    for tok in tokens:
        if tok.type == tokenize.NAME and tok.string not in protected:
            original = tok.string
            if original not in names:
                names[original] = f"_v{counter:03d}"
                counter += 1
            tok = tok._replace(string=names[original])
        out.append(tok)
    transformed = tokenize.untokenize(out)
    reverse_map = {obfuscated: original for original, obfuscated in names.items()}
    return transformed, reverse_map

def main() -> int:
    parser = argparse.ArgumentParser(description="Conservatively rename Python identifiers.")
    parser.add_argument("source", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--map", dest="map_path", type=Path, required=True)
    parser.add_argument("--keep", action="append", default=[], help="Identifier to preserve; repeat as needed.")
    args = parser.parse_args()
    source = args.source.read_text(encoding="utf-8")
    result, mapping = obfuscate(source, set(args.keep))
    compile(result, str(args.output), "exec")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.map_path.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result, encoding="utf-8")
    args.map_path.write_text(json.dumps(mapping, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote transformed source: {args.output}")
    print(f"Wrote reversible mapping: {args.map_path}")
    print(f"Renamed {len(mapping)} distinct identifiers.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
