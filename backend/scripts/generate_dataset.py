import pandas as pd
import numpy as np
import random

# Definir as 15 features de entrada
features = [
   'idade',
   'renda_mensal', 
   'dependentes',
   'estado_civil',  # 0=solteiro, 1=casado, 2=divorciado
   'valor_investir_mensal',
   'experiencia_anos',
   'patrimonio_atual',
   'dividas_percentual',
   'tolerancia_perda_1',  # escala 1-10
   'tolerancia_perda_2',  # escala 1-10
   'objetivo_prazo',  # 1=curto, 2=médio, 3=longo
   'conhecimento_mercado',  # escala 1-10
   'estabilidade_emprego',  # escala 1-10
   'reserva_emergencia',  # 0=não tem, 1=tem
   'planos_grandes_gastos'  # 0=não, 1=sim
]

def generate_dataset(n_samples=300):
   data = []
   
   for i in range(n_samples):
       # Gerar dados realistas para jovens 18-25 anos
       idade = random.randint(18, 25)
       renda_mensal = random.choice([
           random.randint(1000, 2000),   # 30% baixa renda
           random.randint(2000, 4000),   # 50% média renda  
           random.randint(4000, 8000)    # 20% alta renda
       ])
       
       dependentes = random.choices([0, 1, 2], weights=[70, 25, 5])[0]
       estado_civil = random.choices([0, 1, 2], weights=[80, 15, 5])[0]
       
       # Percentual da renda para investir (mais conservador para menor renda)
       if renda_mensal < 2000:
           percentual_invest = random.uniform(0.05, 0.15)
       elif renda_mensal < 4000:
           percentual_invest = random.uniform(0.10, 0.25)
       else:
           percentual_invest = random.uniform(0.15, 0.35)
           
       valor_investir_mensal = renda_mensal * percentual_invest
       
       experiencia_anos = random.choices([0, 1, 2, 3, 4, 5], weights=[40, 25, 15, 10, 7, 3])[0]
       
       # Patrimônio proporcional à idade e renda
       patrimonio_atual = (idade - 18) * renda_mensal * random.uniform(0.5, 2.0)
       
       dividas_percentual = random.uniform(0, 50)
       
       # Tolerância ao risco correlacionada com idade, experiência e renda
       base_tolerance = (idade - 18) * 0.5 + experiencia_anos * 0.8 + (renda_mensal / 1000) * 0.3
       tolerancia_perda_1 = min(10, max(1, int(base_tolerance + random.gauss(0, 1.5))))
       tolerancia_perda_2 = min(10, max(1, tolerancia_perda_1 + random.randint(-2, 2)))
       
       objetivo_prazo = random.choices([1, 2, 3], weights=[20, 30, 50])[0]
       
       conhecimento_mercado = min(10, max(1, experiencia_anos * 2 + random.randint(1, 4)))
       
       estabilidade_emprego = random.randint(4, 10)
       reserva_emergencia = random.choices([0, 1], weights=[60, 40])[0]
       planos_grandes_gastos = random.choices([0, 1], weights=[70, 30])[0]
       
       # CLASSIFICAÇÃO BASEADA EM REGRAS
       # Calcular score de risco (0-100)
       risk_score = 0
       
       # Idade (maior = mais risco)
       risk_score += (idade - 18) * 3
       
       # Renda (maior = mais risco)
       risk_score += min(25, (renda_mensal / 200))
       
       # Tolerância (média das duas perguntas)
       avg_tolerance = (tolerancia_perda_1 + tolerancia_perda_2) / 2
       risk_score += avg_tolerance * 2.5
       
       # Experiência
       risk_score += experiencia_anos * 3
       
       # Objetivo prazo (longo = mais risco)
       risk_score += objetivo_prazo * 5
       
       # Conhecimento
       risk_score += conhecimento_mercado * 2
       
       # Fatores que reduzem risco
       if dependentes > 0:
           risk_score -= 10
       if reserva_emergencia == 0:
           risk_score -= 8
       if dividas_percentual > 30:
           risk_score -= 5
       if planos_grandes_gastos == 1:
           risk_score -= 5
           
       # Classificação final
       if risk_score < 35:
           perfil = 'conservador'
       elif risk_score < 65:
           perfil = 'moderado'
       else:
           perfil = 'agressivo'
           
       # Adicionar alguma aleatoriedade (10% de chance de mudança)
       if random.random() < 0.1:
           profiles = ['conservador', 'moderado', 'agressivo']
           perfil = random.choice(profiles)
       
       record = [
           idade, renda_mensal, dependentes, estado_civil,
           round(valor_investir_mensal, 2), experiencia_anos,
           round(patrimonio_atual, 2), round(dividas_percentual, 1),
           tolerancia_perda_1, tolerancia_perda_2, objetivo_prazo,
           conhecimento_mercado, estabilidade_emprego,
           reserva_emergencia, planos_grandes_gastos, perfil
       ]
       
       data.append(record)
   
   # Criar DataFrame
   columns = features + ['perfil_risco']
   df = pd.DataFrame(data, columns=columns)
   
   return df

# Criar pasta se não existir
import os
os.makedirs('backend/data', exist_ok=True)

# Gerar dataset
dataset = generate_dataset(300)

# Verificar distribuição dos perfis
print("Distribuição dos perfis:")
print(dataset['perfil_risco'].value_counts())
print(f"\nTotal de registros: {len(dataset)}")

# Salvar em CSV
dataset.to_csv('backend/data/dataset_simulado.csv', index=False)
print("\nDataset salvo em: backend/data/dataset_simulado.csv")

# Mostrar alguns exemplos
print("\nPrimeiros 5 registros:")
print(dataset.head())