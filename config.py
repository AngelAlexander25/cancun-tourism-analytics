"""
Configuracion global
"""
from pathlib import Path

# Rutas
PROJECT_ROOT = Path(__file__).parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"

# Crear carpetas
DATA_RAW.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Paises principales para Cancun
TARGET_COUNTRIES = [
    "United States", "Canada", "United Kingdom", 
    "Germany", "France", "Spain", "Brazil", 
    "Argentina", "Colombia", "Mexico"
]

# Configuracion Cancun
CANCUN_COORDS = {"lat": 21.16, "lon": -86.85}