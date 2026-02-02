"""
Extractor de Google Trends - DATOS REALES
"""
from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path
import time

sys.path.append(str(Path(__file__).parent.parent.parent))
from config import DATA_RAW, TARGET_COUNTRIES

def extract_trends():
    """Extrae tendencias REALES de Google"""
    print("Extrayendo Google Trends REAL...")
    
    pytrends = TrendReq(hl='en-US', tz=360)
    
    try:
        # Build payload
        pytrends.build_payload(['Cancun'], timeframe='today 12-m')
        
        # Interes por region
        df_region = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True)
        df_region = df_region.reset_index()
        df_region.columns = ['country', 'interest']
        df_region = df_region[df_region['interest'] > 0]
        df_region['extracted_at'] = datetime.now()
        
        print(f"Obtenidos datos de {len(df_region)} paises")
        
        # Guardar
        df_region.to_csv(DATA_RAW / "trends_real.csv", index=False)
        print(f"Guardado: {DATA_RAW / 'trends_real.csv'}")
        
        time.sleep(2)
        
        # Tendencia temporal
        df_time = pytrends.interest_over_time()
        if not df_time.empty:
            df_time = df_time.reset_index()
            df_time.to_csv(DATA_RAW / "trends_time_real.csv", index=False)
            print(f"Guardado: {DATA_RAW / 'trends_time_real.csv'}")
        
        return df_region
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    extract_trends()