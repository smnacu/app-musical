# Karioka.ok

Karioka.ok es un MVP de aplicación de escritorio para preparar pistas de karaoke de forma simple: cambiar tonalidad, editar metadatos (carátula y descripción), cargar letra y exportar en varios formatos.

Este repositorio contiene un esqueleto modular en Python con GUI (PySide6), procesamiento de audio (librosa/pydub), y soporte para Docker.

## Características del MVP (esqueleto)
- Carga de archivos de audio (MP3, WAV, FLAC, etc.).
- Cambio de tonalidad (subir/bajar semitonos) usando `librosa` (stub funcional con try/catch).
- Edición de metadatos (carátula y descripción) con `mutagen`.
- Carga de letra desde `.txt`.
- Exportación a formatos comunes (WAV, MP3, FLAC) usando `pydub`/`ffmpeg`.
- GUI PySide6 minimalista y colorida.

> Nota: Para exportar a MP3/otros, se requiere `ffmpeg` instalado en el sistema o dentro de Docker.

## Requisitos
- Python 3.10+
- ffmpeg (para exportaciones y algunas operaciones de audio con `pydub`).

## Instalación (local)
1. Crear y activar un entorno virtual.
2. Instalar dependencias desde `requirements.txt`.
3. Ejecutar la app.

## Estructura
- `src/karioka_ok/` paquetes modulares: `audio`, `gui`, `metadata`, `lyrics`, `files`, `utils`.
- `main.py` punto de entrada CLI/GUI.
- `tests/` pruebas mínimas.
- `Dockerfile` preparado para contenerización.

## Docker (opcional)
La GUI dentro de Docker es avanzada (requiere X11/WSLg o soluciones específicas). El Dockerfile aquí sirve para asegurar el entorno y operaciones por CLI/procesamiento. Úsalo para reproducibilidad y CI.

## Licencia
Uso personal/educativo. Verifica licencias de librerías incluidas.
