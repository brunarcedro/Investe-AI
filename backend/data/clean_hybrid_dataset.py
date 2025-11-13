"""
Clean hybrid dataset by handling NaN values
"""
import pandas as pd
from pathlib import Path

# Load dataset
df = pd.read_csv('dataset_hibrido.csv')

print("Original dataset:")
print(f"  Samples: {len(df)}")
print(f"  NaN values:\n{df.isnull().sum()[df.isnull().sum() > 0]}\n")

# Fill NaN values
# tem_reserva_emergencia: fill with 0 (no emergency fund)
df['tem_reserva_emergencia'] = df['tem_reserva_emergencia'].fillna(0).astype(int)

# publico_alvo: fill with 'geral' (general public)
df['publico_alvo'] = df['publico_alvo'].fillna('geral')

# Check for any remaining NaNs
print("After cleaning:")
print(f"  Samples: {len(df)}")
remaining_nans = df.isnull().sum()[df.isnull().sum() > 0]
if len(remaining_nans) > 0:
    print(f"  Remaining NaN values:\n{remaining_nans}")
else:
    print("  ✅ No NaN values!")

# Save cleaned dataset
output_file = 'dataset_hibrido_clean.csv'
df.to_csv(output_file, index=False)
print(f"\n✅ Cleaned dataset saved to: {output_file}")

# Verify
df_check = pd.read_csv(output_file)
print(f"\nVerification:")
print(f"  Loaded {len(df_check)} samples")
print(f"  NaN check: {df_check.isnull().sum().sum()} NaN values")
