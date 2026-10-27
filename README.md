# ObfusKit Python

A small, educational Python source transformer for **your own code**. It renames selected local identifiers and writes a JSON mapping so the original names can be restored by the companion tool.

## Features
- Token-aware identifier renaming (not blind text replacement)
- Skips Python keywords, built-ins, and names explicitly listed in `--keep`
- Writes a reversible JSON mapping
- No packing, encryption, anti-debugging, network activity, or runtime payload loading
- Includes tests and a sample file

## Requirements
Python 3.10+

## Usage
```bash
python obfuskit.py examples/sample.py -o build/sample_obfuscated.py --map build/sample.map.json
```

Keep the mapping file private if it contains meaningful original names. Obfuscation is not encryption or a security boundary. Review transformed code and run your tests before using it.

## Scope
This is a portfolio/learning project, not a production-grade compiler. It handles tokenized Python identifiers conservatively; it does not attempt to rename every symbol safely across reflection, dynamic imports, `globals()`, serialization, or external interfaces.
