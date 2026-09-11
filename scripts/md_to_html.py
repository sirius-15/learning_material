#!/usr/bin/env python3
"""Convert Markdown files under the project root to print-friendly static HTML."""

import pathlib
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.toc import TocExtension

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS_PATH = ROOT / "styles" / "print.css"

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
{css}
</style>
</head>
<body>
<article>
{body}
</article>
</body>
</html>
"""


def title_from_filename(name: str) -> str:
    return name.replace("_", " ").replace("-", " ")


def convert(md_path: pathlib.Path, css: str) -> None:
    source = md_path.read_text(encoding="utf-8")

    md = markdown.Markdown(
        extensions=[
            TableExtension(),
            FencedCodeExtension(),
            CodeHiliteExtension(css_class="highlight", linenums=False, guess_lang=False),
            TocExtension(permalink=False),
            "md_in_html",
        ],
        output_format="html",
    )

    body = md.convert(source)
    title = title_from_filename(md_path.stem)

    html = HTML_TEMPLATE.format(title=title, css=css, body=body)
    out = md_path.with_suffix(".html")
    out.write_text(html, encoding="utf-8")
    print(f"  {md_path.name}  ->  {out.name}  ({len(html):,} bytes)")


def main() -> None:
    css = CSS_PATH.read_text(encoding="utf-8")
    md_files = sorted(ROOT.rglob("*.md"))

    if not md_files:
        print("No .md files found in", ROOT)
        return

    print(f"Converting {len(md_files)} file(s):\n")
    for md_file in md_files:
        convert(md_file, css)

    print("\nDone.")


if __name__ == "__main__":
    main()
