"""
Script maestro - Extrae todos los datos
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

print("\n" + "="*60)
print("EXTRACCION DE DATOS - CANCUN TOURISM")
print("="*60 + "\n")

# 1. Google Trends
print("1/3: Google Trends...")
try:
    from src.extractors.trends_extractor import extract_trends
    extract_trends()
except Exception as e:
    print(f"  Error (usando datos anteriores): {e}")
print()

# 2. World Bank
print("2/3: World Bank API...")
try:
    from src.extractors.worldbank_extractor import extract_tourism_data
    extract_tourism_data()
except Exception as e:
    print(f"  Error (usando datos anteriores): {e}")
print()

# 3. Generar datos completos
print("3/3: Generando datos actualizados...")
from src.extractors.intelligent_generator import generate_current_data
df = generate_current_data()
print()

print("="*60)
print("EXTRACCION COMPLETADA")
print(f"Datos generados para {df['country'].nunique()} paises")
print(f"Anos: {df['year'].min()} - {df['year'].max()}")
print("="*60 + "\n")