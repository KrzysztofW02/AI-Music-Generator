import os
import sys
import subprocess
import numpy as np
import qtvscodestyle as qtvsc
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QComboBox, QHBoxLayout, QSpacerItem, QSizePolicy, QSpinBox
from PyQt5.QtCore import Qt
from src.model_training import load_model, generate_notes
from src.midi_utils import create_midi_from_notes, instrument_programs
from pathlib import Path

class MusicGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('AI Music Generator')
        self.setGeometry(300, 300, 600, 200)

        self.layout = QVBoxLayout()
        self.model_label = QLabel('No model loaded', self)
        self.model_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.model_label)
        
        self.top_layout = QHBoxLayout()
        self.load_button = QPushButton('Load Model', self)
        self.load_button.clicked.connect(self.load_model_dialog)
        self.top_layout.addWidget(self.load_button)

        self.open_midi_button = QPushButton('Open MIDI File', self)
        self.open_midi_button.clicked.connect(self.open_midi_dialog)
        self.top_layout.addWidget(self.open_midi_button)

        self.instrument_dropdown = QComboBox(self)
        self.instrument_dropdown.addItems(instrument_programs.keys())
        self.top_layout.addWidget(self.instrument_dropdown)

        self.layout.addLayout(self.top_layout)
        self.layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.duration_layout = QHBoxLayout()
        self.duration_label = QLabel('Duration (seconds):', self)
        self.duration_layout.addWidget(self.duration_label)

        self.duration_spinbox = QSpinBox(self)
        self.duration_spinbox.setRange(1, 300)  
        self.duration_spinbox.setValue(60)  
        self.duration_layout.addWidget(self.duration_spinbox)

        self.layout.addLayout(self.duration_layout)

        self.generate_button = QPushButton('Generate Music', self)
        self.generate_button.clicked.connect(self.generate_music)
        self.layout.addWidget(self.generate_button)

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

        duration = self.duration_spinbox.value()  
        notes_per_second = 2  
        num_notes = duration * notes_per_second  

        seed_sequence_length = np.random.randint(40, 60)
        seed_sequence = np.random.rand(1, seed_sequence_length, 4)

        generated_notes = generate_notes(self.model, seed_sequence, num_notes=num_notes, temperature=0.8)

        base_dir = Path(__file__).resolve().parent.parent
        midi_file_path = base_dir / 'data' / 'generated_music.mid'
        selected_instrument = self.instrument_dropdown.currentText()
        midi_file_path_str = str(midi_file_path)
        create_midi_from_notes(generated_notes, midi_file_path_str, instrument_name=selected_instrument)
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

