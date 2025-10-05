import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

print("Carregando dataset...")
df = pd.read_csv('backend/data/dataset_simulado.csv')

print("Preparando dados...")
X = df.drop('perfil_risco', axis=1)
y = df['perfil_risco']

print("Dividindo treino/teste...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Normalizando...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Treinando rede neural...")
model = MLPClassifier(hidden_layer_sizes=(10, 5), max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)

print("Testando...")
pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, pred)

print(f"Acurácia: {accuracy:.3f}")
print("Teste concluído!")