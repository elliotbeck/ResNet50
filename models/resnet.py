import tensorflow as tf
import json

class ResNet50(tf.keras.Model):
    INPUT_SHAPE = [227, 227]

    def __init__(self, num_classes, resnet_weights, dropout_rate, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config

        in_shape = self.input_shape + [3]

        self.model = tf.keras.models.Sequential()
        self.model.add(tf.keras.applications.resnet50.ResNet50(include_top=False,
                                                    weights= resnet_weights, input_shape=in_shape))
        self.model.add(tf.keras.layers.GlobalAveragePooling2D())                                    
        self.model.add(tf.keras.layers.Flatten())
        self.model.add(tf.keras.layers.Dropout(dropout_rate))
        self.model.add(tf.keras.layers.Dense(512, activation='relu'))
        # self.model.add(tf.keras.layers.Dropout(dropout_rate))
        # self.model.add(tf.keras.layers.Dense(256, activation='relu'))
        # self.model.add(tf.keras.layers.Dropout(dropout_rate))
        self.model.add(tf.keras.layers.Dense(num_classes, activation='softmax'))

        self.model.build([None] + self.input_shape + [3])  # Batch input shape.

    def call(self, inputs, training=None, mask=None):
        return self.model(inputs, training, mask)

    @property
    def input_shape(self):
        return ResNet50.INPUT_SHAPE