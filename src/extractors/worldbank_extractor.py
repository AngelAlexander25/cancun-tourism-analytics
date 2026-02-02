"""
Extractor de World Bank API - Turismo internacional REAL
"""
import requests
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path
import time

sys.path.append(str(Path(__file__).parent.parent.parent))
from config import DATA_RAW, TARGET_COUNTRIES

def extract_tourism_data():
    """Extrae datos REALES de turismo internacional"""
    print("Extrayendo datos de World Bank API...")
    
    # Codigos ISO de paises
    country_codes = {
        'United States': 'USA', 'Canada': 'CAN', 
        'United Kingdom': 'GBR', 'Germany': 'DEU',
        'France': 'FRA', 'Spain': 'ESP', 
        'Brazil': 'BRA', 'Argentina': 'ARG',
        'Colombia': 'COL', 'Mexico': 'MEX'
    }
    
    all_data = []
    
    # Indicador: ST.INT.ARVL (Llegadas turisticas internacionales)
    for country, code in country_codes.items():
        url = f"https://api.worldbank.org/v2/country/{code}/indicator/ST.INT.ARVL"
        params = {
            'format': 'json',
            'date': '2019:2023',
            'per_page': 100
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if len(data) > 1 and data[1]:
                    for entry in data[1]:
                        if entry['value']:
                            all_data.append({
                                'country': country,
                                'country_code': code,
                                'year': int(entry['date']),
                                'arrivals': int(entry['value']),
                                'extracted_at': datetime.now()
                            })
            
            time.sleep(0.5)
            print(f"  {country}: OK")
            
        except Exception as e:
            print(f"  {country}: Error - {e}")
    
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(DATA_RAW / "worldbank_tourism_real.csv", index=False)
        print(f"\nGuardado: {DATA_RAW / 'worldbank_tourism_real.csv'}")
        print(f"Total registros: {len(df)}")
        return df
    else:
        print("No se obtuvieron datos")
        return None

if __name__ == "__main__":
    extract_tourism_data()