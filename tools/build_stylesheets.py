"""Build a compact stylesheet without changing selectors or declarations."""
import hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent


def compact_css(source):
    output = []
    i = 0
    while i < len(source):
        char = source[i]
        if source.startswith("/*", i):
            end = source.find("*/", i + 2)
            if end < 0:
                raise ValueError("Unterminated CSS comment")
            end += 2
            standalone = (i == 0 or source[i - 1].isspace()) and (end == len(source) or source[end].isspace())
            output.append(" " if standalone else source[i:end])
            i = end
        elif char in ("'", '"'):
            start, quote = i, char
            i += 1
            while i < len(source):
                if source[i] == "\\":
                    i += 2
                elif source[i] == quote:
                    i += 1
                    break
                else:
                    i += 1
            output.append(source[start:i])
        elif char.isspace():
            output.append(" ")
            i += 1
            while i < len(source) and source[i].isspace():
                i += 1
        else:
            output.append(char)
            i += 1
    return "".join(output).strip() + "\n"


def build():
    source = (ROOT / "style.css").read_text(encoding="utf-8")
    digest = hashlib.sha256(source.encode()).hexdigest()[:12]
    output = f"/* source-sha256: {digest} */\n" + compact_css(source)
    (ROOT / "assets/style.compact.css").write_text(output, encoding="utf-8")
    print(f"CSS: {len(source.encode())} -> {len(output.encode())} bytes")


if __name__ == "__main__":
    build()
