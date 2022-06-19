import argparse
import os

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense, BatchNormalization, Dropout
from tensorflow.keras.models import Sequential
import flwr as fl
from PIL import Image
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

# Define Flower client
class FLClient(fl.client.NumPyClient):
    def __init__(self, model, x_train, y_train, x_test, y_test):
        self.model = model
        self.x_train, self.y_train = x_train, y_train
        self.x_test, self.y_test = x_test, y_test

    def get_parameters(self):
        """Get parameters of the local model."""
        return self.model.get_weights()

    def fit(self, parameters, config):
        """Train parameters on the locally held training set."""

        # Update local model parameters
        self.model.set_weights(parameters)

        # Get hyperparameters for this round
        batch_size: int = config["batch_size"]
        epochs: int = config["local_epochs"]
        print("\n\ntraining starting")
        print(len(self.x_train),len(self.y_train))
        # Train the model using hyperparameters from config
        history = self.model.fit(
            self.x_train,
            self.y_train,
            batch_size,
            epochs,
            validation_split=0.1,
            shuffle = True
        )
        print("\n\n training finished")
        # Return updated model parameters and results
        parameters_prime = self.model.get_weights()
        num_examples_train = len(self.x_train)
        results = {
            "loss": history.history["loss"][0],
            "accuracy": history.history["accuracy"][0],
            "val_loss": history.history["val_loss"][0],
            "val_accuracy": history.history["val_accuracy"][0],
        }
        return parameters_prime, num_examples_train, results

    def evaluate(self, parameters, config):
        """Evaluate parameters on the locally held test set."""

        # Update local model with global parameters
        self.model.set_weights(parameters)

        # Get config values
        steps: int = config["val_steps"]

        # Evaluate global model parameters on the local test data and return results
        loss, accuracy = self.model.evaluate(np.array(self.x_test), np.array(self.y_test), 32, steps=steps)
        num_examples_test = len(self.x_test)
        return loss, num_examples_test, {"accuracy": accuracy}


def main() -> None:
    # Parse command line argument `partition`
    parser = argparse.ArgumentParser(description="Flower")
    parser.add_argument("--dataset_path", type=str, required=True)
    args = parser.parse_args()
    # Load and compile Keras model
    model = build_model()
    # Load the local data partition
    x_train,x_test,y_train, y_test = load_dataset(args.dataset_path)
    # Start Flower client
    client = FLClient(model, x_train, y_train, x_test, y_test)
    fl.client.start_numpy_client("127.0.0.1:5001", client=client)

def build_model():
    """
    Builds model and compiles it
    """
    SIZE=64
    model = Sequential()
    model.add(Convolution2D(32, (3, 3), input_shape = (SIZE, SIZE, 3), activation = 'relu', data_format='channels_last'))
    model.add(MaxPooling2D(pool_size = (2, 2), data_format="channels_last"))
    model.add(BatchNormalization(axis = -1))
    model.add(Dropout(0.2))
    model.add(Convolution2D(32, (3, 3), activation = 'relu'))
    model.add(MaxPooling2D(pool_size = (2, 2), data_format="channels_last"))
    model.add(BatchNormalization(axis = -1))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(activation = 'relu', units=512))
    model.add(BatchNormalization(axis = -1))
    model.add(Dropout(0.2))
    model.add(Dense(activation = 'relu', units=256))
    model.add(BatchNormalization(axis = -1))
    model.add(Dropout(0.2))
    model.add(Dense(activation = 'sigmoid', units=2))
   # we compile our model 
    model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
    return model


def load_dataset(dataset_path: str):
    SIZE=64
    parasitized_images = os.listdir(dataset_path + '/Parasitized/')
    uninfected_images = os.listdir(dataset_path + '/Uninfected/')
    dataset=[]
    label=[]
    for i, (image_name_parasited,image_name_uninfected) in enumerate(zip(parasitized_images,uninfected_images)):
        if ('.png' in image_name_parasited) and ('.png' in image_name_uninfected):
            image_parasited = Image.open(dataset_path + '/Parasitized/' + image_name_parasited)
            image_uninfected = Image.open(dataset_path + '/Uninfected/' + image_name_uninfected)
            image_parasited = image_parasited.resize((SIZE, SIZE))
            image_uninfected = image_uninfected.resize((SIZE, SIZE))
            dataset.append(np.array(image_parasited))
            label.append(0)
            dataset.append(np.array(image_uninfected))
            label.append(1)
    X_train, X_test, y_train, y_test = train_test_split(np.array(dataset), to_categorical(np.array(label)), test_size = 0.10, random_state = 0)
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    main()