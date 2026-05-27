import tensorflow as tf
from tensorflow.keras import layers


class FeatureGateLayer(layers.Layer):
    def __init__(self, units, **kwargs):
        super().__init__(**kwargs)
        self.gate_dense = layers.Dense(units, activation="sigmoid")

    def call(self, inputs):
        gate = self.gate_dense(inputs)
        return inputs * gate

    def get_config(self):
        config = super().get_config()
        config.update({
            "units": self.gate_dense.units
        })
        return config


class CustomSparseCategoricalLoss(tf.keras.losses.Loss):
    def __init__(self, name="custom_sparse_categorical_loss"):
        super().__init__(name=name)
        self.base_loss = tf.keras.losses.SparseCategoricalCrossentropy()

    def call(self, y_true, y_pred):
        base_loss = self.base_loss(y_true, y_pred)

        confidence_penalty = tf.reduce_mean(
            tf.reduce_sum(y_pred * tf.math.log(y_pred + 1e-7), axis=1)
        )

        return base_loss + 0.01 * confidence_penalty