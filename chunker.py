"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document

# ── Milestone 3 strategy: split on Markdown headers, not character count. ──
#
# This corpus (city_guides) is structured guides with real headers — each
# "## Getting there" / "## Eat and drink" section is already a self-contained
# idea, decided by the author, not by us. Splitting there costs nothing;
# splitting mid-paragraph loses a thought.
#
# Numbers, from actually measuring the header sections across all 14 docs
# (corpora/city_guides/documents/*.md): they run 23-711 characters, median
# ~285. The short outliers are bare titles ("# Eating across the region")
# that sit alone before the first "##" - fragments with nothing under them.
MIN_CHUNK_CHARS = 150   # merge a fragment this short into the next section
MAX_CHUNK_CHARS = 900   # no section in this corpus needs this; safety net
CHUNK_OVERLAP = 100     # only used if MAX_CHUNK_CHARS ever forces a re-split

_HEADER_SPLIT = re.compile(r"\n(?=#{1,6}\s)")


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _split_into_sections(text: str) -> list[str]:
    """Split on Markdown headers, folding any too-short fragment forward."""
    raw = [part.strip() for part in _HEADER_SPLIT.split(text) if part.strip()]

    sections: list[str] = []
    for part in raw:
        if sections and len(sections[-1]) < MIN_CHUNK_CHARS:
            sections[-1] = f"{sections[-1]}\n\n{part}"
        else:
            sections.append(part)
    return sections


def _split_oversized(section: str) -> list[str]:
    """Fall back to paragraph-by-paragraph splitting for an over-long section."""
    if len(section) <= MAX_CHUNK_CHARS:
        return [section]

    paragraphs = [p.strip() for p in section.split("\n\n") if p.strip()]
    pieces: list[str] = []
    current = ""
    for para in paragraphs:
        candidate = f"{current}\n\n{para}" if current else para
        if len(candidate) > MAX_CHUNK_CHARS and current:
            pieces.append(current)
            tail = current[-CHUNK_OVERLAP:]
            current = f"{tail}\n\n{para}"
        else:
            current = candidate
    if current:
        pieces.append(current)
    return pieces


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split on Markdown headers. Each "## ..." section in this corpus is
    already a self-contained idea, so splitting there (instead of at a fixed
    character count) keeps chunks from cutting a thought in half.

    See the module-level comment above for the reasoning behind
    MIN_CHUNK_CHARS / MAX_CHUNK_CHARS / CHUNK_OVERLAP.
    """
    chunks: list[Chunk] = []
    for doc in documents:
        index = 0
        for section in _split_into_sections(doc.text):
            for piece in _split_oversized(section):
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )
                index += 1
    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
