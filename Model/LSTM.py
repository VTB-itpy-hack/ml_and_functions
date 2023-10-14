import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# Загрузка и подготовка данных
data = pd.read_csv('Офисы.csv')
timeseries = data['rko'].values.reshape(-1, 1)

scaler = MinMaxScaler(feature_range=(0,1))
timeseries_scaled = scaler.fit_transform(timeseries)

X, y = [], []
for i in range(60, len(timeseries_scaled)-1):
    X.append(timeseries_scaled[i-60:i, 0])
    y.append(timeseries_scaled[i, 0])
X, y = np.array(X), np.array(y)

X = np.reshape(X, (X.shape[0], X.shape[1], 1))

# Создание модели LSTM
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)))
model.add(LSTM(units=50))
model.add(Dense(units=1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X, y, epochs=100, batch_size=32)

# Прогнозирование
inputs = timeseries_scaled[-60:]
inputs = inputs.reshape(-1,1)
inputs = scaler.transform(inputs)

X_test = []
for i in range(60, 70):
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

predicted = model.predict(X_test)
predicted = scaler.inverse_transform(predicted)

plt.plot(timeseries)
plt.plot(range(len(timeseries), len(timeseries)+10), predicted)
plt.show()
