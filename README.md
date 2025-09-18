# almacenamiento-hibrido-informe

# Informe y Simulación de Soluciones de Almacenamiento (HDD, SSD, Cinta, Nube)

Proyecto web para publicar un informe técnico y una app en Streamlit que:
- Muestra el informe completo (negocio y tecnología).
- Compara tecnologías con tablas y gráficos (matplotlib, un gráfico por figura y sin fijar colores).
- Ejecuta una simulación sencilla de crecimiento y tiempos estimados por tecnología.

## Cómo ejecutar en Streamlit Community Cloud
1. Asegúrate de que existen estos archivos:
   - `streamlit_app.py`
   - `requirements.txt`
   - `docs/INFORME.md`
   - `data/supuestos.csv`
2. En https://streamlit.io → Sign in → “New app”
3. Selecciona este repositorio, branch `main`, file path `streamlit_app.py` y despliega.

## Estructura

├─ README.md
├─ requirements.txt
├─ streamlit_app.py
├─ data/
│ ├─ supuestos.csv
│ └─ README.md
└─ docs/
└─ INFORME.md

