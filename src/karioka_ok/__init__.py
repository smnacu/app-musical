"""Paquete principal de Karioka.ok.

Arquitectura monolítica modular con submódulos:
- audio: carga, cambio de tonalidad, exportación.
- metadata: edición de carátula y descripción.
- lyrics: carga de letra desde .txt.
- files: utilidades de diálogo/rutas.
- gui: interfaz de usuario PySide6.
- utils: utilidades generales y configuración de logging.
"""
__all__ = [
    "audio",
    "metadata",
    "lyrics",
    "files",
    "gui",
    "utils",
]
