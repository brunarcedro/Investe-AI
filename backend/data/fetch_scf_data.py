"""
Script para extrair dados do SCF usando bibliotecas Python
Usa dados simulados realistas baseados na estrutura do SCF

Para usar dados reais SCF, instale: pip install scf
(Biblioteca experimental que facilita acesso aos dados oficiais)
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

class SCFDataGenerator:
    """
    Gera dados simulados realistas baseados nas distribuições estatísticas
    do Survey of Consumer Finances (SCF) 2022

    Baseado nas estatísticas publicadas pelo Federal Reserve
    """

    def __init__(self, n_samples=1000, random_state=42):
        self.n_samples = n_samples
        self.random_state = random_state
        np.random.seed(random_state)

    def generate_realistic_scf_data(self):
        """
        Gera dados baseados em distribuições reais do SCF 2022

        Estatísticas baseadas em:
        - Federal Reserve SCF 2022 Summary Statistics
        - Median household income: ~$70,000
        - Mean net worth: ~$750,000 (median: ~$120,000)
        """

        print(f"Gerando {self.n_samples} amostras baseadas em distribuições SCF...")

        data = {
            # ID único
            'YY1': range(1, self.n_samples + 1),

            # IDADE: Distribuição realista (foco em 18-80 anos)
            'AGE': self._generate_age_distribution(),

            # RENDA: Distribuição log-normal (realista para renda)
            'INCOME': self._generate_income_distribution(),

            # PATRIMÔNIO LÍQUIDO: Log-normal com mediana ~$120k
            'NETWORTH': self._generate_networth_distribution(),

            # ESTADO CIVIL: 1=Married, 2=Single, 3=Divorced, 4=Widowed
            'MARRIED': self._generate_marital_status(),

            # NÚMERO DE CRIANÇAS/DEPENDENTES
            'KIDS': self._generate_kids_distribution(),

            # EDUCAÇÃO: 1=No HS diploma, 2=HS diploma, 3=Some college, 4=College degree
            'EDUC': self._generate_education_distribution(),

            # TOLERÂNCIA A RISCO: 1=Not willing, 2=Average, 3=Above average, 4=Substantial
            'RISK': self._generate_risk_tolerance(),

            # OCUPAÇÃO: 1=Manager/Professional, 2=Technical/Sales, 3=Service, 4=Not working
            'OCCAT': self._generate_occupation(),

            # ESTRUTURA FAMILIAR: simplificado
            'FAMSTRUCT': np.random.randint(1, 5, self.n_samples),
        }

        df = pd.DataFrame(data)

        # Calcular campos derivados
        df['ASSET'] = df.apply(lambda row: self._calculate_assets(row), axis=1)
        df['DEBT'] = df.apply(lambda row: self._calculate_debt(row), axis=1)
        df['LIQ'] = df.apply(lambda row: self._calculate_liquid_assets(row), axis=1)

        # Renda de investimentos (baseada em patrimônio e educação)
        df['EQUITINC'] = df.apply(lambda row: self._calculate_equity_income(row), axis=1)

        # Percentil de renda
        df['INCOME_PERCENTILE'] = pd.qcut(df['INCOME'], q=100, labels=False, duplicates='drop') + 1

        print(f"Dataset gerado com {len(df)} registros e {len(df.columns)} colunas")

        return df

    def _generate_age_distribution(self):
        """Distribuição de idade realista (adultos 18-85)"""
        # Distribuição com pico em 40-50 anos
        ages = np.random.beta(2, 2, self.n_samples) * 67 + 18
        return ages.astype(int)

    def _generate_income_distribution(self):
        """
        Distribuição de renda (log-normal)
        Mediana: ~$70,000 | Média: ~$105,000
        """
        # Log-normal distribution
        mu = 11.1  # ln(70000) aproximadamente
        sigma = 0.8
        income = np.random.lognormal(mu, sigma, self.n_samples)

        # Limitar valores extremos
        income = np.clip(income, 0, 2000000)

        return income.astype(int)

    def _generate_networth_distribution(self):
        """
        Distribuição de patrimônio líquido
        Mediana: ~$120,000 | Média: ~$750,000
        """
        # Log-normal com valores negativos possíveis (dívidas)
        base = np.random.lognormal(11.7, 1.5, self.n_samples)

        # 15% das famílias têm patrimônio líquido negativo
        negative_mask = np.random.random(self.n_samples) < 0.15
        networth = np.where(negative_mask, -base * 0.3, base)

        return networth.astype(int)

    def _generate_marital_status(self):
        """
        Estado civil baseado em estatísticas dos EUA
        1=Married(~50%), 2=Single(~30%), 3=Divorced(~10%), 4=Widowed(~10%)
        """
        return np.random.choice([1, 2, 3, 4], self.n_samples, p=[0.50, 0.30, 0.10, 0.10])

    def _generate_kids_distribution(self):
        """Número de crianças/dependentes (0-5)"""
        # Maioria sem crianças ou com 1-2
        return np.random.choice([0, 1, 2, 3, 4, 5], self.n_samples,
                               p=[0.40, 0.25, 0.20, 0.10, 0.04, 0.01])

    def _generate_education_distribution(self):
        """
        Nível educacional
        1=No HS diploma(10%), 2=HS diploma(25%), 3=Some college(30%), 4=College degree(35%)
        """
        return np.random.choice([1, 2, 3, 4], self.n_samples,
                               p=[0.10, 0.25, 0.30, 0.35])

    def _generate_risk_tolerance(self):
        """
        Tolerância a risco financeiro (escala 1-4 do SCF)
        1=Not willing to take any risk (30%)
        2=Average risk (40%)
        3=Above average risk (20%)
        4=Substantial risk (10%)
        """
        return np.random.choice([1, 2, 3, 4], self.n_samples,
                               p=[0.30, 0.40, 0.20, 0.10])

    def _generate_occupation(self):
        """Categoria de ocupação"""
        return np.random.choice([1, 2, 3, 4], self.n_samples,
                               p=[0.35, 0.30, 0.25, 0.10])

    def _calculate_assets(self, row):
        """Calcula ativos totais baseado em renda e patrimônio"""
        if row['NETWORTH'] < 0:
            return abs(row['NETWORTH']) * 0.5  # Tem alguns ativos mesmo com dívida
        else:
            return row['NETWORTH'] + abs(row['NETWORTH']) * np.random.uniform(0.2, 0.5)

    def _calculate_debt(self, row):
        """Calcula dívidas totais"""
        if row['NETWORTH'] < 0:
            return abs(row['NETWORTH']) * 1.5
        else:
            # Dívida = Ativos - Patrimônio Líquido
            debt = row['ASSET'] - row['NETWORTH']
            return max(0, debt)

    def _calculate_liquid_assets(self, row):
        """Calcula ativos líquidos (10-30% dos ativos totais)"""
        return row['ASSET'] * np.random.uniform(0.10, 0.30)

    def _calculate_equity_income(self, row):
        """Renda de ações (baseada em patrimônio e educação)"""
        if row['NETWORTH'] > 100000 and row['EDUC'] >= 3:
            return row['NETWORTH'] * np.random.uniform(0.03, 0.08)  # 3-8% retorno
        return 0

    def save_to_csv(self, df, filename='scf_simulated_data.csv'):
        """Salva dataset em CSV"""
        filepath = self.get_data_path(filename)
        df.to_csv(filepath, index=False)
        print(f"Dataset salvo em: {filepath}")
        return filepath

    def get_data_path(self, filename):
        """Retorna o caminho completo para o arquivo de dados"""
        from pathlib import Path
        data_dir = Path(__file__).parent
        return data_dir / filename

    def print_statistics(self, df):
        """Imprime estatísticas descritivas do dataset"""
        print("\n" + "=" * 70)
        print("ESTATISTICAS DO DATASET SCF SIMULADO")
        print("=" * 70)

        print(f"\nEstatisticas de Renda (INCOME):")
        print(f"   Mediana: ${df['INCOME'].median():,.2f}")
        print(f"   Média: ${df['INCOME'].mean():,.2f}")
        print(f"   P25: ${df['INCOME'].quantile(0.25):,.2f}")
        print(f"   P75: ${df['INCOME'].quantile(0.75):,.2f}")

        print(f"\nEstatisticas de Patrimonio (NETWORTH):")
        print(f"   Mediana: ${df['NETWORTH'].median():,.2f}")
        print(f"   Média: ${df['NETWORTH'].mean():,.2f}")
        print(f"   % com patrimonio negativo: {(df['NETWORTH'] < 0).sum() / len(df) * 100:.1f}%")

        print(f"\nDemografia:")
        print(f"   Idade media: {df['AGE'].mean():.1f} anos")
        print(f"   % casados: {(df['MARRIED'] == 1).sum() / len(df) * 100:.1f}%")
        print(f"   Media de filhos: {df['KIDS'].mean():.2f}")

        print(f"\nEducacao:")
        educ_counts = df['EDUC'].value_counts(normalize=True).sort_index() * 100
        labels = {1: 'Sem HS', 2: 'HS', 3: 'Algum College', 4: 'College+'}
        for educ, pct in educ_counts.items():
            print(f"   {labels[educ]}: {pct:.1f}%")

        print(f"\nTolerancia a Risco:")
        risk_counts = df['RISK'].value_counts(normalize=True).sort_index() * 100
        risk_labels = {1: 'Nenhum risco', 2: 'Risco medio', 3: 'Risco acima media', 4: 'Risco substancial'}
        for risk, pct in risk_counts.items():
            print(f"   {risk_labels[risk]}: {pct:.1f}%")


def main():
    """Função principal"""
    print("=" * 70)
    print("GERADOR DE DADOS SCF (Survey of Consumer Finances)")
    print("=" * 70)

    # Gerar dataset
    generator = SCFDataGenerator(n_samples=1000, random_state=42)
    df_scf = generator.generate_realistic_scf_data()

    # Mostrar estatísticas
    generator.print_statistics(df_scf)

    # Salvar
    filepath = generator.save_to_csv(df_scf)

    print(f"\nDataset SCF gerado com sucesso!")
    print(f"Proximo passo: Execute etl_scf_to_features.py para converter para suas 15 features")

    return df_scf


if __name__ == "__main__":
    df = main()
