"""
Script para baixar e processar dados do Survey of Consumer Finances (SCF)
Federal Reserve - Dataset público de finanças de consumidores americanos

Fonte: https://www.federalreserve.gov/econres/scfindex.htm
"""

import pandas as pd
import numpy as np
import requests
import zipfile
import io
import os
from pathlib import Path

class SCFDownloader:
    """Classe para baixar e processar dados do SCF"""

    def __init__(self):
        self.base_url = "https://www.federalreserve.gov/econres/files"
        self.data_dir = Path(__file__).parent
        self.scf_raw_path = self.data_dir / "scf_raw_data.csv"

    def baixar_scf_2022(self):
        """
        Baixa o dataset SCF 2022 (versão resumida - summary extract)

        O SCF disponibiliza diferentes formatos:
        - Summary Extract Public Data (formato mais acessível)
        - Full Public Data (mais completo, formato SAS/Stata)
        """
        print("🔄 Baixando dados do SCF 2022...")

        # URL do Summary Extract (CSV format) - mais fácil de processar
        # Nota: O Federal Reserve disponibiliza os dados em formato SAS principalmente
        # Vamos usar uma abordagem alternativa com dados pré-processados

        print("⚠️  O dataset SCF oficial vem em formato SAS/Stata.")
        print("📊 Usando dados de exemplo baseados na estrutura do SCF...")

        # Criar dados de exemplo baseados na estrutura real do SCF
        # Em produção, você baixaria o arquivo oficial e processaria com pandas/statsmodels
        return self._criar_exemplo_estrutura_scf()

    def _criar_exemplo_estrutura_scf(self):
        """
        Cria estrutura de exemplo baseada nas variáveis reais do SCF

        Variáveis principais do SCF que usaremos:
        - YY1: ID da família
        - AGE: Idade do respondente
        - INCOME: Renda familiar anual
        - NETWORTH: Patrimônio líquido
        - MARRIED: Estado civil (1=casado, 2=solteiro, etc)
        - KIDS: Número de crianças
        - EDUC: Nível educacional
        - RISK: Tolerância a risco (1-4 scale)
        - DEBT: Dívidas totais
        - LIQ: Ativos líquidos
        - EQUITINC: Renda de ações
        - FAMSTRUCT: Estrutura familiar
        """

        print("📋 Estrutura do SCF contém as seguintes variáveis-chave:")
        variaveis_scf = {
            'YY1': 'ID da família',
            'AGE': 'Idade do respondente principal',
            'INCOME': 'Renda familiar anual total',
            'NETWORTH': 'Patrimônio líquido (ativos - dívidas)',
            'ASSET': 'Total de ativos',
            'DEBT': 'Total de dívidas',
            'LIQ': 'Ativos líquidos (poupança, conta corrente)',
            'MARRIED': 'Estado civil',
            'KIDS': 'Número de crianças',
            'EDUC': 'Nível educacional (1-4: menos que high school até college+)',
            'RISK': 'Tolerância a risco financeiro (1-4)',
            'EQUITINC': 'Renda de investimentos em ações',
            'NEQUITINC': 'Renda de investimentos não-ações',
            'FAMSTRUCT': 'Estrutura familiar',
            'HOUSECL': 'Classe de moradia',
            'OCCAT': 'Ocupação/categoria de trabalho',
            'INCOME_PERCENTILE': 'Percentil de renda'
        }

        for var, desc in variaveis_scf.items():
            print(f"  • {var}: {desc}")

        return variaveis_scf

    def download_scf_via_api(self):
        """
        Método alternativo: alguns pesquisadores disponibilizam versões processadas
        do SCF em formatos mais acessíveis
        """
        print("\n💡 INSTRUÇÕES PARA BAIXAR O DATASET SCF OFICIAL:\n")
        print("1. Acesse: https://www.federalreserve.gov/econres/scfindex.htm")
        print("2. Vá em 'Download Survey Data'")
        print("3. Baixe o 'Summary Extract Public Data' (formato CSV ou Excel)")
        print("4. Ou use o pacote Python 'scfdata' para acesso direto")
        print("\n📦 Instalação alternativa:")
        print("   pip install pandas-datareader")
        print("   pip install wbgapi  # World Bank API (alternativa)")

        return None

    def processar_scf_manual(self, scf_file_path):
        """
        Processa arquivo SCF baixado manualmente pelo usuário

        Args:
            scf_file_path: Caminho para o arquivo SCF (CSV, Excel, ou SAS)
        """
        if not os.path.exists(scf_file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {scf_file_path}")

        print(f"📂 Processando arquivo: {scf_file_path}")

        # Detectar formato do arquivo
        if scf_file_path.endswith('.csv'):
            df = pd.read_csv(scf_file_path)
        elif scf_file_path.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(scf_file_path)
        elif scf_file_path.endswith('.dta'):  # Stata
            df = pd.read_stata(scf_file_path)
        elif scf_file_path.endswith('.sas7bdat'):  # SAS
            df = pd.read_sas(scf_file_path)
        else:
            raise ValueError("Formato de arquivo não suportado")

        print(f"✅ Dataset carregado: {len(df)} registros, {len(df.columns)} colunas")
        print(f"📊 Colunas disponíveis: {list(df.columns)[:10]}...")

        return df


def main():
    """Função principal para demonstração"""
    downloader = SCFDownloader()

    print("=" * 70)
    print("🏦 SURVEY OF CONSUMER FINANCES (SCF) - DATASET DOWNLOADER")
    print("=" * 70)

    # Mostrar estrutura do SCF
    variaveis = downloader.baixar_scf_2022()

    print("\n" + "=" * 70)
    downloader.download_scf_via_api()
    print("=" * 70)

    print("\n✅ Próximo passo: Após baixar o dataset oficial, execute:")
    print("   python etl_scf_to_features.py")


if __name__ == "__main__":
    main()
