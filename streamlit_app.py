import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Almacenamiento: Informe y Simulación", layout="wide")

# --------------------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------------------
DATA_CSV = Path("data/supuestos.csv")
INFORME_MD = Path("docs/INFORME.md")

DEFAULT_DATA = pd.DataFrame({
    "tecnologia": ["HDD", "SSD", "Cinta", "Nube"],
    "lectura_mb_s": [200, 2500, 250, 300],
    "escritura_mb_s": [170, 1800, 200, 250],
    "capacidad_tb": [20, 8, 30, 1_000_000],
    "costo_gb_usd": [0.035, 0.15, 0.008, 0.025],
    "mtbf_h": [1_200_000, 1_500_000, 2_000_000, 0],  # 0 para nube (N/A)
    "consumo_w": [8, 4, 7, 0],
    "seguridad_q": [3, 4, 2, 5],
    "escalabilidad_q": [3, 3, 2, 5],
})

def load_data():
    if DATA_CSV.exists():
        try:
            df = pd.read_csv(DATA_CSV)
            # Validación de columnas mínimas
            required = set(DEFAULT_DATA.columns)
            if not required.issubset(set(df.columns)):
                st.warning("`data/supuestos.csv` no tiene todas las columnas esperadas. Se usarán valores por defecto.")
                return DEFAULT_DATA.copy()
            return df
        except Exception as e:
            st.warning(f"No se pudo leer `data/supuestos.csv`: {e}. Se usan valores por defecto.")
            return DEFAULT_DATA.copy()
    else:
        st.info("No se encontró `data/supuestos.csv`. Se usan valores por defecto.")
        return DEFAULT_DATA.copy()

def load_informe():
    if INFORME_MD.exists():
        try:
            return INFORME_MD.read_text(encoding="utf-8")
        except Exception as e:
            st.warning(f"No se pudo leer `docs/INFORME.md`: {e}. Se muestra resumen mínimo.")
    return (
        "# Informe (resumen mínimo)\n"
        "Consulte `docs/INFORME.md` para el informe completo con metodología, comparación, gráficos y simulación.\n"
    )

def normalize_to_1_5(series):
    # Excluye ceros para normalización de MTBF (p. ej., nube N/A)
    s = series.replace(0, np.nan)
    min_v = s.min()
    max_v = s.max()
    if pd.isna(min_v) or pd.isna(max_v) or max_v == min_v:
        return pd.Series([3] * len(series), index=series.index)  # neutral
    scaled = 1 + 4 * (s - min_v) / (max_v - min_v)
    return scaled.fillna(0)  # 0 para los N/A (p. ej., nube en MTBF)

# --------------------------------------------------------------------------------------
# Encabezado
# --------------------------------------------------------------------------------------
st.title("Soluciones de Almacenamiento: Informe, Comparativa y Simulación")
st.write("Proyecto educativo. Gráficos con matplotlib, un gráfico por figura y sin fijar colores.")

# --------------------------------------------------------------------------------------
# Sidebar: parámetros de simulación
# --------------------------------------------------------------------------------------
st.sidebar.header("Parámetros de simulación")
V0 = st.sidebar.number_input("Volumen inicial (TB)", min_value=1.0, value=100.0, step=10.0)
growth_pct = st.sidebar.number_input("Crecimiento anual (%)", min_value=0.0, value=20.0, step=1.0)
years = st.sidebar.number_input("Horizonte (años)", min_value=1, max_value=15, value=5, step=1)

# --------------------------------------------------------------------------------------
# Cargar datos e informe
# --------------------------------------------------------------------------------------
df = load_data()
informe_md = load_informe()

# --------------------------------------------------------------------------------------
# Sección: Informe
# --------------------------------------------------------------------------------------
with st.expander("Ver informe (docs/INFORME.md)", expanded=False):
    st.markdown(informe_md)

st.subheader("Tabla comparativa (desde data/supuestos.csv)")
st.caption("Valores de referencia. Ver etiquetas [Inference]/[Unverified] en el informe.")
st.dataframe(df, use_container_width=True)

# --------------------------------------------------------------------------------------
# Gráfico: Lectura (MB/s)
# --------------------------------------------------------------------------------------
fig1, ax1 = plt.subplots()
ax1.bar(df["tecnologia"], df["lectura_mb_s"])
ax1.set_title("Velocidad de lectura (MB/s)")
ax1.set_xlabel("Tecnología")
ax1.set_ylabel("MB/s")
st.pyplot(fig1)

# --------------------------------------------------------------------------------------
# Gráfico: Escritura (MB/s)
# --------------------------------------------------------------------------------------
fig2, ax2 = plt.subplots()
ax2.bar(df["tecnologia"], df["escritura_mb_s"])
ax2.set_title("Velocidad de escritura (MB/s)")
ax2.set_xlabel("Tecnología")
ax2.set_ylabel("MB/s")
st.pyplot(fig2)

# --------------------------------------------------------------------------------------
# Gráfico: Costo por GB (USD)
# --------------------------------------------------------------------------------------
fig3, ax3 = plt.subplots()
ax3.bar(df["tecnologia"], df["costo_gb_usd"])
ax3.set_title("Costo por GB (USD)")
ax3.set_xlabel("Tecnología")
ax3.set_ylabel("USD/GB")
st.pyplot(fig3)

# --------------------------------------------------------------------------------------
# Gráfico: Radar (Fiabilidad normalizada 1–5, Escalabilidad 1–5, Seguridad 1–5)
# Nota: Nube tiene MTBF = 0 (N/A) y quedará en 0 para fiabilidad.
# --------------------------------------------------------------------------------------
cats = ["Fiabilidad", "Escalabilidad", "Seguridad"]
fiab = normalize_to_1_5(df["mtbf_h"])
esc = df["escalabilidad_q"]
seg = df["seguridad_q"]

# Radar para cada tecnología
import math
angles = np.linspace(0, 2 * math.pi, len(cats), endpoint=False).tolist()
angles += angles[:1]  # cerrar

fig4 = plt.figure()
ax4 = plt.subplot(111, polar=True)
for i, row in df.iterrows():
    vals = [
        fiab.iloc[i],
        esc.iloc[i],
        seg.iloc[i],
    ]
    vals += vals[:1]
    ax4.plot(angles, vals, label=row["tecnologia"])
    ax4.fill(angles, vals, alpha=0.1)
ax4.set_xticks(angles[:-1])
ax4.set_xticklabels(cats)
ax4.set_yticklabels([])  # sin forzar valores de eje
ax4.set_title("Radar: Fiabilidad (1–5), Escalabilidad (1–5), Seguridad (1–5)")
ax4.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1))
st.pyplot(fig4)

st.caption("Normalización de Fiabilidad: 1 al mínimo MTBF y 5 al máximo; Nube se trata como N/A (0 en este radar).")

# --------------------------------------------------------------------------------------
# Simulación
# --------------------------------------------------------------------------------------
st.subheader("Simulación de crecimiento y tiempos aproximados [Inference]")

growth = growth_pct / 100.0
years_range = list(range(1, years + 1))
vols = [V0 * ((1 + growth) ** (n - 1)) for n in years_range]

# Velocidades de lectura por tecnología
speeds = dict(zip(df["tecnologia"], df["lectura_mb_s"]))

def time_hours(volume_tb, speed_mb_s):
    if speed_mb_s <= 0:
        return np.nan
    return (volume_tb * 1_000_000) / speed_mb_s / 3600.0

results = []
techs = ["HDD", "SSD", "Cinta", "Nube"]
for n, vol in zip(years_range, vols):
    row = {"Año": n, "Volumen (TB)": round(vol, 2)}
    for t in techs:
        row[f"Tiempo {t} (h)"] = round(time_hours(vol, speeds.get(t, np.nan)), 2)
    results.append(row)

sim_df = pd.DataFrame(results)
st.dataframe(sim_df, use_container_width=True)

st.write(
    "Interpretación ejecutiva: a medida que el volumen crece, los tiempos basados en lectura secuencial aumentan. "
    "SSD mantiene tiempos inferiores, HDD y cinta se degradan antes, y la nube depende adicionalmente de la conectividad."
)

# --------------------------------------------------------------------------------------
# Conclusiones
# --------------------------------------------------------------------------------------
st.subheader("Conclusiones y próximos pasos")
st.write("- Priorizar arquitectura híbrida: SSD (crítico), HDD (activo), Cinta (archivo), Nube (elasticidad/DR).")
st.write("- Ejecutar PoC, validar costes reales con proveedores, pruebas de carga, y definir métricas (SLA, TCO, RPO/RTO).")

st.markdown("---")
st.caption("Código educativo. Gráficos con matplotlib. Sin seaborn. Un gráfico por figura. Sin colores fijados.")
