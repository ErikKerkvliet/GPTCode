import os
import time

import tensorflow as tf
from tensorflow import keras


class ImageClassifier:

    def __init__(self, model_path=None):
        self.model = None

        # Controleer of er al een getraind model bestaat.
        if model_path and os.path.exists(model_path):
            self.load_model(f'../models/{model_path}')

    def build_model(self):
        if self.model:
            return

        # Bouw het model op door middel van convolutionele lagen met max-pooling-lagen.
        self.model = keras.Sequential([
            keras.layers.Conv2D(32, (5, 5), input_shape=(244, 244, 1), activation='relu'),
            keras.layers.MaxPooling2D(pool_size=(4, 4)),
            keras.layers.Conv2D(64, (5, 5), activation='relu'),
            keras.layers.MaxPooling2D(pool_size=(4, 4)),
            keras.layers.Flatten(),
            keras.layers.Dense(1000, kernel_initializer='uniform', activation='relu'),
            keras.layers.Dense(500, kernel_initializer='uniform', activation='relu'),
            keras.layers.Dense(1, kernel_initializer='uniform', activation='sigmoid')
        ])

        # Compileer het model door middel van binary_crossentropy loss en gebruik de Adam optimizer.
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    def train(self):
        # Laad de dataset in door gebruik te maken van `ImageDataGenerator` en `flow_from_directory`.
        train_datagen = keras.preprocessing.image.ImageDataGenerator(
            rescale=1./255,
            shear_range=0.2,
            zoom_range=4,
            horizontal_flip=True)

        training_set = train_datagen.flow_from_directory(
            directory='../dataset/',
            target_size=(244, 244),
            color_mode="grayscale",
            batch_size=32,
            class_mode='binary')

        # Train het model met behulp van `fit_generator`.
        self.model.fit(training_set, steps_per_epoch=len(training_set), epochs=5)

        # Maak een map 'models' als deze nog niet bestaat.
        if not os.path.exists("../models"):
            os.makedirs("../models")

        # Sla het getrainde model op in een H5-bestand met de huidige tijd als naamgeving.
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"model_{timestamp}.h5"
        filepath = os.path.join("../models", filename)

        self.model.save(filepath)

    def predict(self, image_path):
        # Laad de afbeelding en converteer deze naar een numpy-array.
        img = keras.preprocessing.image.load_img(image_path, target_size=(244, 244), color_mode="grayscale")
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array /= 255.0
        img_array = tf.expand_dims(img_array, axis=0)

        # Gebruik het getrainde model om voorspellingen te doen op de nieuwe afbeelding.
        if self.model.predict(img_array)[0][0] > 0.5:
            return "plus"
        else:
            return "minus"

    def load_model(self, model_path):
        # Laad een eerder opgeslagen model uit een bestand.
        self.model = keras.models.load_model(model_path)


# Importeer de ImageClassifier-klasse.
# from image_classifier import ImageClassifier

classifier = ImageClassifier('model_20230622-225034.h5')  # current best
# classifier = ImageClassifier()

if not classifier.model:
    classifier.build_model()

    # Train het model op basis van de dataset en sla het getrainde model op.
    classifier.train()


correct_count = 0
total_count = 0

for class_name in ["m", "p"]:
    count = 1
    for img_file in os.listdir(f"../testmp/{class_name}"):
        count += 1
        # Voert voorspellingen uit op deze afbeelding door onze classifier te gebruiken.
        prediction = classifier.predict(f"../testmp/{class_name}/{img_file}")
        print(prediction)
        # Telt correcte classificaties bij, telt ook totaal aantal bekeken afbeeldingen bij.
        if prediction == class_name:
            correct_count += 1
            print('correct')
        else:
            print('incorrect')
        total_count += 1

        if count == 100:
            print('break')
            break

print(f"Totaal aantal geanalyseerde afbeeldingen: {total_count}")
print(f"Aantal correct geclassificeerde afbeeldingen: {correct_count}")
