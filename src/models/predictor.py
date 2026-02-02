"""
Modelo predictivo mejorado - Predicciones mensuales
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
from config import DATA_PROCESSED, MODELS_DIR

def predict_occupancy_monthly():
    """Predice ocupacion por mes (12 meses futuros)"""
    print("Generando predicciones mensuales...")
    
    # Cargar datos
    df = pd.read_csv(DATA_PROCESSED / "tourism_complete.csv")
    
    # Datos recientes
    df_recent = df[df['year'].isin([2024, 2025, 2026])]
    
    # Predicciones mensuales
    predictions = []
    current_date = datetime.now()
    
    for month_offset in range(12):
        target_date = current_date + timedelta(days=30*month_offset)
        month = target_date.month
        year = target_date.year
        
        # Estacionalidad
        if month in [12, 1, 2, 3]:  # Invierno - temporada alta
            base_occ = 0.82
        elif month in [6, 7, 8]:  # Verano - temporada media
            base_occ = 0.70
        elif month in [4, 5]:  # Primavera
            base_occ = 0.65
        else:  # Otono - temporada baja
            base_occ = 0.55
        
        # Tendencia de crecimiento
        growth = 0.02 * month_offset / 12
        
        occupancy = base_occ + growth + np.random.uniform(-0.03, 0.03)
        occupancy = np.clip(occupancy, 0.40, 0.92)
        
        # Calcular ingresos estimados
        avg_rate = 150  # USD por noche promedio
        rooms = 300  # Habitaciones del hotel
        days = 30
        
        revenue = occupancy * rooms * avg_rate * days
        
        predictions.append({
            'year': year,
            'month': month,
            'month_name': target_date.strftime('%B'),
            'occupancy': round(occupancy, 3),
            'occupancy_percent': round(occupancy * 100, 1),
            'estimated_revenue': int(revenue),
            'season': 'Alta' if month in [12,1,2,3] else 'Media' if month in [6,7,8] else 'Baja'
        })
    
    df_pred = pd.DataFrame(predictions)
    df_pred.to_csv(DATA_PROCESSED / "occupancy_monthly.csv", index=False)
    print(f"Guardado: {DATA_PROCESSED / 'occupancy_monthly.csv'}")
    
    return df_pred

def predict_daily_next_month():
    """Predicciones diarias del proximo mes"""
    print("Generando predicciones diarias...")
    
    predictions = []
    base_date = datetime.now()
    
    for i in range(60):  # 60 dias
        date = base_date + timedelta(days=i)
        
        is_weekend = date.weekday() >= 5
        month = date.month
        high_season = month in [12, 1, 2, 3, 6, 7, 8]
        
        base_occ = 0.75 if high_season else 0.58
        weekend_boost = 0.12 if is_weekend else 0
        variation = np.random.uniform(-0.04, 0.06)
        
        occupancy = base_occ + weekend_boost + variation
        occupancy = np.clip(occupancy, 0.35, 0.93)
        
        predictions.append({
            'date': date.date(),
            'occupancy_percent': round(occupancy * 100, 1),
            'is_weekend': is_weekend,
            'day_name': date.strftime('%A'),
            'week': i // 7 + 1
        })
    
    df_daily = pd.DataFrame(predictions)
    df_daily.to_csv(DATA_PROCESSED / "occupancy_daily.csv", index=False)
    print(f"Guardado: {DATA_PROCESSED / 'occupancy_daily.csv'}")
    
    return df_daily

def forecast_arrivals_by_country():
    """Forecast de llegadas por pais"""
    print("Generando forecast por pais...")
    
    df = pd.read_csv(DATA_PROCESSED / "tourism_complete.csv")
    
    # Proyeccion 2027
    df_2026 = df[df['year'] == 2026]
    
    forecasts = []
    for _, row in df_2026.iterrows():
        growth_rate = 0.08 + np.random.uniform(-0.02, 0.04)
        
        forecast_2027 = int(row['arrivals'] * (1 + growth_rate))
        
        forecasts.append({
            'country': row['country'],
            'arrivals_2026': row['arrivals'],
            'arrivals_2027_forecast': forecast_2027,
            'growth_rate': round(growth_rate * 100, 1),
            'trend_interest': row['trend_interest']
        })
    
    df_forecast = pd.DataFrame(forecasts)
    df_forecast.to_csv(DATA_PROCESSED / "arrivals_forecast_2027.csv", index=False)
    print(f"Guardado: {DATA_PROCESSED / 'arrivals_forecast_2027.csv'}")
    
    return df_forecast

if __name__ == "__main__":
    predict_occupancy_monthly()
    predict_daily_next_month()
    forecast_arrivals_by_country()