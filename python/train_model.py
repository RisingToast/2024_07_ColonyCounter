import tensorflow as tf
from data_preprocessing import create_dataset
from model_definition import create_model

def train_model(model, dataset, epochs=10):
    dataset = dataset.batch(32)
    model.fit(dataset, epochs=epochs)

if __name__ == "__main__":
    dataset = create_dataset()
    model = create_model(dataset)
    train_model(model, dataset)
