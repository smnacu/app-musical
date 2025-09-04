import os
import unittest
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QApplication
from karioka_ok.gui.app import MainWindow
from karioka_ok.audio.audio_processor import AudioData
from pydub import AudioSegment

class TestMainWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication([])

    def setUp(self):
        self.window = MainWindow()

    @patch('karioka_ok.gui.app.open_file_dialog')
    def test_load_audio(self, mock_open_file_dialog):
        # Simulamos la selección de un archivo de audio
        mock_open_file_dialog.return_value = 'test_audio.wav'
        
        # Creamos un archivo de audio falso para la prueba
        audio = AudioSegment.silent(duration=1000)
        audio.export('test_audio.wav', format='wav')
        
        # Verificamos que el audio se carga correctamente
        self.window.on_load_audio()
        self.assertIsNotNone(self.window.audio)
        self.assertEqual(self.window.lbl_audio.text(), 'Cargado: test_audio.wav')

    def test_apply_pitch(self):
        # Creamos un objeto AudioData para la prueba
        self.window.audio = AudioData(segment=AudioSegment.silent(duration=1000), sample_rate=44100, channels=1)
        
        # Verificamos que el tono se aplica correctamente
        self.window.spin_semitones.setValue(2)
        self.window.on_apply_pitch()
        self.assertEqual(self.window.semitones, 2)

    @patch('karioka_ok.gui.app.open_file_dialog')
    def test_select_cover(self, mock_open_file_dialog):
        # Simulamos la selección de un archivo de imagen
        mock_open_file_dialog.return_value = 'test_cover.jpg'
        
        # Verificamos que la carátula se selecciona correctamente
        self.window.on_select_cover()
        self.assertEqual(self.window.meta.cover_image_path, 'test_cover.jpg')

    @patch('karioka_ok.gui.app.open_file_dialog')
    def test_load_lyrics(self, mock_open_file_dialog):
        # Simulamos la selección de un archivo de letra
        mock_open_file_dialog.return_value = 'test_lyrics.txt'
        
        # Creamos un archivo de letra falso para la prueba
        with open('test_lyrics.txt', 'w') as f:
            f.write('Letra de prueba')
            
        # Verificamos que la letra se carga correctamente
        self.window.on_load_lyrics()
        self.assertIsNotNone(self.window.lyrics)
        self.assertEqual(self.window.lbl_lyrics.text(), 'Letra: test_lyrics.txt')

    @patch('karioka_ok.gui.app.save_file_dialog')
    @patch('karioka_ok.gui.app.export_audio')
    def test_export_audio(self, mock_export_audio, mock_save_file_dialog):
        # Creamos un objeto AudioData para la prueba
        self.window.audio = AudioData(segment=AudioSegment.silent(duration=1000), sample_rate=44100, channels=1)
        
        # Simulamos la selección de una ruta de guardado
        mock_save_file_dialog.return_value = 'test_output.wav'
        
        # Verificamos que el audio se exporta correctamente
        self.window.on_export('wav')
        mock_export_audio.assert_called_once()

    def tearDown(self):
        # Eliminamos los archivos de prueba
        if os.path.exists('test_audio.wav'):
            os.remove('test_audio.wav')
        if os.path.exists('test_lyrics.txt'):
            os.remove('test_lyrics.txt')

if __name__ == '__main__':
    unittest.main()
