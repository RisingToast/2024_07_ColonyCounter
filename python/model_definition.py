# model_definition.py

import tensorflow as tf

def create_model(input_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=input_shape),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(4)  # Output layer
    ])
    
    model.compile(optimizer='adam',
                  loss='mean_squared_error',  # Ensure this matches your task
                  metrics=['accuracy'])
    
    return model
