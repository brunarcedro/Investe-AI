print("Iniciando teste...")
import pandas as pd
print("Pandas importado")
import sklearn
print("Sklearn importado")

# Testar carregamento do dataset
df = pd.read_csv('backend/data/dataset_simulado.csv')
print(f"Dataset carregado: {len(df)} linhas")
print("Teste concluído!")