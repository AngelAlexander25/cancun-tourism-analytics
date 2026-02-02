"""
Dashboard Cancun Tourism Analytics - Version Completa
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

st.set_page_config(
    page_title="Cancun Tourism Analytics",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 3rem; font-weight: bold; color: #1f77b4;}
    .sub-header {font-size: 1.5rem; color: #555;}
    .metric-card {background-color: #f0f2f6; padding: 20px; border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

# Rutas
PROCESSED = Path("data/processed")

# Cargar datos
@st.cache_data
def load_data():
    tourism = pd.read_csv(PROCESSED / "tourism_complete.csv")
    occ_monthly = pd.read_csv(PROCESSED / "occupancy_monthly.csv")
    occ_daily = pd.read_csv(PROCESSED / "occupancy_daily.csv")
    forecast_2027 = pd.read_csv(PROCESSED / "arrivals_forecast_2027.csv")
    
    occ_daily['date'] = pd.to_datetime(occ_daily['date'])
    
    return tourism, occ_monthly, occ_daily, forecast_2027

tourism, occ_monthly, occ_daily, forecast_2027 = load_data()

# Sidebar
st.sidebar.title("Menu de Navegacion")
page = st.sidebar.radio("Selecciona una seccion:", 
    ["Dashboard Principal", "Predicciones Detalladas", "Analisis por Pais", "Forecast 2027"])

st.sidebar.markdown("---")
st.sidebar.info("""
**Fuentes de Datos:**
- Google Trends (Real)
- World Bank API (Real)
- Modelos Predictivos ML

**Actualizacion:** Cada 3 semanas
""")

# ============================================
# PAGINA 1: DASHBOARD PRINCIPAL
# ============================================
if page == "Dashboard Principal":
    st.markdown('<p class="main-header">✈️ Cancun Tourism Analytics</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Dashboard Integral de Analisis Turistico</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # KPIs Principales
    st.subheader("Metricas Clave 2026")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    tourism_2026 = tourism[tourism['year'] == 2026]
    total_arrivals = tourism_2026['arrivals'].sum()
    avg_occupancy = occ_monthly['occupancy_percent'].mean()
    top_country = tourism_2026.nlargest(1, 'arrivals')['country'].values[0]
    total_revenue = occ_monthly['estimated_revenue'].sum()
    
    with col1:
        st.metric("Llegadas 2026", f"{total_arrivals/1e6:.2f}M")
    with col2:
        st.metric("Ocupacion Promedio", f"{avg_occupancy:.1f}%")
    with col3:
        st.metric("Pais Principal", top_country)
    with col4:
        growth = ((tourism_2026['arrivals'].sum() - tourism[tourism['year']==2025]['arrivals'].sum()) / tourism[tourism['year']==2025]['arrivals'].sum() * 100)
        st.metric("Crecimiento Anual", f"+{growth:.1f}%")
    with col5:
        st.metric("Revenue Anual", f"${total_revenue/1e6:.1f}M")
    
    st.markdown("---")
    
    # Graficos principales
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Paises por Llegadas 2026")
        top10 = tourism_2026.nlargest(10, 'arrivals').sort_values('arrivals', ascending=True)
        fig = px.bar(
            top10,
            y='country',
            x='arrivals',
            orientation='h',
            title='',
            labels={'arrivals': 'Turistas', 'country': ''},
            color='arrivals',
            color_continuous_scale='Blues'
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader("Tendencia Historica 2020-2026")
        yearly = tourism.groupby('year')['arrivals'].sum().reset_index()
        fig = px.line(
            yearly,
            x='year',
            y='arrivals',
            markers=True,
            title=''
        )
        fig.add_scatter(
            x=yearly['year'], 
            y=yearly['arrivals'],
            mode='markers+text',
            text=yearly['arrivals'].apply(lambda x: f'{x/1e6:.1f}M'),
            textposition='top center',
            showlegend=False
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
    
    # Ocupacion mensual
    st.markdown("---")
    st.subheader("Ocupacion Hotelera por Mes (Proximos 12 Meses)")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=occ_monthly['month_name'],
        y=occ_monthly['occupancy_percent'],
        text=occ_monthly['occupancy_percent'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside',
        marker_color=occ_monthly['occupancy_percent'],
        marker=dict(
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Ocupacion %")
        )
    ))
    fig.update_layout(
        xaxis_title='Mes',
        yaxis_title='Ocupacion (%)',
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig, width='stretch')
    
    # Revenue por mes
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ingresos Estimados Mensuales")
        fig = px.area(
            occ_monthly,
            x='month_name',
            y='estimated_revenue',
            title='',
            labels={'estimated_revenue': 'Revenue (USD)', 'month_name': 'Mes'}
        )
        fig.update_traces(line_color='green', fillcolor='rgba(0,255,0,0.3)')
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader("Distribucion por Temporada")
        season_data = occ_monthly.groupby('season')['occupancy_percent'].mean().reset_index()
        fig = px.pie(
            season_data,
            names='season',
            values='occupancy_percent',
            title='',
            color_discrete_sequence=['#ff4444', '#ffaa00', '#00cc00']
        )
        st.plotly_chart(fig, width='stretch')

# ============================================
# PAGINA 2: PREDICCIONES DETALLADAS
# ============================================
elif page == "Predicciones Detalladas":
    st.markdown('<p class="main-header">📊 Predicciones Detalladas</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Predicciones diarias (proximos 60 dias)
    st.subheader("Prediccion Diaria de Ocupacion - Proximos 60 Dias")
    
    fig = go.Figure()
    
    # Linea principal
    fig.add_trace(go.Scatter(
        x=occ_daily['date'],
        y=occ_daily['occupancy_percent'],
        mode='lines',
        name='Ocupacion',
        line=dict(color='blue', width=2)
    ))
    
    # Resaltar fines de semana
    weekends = occ_daily[occ_daily['is_weekend']]
    fig.add_trace(go.Scatter(
        x=weekends['date'],
        y=weekends['occupancy_percent'],
        mode='markers',
        name='Fines de Semana',
        marker=dict(color='red', size=8, symbol='diamond')
    ))
    
    fig.update_layout(
        xaxis_title='Fecha',
        yaxis_title='Ocupacion (%)',
        hovermode='x unified',
        height=500
    )
    st.plotly_chart(fig, width='stretch')
    
    # Analisis por semana
    st.markdown("---")
    st.subheader("Ocupacion Promedio por Semana")
    
    weekly = occ_daily.groupby('week')['occupancy_percent'].agg(['mean', 'min', 'max']).reset_index()
    weekly['week'] = 'Semana ' + weekly['week'].astype(str)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=weekly['week'],
        y=weekly['mean'],
        name='Promedio',
        error_y=dict(
            type='data',
            symmetric=False,
            array=weekly['max'] - weekly['mean'],
            arrayminus=weekly['mean'] - weekly['min']
        )
    ))
    fig.update_layout(
        xaxis_title='',
        yaxis_title='Ocupacion (%)',
        height=400
    )
    st.plotly_chart(fig, width='stretch')
    
    # Comparativa Dias de Semana vs Fines de Semana
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ocupacion: Dias de Semana vs Fin de Semana")
        weekday_avg = occ_daily[~occ_daily['is_weekend']]['occupancy_percent'].mean()
        weekend_avg = occ_daily[occ_daily['is_weekend']]['occupancy_percent'].mean()
        
        comparison = pd.DataFrame({
            'Tipo': ['Dias de Semana', 'Fin de Semana'],
            'Ocupacion': [weekday_avg, weekend_avg]
        })
        
        fig = px.bar(
            comparison,
            x='Tipo',
            y='Ocupacion',
            text='Ocupacion',
            color='Ocupacion',
            color_continuous_scale='Viridis'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader("Proximos 7 Dias")
        next_7 = occ_daily.head(7)[['date', 'day_name', 'occupancy_percent', 'is_weekend']]
        next_7['Dia'] = next_7['date'].dt.strftime('%d/%m') + ' - ' + next_7['day_name']
        next_7['Ocupacion (%)'] = next_7['occupancy_percent']
        next_7['Tipo'] = next_7['is_weekend'].apply(lambda x: '🔴 Fin de Semana' if x else '🔵 Entre Semana')
        
        st.dataframe(
            next_7[['Dia', 'Ocupacion (%)', 'Tipo']],
            width='stretch',
            hide_index=True
        )

# ============================================
# PAGINA 3: ANALISIS POR PAIS
# ============================================
elif page == "Analisis por Pais":
    st.markdown('<p class="main-header">🌍 Analisis por Pais</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Selector de pais
    countries = sorted(tourism['country'].unique())
    selected_country = st.selectbox("Selecciona un pais:", countries, index=0)
    
    # Datos del pais
    country_data = tourism[tourism['country'] == selected_country]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        arrivals_2026 = country_data[country_data['year'] == 2026]['arrivals'].values[0]
        st.metric("Llegadas 2026", f"{arrivals_2026:,}")
    
    with col2:
        growth = ((country_data[country_data['year']==2026]['arrivals'].values[0] - 
                  country_data[country_data['year']==2025]['arrivals'].values[0]) / 
                 country_data[country_data['year']==2025]['arrivals'].values[0] * 100)
        st.metric("Crecimiento 2025-2026", f"{growth:+.1f}%")
    
    with col3:
        trend = country_data['trend_interest'].values[0]
        st.metric("Interes Google Trends", f"{trend}/100")
    
    st.markdown("---")
    
    # Evolucion historica del pais
    st.subheader(f"Evolucion de Llegadas - {selected_country}")
    
    fig = px.line(
        country_data,
        x='year',
        y='arrivals',
        markers=True,
        title=''
    )
    fig.add_scatter(
        x=country_data['year'],
        y=country_data['arrivals'],
        mode='markers+text',
        text=country_data['arrivals'].apply(lambda x: f'{x/1000:.0f}K'),
        textposition='top center',
        showlegend=False
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')
    
    # Comparacion con otros paises
    st.markdown("---")
    st.subheader("Comparacion con Otros Mercados (2026)")
    
    comparison = tourism[tourism['year'] == 2026][['country', 'arrivals', 'trend_interest']].sort_values('arrivals', ascending=False)
    
    # Resaltar pais seleccionado
    comparison['color'] = comparison['country'].apply(lambda x: 'Seleccionado' if x == selected_country else 'Otros')
    
    fig = px.bar(
        comparison,
        x='country',
        y='arrivals',
        color='color',
        title='',
        labels={'arrivals': 'Turistas', 'country': 'Pais'},
        color_discrete_map={'Seleccionado': 'red', 'Otros': 'lightblue'}
    )
    st.plotly_chart(fig, width='stretch')

# ============================================
# PAGINA 4: FORECAST 2027
# ============================================
else:
    st.markdown('<p class="main-header">🔮 Forecast 2027</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # KPIs Forecast
    col1, col2, col3 = st.columns(3)
    
    total_2027 = forecast_2027['arrivals_2027_forecast'].sum()
    avg_growth = forecast_2027['growth_rate'].mean()
    
    with col1:
        st.metric("Proyeccion Total 2027", f"{total_2027/1e6:.2f}M")
    with col2:
        st.metric("Crecimiento Promedio", f"+{avg_growth:.1f}%")
    with col3:
        top_growth = forecast_2027.nlargest(1, 'growth_rate')
        st.metric("Mayor Crecimiento", f"{top_growth['country'].values[0]} (+{top_growth['growth_rate'].values[0]:.1f}%)")
    
    st.markdown("---")
    
    # Comparativa 2026 vs 2027
    st.subheader("Comparativa 2026 vs 2027 (Forecast)")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=forecast_2027['country'],
        y=forecast_2027['arrivals_2026'],
        name='2026 (Real)',
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        x=forecast_2027['country'],
        y=forecast_2027['arrivals_2027_forecast'],
        name='2027 (Forecast)',
        marker_color='darkblue'
    ))
    
    fig.update_layout(
        barmode='group',
        xaxis_title='Pais',
        yaxis_title='Turistas',
        height=500
    )
    st.plotly_chart(fig, width='stretch')
    
    # Tabla detallada
    st.markdown("---")
    st.subheader("Detalle por Pais")
    
    display = forecast_2027.copy()
    display['Pais'] = display['country']
    display['Llegadas 2026'] = display['arrivals_2026'].apply(lambda x: f'{x:,}')
    display['Forecast 2027'] = display['arrivals_2027_forecast'].apply(lambda x: f'{x:,}')
    display['Crecimiento (%)'] = display['growth_rate'].apply(lambda x: f'+{x:.1f}%')
    display['Interes Google'] = display['trend_interest']
    
    st.dataframe(
        display[['Pais', 'Llegadas 2026', 'Forecast 2027', 'Crecimiento (%)', 'Interes Google']],
        width='stretch',
        hide_index=True
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888;'>
    <p><b>Cancun Tourism Analytics Dashboard</b></p>
    <p>Datos actualizados automaticamente cada 3 semanas via GitHub Actions</p>
    <p>Fuentes: Google Trends (Real) | World Bank API (Real) | Modelos Predictivos ML</p>
</div>
""", unsafe_allow_html=True)