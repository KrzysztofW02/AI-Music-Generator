import pickle
import numpy as np
from model_training import create_model, save_model
from tensorflow.keras.callbacks import EarlyStopping
from pathlib import Path

processed_data_path = Path(__file__).resolve().parent.parent / 'data' / 'preprocessed_data.pkl'

sequence_length = 50
batch_size = 128  
epochs = 5  
max_chunks = 3000
chunk_counter = 0

early_stopping = EarlyStopping(monitor='loss', patience=2, restore_best_weights=True)

def load_preprocessed_data_in_chunks(processed_data_path, chunk_size=1000):
    with open(processed_data_path, 'rb') as f:
        while True:
            try:
                inputs, targets = pickle.load(f)
                inputs = np.array(inputs).astype(np.float32)  
                targets = [np.array(t).flatten() for t in targets] 
                targets = [t for t in targets if len(t) == 4]  
                targets = np.array(targets).astype(np.float32)

                if len(inputs) != len(targets):
                    min_samples = min(len(inputs), len(targets))
                    inputs = inputs[:min_samples]
                    targets = targets[:min_samples]

                yield inputs, targets

            except EOFError:
                break

model = create_model(sequence_length=sequence_length)

for inputs, targets in load_preprocessed_data_in_chunks(processed_data_path):
    if chunk_counter >= max_chunks:
        break
    model.fit(inputs, targets, epochs=epochs, batch_size=batch_size, callbacks=[early_stopping])
    chunk_counter += 1

save_model(model, 'models/music_generation_model.h5')
print("Model training complete and saved to models/music_generation_model.h5")