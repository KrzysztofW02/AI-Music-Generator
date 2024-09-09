import sys
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

        seed_sequence = [[0.5]] * 50
        seed_sequence = np.array(seed_sequence).reshape(1, 50, 1)

        generated_notes = generate_notes(self.model, seed_sequence)

        create_midi_from_notes(generated_notes, 'data/generated_music.mid')
        print("Music generated and saved to 'data/generated_music.mid'")

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
