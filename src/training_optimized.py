import pickle
import numpy as np
from model_training import create_model, train_model, save_model
from tensorflow.keras.callbacks import EarlyStopping
from pathlib import Path

processed_data_path = base_dir = Path(__file__).resolve().parent.parent / 'data' / 'preprocessed_data.pkl'

sequence_length = 50
batch_size = 128  
epochs = 5  
max_chunks = 2000  
chunk_counter = 0

early_stopping = EarlyStopping(monitor='loss', patience=2, restore_best_weights=True)

def load_preprocessed_data_in_chunks(processed_data_path, chunk_size=1000):
    with open(processed_data_path, 'rb') as f:
        while True:
            try:
                inputs, targets = pickle.load(f)
                inputs = np.expand_dims(np.array(inputs), axis=-1)
                targets = np.array(targets)
                if len(targets) % 4 == 0:
                    targets = np.reshape(targets, (-1, 4))
                else:
                    remainder = len(targets) % 4
                    targets = targets[:-remainder] 
                    targets = np.reshape(targets, (-1, 4))
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
    print(f"Training on chunk with {len(inputs)} samples")
    model.fit(inputs, targets, epochs=epochs, batch_size=batch_size, callbacks=[early_stopping])
    chunk_counter += 1

save_model(model, 'models/music_generation_model.h5')
print("Model training complete and saved to models/music_generation_model.h5")
