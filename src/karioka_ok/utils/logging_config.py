"""Configuración simple de logging para la app.

Este módulo centraliza la configuración de los logs para reusarlos
en toda la aplicación. Pensado para ampliarse con handlers/formatters
según necesidades (archivo, consola, etc.).
"""
from __future__ import annotations

import logging
from logging import Logger


def get_logger(name: str = "karioka_ok") -> Logger:
    """Devuelve un logger con formato básico y nivel INFO por defecto.

    Args:
        name: Nombre del logger

    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s - %(name)s - %(message)s", "%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
