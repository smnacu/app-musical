"""Procesamiento de audio: carga, cambio de tonalidad y exportación.

Implementa funciones mínimas usando librosa/pydub. En un MVP, priorizamos
claridad y manejo de errores. Para producción, optimizar y manejar más casos.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pydub import AudioSegment

try:
    import librosa
    import numpy as np
    HAS_LIBROSA = True
except Exception:  # pragma: no cover - el entorno podría no tener dependencias aún
    HAS_LIBROSA = False
    librosa = None  # type: ignore
    np = None  # type: ignore


@dataclass
class AudioData:
    """Representa una pista de audio en memoria."""
    segment: AudioSegment
    sample_rate: int
    channels: int
    path: Optional[str] = None


def load_audio(path: str) -> AudioData:
    """Carga un archivo de audio en AudioSegment.

    Args:
        path: Ruta del archivo de audio
    Returns:
        AudioData con metadata básica
    """
    seg = AudioSegment.from_file(path)
    return AudioData(segment=seg, sample_rate=seg.frame_rate, channels=seg.channels, path=path)


def change_pitch_semitones(audio: AudioData, semitones: int) -> AudioData:
    """Cambia la tonalidad de la pista en semitonos usando librosa si está disponible.

    Si librosa no está disponible, se aplica un cambio de velocidad/resample básico
    con pydub como stub (no mantiene duración con fidelidad).
    """
    if semitones == 0:
        return audio

    if HAS_LIBROSA:
        # Convertir a np.ndarray (float32), procesar con librosa, volver a AudioSegment
        import soundfile as sf
        import io

        # Exportar el segmento a bytes WAV
        buf = io.BytesIO()
        audio.segment.export(buf, format="wav")
        buf.seek(0)
        y, sr = sf.read(buf, dtype="float32")
        y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=float(semitones))

        # Guardar de vuelta a WAV en memoria y re-crear AudioSegment
        out_buf = io.BytesIO()
        sf.write(out_buf, y_shifted, sr, format="WAV")
        out_buf.seek(0)
        shifted = AudioSegment.from_file(out_buf, format="wav")
        return AudioData(segment=shifted, sample_rate=shifted.frame_rate, channels=shifted.channels, path=audio.path)

    # Fallback simple: cambiar velocidad (afecta tono y duración)
    new_frame_rate = int(audio.segment.frame_rate * (2.0 ** (semitones / 12.0)))
    shifted = audio.segment._spawn(audio.segment.raw_data, overrides={"frame_rate": new_frame_rate}).set_frame_rate(audio.segment.frame_rate)
    return AudioData(segment=shifted, sample_rate=shifted.frame_rate, channels=shifted.channels, path=audio.path)


def export_audio(audio: AudioData, out_path: str, format_hint: Optional[str] = None) -> None:
    """Exporta el audio a una ruta, intentando deducir el formato por extensión.

    Requiere ffmpeg para MP3/FLAC en la mayoría de plataformas.
    """
    fmt = format_hint or (out_path.split(".")[-1].lower() if "." in out_path else "wav")
    audio.segment.export(out_path, format=fmt)
