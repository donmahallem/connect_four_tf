from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Input, Dropout, GlobalAveragePooling2D, BatchNormalization, Conv2D, MaxPool2D
import tensorflow as tf


def huber_loss(y_true, y_pred, clip_delta=1.0):
    error = y_true - y_pred
    cond = tf.keras.backend.abs(error) < clip_delta

    squared_loss = 0.5 * tf.keras.backend.square(error)
    linear_loss = clip_delta * (tf.keras.backend.abs(error) - 0.5 * clip_delta)

    return tf.where(cond, squared_loss, linear_loss)


'''
 ' Same as above but returns the mean loss.
'''


def huber_loss_mean(y_true, y_pred, clip_delta=1.0):
    return tf.keras.backend.mean(huber_loss(y_true, y_pred, clip_delta))


class QNet:
    def __init__(self):
        inputs = Input(shape=(6, 7, 1))
        x = Conv2D(128, (2, 3))(inputs)
        #x = MaxPool2D(3)(x)
        x = BatchNormalization()(x)
        x = Conv2D(256, 3)(x)
        x = GlobalAveragePooling2D()(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.2)(x)
        x = Dense(64, activation='relu')(x)
        x = Dense(7, activation='linear')(x)

        self._model = Model(inputs=inputs, outputs=x)
        self._model.compile('rmsprop', tf.losses.huber_loss)

    def getModel(self):
        return self._model

    def fit(self, data, epochs=1):
        train_data = data.reshape(
            (data.shape[0], data.shape[1], data.shape[2], 1))
        self._model.fit(train_data, epochs=epochs, batch_size=64)

    def predict(self, data):
        train_data = data.reshape(
            (data.shape[0], data.shape[1], data.shape[2], 1))
        return self._model.predict(train_data)
