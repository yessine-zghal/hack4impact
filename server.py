from typing import Any, Callable, Dict, List, Optional, Tuple

import flwr as fl
import tensorflow as tf
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense, BatchNormalization, Dropout
from tensorflow.keras.models import Sequential
import flwr as fl
from PIL import Image
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical


def main() -> None:
    # Load and compile model for
    # server-side parameter initialization
    model=build_model()
    # Create strategy
    strategy = fl.server.strategy.FedAvg(
        fraction_fit=1.0,
        fraction_eval=1.0,
        min_fit_clients=2,
        min_eval_clients=2,
        min_available_clients=2,
        on_fit_config_fn=fit_config,
        on_evaluate_config_fn=evaluate_config,
        initial_parameters=fl.common.weights_to_parameters(model.get_weights()),
    )

    # Start Flower server for four rounds of federated learning
    fl.server.start_server("127.0.0.1:5001", config={"num_rounds": 2}, strategy=strategy,grpc_max_message_length = 1024*1024*1024)


def fit_config(rnd: int):
    """Return training configuration dict for each round.
    Keep batch size fixed at 32, perform two rounds of training with 10
    local epoch.
    """
    config = {
        "batch_size": 32,
        "local_epochs": 10,
    }
    return config


def evaluate_config(rnd: int):
    """Return evaluation configuration dict for each round.
    Perform five local evaluation steps on each client (i.e., use five
    batches) during rounds one to three, then increase to ten local
    evaluation steps.
    """
    val_steps = 10
    return {"val_steps": val_steps}
def build_model():
    SIZE = 64  # our neural nets expect input data of same format so we will use resize our images to (size x size) 
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Conv2D(filters=128, kernel_size=3, padding='same', activation='relu', input_shape=(64,64,3))) 
    model.add(tf.keras.layers.MaxPooling2D(pool_size=3))
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Conv2D(filters=128, kernel_size=3, padding='same', activation='relu'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=3))
    model.add(tf.keras.layers.Conv2D(filters=64, kernel_size=3, padding='same', activation='relu'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=3))
    model.add(tf.keras.layers.Conv2D(filters=64, kernel_size=2, padding='same', activation='relu'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(256, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))                
    model.add(tf.keras.layers.Dense(32, activation='softmax'))
    model.summary()
    model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
    return model

if __name__ == "__main__":
    main()