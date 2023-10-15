import pandas as pd
from keras.models import Model
from keras.layers import Input, Dense, Embedding, Flatten, Concatenate
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

data = pd.read_csv('Офисы.csv')

categorical_vars = ['address', 'salePointCode', 'status', 'openHours__days', 'openHours__hours',
                    'rko', 'network', 'openHoursIndividual__days', 'openHoursIndividual__hours',
                    'salePointFormat', 'suoAvailability', 'hasRamp', 'metroStation', 'kep', 'myBranch']

numeric_vars = ['latitude', 'longitude', 'distance']

label_encoders = {}
for col in categorical_vars:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col].astype(str))
    label_encoders[col] = le

scaler = StandardScaler()
data[numeric_vars] = scaler.fit_transform(data[numeric_vars])

inputs = []
concat_layers = []

for col in categorical_vars:
    num_unique_values = int(data[col].nunique())
    embed_dim = int(min(np.ceil(num_unique_values/2), 50))
    inp = Input(shape=(1,))
    embed = Embedding(num_unique_values + 1, embed_dim)(inp)
    flat = Flatten()(embed)
    inputs.append(inp)
    concat_layers.append(flat)

numeric_input = Input(shape=(len(numeric_vars),))
inputs.append(numeric_input)
concat_layers.append(numeric_input)

concat = Concatenate()(concat_layers)
dense1 = Dense(128, activation='relu')(concat)
dense2 = Dense(64, activation='relu')(dense1)
output = Dense(data['officeType'].nunique(), activation='softmax')(dense2)

model = Model(inputs=inputs, outputs=output)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

X = [data[col] for col in categorical_vars] + [data[numeric_vars]]
y = data['officeType']

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

model.fit(X_train, y_train, epochs=10, batch_size=64, validation_data=(X_val, y_val))
