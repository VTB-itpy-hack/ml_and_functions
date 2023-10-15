import numpy as np
import pandas as pd
from keras.models import Model
from keras.layers import Input, Embedding, Flatten, Concatenate, Dense
import matplotlib.pyplot as plt

data = pd.read_csv('Офисы.csv')
interactions = pd.read_csv('interactions.csv')

# Кодирование категориальных переменных
user_ids = interactions['user_id'].unique()
salePoint_ids = data['salePointCode'].unique()

num_users = len(user_ids)
num_salePoints = len(salePoint_ids)

user2user_encoded = {x: i for i, x in enumerate(user_ids)}
user_encoded2user = {i: x for i, x in enumerate(user_ids)}
salePoint2salePoint_encoded = {x: i for i, x in enumerate(salePoint_ids)}
salePoint_encoded2salePoint = {i: x for i, x in enumerate(salePoint_ids)}

interactions['user'] = interactions['user_id'].map(user2user_encoded)
interactions['salePoint'] = interactions['salePointCode'].map(salePoint2salePoint_encoded)

# Создание модели
user_input = Input(shape=(1,))
user_embedded = Embedding(num_users, 10)(user_input)
user_flattened = Flatten()(user_embedded)

salePoint_input = Input(shape=(1,))
salePoint_embedded = Embedding(num_salePoints, 10)(salePoint_input)
salePoint_flattened = Flatten()(salePoint_embedded)

user_type_input = Input(shape=(1,))

concat_layer = Concatenate()([user_flattened, salePoint_flattened, user_type_input])

dense1 = Dense(128, activation='relu')(concat_layer)
dense2 = Dense(64, activation='relu')(dense1)
output = Dense(1, activation='sigmoid')(dense2)  # Sigmoid, так как наша задача бинарной классификации

model = Model(inputs=[user_input, salePoint_input, user_type_input], outputs=output)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Обучение модели
X_users = interactions['user'].values
X_salePoints = interactions['salePoint'].values
X_user_types = interactions['user_type'].values
y = interactions['rating'].values

model.fit([X_users, X_salePoints, X_user_types], y, epochs=5, batch_size=64, validation_split=0.2)

history = model.fit([X_users, X_salePoints, X_user_types], y, epochs=5, batch_size=64, validation_split=0.2)

# Визуализация функции потерь
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.title('Loss Evolution')

# Визуализация точности
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.title('Accuracy Evolution')

plt.tight_layout()
plt.show()
