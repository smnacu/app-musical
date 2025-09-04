"""Aplicación PySide6: ventana principal y wiring de módulos.

La UI es minimalista y colorida. Contiene secciones para: carga de audio,
cambio de tonalidad, metadatos (carátula y descripción), letra y exportación.
"""
from __future__ import annotations

from typing import Optional

from PySide6 import QtWidgets, QtGui

from karioka_ok.utils.logging_config import get_logger
from karioka_ok.files.file_dialogs import FileFilters, open_file_dialog, save_file_dialog
from karioka_ok.audio.audio_processor import (
    AudioData,
    load_audio,
    change_pitch_semitones,
    export_audio,
)
from karioka_ok.metadata.metadata_editor import TrackMetadata, set_metadata
from karioka_ok.lyrics.lyrics_loader import Lyrics, load_lyrics


logger = get_logger("karioka_ok.gui")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Karioka.ok")
        self.resize(900, 600)

        # Paleta colorida minimalista
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtGui.QColor("#1b1f3b"))
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor("#ffffff"))
        self.setPalette(palette)

        # Estado de la app
        self.original_audio: Optional[AudioData] = None
        self.lyrics: Optional[Lyrics] = None
        self.meta = TrackMetadata()

        # Widgets principales
        central = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setSpacing(12)

        # Sección: carga de audio
        self.btn_load_audio = QtWidgets.QPushButton("Cargar audio…")
        self.lbl_audio = QtWidgets.QLabel("Ningún archivo cargado")
        self.lbl_audio.setStyleSheet("color: #a0a4c0")
        layout.addWidget(self.btn_load_audio)
        layout.addWidget(self.lbl_audio)

        # Sección: cambio de tonalidad
        pitch_layout = QtWidgets.QHBoxLayout()
        self.spin_semitones = QtWidgets.QSpinBox()
        self.spin_semitones.setRange(-12, 12)
        self.spin_semitones.setValue(0)
        self.spin_semitones.setToolTip("Define el cambio de tono que se aplicará al exportar")
        pitch_layout.addWidget(QtWidgets.QLabel("Semitonos:"))
        pitch_layout.addWidget(self.spin_semitones)
        layout.addLayout(pitch_layout)

        # Sección: metadatos
        meta_layout = QtWidgets.QHBoxLayout()
        self.txt_description = QtWidgets.QLineEdit()
        self.txt_description.setPlaceholderText("Descripción / notas de la pista")
        self.btn_select_cover = QtWidgets.QPushButton("Seleccionar carátula…")
        meta_layout.addWidget(self.txt_description)
        meta_layout.addWidget(self.btn_select_cover)
        layout.addLayout(meta_layout)

        # Sección: letra
        lyrics_layout = QtWidgets.QHBoxLayout()
        self.btn_load_lyrics = QtWidgets.QPushButton("Cargar letra (.txt)…")
        self.lbl_lyrics = QtWidgets.QLabel("Sin letra")
        self.lbl_lyrics.setStyleSheet("color: #a0a4c0")
        lyrics_layout.addWidget(self.btn_load_lyrics)
        lyrics_layout.addWidget(self.lbl_lyrics)
        layout.addLayout(lyrics_layout)

        # Sección: exportación
        export_layout = QtWidgets.QHBoxLayout()
        self.btn_export_wav = QtWidgets.QPushButton("Exportar WAV")
        self.btn_export_mp3 = QtWidgets.QPushButton("Exportar MP3")
        self.btn_export_flac = QtWidgets.QPushButton("Exportar FLAC")
        self.btn_export_original = QtWidgets.QPushButton("Exportar Original")
        export_layout.addWidget(self.btn_export_wav)
        export_layout.addWidget(self.btn_export_mp3)
        export_layout.addWidget(self.btn_export_flac)
        export_layout.addWidget(self.btn_export_original)
        layout.addLayout(export_layout)

        self.setCentralWidget(central)

        # Estilos minimalistas
        self.setStyleSheet(
            """
            QWidget { color: #ffffff; font-size: 14px; }
            QPushButton { background-color: #5e60ce; padding: 8px 12px; border-radius: 6px; }
            QPushButton:hover { background-color: #6930c3; }
            QLineEdit { background: #2c2f52; border: 1px solid #444b8a; border-radius: 6px; padding: 6px; }
            QLabel { color: #ffffff; }
            """
        )

        # Conexiones
        self.btn_load_audio.clicked.connect(self.on_load_audio)
        self.btn_select_cover.clicked.connect(self.on_select_cover)
        self.btn_load_lyrics.clicked.connect(self.on_load_lyrics)
        self.btn_export_wav.clicked.connect(lambda: self.on_export("wav"))
        self.btn_export_mp3.clicked.connect(lambda: self.on_export("mp3"))
        self.btn_export_flac.clicked.connect(lambda: self.on_export("flac"))
        self.btn_export_original.clicked.connect(self.on_export_original)

    # Slots
    def on_load_audio(self) -> None:
        path = open_file_dialog(self, "Seleccionar audio", FileFilters.audio)
        if not path:
            return
        try:
            self.original_audio = load_audio(path)
            self.lbl_audio.setText(f"Cargado: {path}")
            logger.info("Audio cargado: %s", path)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"No se pudo cargar el audio:\n{e}")

    def on_select_cover(self) -> None:
        path = open_file_dialog(self, "Seleccionar carátula", FileFilters.image)
        if not path:
            return
        self.meta.cover_image_path = path
        logger.info("Carátula seleccionada: %s", path)

    def on_load_lyrics(self) -> None:
        path = open_file_dialog(self, "Seleccionar letra (.txt)", FileFilters.text)
        if not path:
            return
        try:
            self.lyrics = load_lyrics(path)
            self.lbl_lyrics.setText(f"Letra: {path}")
            logger.info("Letra cargada: %s", path)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"No se pudo cargar la letra:\n{e}")

    def on_export(self, fmt: str) -> None:
        if not self.original_audio:
            QtWidgets.QMessageBox.warning(self, "Atención", "Carga un audio primero.")
            return

        # Actualizar descripción desde la UI
        self.meta.description = self.txt_description.text().strip() or None

        out_path = save_file_dialog(self, f"Exportar {fmt.upper()}", "salida." + fmt, f"*.{fmt}")
        if not out_path:
            return

        try:
            # Determinar si hay que aplicar cambio de tono
            audio_to_export = self.original_audio
            semitones = int(self.spin_semitones.value())

            if semitones != 0:
                logger.info("Aplicando cambio de %d semitonos para la exportación...", semitones)
                # Aplicar el cambio de forma no destructiva, desde el audio original
                audio_to_export = change_pitch_semitones(self.original_audio, semitones)

            # Exportar el audio (original o modificado)
            export_audio(audio_to_export, out_path, format_hint=fmt)

            # Escribir metadatos si corresponde
            try:
                set_metadata(out_path, self.meta)
            except Exception as meta_err:
                logger.warning("No se pudieron escribir metadatos: %s", meta_err)

            QtWidgets.QMessageBox.information(self, "Listo", f"Archivo exportado en {out_path}")
            logger.info("Exportado: %s", out_path)
        except Exception as e:
            logger.critical("No se pudo exportar el audio: %s", e, exc_info=True)
            QtWidgets.QMessageBox.critical(self, "Error", f"No se pudo exportar:\n{e}")

    def on_export_original(self) -> None:
        if not self.original_audio or not self.original_audio.path:
            QtWidgets.QMessageBox.warning(self, "Atención", "Carga un audio primero.")
            return
        # Deducir formato original por extensión
        ext = self.original_audio.path.split(".")[-1].lower()
        self.on_export(ext)


def run() -> None:
    app = QtWidgets.QApplication([])
    win = MainWindow()
    win.show()
    app.exec()
