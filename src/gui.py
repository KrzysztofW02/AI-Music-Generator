import os
import sys
import subprocess
import numpy as np
import qtvscodestyle as qtvsc
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel
from src.model_training import load_model, generate_notes
from src.midi_utils import create_midi_from_notes
class MusicGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('AI Music Generator')
        self.setGeometry(100, 100, 300, 150)

        self.layout = QVBoxLayout()

        self.model_label = QLabel('No model loaded', self)
        self.layout.addWidget(self.model_label)

        self.load_button = QPushButton('Load Model', self)
        self.load_button.clicked.connect(self.load_model_dialog)
        self.layout.addWidget(self.load_button)

        self.generate_button = QPushButton('Generate Music', self)
        self.generate_button.clicked.connect(self.generate_music)
        self.layout.addWidget(self.generate_button)

        self.open_midi_button = QPushButton('Open MIDI File', self)
        self.open_midi_button.clicked.connect(self.open_midi_dialog)
        self.layout.addWidget(self.open_midi_button)

        self.setLayout(self.layout)
        self.model = None

    def load_model_dialog(self):
        model_path, _ = QFileDialog.getOpenFileName(self, "Open Model File", "", "Model Files (*.h5)")
        if model_path:
            self.model = load_model(model_path)
            self.model_label.setText(f"Model loaded: {model_path}")
            print("Model loaded successfully!")

    def generate_music(self):
        if self.model is None:
            print("No model loaded!")
            return

        seed_sequence = np.random.rand(1, 50, 1)  
        generated_notes = generate_notes(self.model, seed_sequence)

        midi_file_path = 'C:/Users/Darkr/Desktop/Python/AI-Music-Generator/data/generated_music.mid'
        create_midi_from_notes(generated_notes, midi_file_path)
        print(f"Music generated and saved to '{midi_file_path}'")

        self.open_midi_file(midi_file_path)

    def open_midi_dialog(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        midi_file_path, _ = QFileDialog.getOpenFileName(self, "Open MIDI File", base_dir, "MIDI Files (*.mid)")

        if midi_file_path:
            self.open_midi_file(midi_file_path)

    def open_midi_file(self, file_path):
        if sys.platform.startswith('win'):
            os.startfile(file_path)  
        elif sys.platform.startswith('darwin'):
            subprocess.call(('open', file_path))  
        elif sys.platform.startswith('linux'):
            subprocess.call(('xdg-open', file_path))  

def start_gui():
    app = QApplication(sys.argv)
    stylesheet = qtvsc.load_stylesheet(qtvsc.Theme.DARK_VS)
    
    custom_button_style = """
    QPushButton {
        background-color: #323232; 
        color: #FFF;  
        border: 1px solid #555; 
        border-radius: 10px;  
        padding: 5px;  
    }
    QPushButton:hover {
        background-color: #444; 
        color: #FFF;  
        border: 1px solid #666;  
    }
    QPushButton:pressed {
        background-color: #555;  
        color: #FFF; 
        border: 1px solid #777; 
    }
    """
    
    app.setStyleSheet(stylesheet + custom_button_style)
    gui = MusicGeneratorApp()
    gui.show()
    sys.exit(app.exec_())

