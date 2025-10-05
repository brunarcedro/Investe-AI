import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import os

class RiskProfileClassifier:
   def __init__(self):
       self.model = MLPClassifier( # A rede neural
           hidden_layer_sizes=(10, 5),
           activation='relu',
           solver='adam',
           max_iter=1000,
           random_state=42
       )
       self.scaler = StandardScaler() # Normalizador de dados
       self.is_trained = False  # Status de treinamento
       
   def load_dataset(self, filepath='../data/dataset_simulado.csv'):
       """Carrega o dataset e separa features do target"""
       print("Carregando dataset...")
       # Tenta múltiplos caminhos possíveis
       import os
       possible_paths = [
           filepath,
           'data/dataset_simulado.csv',
           '../data/dataset_simulado.csv',
           'backend/data/dataset_simulado.csv'
       ]

       df = None
       for path in possible_paths:
           if os.path.exists(path):
               df = pd.read_csv(path)
               print(f"Dataset carregado de: {path}")
               break

       if df is None:
           raise FileNotFoundError(f"Dataset não encontrado. Tentou: {possible_paths}")
       
       # Separar features (X) e target (y)
       X = df.drop('perfil_risco', axis=1)
       y = df['perfil_risco']
       
       print(f"Dataset carregado: {len(df)} registros")
       print(f"Features: {list(X.columns)}")
       print(f"Distribuição das classes:")
       print(y.value_counts())
       
       return X, y
   
   def train(self, X, y, test_size=0.2):
       """Treina a rede neural"""
       print("\nDividindo dados em treino e teste...")
       # Dividir dados em treino e teste
       X_train, X_test, y_train, y_test = train_test_split(
           X, y, test_size=test_size, random_state=42, stratify=y
       )
       
       print("Normalizando dados...")
       # Normalizar dados
       X_train_scaled = self.scaler.fit_transform(X_train)
       X_test_scaled = self.scaler.transform(X_test)
       
       # Treinar modelo
       print("Treinando rede neural...")
       self.model.fit(X_train_scaled, y_train)
       
       # Avaliar performance
       print("Avaliando performance...")
       train_pred = self.model.predict(X_train_scaled)
       test_pred = self.model.predict(X_test_scaled)
       
       train_accuracy = accuracy_score(y_train, train_pred)
       test_accuracy = accuracy_score(y_test, test_pred)
       
       print(f"\n=== RESULTADOS DO TREINAMENTO ===")
       print(f"Acurácia no treino: {train_accuracy:.3f}")
       print(f"Acurácia no teste: {test_accuracy:.3f}")
       
       # Relatório detalhado
       print(f"\n=== RELATÓRIO DE CLASSIFICAÇÃO ===")
       print(classification_report(y_test, test_pred))
       
       # Matriz de confusão
       print(f"\n=== MATRIZ DE CONFUSÃO ===")
       cm = confusion_matrix(y_test, test_pred)
       print(cm)
       
       self.is_trained = True
       return train_accuracy, test_accuracy

   def save_model(self, filepath='neural_network.pkl'):
       """Salva o modelo treinado"""
       import joblib
       if not self.is_trained:
           raise ValueError("Modelo não foi treinado ainda!")

       joblib.dump({
           'model': self.model,
           'scaler': self.scaler,
           'is_trained': self.is_trained
       }, filepath)
       print(f"\nModelo salvo em: {filepath}")

   def load_model(self, filepath='neural_network.pkl'):
       """Carrega um modelo treinado"""
       import joblib
       import os

       if not os.path.exists(filepath):
           raise FileNotFoundError(f"Modelo não encontrado: {filepath}")

       data = joblib.load(filepath)
       self.model = data['model']
       self.scaler = data['scaler']
       self.is_trained = data['is_trained']
       print(f"Modelo carregado de: {filepath}")
   
   def predict(self, user_data):
       """Classifica um novo usuário"""
       if not self.is_trained:
           raise ValueError("Modelo não foi treinado ainda!")
       
       # Normalizar dados
       user_scaled = self.scaler.transform([user_data])
       
       # Predição
       prediction = self.model.predict(user_scaled)[0]
       probabilities = self.model.predict_proba(user_scaled)[0]
       
       # Mapear probabilidades para classes
       classes = self.model.classes_
       prob_dict = dict(zip(classes, probabilities))
       
       return {
           'perfil_previsto': prediction,
           'confianca': max(probabilities),
           'probabilidades': prob_dict
       }

def test_classifier():
   """Função para testar a rede neural"""
   print("=== TESTE DA REDE NEURAL ===")
   
   # Inicializar classificador
   print("Inicializando classificador...")
   classifier = RiskProfileClassifier()
   
   # Carregar dados
   print("Carregando dados...")
   X, y = classifier.load_dataset()
   
   # Treinar modelo
   print("Iniciando treinamento...")
   train_acc, test_acc = classifier.train(X, y)
   
   # Testar com exemplos
   print("\n=== TESTE COM EXEMPLOS ===")
   
   # Exemplo 1: Perfil conservador (jovem, baixa renda, conservador)
   print("\nTeste 1 - Perfil Conservador:")
   exemplo_conservador = [20, 1500, 1, 0, 150, 0, 2000, 30, 3, 4, 1, 2, 6, 0, 1]
   resultado = classifier.predict(exemplo_conservador)
   print(f"Resultado: {resultado}")
   
   # Exemplo 2: Perfil agressivo (jovem, alta renda, experiente)
   print("\nTeste 2 - Perfil Agressivo:")
   exemplo_agressivo = [24, 6000, 0, 0, 1800, 3, 15000, 10, 9, 8, 3, 8, 9, 1, 0]
   resultado = classifier.predict(exemplo_agressivo)
   print(f"Resultado: {resultado}")
   
   # Exemplo 3: Perfil moderado
   print("\nTeste 3 - Perfil Moderado:")
   exemplo_moderado = [22, 3500, 0, 0, 700, 1, 8000, 20, 6, 5, 2, 5, 7, 1, 0]
   resultado = classifier.predict(exemplo_moderado)
   print(f"Resultado: {resultado}")
   
   print(f"\n=== TESTE CONCLUÍDO ===")
   print(f"Acurácia final: {test_acc:.3f}")

   # Salvar modelo
   print("\n=== SALVANDO MODELO ===")
   classifier.save_model('neural_network.pkl')

   return classifier

if __name__ == "__main__":
   print("Iniciando teste da rede neural...")
   classifier = test_classifier()
   print("\nTeste finalizado com sucesso!")
   print("Modelo salvo e pronto para uso!")