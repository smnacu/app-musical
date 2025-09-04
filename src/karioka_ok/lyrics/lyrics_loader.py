"""Carga y asociación de letra desde un archivo .txt.

El MVP guarda la letra como string en memoria asociada a una pista.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Lyrics:
    text: str
    path: Optional[str] = None


def load_lyrics(path: str, encoding: str = "utf-8") -> Lyrics:
    with open(path, "r", encoding=encoding) as f:
        return Lyrics(text=f.read(), path=path)
