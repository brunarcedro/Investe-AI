"""
Versao RAPIDA do otimizador - para testes
Executa as principais otimizacoes sem demorar muito
"""

import sys
sys.path.append('.')

from otimizar_redes_avancado import AdvancedNeuralNetworkOptimizer
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


def main():
    print("="*70)
    print("OTIMIZACAO RAPIDA - TESTE")
    print("="*70)

    # Dataset
    dataset_path = Path(__file__).parent / 'data' / 'dataset_hibrido.csv'

    if not dataset_path.exists():
        print(f"ERRO: Dataset nao encontrado: {dataset_path}")
        return

    # Criar otimizador
    optimizer = AdvancedNeuralNetworkOptimizer(dataset_path)

    # Executar versao rapida
    print("\nConfiguracao RAPIDA:")
    print("  - SMOTE: SIM")
    print("  - PCA: NAO")
    print("  - Ensemble: Voting")
    print("  - Otimizacao HP: NAO (usa config otimizada manual)")
    print("\n(Para otimizacao completa, use otimizar_redes_avancado.py)")

    results = optimizer.run_complete_optimization(
        use_smote=True,
        use_pca=False,
        use_ensemble='voting',
        optimize_hp=False  # Mais rapido
    )

    print("\n" + "="*70)
    print("TESTE CONCLUIDO!")
    print("="*70)


if __name__ == "__main__":
    main()
