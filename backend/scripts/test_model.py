"""
Script para testar o modelo otimizado (84.13% accuracy)
Compara com modelo anterior e testa casos reais
"""

import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class ModeloOtimizadoTester:
    """Testa modelo otimizado"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.models_dir = self.project_root / 'models'

        # Carregar modelos
        self.modelo_otimizado = None
        self.modelo_anterior = None
        self.load_models()

    def load_models(self):
        """Carrega modelos otimizado e anterior"""
        print("="*70)
        print("CARREGANDO MODELOS")
        print("="*70)

        # Modelo otimizado
        try:
            path = self.models_dir / 'neural_network_otimizado.pkl'
            data = joblib.load(path)
            self.modelo_otimizado = {
                'model': data['model'],
                'scaler': data['scaler'],
                'label_encoder': data['label_encoder'],
                'type': data.get('model_type', 'unknown'),
                'accuracy': data.get('test_accuracy', 0)
            }
            print(f"\nModelo OTIMIZADO carregado:")
            print(f"  Tipo: {self.modelo_otimizado['type']}")
            print(f"  Accuracy: {self.modelo_otimizado['accuracy']:.4f}")
        except Exception as e:
            print(f"\nERRO ao carregar modelo otimizado: {e}")

        # Modelo anterior (híbrido)
        try:
            path = self.models_dir / 'neural_network_hibrido.pkl'
            data = joblib.load(path)
            self.modelo_anterior = {
                'model': data['model'],
                'label_encoder': data['label_encoder']
            }
            print(f"\nModelo ANTERIOR (hibrido) carregado")
        except Exception as e:
            print(f"\nModelo anterior nao encontrado: {e}")

    def create_features(self, dados):
        """
        Cria as 23 features (15 basicas + 8 derivadas)
        igual ao modelo de treino
        """
        features = {}

        # 15 features basicas
        features['idade'] = dados['idade']
        features['renda_mensal'] = dados['renda_mensal']
        features['dependentes'] = dados.get('dependentes', 0)
        features['estado_civil'] = dados.get('estado_civil', 0)
        features['valor_investir_mensal'] = dados.get('valor_investir_mensal', 0)
        features['experiencia_anos'] = dados.get('experiencia_anos', 0)
        features['patrimonio_atual'] = dados.get('patrimonio_atual', 0)
        features['dividas_percentual'] = dados.get('dividas_percentual', 0)
        features['tolerancia_perda_1'] = dados.get('tolerancia_perda_1', 5)
        features['tolerancia_perda_2'] = dados.get('tolerancia_perda_2', 5)
        features['horizonte_investimento'] = dados.get('horizonte_investimento', 10)
        features['conhecimento_mercado'] = dados.get('conhecimento_mercado', 5)
        features['estabilidade_emprego'] = dados.get('estabilidade_emprego', 5)
        features['tem_reserva_emergencia'] = dados.get('tem_reserva_emergencia', 0)
        features['planos_grandes_gastos'] = dados.get('planos_grandes_gastos', 0)

        # 8 features derivadas (IMPORTANTE: mesmas do treino!)
        features['renda_por_dependente'] = features['renda_mensal'] / (features['dependentes'] + 1)
        features['patrimonio_sobre_renda'] = features['patrimonio_atual'] / (features['renda_mensal'] * 12 + 1)
        features['taxa_poupanca'] = features['valor_investir_mensal'] / (features['renda_mensal'] + 1)
        features['tolerancia_media'] = (features['tolerancia_perda_1'] + features['tolerancia_perda_2']) / 2
        features['tolerancia_diff'] = abs(features['tolerancia_perda_1'] - features['tolerancia_perda_2'])
        features['experiencia_relativa'] = features['experiencia_anos'] / (features['idade'] - 17 + 1)
        features['expertise_score'] = (features['conhecimento_mercado'] + features['experiencia_anos']) / 2
        features['seguranca_financeira'] = int(
            features['tem_reserva_emergencia'] == 1 and features['estabilidade_emprego'] >= 7
        )

        # Ordem das features (CRÍTICO: mesma ordem do treino!)
        feature_order = [
            'idade', 'renda_mensal', 'dependentes', 'estado_civil',
            'valor_investir_mensal', 'experiencia_anos', 'patrimonio_atual',
            'dividas_percentual', 'tolerancia_perda_1', 'tolerancia_perda_2',
            'horizonte_investimento', 'conhecimento_mercado',
            'estabilidade_emprego', 'tem_reserva_emergencia',
            'planos_grandes_gastos',
            'renda_por_dependente', 'patrimonio_sobre_renda', 'taxa_poupanca',
            'tolerancia_media', 'tolerancia_diff', 'experiencia_relativa',
            'expertise_score', 'seguranca_financeira'
        ]

        return [features[f] for f in feature_order]

    def predict(self, dados):
        """Faz predicao com modelo otimizado"""
        if not self.modelo_otimizado:
            print("Modelo otimizado nao carregado!")
            return None

        # Criar features
        features = self.create_features(dados)

        # Normalizar
        features_scaled = self.modelo_otimizado['scaler'].transform([features])

        # Predizer
        pred_encoded = self.modelo_otimizado['model'].predict(features_scaled)[0]

        # Probabilidades (se disponível)
        try:
            probs = self.modelo_otimizado['model'].predict_proba(features_scaled)[0]
            confidence = probs.max()
        except:
            confidence = 1.0

        # Decodificar
        perfil = self.modelo_otimizado['label_encoder'].inverse_transform([pred_encoded])[0]

        return {
            'perfil': perfil,
            'confidence': confidence,
            'features_count': len(features)
        }

    def compare_predictions(self, dados):
        """Compara predicoes entre modelos"""
        print("\n" + "="*70)
        print("COMPARANDO PREDICOES")
        print("="*70)

        # Otimizado
        pred_otimizado = self.predict(dados)

        print(f"\nModelo OTIMIZADO:")
        if pred_otimizado:
            print(f"  Perfil: {pred_otimizado['perfil'].capitalize()}")
            print(f"  Confianca: {pred_otimizado['confidence']:.2%}")
            print(f"  Features: {pred_otimizado['features_count']}")
        else:
            print("  Nao disponivel")

        # Anterior (se disponível)
        if self.modelo_anterior:
            # Para modelo anterior, usar apenas 15 features basicas
            features_basicas = self.create_features(dados)[:15]
            pred_encoded = self.modelo_anterior['model'].predict([features_basicas])[0]
            perfil_anterior = self.modelo_anterior['label_encoder'].inverse_transform([pred_encoded])[0]

            print(f"\nModelo ANTERIOR (hibrido):")
            print(f"  Perfil: {perfil_anterior.capitalize()}")
            print(f"  Features: 15")

            if pred_otimizado:
                if pred_otimizado['perfil'] == perfil_anterior:
                    print(f"\n  CONCORDAM: Ambos classificaram como {perfil_anterior.capitalize()}")
                else:
                    print(f"\n  DISCORDAM:")
                    print(f"    Otimizado: {pred_otimizado['perfil'].capitalize()}")
                    print(f"    Anterior:  {perfil_anterior.capitalize()}")

    def test_casos_reais(self):
        """Testa com casos de uso reais"""
        print("\n" + "="*70)
        print("TESTANDO CASOS REAIS")
        print("="*70)

        casos = {
            "Jovem Conservador": {
                'idade': 22,
                'renda_mensal': 3000,
                'dependentes': 0,
                'estado_civil': 0,
                'valor_investir_mensal': 300,
                'experiencia_anos': 1,
                'patrimonio_atual': 5000,
                'dividas_percentual': 10,
                'tolerancia_perda_1': 3,
                'tolerancia_perda_2': 2,
                'horizonte_investimento': 30,
                'conhecimento_mercado': 3,
                'estabilidade_emprego': 6,
                'tem_reserva_emergencia': 1,
                'planos_grandes_gastos': 0
            },

            "Jovem Agressivo": {
                'idade': 25,
                'renda_mensal': 8000,
                'dependentes': 0,
                'estado_civil': 0,
                'valor_investir_mensal': 2000,
                'experiencia_anos': 5,
                'patrimonio_atual': 50000,
                'dividas_percentual': 5,
                'tolerancia_perda_1': 9,
                'tolerancia_perda_2': 8,
                'horizonte_investimento': 35,
                'conhecimento_mercado': 8,
                'estabilidade_emprego': 8,
                'tem_reserva_emergencia': 1,
                'planos_grandes_gastos': 0
            },

            "Adulto Moderado": {
                'idade': 40,
                'renda_mensal': 10000,
                'dependentes': 2,
                'estado_civil': 1,
                'valor_investir_mensal': 1500,
                'experiencia_anos': 10,
                'patrimonio_atual': 200000,
                'dividas_percentual': 30,
                'tolerancia_perda_1': 6,
                'tolerancia_perda_2': 5,
                'horizonte_investimento': 20,
                'conhecimento_mercado': 6,
                'estabilidade_emprego': 7,
                'tem_reserva_emergencia': 1,
                'planos_grandes_gastos': 1
            },

            "Senior Conservador": {
                'idade': 60,
                'renda_mensal': 15000,
                'dependentes': 0,
                'estado_civil': 1,
                'valor_investir_mensal': 3000,
                'experiencia_anos': 25,
                'patrimonio_atual': 800000,
                'dividas_percentual': 0,
                'tolerancia_perda_1': 2,
                'tolerancia_perda_2': 3,
                'horizonte_investimento': 5,
                'conhecimento_mercado': 7,
                'estabilidade_emprego': 9,
                'tem_reserva_emergencia': 1,
                'planos_grandes_gastos': 0
            },

            "Iniciante sem reserva": {
                'idade': 20,
                'renda_mensal': 2000,
                'dependentes': 0,
                'estado_civil': 0,
                'valor_investir_mensal': 200,
                'experiencia_anos': 0,
                'patrimonio_atual': 1000,
                'dividas_percentual': 50,
                'tolerancia_perda_1': 4,
                'tolerancia_perda_2': 4,
                'horizonte_investimento': 40,
                'conhecimento_mercado': 2,
                'estabilidade_emprego': 4,
                'tem_reserva_emergencia': 0,
                'planos_grandes_gastos': 1
            }
        }

        for nome, dados in casos.items():
            print(f"\n{'-'*70}")
            print(f"CASO: {nome}")
            print(f"{'-'*70}")
            print(f"Idade: {dados['idade']}, Renda: R${dados['renda_mensal']:,.2f}, "
                  f"Tolerancia: {dados['tolerancia_perda_1']}/10")

            resultado = self.predict(dados)

            if resultado:
                print(f"\nRESULTADO:")
                print(f"  Perfil: {resultado['perfil'].upper()}")
                print(f"  Confianca: {resultado['confidence']:.1%}")

                # Validar se faz sentido
                esperado = nome.split()[1].lower()
                if esperado in resultado['perfil'].lower():
                    print(f"  VALIDACAO: OK (esperado {esperado})")
                else:
                    print(f"  VALIDACAO: Esperado {esperado}, obteve {resultado['perfil']}")

    def test_edge_cases(self):
        """Testa casos extremos"""
        print("\n" + "="*70)
        print("TESTANDO CASOS EXTREMOS")
        print("="*70)

        casos_extremos = {
            "Milionario Jovem": {
                'idade': 23,
                'renda_mensal': 50000,
                'patrimonio_atual': 5000000,
                'tolerancia_perda_1': 10,
                'tolerancia_perda_2': 10,
                'conhecimento_mercado': 9,
                'experiencia_anos': 3
            },

            "Aposentado Rico": {
                'idade': 70,
                'renda_mensal': 20000,
                'patrimonio_atual': 2000000,
                'tolerancia_perda_1': 1,
                'tolerancia_perda_2': 1,
                'conhecimento_mercado': 10,
                'experiencia_anos': 40
            },

            "Jovem Endividado": {
                'idade': 25,
                'renda_mensal': 3000,
                'patrimonio_atual': -10000,
                'tolerancia_perda_1': 7,
                'tolerancia_perda_2': 8,
                'dividas_percentual': 90,
                'tem_reserva_emergencia': 0
            }
        }

        for nome, dados_parciais in casos_extremos.items():
            # Completar com valores padrão
            dados = {
                'idade': dados_parciais.get('idade', 30),
                'renda_mensal': dados_parciais.get('renda_mensal', 5000),
                'dependentes': dados_parciais.get('dependentes', 0),
                'estado_civil': dados_parciais.get('estado_civil', 0),
                'valor_investir_mensal': dados_parciais.get('renda_mensal', 5000) * 0.2,
                'experiencia_anos': dados_parciais.get('experiencia_anos', 5),
                'patrimonio_atual': dados_parciais.get('patrimonio_atual', 50000),
                'dividas_percentual': dados_parciais.get('dividas_percentual', 20),
                'tolerancia_perda_1': dados_parciais.get('tolerancia_perda_1', 5),
                'tolerancia_perda_2': dados_parciais.get('tolerancia_perda_2', 5),
                'horizonte_investimento': dados_parciais.get('horizonte_investimento', 20),
                'conhecimento_mercado': dados_parciais.get('conhecimento_mercado', 5),
                'estabilidade_emprego': dados_parciais.get('estabilidade_emprego', 7),
                'tem_reserva_emergencia': dados_parciais.get('tem_reserva_emergencia', 1),
                'planos_grandes_gastos': dados_parciais.get('planos_grandes_gastos', 0)
            }

            print(f"\n{nome}:")
            resultado = self.predict(dados)
            if resultado:
                print(f"  Perfil: {resultado['perfil'].upper()}")
                print(f"  Confianca: {resultado['confidence']:.1%}")

    def generate_api_example(self):
        """Gera exemplo de uso na API"""
        print("\n" + "="*70)
        print("EXEMPLO DE INTEGRACAO COM API")
        print("="*70)

        print("""
# Como usar o modelo otimizado na API FastAPI:

from fastapi import FastAPI
import joblib
from pathlib import Path

app = FastAPI()

# Carregar modelo otimizado
modelo_path = Path('models/neural_network_otimizado.pkl')
modelo_data = joblib.load(modelo_path)

model = modelo_data['model']
scaler = modelo_data['scaler']
label_encoder = modelo_data['label_encoder']

@app.post("/classificar-perfil-otimizado")
def classificar_perfil_otimizado(dados: PerfilInvestidor):
    # Criar 23 features (15 basicas + 8 derivadas)
    features = create_features(dados.dict())

    # Normalizar
    features_scaled = scaler.transform([features])

    # Predizer
    pred = model.predict(features_scaled)[0]
    probs = model.predict_proba(features_scaled)[0]

    # Decodificar
    perfil = label_encoder.inverse_transform([pred])[0]
    confidence = probs.max()

    return {
        "perfil": perfil,
        "confidence": confidence,
        "accuracy_modelo": 0.8413  # 84.13%
    }

# Endpoint de teste
@app.get("/modelo-info")
def modelo_info():
    return {
        "modelo": "Neural Network Otimizado",
        "tipo": "MLP (50, 25, 10)",
        "accuracy": 0.8413,
        "features": 23,
        "tecnicas": [
            "Feature Engineering",
            "SMOTE Balanceamento",
            "StandardScaler",
            "Early Stopping",
            "Regularizacao L2"
        ]
    }
""")


def main():
    """Funcao principal"""
    print("="*70)
    print("TESTE DO MODELO OTIMIZADO (84.13% ACCURACY)")
    print("="*70)

    tester = ModeloOtimizadoTester()

    # Testes
    tester.test_casos_reais()
    tester.test_edge_cases()
    tester.generate_api_example()

    print("\n" + "="*70)
    print("TESTE CONCLUIDO!")
    print("="*70)
    print("\nPROXIMO PASSO:")
    print("  Atualizar API para usar modelo otimizado")
    print("  Arquivo: backend/api/main.py")
    print(f"\nModelo disponivel em:")
    print(f"  models/neural_network_otimizado.pkl")
    print(f"  Accuracy: 84.13%")


if __name__ == "__main__":
    main()
