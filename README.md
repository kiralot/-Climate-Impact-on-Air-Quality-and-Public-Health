# Impacto del Cambio Climático en la Calidad del Aire y la Salud

Análisis de cómo las variaciones climáticas y las políticas medioambientales han afectado la calidad del aire y la salud pública en distintos países durante 1990-2019.

## Estructura del Proyecto

```
global-weather-analysis/
├── data/
│   ├── raw/                      # Datos originales sin procesar
│   ├── processed/                # Datos procesados
│   └── external/                 # Datos externos descargados
├── scripts/                      # Scripts de procesamiento
│   ├── 01_select_countries.py   # Selección de países para análisis
│   └── utils/                    # Funciones auxiliares
├── notebooks/                    # Jupyter notebooks para exploración
├── src/                          # Código fuente modular
├── models/                       # Modelos entrenados
├── results/                      # Resultados y visualizaciones
│   ├── figures/
│   └── reports/
└── dashboard/                    # Dashboard interactivo
```

## Objetivos

1. Analizar la evolución temporal de contaminantes atmosféricos
2. Correlacionar niveles de contaminación con variables climáticas
3. Explorar efectos sobre la salud pública
4. Predecir niveles de contaminación mediante modelos de series temporales
5. Crear un dashboard interactivo para comparar países

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

1. Crea un archivo `.env` con tus credenciales de Copernicus CDS:
```
CDS_URL=https://cds.climate.copernicus.eu/api
CDS_API_KEY=tu_api_key_aqui
```

2. El archivo `.env` está incluido en `.gitignore` y no se subirá a GitHub.

## Uso

1. Seleccionar países para análisis:
```bash
python scripts/01_select_countries.py
```

## Datos

- Mortalidad por causas: 1990-2019, 204 países
- Países seleccionados: 50 países (10 por continente)
- Variables climáticas: temperatura, precipitación, humedad
- Contaminantes: NO₂, PM2.5, PM10, O₃, CO, SO₂

## Autor

Ignacio

## Licencia

MIT
