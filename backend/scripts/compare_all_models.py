"""
Compare all model versions to find the best one
"""
import joblib
from pathlib import Path
import json

def load_and_check_model(model_path):
    """Load model and return info"""
    try:
        data = joblib.load(model_path)

        info = {
            'path': str(model_path),
            'name': model_path.stem,
            'exists': True,
            'has_model': 'model' in data,
            'has_scaler': 'scaler' in data,
            'is_trained': data.get('is_trained', data.get('trained', False)),
        }

        # Try to get model info
        if 'model' in data:
            model = data['model']
            info['model_type'] = type(model).__name__

            # Check if it has score/metrics
            if hasattr(model, 'best_score_'):
                info['best_score'] = float(model.best_score_)
            if hasattr(model, 'loss_'):
                info['final_loss'] = float(model.loss_)

        return info
    except Exception as e:
        return {
            'path': str(model_path),
            'name': model_path.stem,
            'exists': True,
            'error': str(e)
        }

def main():
    base_path = Path(__file__).parent.parent / 'models'

    print("=" * 80)
    print("MODEL COMPARISON - Finding the Best Versions")
    print("=" * 80)

    # First Network Models
    print("\n🔵 NETWORK 1: Risk Classifier")
    print("-" * 80)

    risk_models = [
        base_path / 'risk_classifier' / 'neural_network.pkl',
        base_path / 'risk_classifier' / 'neural_network_validado.pkl',
        base_path / 'risk_classifier' / 'neural_network_hibrido.pkl',
        base_path / 'risk_classifier' / 'neural_network_otimizado.pkl',
    ]

    risk_results = []
    for model_path in risk_models:
        if model_path.exists():
            info = load_and_check_model(model_path)
            risk_results.append(info)

            print(f"\n📦 {info['name']}")
            print(f"   Type: {info.get('model_type', 'Unknown')}")
            print(f"   Trained: {info.get('is_trained', 'Unknown')}")
            if 'best_score' in info:
                print(f"   Best Score: {info['best_score']:.4f}")
            if 'final_loss' in info:
                print(f"   Final Loss: {info['final_loss']:.4f}")
            if 'error' in info:
                print(f"   ⚠️  Error: {info['error']}")

    # Second Network Models
    print("\n\n🟢 NETWORK 2: Portfolio Allocator")
    print("-" * 80)

    portfolio_models = [
        base_path / 'portfolio_allocator' / 'segunda_rede_neural.pkl',
    ]

    portfolio_results = []
    for model_path in portfolio_models:
        if model_path.exists():
            info = load_and_check_model(model_path)
            portfolio_results.append(info)

            print(f"\n📦 {info['name']}")
            print(f"   Type: {info.get('model_type', 'Unknown')}")
            print(f"   Trained: {info.get('is_trained', 'Unknown')}")
            if 'best_score' in info:
                print(f"   Best Score: {info['best_score']:.4f}")
            if 'final_loss' in info:
                print(f"   Final Loss: {info['final_loss']:.4f}")
            if 'error' in info:
                print(f"   ⚠️  Error: {info['error']}")

    # Recommendations
    print("\n\n" + "=" * 80)
    print("📊 RECOMMENDATIONS")
    print("=" * 80)

    print("\n✅ BEST MODEL FOR NETWORK 1 (Risk Classifier):")
    print("   → neural_network_otimizado.pkl (if it has best metrics)")
    print("   → neural_network_validado.pkl (if validated by expert)")
    print("   → neural_network.pkl (baseline)")

    print("\n✅ BEST MODEL FOR NETWORK 2 (Portfolio):")
    print("   → segunda_rede_neural.pkl (currently only one)")

    print("\n💡 NEXT STEPS:")
    print("   1. Check metrics in docs/markdown/final_metrics_comparison.md")
    print("   2. Select best model based on:")
    print("      - Highest accuracy/R²")
    print("      - Lowest loss")
    print("      - Expert validation")
    print("   3. Rename best model to 'best_model.pkl'")
    print("   4. Update API to use best model")

    # Save comparison to file
    comparison = {
        'network_1_risk_classifier': risk_results,
        'network_2_portfolio': portfolio_results
    }

    output_file = base_path / 'model_comparison_results.json'
    with open(output_file, 'w') as f:
        json.dump(comparison, f, indent=2)

    print(f"\n📁 Results saved to: {output_file}")
    print("=" * 80)

if __name__ == '__main__':
    main()
