"""
Script de ETL (Extract, Transform, Load) para converter dados do SCF
para o formato das 15 features do modelo de classificação de perfil de risco

Mapeamento SCF -> Features do Modelo:
------------------------------------
SCF Variable       -> Model Feature              -> Transformação
AGE                -> idade                      -> Direto
INCOME             -> renda_mensal               -> INCOME / 12 (anual -> mensal)
KIDS               -> dependentes                -> Direto
MARRIED            -> estado_civil               -> 1=married->1, 2=single->0, 3=divorced->2
INCOME * 0.15      -> valor_investir_mensal      -> 10-20% da renda mensal
AGE - 18           -> experiencia_anos           -> Proxy: (idade-18) * conhecimento_fator
NETWORTH           -> patrimonio_atual           -> Direto
DEBT/ASSET         -> dividas_percentual         -> (DEBT / ASSET) * 100
RISK               -> tolerancia_perda_1         -> Escala 1-4 -> 1-10
RISK               -> tolerancia_perda_2         -> Variação de tolerancia_perda_1
AGE-based          -> horizonte_investimento     -> Função de idade (jovem = mais anos)
EDUC               -> conhecimento_mercado       -> 1-4 -> 1-10 scale
OCCAT              -> estabilidade_emprego       -> Baseado em ocupação
LIQ > threshold    -> tem_reserva_emergencia     -> Boolean (LIQ >= 6 meses renda)
KIDS > 0 or...     -> planos_grandes_gastos      -> Heurística baseada em dependentes
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class SCFToFeaturesETL:
    """ETL para converter dados SCF para as 15 features do modelo"""

    def __init__(self, scf_file='scf_simulated_data.csv'):
        self.data_dir = Path(__file__).parent
        self.scf_file = self.data_dir / scf_file
        self.output_file = self.data_dir / 'dataset_from_scf.csv'

    def extract(self):
        """Carrega dados SCF"""
        print("="*70)
        print("STEP 1: EXTRACT - Carregando dados SCF")
        print("="*70)

        if not self.scf_file.exists():
            raise FileNotFoundError(f"Arquivo SCF não encontrado: {self.scf_file}")

        df = pd.read_csv(self.scf_file)
        print(f"Dataset SCF carregado: {len(df)} registros, {len(df.columns)} colunas")
        print(f"Colunas: {list(df.columns)}")

        return df

    def transform(self, df_scf):
        """
        Transforma dados SCF para as 15 features do modelo

        15 Features esperadas:
        1. idade
        2. renda_mensal
        3. dependentes
        4. estado_civil
        5. valor_investir_mensal
        6. experiencia_anos
        7. patrimonio_atual / patrimonio_total
        8. dividas_percentual
        9. tolerancia_perda_1
        10. tolerancia_perda_2
        11. objetivo_prazo / horizonte_investimento
        12. conhecimento_mercado
        13. estabilidade_emprego
        14. tem_reserva_emergencia
        15. planos_grandes_gastos
        """
        print("\n" + "="*70)
        print("STEP 2: TRANSFORM - Convertendo para 15 features do modelo")
        print("="*70)

        df_transformed = pd.DataFrame()

        # 1. IDADE - Direto do SCF
        df_transformed['idade'] = df_scf['AGE'].astype(int)
        print("1. idade: Copiado de AGE")

        # 2. RENDA MENSAL - Income anual / 12
        df_transformed['renda_mensal'] = (df_scf['INCOME'] / 12).round(2)
        print("2. renda_mensal: INCOME / 12 (convertido de anual para mensal)")

        # 3. DEPENDENTES - Direto do KIDS
        df_transformed['dependentes'] = df_scf['KIDS'].astype(int)
        print("3. dependentes: Copiado de KIDS")

        # 4. ESTADO CIVIL - Mapeamento MARRIED
        # SCF: 1=Married, 2=Single, 3=Divorced, 4=Widowed
        # Modelo: 0=single, 1=married, 2=divorced
        def map_marital_status(married_code):
            mapping = {1: 1, 2: 0, 3: 2, 4: 2}  # Widowed -> divorced
            return mapping.get(married_code, 0)

        df_transformed['estado_civil'] = df_scf['MARRIED'].apply(map_marital_status)
        print("4. estado_civil: MARRIED (1=married, 2=single->0, 3=divorced->2)")

        # 5. VALOR INVESTIR MENSAL - 10-20% da renda mensal
        # Baseado em renda e educação
        investment_rate = 0.10 + (df_scf['EDUC'] / 4) * 0.10  # 10-20%
        df_transformed['valor_investir_mensal'] = (
            df_transformed['renda_mensal'] * investment_rate
        ).round(2)
        print("5. valor_investir_mensal: 10-20% da renda mensal (baseado em educacao)")

        # 6. EXPERIENCIA ANOS - Proxy baseado em idade e educação
        # Assumindo que começa a investir após educação
        education_years = df_scf['EDUC'].map({1: 0, 2: 2, 3: 5, 4: 10})
        df_transformed['experiencia_anos'] = np.maximum(
            0,
            ((df_transformed['idade'] - 25) * (df_scf['EDUC'] / 4)).round(0)
        ).astype(int)
        df_transformed['experiencia_anos'] = np.clip(df_transformed['experiencia_anos'], 0, 40)
        print("6. experiencia_anos: Calculado com base em idade e educacao")

        # 7. PATRIMONIO ATUAL - Networth do SCF
        df_transformed['patrimonio_total'] = df_scf['NETWORTH'].round(2)
        print("7. patrimonio_total: Copiado de NETWORTH")

        # 8. DIVIDAS PERCENTUAL - (DEBT / ASSET) * 100
        # Tratamento de divisão por zero
        df_transformed['dividas_percentual'] = np.where(
            df_scf['ASSET'] > 0,
            np.clip((df_scf['DEBT'] / df_scf['ASSET']) * 100, 0, 100),
            0
        ).round(2)
        print("8. dividas_percentual: (DEBT / ASSET) * 100")

        # 9. TOLERANCIA PERDA 1 - RISK escalado de 1-4 para 1-10
        # SCF RISK: 1=no risk, 2=average, 3=above avg, 4=substantial
        # Escalar para 1-10: 1->2.5, 2->5.0, 3->7.5, 4->10.0
        risk_mapping = {1: 2.5, 2: 5.0, 3: 7.5, 4: 10.0}
        df_transformed['tolerancia_perda_1'] = df_scf['RISK'].map(risk_mapping)
        print("9. tolerancia_perda_1: RISK escalado de 1-4 para escala 1-10")

        # 10. TOLERANCIA PERDA 2 - Variação de tolerancia_perda_1
        # Adicionar pequena variação aleatória para simular diferentes respostas
        noise = np.random.uniform(-0.5, 0.5, len(df_transformed))
        df_transformed['tolerancia_perda_2'] = np.clip(
            df_transformed['tolerancia_perda_1'] + noise,
            1, 10
        ).round(1)
        print("10. tolerancia_perda_2: Variacao de tolerancia_perda_1 com ruido")

        # 11. HORIZONTE INVESTIMENTO - Baseado em idade
        # Jovens: horizonte mais longo | Mais velhos: horizonte mais curto
        # Fórmula: max(5, min(40, 65 - idade))
        df_transformed['horizonte_investimento'] = np.clip(
            65 - df_transformed['idade'],
            5, 40
        ).astype(int)
        print("11. horizonte_investimento: Calculado como 65 - idade (min 5, max 40 anos)")

        # 12. CONHECIMENTO MERCADO - EDUC escalado para 1-10
        # 1=No HS -> 2, 2=HS -> 4, 3=Some college -> 6, 4=College+ -> 8
        educ_to_knowledge = {1: 2, 2: 4, 3: 6, 4: 8}
        base_knowledge = df_scf['EDUC'].map(educ_to_knowledge)
        # Adicionar bônus por experiência e renda de ações
        has_equity = (df_scf['EQUITINC'] > 0).astype(int) * 2
        df_transformed['conhecimento_mercado'] = np.clip(
            base_knowledge + has_equity,
            1, 10
        ).astype(int)
        print("12. conhecimento_mercado: EDUC escalado + bonus por investimentos em acoes")

        # 13. ESTABILIDADE EMPREGO - Baseado em OCCAT e idade
        # OCCAT: 1=Manager, 2=Technical, 3=Service, 4=Not working
        occat_stability = df_scf['OCCAT'].map({1: 8, 2: 7, 3: 5, 4: 2})
        # Ajuste por idade (mais velho = mais estável até certo ponto)
        age_factor = np.where(df_transformed['idade'] < 65,
                              np.clip(df_transformed['idade'] - 20, 0, 30) / 30 * 2,
                              -2)  # Penalidade pós-65
        df_transformed['estabilidade_emprego'] = np.clip(
            occat_stability + age_factor,
            1, 10
        ).round(0).astype(int)
        print("13. estabilidade_emprego: Baseado em OCCAT e idade")

        # 14. TEM RESERVA EMERGENCIA - LIQ >= 6 meses de renda
        emergency_fund_threshold = df_transformed['renda_mensal'] * 6
        df_transformed['tem_reserva_emergencia'] = (
            df_scf['LIQ'] >= emergency_fund_threshold
        ).astype(int)
        pct_with_emergency = df_transformed['tem_reserva_emergencia'].mean() * 100
        print(f"14. tem_reserva_emergencia: LIQ >= 6 meses renda ({pct_with_emergency:.1f}% tem reserva)")

        # 15. PLANOS GRANDES GASTOS - Heurística
        # Tem filhos pequenos, ou vai comprar casa, ou se aproxima da aposentadoria
        has_young_kids = df_scf['KIDS'] > 0
        close_to_retirement = (df_transformed['idade'] >= 55) & (df_transformed['idade'] < 70)
        low_networth_high_income = (df_scf['NETWORTH'] < df_scf['INCOME']) & (df_scf['INCOME'] > 50000)

        df_transformed['planos_grandes_gastos'] = (
            has_young_kids | close_to_retirement | low_networth_high_income
        ).astype(int)
        pct_with_plans = df_transformed['planos_grandes_gastos'].mean() * 100
        print(f"15. planos_grandes_gastos: Heuristica baseada em filhos/aposentadoria ({pct_with_plans:.1f}%)")

        print(f"\nTransformacao completa: {len(df_transformed)} registros, {len(df_transformed.columns)} features")

        return df_transformed

    def add_risk_classification(self, df):
        """
        Adiciona coluna de classificação de perfil de risco
        usando a mesma lógica do generate_dataset.py original
        """
        print("\n" + "="*70)
        print("STEP 3: Adicionando classificacao de perfil de risco")
        print("="*70)

        def classificar_perfil(row):
            """Lógica de classificação de perfil"""
            score = 0

            # Idade (peso: 1.0)
            if row['idade'] < 30:
                score += 3
            elif row['idade'] < 50:
                score += 2
            else:
                score += 1

            # Renda (peso: 1.5)
            if row['renda_mensal'] > 15000:
                score += 4.5
            elif row['renda_mensal'] > 7000:
                score += 3
            elif row['renda_mensal'] > 3000:
                score += 1.5

            # Dependentes (peso: -0.5)
            score -= row['dependentes'] * 0.5

            # Tolerância a risco (peso: 2.0)
            score += (row['tolerancia_perda_1'] / 10) * 6
            score += (row['tolerancia_perda_2'] / 10) * 6

            # Horizonte de investimento (peso: 1.0)
            if row['horizonte_investimento'] > 20:
                score += 3
            elif row['horizonte_investimento'] > 10:
                score += 2
            else:
                score += 1

            # Conhecimento de mercado (peso: 1.5)
            score += (row['conhecimento_mercado'] / 10) * 4.5

            # Reserva de emergência (peso: 1.0)
            if row['tem_reserva_emergencia']:
                score += 2

            # Dívidas (peso: -1.0)
            if row['dividas_percentual'] > 50:
                score -= 3
            elif row['dividas_percentual'] > 30:
                score -= 1.5

            # Classificação final
            if score >= 18:
                return 'agressivo'
            elif score >= 12:
                return 'moderado'
            else:
                return 'conservador'

        df['perfil_risco'] = df.apply(classificar_perfil, axis=1)

        # Estatísticas
        distribution = df['perfil_risco'].value_counts(normalize=True) * 100
        print("\nDistribuicao de perfis:")
        for perfil, pct in distribution.items():
            print(f"  {perfil.capitalize()}: {pct:.1f}%")

        return df

    def load(self, df):
        """Salva dataset transformado"""
        print("\n" + "="*70)
        print("STEP 4: LOAD - Salvando dataset transformado")
        print("="*70)

        df.to_csv(self.output_file, index=False)
        print(f"Dataset salvo em: {self.output_file}")
        print(f"Total de registros: {len(df)}")
        print(f"Total de features: {len(df.columns)}")

        return self.output_file

    def validate(self, df):
        """Valida dataset transformado"""
        print("\n" + "="*70)
        print("VALIDACAO DO DATASET")
        print("="*70)

        # Verificar colunas esperadas
        expected_columns = [
            'idade', 'renda_mensal', 'dependentes', 'estado_civil',
            'valor_investir_mensal', 'experiencia_anos', 'patrimonio_total',
            'dividas_percentual', 'tolerancia_perda_1', 'tolerancia_perda_2',
            'horizonte_investimento', 'conhecimento_mercado',
            'estabilidade_emprego', 'tem_reserva_emergencia',
            'planos_grandes_gastos', 'perfil_risco'
        ]

        missing = set(expected_columns) - set(df.columns)
        if missing:
            print(f"ERRO: Colunas faltando: {missing}")
            return False

        print("Todas as 15 features + perfil_risco presentes")

        # Verificar valores nulos
        null_counts = df.isnull().sum()
        if null_counts.any():
            print("\nAVISO: Valores nulos encontrados:")
            print(null_counts[null_counts > 0])
        else:
            print("Nenhum valor nulo encontrado")

        # Estatísticas básicas
        print("\nEstatisticas basicas:")
        print(f"  Idade: {df['idade'].min()}-{df['idade'].max()} (media: {df['idade'].mean():.1f})")
        print(f"  Renda mensal: R$ {df['renda_mensal'].min():.2f} - R$ {df['renda_mensal'].max():.2f}")
        print(f"  Tolerancia risco: {df['tolerancia_perda_1'].min():.1f}-{df['tolerancia_perda_1'].max():.1f}")

        return True

    def run(self):
        """Executa pipeline ETL completo"""
        print("\n" + "="*70)
        print("ETL: SCF -> 15 FEATURES DO MODELO")
        print("="*70 + "\n")

        # Extract
        df_scf = self.extract()

        # Transform
        df_features = self.transform(df_scf)

        # Add classification
        df_final = self.add_risk_classification(df_features)

        # Validate
        self.validate(df_final)

        # Load
        output_path = self.load(df_final)

        print("\n" + "="*70)
        print("ETL CONCLUIDO COM SUCESSO!")
        print("="*70)
        print(f"\nArquivo gerado: {output_path}")

        return df_final


def main():
    """Função principal"""
    etl = SCFToFeaturesETL()
    df_final = etl.run()

    print("\nProximo passo: Execute combinar_datasets.py para mesclar com dados sinteticos")

    return df_final


if __name__ == "__main__":
    df = main()
