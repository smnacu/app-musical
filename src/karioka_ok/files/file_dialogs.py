"""Utilidades de selección de archivos y guardado.

Encapsula el uso de diálogos de archivo para facilitar pruebas y
cambiar la implementación en el futuro si es necesario.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from PySide6 import QtWidgets


@dataclass
class FileFilters:
    audio: str = "Audio Files (*.mp3 *.wav *.flac)"
    image: str = "Images (*.png *.jpg *.jpeg)"
    text: str = "Text Files (*.txt)"
    any: str = "All Files (*.*)"


def open_file_dialog(
    parent: Optional[QtWidgets.QWidget] = None,
    caption: str = "Seleccionar archivo",
    filter_str: str = FileFilters.any,
) -> Optional[str]:
    """Abre un diálogo para seleccionar un archivo y devuelve la ruta."""
    file_path, _ = QtWidgets.QFileDialog.getOpenFileName(parent, caption, "", filter_str)
    return file_path or None


def save_file_dialog(
    parent: Optional[QtWidgets.QWidget] = None,
    caption: str = "Guardar como",
    suggested_name: str = "output",
    filter_str: str = FileFilters.any,
) -> Optional[str]:
    """Abre un diálogo para guardar y devuelve la ruta seleccionada."""
    file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
        parent, caption, suggested_name, filter_str
    )
    return file_path or None
