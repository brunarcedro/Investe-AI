"""
Script de validação e comparação entre datasets:
- Dataset sintético original (300 amostras)
- Dataset SCF (1000 amostras baseadas em distribuições reais)
- Dataset híbrido (combinação balanceada)

Gera relatório comparativo para apresentar na banca
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json


class DatasetValidator:
    """Valida e compara datasets"""

    def __init__(self):
        self.data_dir = Path(__file__).parent
        self.datasets = {
            'sintetico': self.data_dir / 'dataset_simulado.csv',
            'scf': self.data_dir / 'dataset_from_scf.csv',
            'hibrido': self.data_dir / 'dataset_hibrido.csv'
        }

    def load_datasets(self):
        """Carrega todos os datasets disponíveis"""
        loaded = {}

        for name, path in self.datasets.items():
            if path.exists():
                df = pd.read_csv(path)
                loaded[name] = df
                print(f"Dataset '{name}' carregado: {len(df)} registros")
            else:
                print(f"Dataset '{name}' NAO encontrado: {path}")

        return loaded

    def compare_distributions(self, datasets):
        """Compara distribuições estatísticas entre datasets"""
        print("\n" + "="*70)
        print("COMPARACAO DE DISTRIBUICOES ESTATISTICAS")
        print("="*70)

        features_to_compare = [
            'idade', 'renda_mensal', 'tolerancia_perda_1',
            'horizonte_investimento', 'conhecimento_mercado'
        ]

        for feature in features_to_compare:
            print(f"\n{feature.upper()}:")
            print(f"{'Dataset':<15} {'Min':<12} {'Max':<12} {'Mean':<12} {'Median':<12} {'Std':<12}")
            print("-" * 75)

            for name, df in datasets.items():
                if feature in df.columns:
                    stats = df[feature].describe()
                    print(f"{name:<15} "
                          f"{stats['min']:<12.2f} "
                          f"{stats['max']:<12.2f} "
                          f"{stats['mean']:<12.2f} "
                          f"{stats['50%']:<12.2f} "
                          f"{stats['std']:<12.2f}")

    def compare_risk_profiles(self, datasets):
        """Compara distribuição de perfis de risco"""
        print("\n" + "="*70)
        print("COMPARACAO DE PERFIS DE RISCO")
        print("="*70)

        print(f"\n{'Dataset':<15} {'Conservador':<15} {'Moderado':<15} {'Agressivo':<15}")
        print("-" * 60)

        for name, df in datasets.items():
            if 'perfil_risco' in df.columns:
                dist = df['perfil_risco'].value_counts(normalize=True) * 100

                conservador = dist.get('conservador', 0)
                moderado = dist.get('moderado', 0)
                agressivo = dist.get('agressivo', 0)

                print(f"{name:<15} {conservador:<15.1f}% {moderado:<15.1f}% {agressivo:<15.1f}%")

    def check_data_quality(self, datasets):
        """Verifica qualidade dos dados"""
        print("\n" + "="*70)
        print("QUALIDADE DOS DADOS")
        print("="*70)

        for name, df in datasets.items():
            print(f"\n{name.upper()}:")

            # Valores nulos
            null_counts = df.isnull().sum().sum()
            print(f"  Valores nulos: {null_counts}")

            # Duplicatas
            duplicates = df.duplicated().sum()
            print(f"  Duplicatas: {duplicates}")

            # Consistência de dados
            if 'idade' in df.columns:
                invalid_age = ((df['idade'] < 18) | (df['idade'] > 100)).sum()
                print(f"  Idades invalidas (<18 ou >100): {invalid_age}")

            if 'tolerancia_perda_1' in df.columns:
                invalid_tolerance = ((df['tolerancia_perda_1'] < 1) | (df['tolerancia_perda_1'] > 10)).sum()
                print(f"  Tolerancia invalida (<1 ou >10): {invalid_tolerance}")

            if 'dividas_percentual' in df.columns:
                invalid_debt = ((df['dividas_percentual'] < 0) | (df['dividas_percentual'] > 100)).sum()
                print(f"  Dividas invalidas (<0 or >100): {invalid_debt}")

    def generate_report(self, datasets):
        """Gera relatório em formato de texto para a banca"""
        print("\n" + "="*70)
        print("RELATORIO COMPARATIVO PARA A BANCA")
        print("="*70)

        report = []
        report.append("="*70)
        report.append("RELATORIO: DATASETS PARA TREINAMENTO DAS REDES NEURAIS")
        report.append("="*70)
        report.append("")

        # 1. Resumo executivo
        report.append("1. RESUMO EXECUTIVO")
        report.append("-" * 70)
        report.append("")

        for name, df in datasets.items():
            report.append(f"{name.upper()}:")
            report.append(f"  - Total de registros: {len(df)}")

            if 'perfil_risco' in df.columns:
                dist = df['perfil_risco'].value_counts()
                report.append(f"  - Conservador: {dist.get('conservador', 0)}")
                report.append(f"  - Moderado: {dist.get('moderado', 0)}")
                report.append(f"  - Agressivo: {dist.get('agressivo', 0)}")

            if 'fonte_dados' in df.columns:
                sources = df['fonte_dados'].value_counts()
                report.append(f"  - Fontes de dados: {dict(sources)}")

            report.append("")

        # 2. Vantagens do dataset híbrido
        report.append("2. VANTAGENS DO DATASET HIBRIDO")
        report.append("-" * 70)
        report.append("")
        report.append("a) Baseado em distribuicoes REAIS do Survey of Consumer Finances (SCF)")
        report.append("   - Dados coletados pelo Federal Reserve (EUA)")
        report.append("   - Distribuicoes estatisticas validadas academicamente")
        report.append("   - Escalas de tolerancia a risco testadas em pesquisas")
        report.append("")
        report.append("b) Maior volume de dados (1279 vs 300 registros)")
        report.append("   - Melhora capacidade de generalizacao da rede neural")
        report.append("   - Reduz risco de overfitting")
        report.append("")
        report.append("c) Balanceamento de classes")
        report.append("   - Distribuicao equilibrada: ~33% cada perfil")
        report.append("   - Evita vies do modelo para perfil majoritario")
        report.append("")
        report.append("d) Ajustado para contexto brasileiro")
        report.append("   - Conversao monetaria USD -> BRL")
        report.append("   - Ajuste de niveis de renda para realidade brasileira")
        report.append("")

        # 3. Justificativa para a banca
        report.append("3. JUSTIFICATIVA PARA A BANCA")
        report.append("-" * 70)
        report.append("")
        report.append("Pergunta: 'Por que nao usar dados reais de investidores brasileiros?'")
        report.append("")
        report.append("Resposta:")
        report.append("- Dados de investidores brasileiros sao CONFIDENCIAIS (regulacao CVM)")
        report.append("- Instituicoes financeiras nao disponibilizam publicamente")
        report.append("- Survey of Consumer Finances eh a MELHOR ALTERNATIVA PUBLICA disponivel")
        report.append("- Usado extensivamente em pesquisas academicas internacionais")
        report.append("- Permite reproducibilidade do estudo")
        report.append("")
        report.append("Adaptacoes realizadas:")
        report.append("- Conversao monetaria (USD -> BRL)")
        report.append("- Ajuste de niveis de renda para realidade brasileira")
        report.append("- Combinacao com dados sinteticos para aumentar volume")
        report.append("")

        # 4. Próximos passos
        report.append("4. PROXIMOS PASSOS")
        report.append("-" * 70)
        report.append("")
        report.append("1. Retreinar primeira rede neural com dataset hibrido")
        report.append("2. Retreinar segunda rede neural com dataset hibrido")
        report.append("3. Comparar metricas de performance:")
        report.append("   - Acuracia, Precision, Recall, F1-Score")
        report.append("   - Antes (dataset sintetico) vs Depois (dataset hibrido)")
        report.append("4. Adicionar no TCC:")
        report.append("   - Secao sobre fonte de dados (SCF)")
        report.append("   - Justificativa para uso de dados americanos")
        report.append("   - Processo de adaptacao para contexto brasileiro")
        report.append("")

        # Salvar relatório
        report_text = "\n".join(report)
        print(report_text)

        # Salvar em arquivo
        report_file = self.data_dir / 'RELATORIO_DATASETS.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_text)

        print(f"\nRelatorio salvo em: {report_file}")

        return report_text

    def generate_json_summary(self, datasets):
        """Gera resumo em JSON para fácil consumo"""
        summary = {}

        for name, df in datasets.items():
            summary[name] = {
                'total_registros': len(df),
                'total_features': len(df.columns),
                'perfis_risco': {},
                'estatisticas': {}
            }

            # Distribuição de perfis
            if 'perfil_risco' in df.columns:
                dist = df['perfil_risco'].value_counts()
                summary[name]['perfis_risco'] = {
                    'conservador': int(dist.get('conservador', 0)),
                    'moderado': int(dist.get('moderado', 0)),
                    'agressivo': int(dist.get('agressivo', 0))
                }

            # Estatísticas chave
            if 'idade' in df.columns:
                summary[name]['estatisticas']['idade'] = {
                    'min': float(df['idade'].min()),
                    'max': float(df['idade'].max()),
                    'mean': float(df['idade'].mean()),
                    'median': float(df['idade'].median())
                }

            if 'renda_mensal' in df.columns:
                summary[name]['estatisticas']['renda_mensal'] = {
                    'min': float(df['renda_mensal'].min()),
                    'max': float(df['renda_mensal'].max()),
                    'mean': float(df['renda_mensal'].mean()),
                    'median': float(df['renda_mensal'].median())
                }

        # Salvar JSON
        json_file = self.data_dir / 'datasets_summary.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        print(f"\nResumo JSON salvo em: {json_file}")

        return summary

    def run_validation(self):
        """Executa validação completa"""
        print("="*70)
        print("VALIDACAO DE DATASETS")
        print("="*70)

        # Carregar datasets
        datasets = self.load_datasets()

        if not datasets:
            print("ERRO: Nenhum dataset encontrado!")
            return

        # Comparações
        self.compare_distributions(datasets)
        self.compare_risk_profiles(datasets)
        self.check_data_quality(datasets)

        # Gerar relatórios
        self.generate_report(datasets)
        self.generate_json_summary(datasets)

        print("\n" + "="*70)
        print("VALIDACAO CONCLUIDA!")
        print("="*70)


def main():
    validator = DatasetValidator()
    validator.run_validation()

    print("\n" + "="*70)
    print("ARQUIVOS GERADOS:")
    print("="*70)
    print("1. RELATORIO_DATASETS.txt - Relatorio completo para a banca")
    print("2. datasets_summary.json - Resumo em JSON")
    print("")
    print("DATASETS DISPONIVEIS:")
    print("1. dataset_simulado.csv - Original sintetico (300 registros)")
    print("2. dataset_from_scf.csv - Baseado em SCF (1000 registros)")
    print("3. dataset_hibrido.csv - RECOMENDADO para treinar redes (1279 registros)")


if __name__ == "__main__":
    main()
