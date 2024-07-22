import tensorflow as tf
import matplotlib.pyplot as plt
from data_preprocessing import dataset
from model_definition import create_model

model = tf.keras.models.load_model('my_model.h5')

def visualize_predictions(image, predictions):
    plt.imshow(image)
    for bbox in predictions:
        rect = plt.Rectangle((bbox['left'], bbox['top']),
                             bbox['width'], bbox['height'],
                             fill=False, edgecolor='red', linewidth=2)
        plt.gca().add_patch(rect)
    plt.show()

for image, _ in dataset.take(1):
    predictions = model.predict(image)
    visualize_predictions(image[0], predictions[0])
