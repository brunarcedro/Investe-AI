"""
Script para combinar dados SCF (baseados em distribuições reais)
com dados sintéticos existentes, criando um dataset híbrido robusto

Estratégias de combinação:
1. Concatenação simples (manter todos os dados)
2. Balanceamento de perfis de risco
3. Remoção de duplicatas e outliers extremos
4. Ajuste de distribuições para contexto brasileiro
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class DatasetCombiner:
    """Combina datasets SCF e sintéticos em um dataset híbrido"""

    def __init__(self):
        self.data_dir = Path(__file__).parent
        self.scf_file = self.data_dir / 'dataset_from_scf.csv'
        self.synthetic_file = self.data_dir / 'dataset_simulado.csv'
        self.output_file = self.data_dir / 'dataset_hibrido.csv'

    def load_datasets(self):
        """Carrega ambos os datasets"""
        print("="*70)
        print("CARREGANDO DATASETS")
        print("="*70)

        # Dataset SCF
        if not self.scf_file.exists():
            raise FileNotFoundError(f"Dataset SCF nao encontrado: {self.scf_file}")

        df_scf = pd.read_csv(self.scf_file)
        print(f"\nDataset SCF carregado:")
        print(f"  Registros: {len(df_scf)}")
        print(f"  Features: {len(df_scf.columns)}")
        print(f"  Origem: Survey of Consumer Finances (distribuicoes reais)")

        # Dataset sintético
        if not self.synthetic_file.exists():
            print(f"\nAVISO: Dataset sintetico nao encontrado: {self.synthetic_file}")
            print("Continuando apenas com dados SCF...")
            return df_scf, None

        df_synthetic = pd.read_csv(self.synthetic_file)
        print(f"\nDataset Sintetico carregado:")
        print(f"  Registros: {len(df_synthetic)}")
        print(f"  Features: {len(df_synthetic.columns)}")
        print(f"  Origem: Dados sinteticos originais")

        return df_scf, df_synthetic

    def harmonize_columns(self, df_scf, df_synthetic):
        """
        Harmoniza nomes e tipos de colunas entre os datasets

        Dataset SCF tem colunas:
        - patrimonio_total (ao invés de patrimonio_atual)
        - Pode ter colunas extras

        Dataset sintético pode ter:
        - patrimonio_atual
        - objetivo_prazo
        """
        print("\n" + "="*70)
        print("HARMONIZANDO COLUNAS")
        print("="*70)

        # Colunas esperadas (15 features + perfil_risco)
        expected_cols = [
            'idade', 'renda_mensal', 'dependentes', 'estado_civil',
            'valor_investir_mensal', 'experiencia_anos',
            'dividas_percentual', 'tolerancia_perda_1', 'tolerancia_perda_2',
            'horizonte_investimento', 'conhecimento_mercado',
            'estabilidade_emprego', 'tem_reserva_emergencia',
            'planos_grandes_gastos', 'perfil_risco'
        ]

        # Adicionar coluna de patrimônio (nome padronizado)
        expected_cols.insert(7, 'patrimonio_atual')

        # Renomear patrimonio_total -> patrimonio_atual no SCF se necessário
        if 'patrimonio_total' in df_scf.columns and 'patrimonio_atual' not in df_scf.columns:
            df_scf = df_scf.rename(columns={'patrimonio_total': 'patrimonio_atual'})
            print("Renomeado: patrimonio_total -> patrimonio_atual (SCF)")

        # Renomear objetivo_prazo -> horizonte_investimento no sintético se necessário
        if df_synthetic is not None:
            if 'objetivo_prazo' in df_synthetic.columns and 'horizonte_investimento' not in df_synthetic.columns:
                df_synthetic = df_synthetic.rename(columns={'objetivo_prazo': 'horizonte_investimento'})
                print("Renomeado: objetivo_prazo -> horizonte_investimento (Sintetico)")

        # Selecionar apenas colunas esperadas
        df_scf_clean = df_scf[[col for col in expected_cols if col in df_scf.columns]].copy()

        if df_synthetic is not None:
            df_synthetic_clean = df_synthetic[[col for col in expected_cols if col in df_synthetic.columns]].copy()

            # Adicionar colunas faltantes com valores padrão
            for col in expected_cols:
                if col not in df_scf_clean.columns:
                    print(f"AVISO: Coluna {col} faltando no SCF")
                if col not in df_synthetic_clean.columns:
                    print(f"AVISO: Coluna {col} faltando no Sintetico")
        else:
            df_synthetic_clean = None

        print(f"\nColunas harmonizadas: {len(df_scf_clean.columns)}")

        return df_scf_clean, df_synthetic_clean

    def adjust_to_brazilian_context(self, df_scf):
        """
        Ajusta dados SCF (americanos) para contexto brasileiro

        Ajustes:
        1. Converter renda USD -> BRL (fator ~5x)
        2. Ajustar patrimônio USD -> BRL
        3. Ajustar foco em investidores jovens (18-25 anos)
        """
        print("\n" + "="*70)
        print("AJUSTANDO PARA CONTEXTO BRASILEIRO")
        print("="*70)

        df = df_scf.copy()

        # 1. Conversão monetária USD -> BRL (taxa aproximada: 1 USD = 5 BRL)
        USD_TO_BRL = 5.0

        print(f"\n1. Convertendo valores monetarios (USD -> BRL, fator {USD_TO_BRL}x)")

        if 'renda_mensal' in df.columns:
            df['renda_mensal'] = (df['renda_mensal'] * USD_TO_BRL).round(2)
            print(f"   renda_mensal: R$ {df['renda_mensal'].median():,.2f} (mediana)")

        if 'valor_investir_mensal' in df.columns:
            df['valor_investir_mensal'] = (df['valor_investir_mensal'] * USD_TO_BRL).round(2)

        if 'patrimonio_atual' in df.columns:
            df['patrimonio_atual'] = (df['patrimonio_atual'] * USD_TO_BRL).round(2)
            print(f"   patrimonio_atual: R$ {df['patrimonio_atual'].median():,.2f} (mediana)")

        # 2. Criar subset focado em jovens (18-25 anos) - público-alvo do TCC
        print(f"\n2. Perfil de idade:")
        print(f"   Original: {df['idade'].min()}-{df['idade'].max()} anos (media: {df['idade'].mean():.1f})")

        # Manter todos os dados, mas adicionar peso/flag para jovens
        df['publico_alvo'] = (df['idade'] <= 25).astype(int)
        pct_young = df['publico_alvo'].mean() * 100
        print(f"   Jovens (18-25): {pct_young:.1f}% do dataset")

        # 3. Ajustar níveis de renda para realidade brasileira (reduzir um pouco)
        # Renda média brasileira é menor que americana
        INCOME_ADJUSTMENT = 0.6  # Reduzir 40%

        print(f"\n3. Ajustando niveis de renda (fator {INCOME_ADJUSTMENT}x)")
        df['renda_mensal'] = (df['renda_mensal'] * INCOME_ADJUSTMENT).round(2)
        df['valor_investir_mensal'] = (df['valor_investir_mensal'] * INCOME_ADJUSTMENT).round(2)

        print(f"   Nova renda mensal mediana: R$ {df['renda_mensal'].median():,.2f}")

        return df

    def balance_risk_profiles(self, df_combined):
        """
        Balanceia distribuição de perfis de risco para evitar viés

        Objetivo: distribuição aproximadamente igual entre perfis
        (33% conservador, 33% moderado, 33% agressivo)
        """
        print("\n" + "="*70)
        print("BALANCEANDO PERFIS DE RISCO")
        print("="*70)

        # Distribuição atual
        current_dist = df_combined['perfil_risco'].value_counts(normalize=True) * 100
        print("\nDistribuicao atual:")
        for perfil, pct in current_dist.items():
            print(f"  {perfil.capitalize()}: {pct:.1f}%")

        # Calcular target (33% cada)
        total = len(df_combined)
        target_per_profile = total // 3

        # Undersample perfis sobre-representados
        balanced_dfs = []

        for perfil in ['conservador', 'moderado', 'agressivo']:
            df_perfil = df_combined[df_combined['perfil_risco'] == perfil]
            current_count = len(df_perfil)

            if current_count > target_per_profile:
                # Undersample
                df_sampled = df_perfil.sample(n=target_per_profile, random_state=42)
                print(f"\n{perfil.capitalize()}: {current_count} -> {target_per_profile} (undersample)")
            else:
                # Manter todos + oversample se necessário
                n_copies = (target_per_profile // current_count)
                n_remaining = target_per_profile % current_count

                df_sampled = pd.concat([df_perfil] * n_copies, ignore_index=True)
                if n_remaining > 0:
                    df_sampled = pd.concat([
                        df_sampled,
                        df_perfil.sample(n=n_remaining, random_state=42)
                    ], ignore_index=True)

                print(f"\n{perfil.capitalize()}: {current_count} -> {len(df_sampled)} (oversample)")

            balanced_dfs.append(df_sampled)

        df_balanced = pd.concat(balanced_dfs, ignore_index=True)

        # Shuffle
        df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

        # Nova distribuição
        new_dist = df_balanced['perfil_risco'].value_counts(normalize=True) * 100
        print("\nNova distribuicao:")
        for perfil, pct in new_dist.items():
            print(f"  {perfil.capitalize()}: {pct:.1f}%")

        print(f"\nTotal de registros: {len(df_combined)} -> {len(df_balanced)}")

        return df_balanced

    def remove_outliers(self, df):
        """Remove outliers extremos que podem prejudicar o treinamento"""
        print("\n" + "="*70)
        print("REMOVENDO OUTLIERS EXTREMOS")
        print("="*70)

        initial_count = len(df)

        # Remover valores impossíveis ou extremos
        filters = {
            'idade': (df['idade'] >= 18) & (df['idade'] <= 100),
            'renda_mensal': (df['renda_mensal'] >= 0) & (df['renda_mensal'] <= 500000),
            'patrimonio_atual': (df['patrimonio_atual'] >= -1000000) & (df['patrimonio_atual'] <= 50000000),
            'dividas_percentual': (df['dividas_percentual'] >= 0) & (df['dividas_percentual'] <= 100),
            'tolerancia_perda_1': (df['tolerancia_perda_1'] >= 1) & (df['tolerancia_perda_1'] <= 10),
            'horizonte_investimento': (df['horizonte_investimento'] >= 1) & (df['horizonte_investimento'] <= 50),
        }

        # Aplicar filtros
        combined_filter = pd.Series([True] * len(df))
        for col, filter_condition in filters.items():
            if col in df.columns:
                combined_filter &= filter_condition

        df_clean = df[combined_filter].copy()

        removed = initial_count - len(df_clean)
        pct_removed = (removed / initial_count) * 100

        print(f"\nOutliers removidos: {removed} ({pct_removed:.2f}%)")
        print(f"Registros restantes: {len(df_clean)}")

        return df_clean

    def add_metadata(self, df, source='hibrido'):
        """Adiciona metadados sobre origem dos dados"""
        df = df.copy()
        df['fonte_dados'] = source
        return df

    def combine(self, strategy='balanced'):
        """
        Combina datasets usando estratégia especificada

        Estratégias:
        - 'concat': Concatenação simples
        - 'balanced': Balanceamento de perfis de risco
        - 'scf_only': Apenas dados SCF ajustados
        """
        print("\n" + "="*70)
        print(f"ESTRATEGIA DE COMBINACAO: {strategy.upper()}")
        print("="*70)

        # 1. Carregar datasets
        df_scf, df_synthetic = self.load_datasets()

        # 2. Harmonizar colunas
        df_scf, df_synthetic = self.harmonize_columns(df_scf, df_synthetic)

        # 3. Ajustar SCF para contexto brasileiro
        df_scf_br = self.adjust_to_brazilian_context(df_scf)

        # 4. Adicionar metadados
        df_scf_br = self.add_metadata(df_scf_br, source='scf')

        if df_synthetic is not None:
            df_synthetic = self.add_metadata(df_synthetic, source='sintetico')

            # 5. Combinar
            if strategy == 'concat':
                df_combined = pd.concat([df_scf_br, df_synthetic], ignore_index=True)
            elif strategy == 'balanced':
                df_combined = pd.concat([df_scf_br, df_synthetic], ignore_index=True)
                df_combined = self.balance_risk_profiles(df_combined)
            else:
                df_combined = df_scf_br
        else:
            print("\nUsando apenas dados SCF (dataset sintetico nao encontrado)")
            df_combined = df_scf_br
            if strategy == 'balanced':
                df_combined = self.balance_risk_profiles(df_combined)

        # 6. Remover outliers
        df_final = self.remove_outliers(df_combined)

        # 7. Shuffle final
        df_final = df_final.sample(frac=1, random_state=42).reset_index(drop=True)

        return df_final

    def save(self, df, filename=None):
        """Salva dataset combinado"""
        if filename is None:
            filename = self.output_file

        df.to_csv(filename, index=False)
        print(f"\n" + "="*70)
        print("DATASET HIBRIDO SALVO")
        print("="*70)
        print(f"Arquivo: {filename}")
        print(f"Registros: {len(df)}")
        print(f"Features: {len(df.columns)}")

        return filename

    def print_summary(self, df):
        """Imprime resumo do dataset final"""
        print("\n" + "="*70)
        print("RESUMO DO DATASET HIBRIDO")
        print("="*70)

        # Distribuição de perfis
        print("\n1. Distribuicao de Perfis de Risco:")
        profile_dist = df['perfil_risco'].value_counts(normalize=True) * 100
        for perfil, pct in profile_dist.items():
            count = (df['perfil_risco'] == perfil).sum()
            print(f"   {perfil.capitalize()}: {count} ({pct:.1f}%)")

        # Distribuição de origem
        if 'fonte_dados' in df.columns:
            print("\n2. Distribuicao por Fonte:")
            source_dist = df['fonte_dados'].value_counts()
            for source, count in source_dist.items():
                pct = (count / len(df)) * 100
                print(f"   {source.upper()}: {count} ({pct:.1f}%)")

        # Público-alvo (jovens)
        if 'publico_alvo' in df.columns:
            young_count = df['publico_alvo'].sum()
            young_pct = (young_count / len(df)) * 100
            print(f"\n3. Publico-alvo (18-25 anos): {young_count} ({young_pct:.1f}%)")

        # Estatísticas demográficas
        print("\n4. Estatisticas Demograficas:")
        print(f"   Idade: {df['idade'].min()}-{df['idade'].max()} (media: {df['idade'].mean():.1f})")
        print(f"   Renda mensal: R$ {df['renda_mensal'].min():,.2f} - R$ {df['renda_mensal'].max():,.2f}")
        print(f"   Renda mediana: R$ {df['renda_mensal'].median():,.2f}")

        # Reserva de emergência
        if 'tem_reserva_emergencia' in df.columns:
            with_emergency = df['tem_reserva_emergencia'].sum()
            pct_emergency = (with_emergency / len(df)) * 100
            print(f"\n5. Com reserva de emergencia: {with_emergency} ({pct_emergency:.1f}%)")


def main():
    """Função principal"""
    print("="*70)
    print("COMBINADOR DE DATASETS - SCF + SINTETICO")
    print("="*70)

    combiner = DatasetCombiner()

    # Combinar datasets com estratégia de balanceamento
    df_hibrido = combiner.combine(strategy='balanced')

    # Salvar
    output_path = combiner.save(df_hibrido)

    # Resumo
    combiner.print_summary(df_hibrido)

    print("\n" + "="*70)
    print("PROCESSO CONCLUIDO!")
    print("="*70)
    print(f"\nDataset hibrido criado: {output_path}")
    print("\nProximo passo:")
    print("  1. Treinar redes neurais com dataset hibrido")
    print("  2. Comparar metricas: dataset sintetico vs hibrido")
    print("  3. Apresentar para banca: 'dados baseados em distribuicoes reais (SCF)'")

    return df_hibrido


if __name__ == "__main__":
    df = main()
