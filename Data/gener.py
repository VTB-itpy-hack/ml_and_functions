import pandas as pd
import random

# Количество пользователей и отделений
num_users = 1000
num_salePoints = 100

# Генерация данных
data = {
    'user_id': [random.randint(1, num_users) for _ in range(5000)],  # Предположим, у нас будет 5000 взаимодействий
    'salePointCode': [random.randint(1, num_salePoints) for _ in range(5000)],
    'user_type': [random.randint(0, 1) for _ in range(5000)],  # 0 для физ. лиц и 1 для юр. лиц
    'rating': [random.randint(0, 1) for _ in range(5000)]  # 1 для лайка и 0 для дизлайка
}

# Создание DataFrame
df = pd.DataFrame(data)

# Сохранение данных в CSV
df.to_csv('interactions.csv', index=False)
