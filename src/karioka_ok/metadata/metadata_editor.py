"""Edición de metadatos: carátula y descripción.

Usa mutagen para escribir metadatos en archivos comunes (MP3, FLAC). Para WAV,
los metadatos son limitados; este MVP se centra en MP3/FLAC.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from mutagen.flac import FLAC, Picture
from mutagen.id3 import ID3, APIC, COMM, error as ID3Error


@dataclass
class TrackMetadata:
    description: Optional[str] = None
    cover_image_path: Optional[str] = None


def set_metadata(file_path: str, meta: TrackMetadata) -> None:
    """Escribe metadatos básicos en el archivo si es compatible (MP3/FLAC).

    - MP3: usa ID3 (APIC para carátula, COMM para comentario/descr.).
    - FLAC: usa PICTURE block y tag "DESCRIPTION".
    """
    suffix = Path(file_path).suffix.lower()

    if suffix == ".mp3":
        _set_mp3_metadata(file_path, meta)
    elif suffix == ".flac":
        _set_flac_metadata(file_path, meta)
    else:
        # Para MVP: sin-op para formatos no soportados
        return


def _set_mp3_metadata(file_path: str, meta: TrackMetadata) -> None:
    try:
        tags = ID3(file_path)
    except ID3Error:
        tags = ID3()

    if meta.cover_image_path:
        with open(meta.cover_image_path, "rb") as img:
            apic = APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=img.read())
            tags.add(apic)

    if meta.description:
        comm = COMM(encoding=3, lang="eng", desc="desc", text=meta.description)
        tags.add(comm)

    tags.save(file_path)


def _set_flac_metadata(file_path: str, meta: TrackMetadata) -> None:
    flac = FLAC(file_path)
    if meta.description:
        flac["DESCRIPTION"] = [meta.description]
    if meta.cover_image_path:
        pic = Picture()
        pic.type = 3  # Cover (front)
        pic.mime = "image/jpeg"
        with open(meta.cover_image_path, "rb") as img:
            pic.data = img.read()
        flac.clear_pictures()
        flac.add_picture(pic)
    flac.save()
