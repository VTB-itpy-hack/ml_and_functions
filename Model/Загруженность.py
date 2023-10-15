import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

# Загрузка данных
data_path = 'Офисы.csv'
data = pd.read_csv(data_path)

# Замена NaN на медианные значения
data.fillna(data.median(), inplace=True)

# Создание синтетической целевой переменной на основе расстояния до метро
data['synthetic_load'] = 1 / (data['distance'] + 1)

# Выборка признаков
features = ['address', 'salePointCode', 'openHours__days', 'openHours__hours',
            'openHoursIndividual__days', 'openHoursIndividual__hours',
            'officeType', 'salePointFormat', 'latitude', 'longitude', 'metroStation']
X = pd.get_dummies(data[features])  # Преобразование категориальных переменных
y = data['synthetic_load']

# Удаление столбцов, содержащих бесконечные значения
X = X.replace([np.inf, -np.inf], np.nan)
X = X.dropna(axis=1, how='any')

# Разбиение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание и обучение модели
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Предсказание
y_pred = model.predict(X_test)

# Вывод результатов
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Визуализация реальных и предсказанных значений
plt.figure(figsize=(10, 6))
plt.plot(y_test.values, label="Actual")
plt.plot(y_pred, label="Predicted")
plt.title("Actual vs. Predicted Load")
plt.legend()
plt.show()
