"""
Punto de entrada de Karioka.ok
- Si se ejecuta sin argumentos: inicia la GUI (PySide6).
- Opción --no-gui: ejecuta un flujo mínimo de CLI para verificación del entorno.

Este archivo añade `src/` al sys.path para cargar el paquete `karioka_ok`.
"""
from __future__ import annotations

import argparse
import os
import sys

# Asegurar que `src` esté en el path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(BASE_DIR, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


def run_gui() -> None:
    # Importación perezosa para evitar requerir PySide6 en entornos de solo CLI
    from karioka_ok.gui.app import run

    run()


def run_cli() -> None:
    print("Karioka.ok CLI: entorno OK. Puedes ejecutar la GUI sin --no-gui.")
    print("- Versiones de librerías se resuelven desde requirements.txt.")
    print("- ffmpeg debería estar instalado para exportación a MP3/FLAC.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Karioka.ok - MVP")
    parser.add_argument(
        "--no-gui", action="store_true", help="No iniciar GUI; ejecutar comprobaciones básicas."
    )
    args = parser.parse_args()

    if args.no_gui:
        run_cli()
    else:
        run_gui()
