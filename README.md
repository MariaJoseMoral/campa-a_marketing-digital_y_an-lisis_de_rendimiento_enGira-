# 🎭 enGira! · Análisis de campañas y estrategia de marketing digital

## 📌 Descripción del proyecto

Este proyecto tiene como objetivo analizar el rendimiento histórico de las campañas de **newsletter enviadas desde el lanzamiento de la plataforma enGira!** para extraer patrones de comportamiento y convertirlos en **insights accionables** que sirvan de base para una futura **campaña de marketing digital multicanal**.

La campaña está orientada a dos grandes públicos (Artistas y Programadores) y busca optimizar la captación de leads y la conversión a programas de acompañamiento profesional.

---

## 🎯 Objetivos del proyecto

- **Analizar el rendimiento histórico** (2024-2026) de e-mail marketing.
- **Segmentar audiencias** y definir mensajes clave basados en datos reales.
- **Diseñar una estrategia multicanal** (Email, Instagram, LinkedIn, Web) alineada con los hallazgos.
- **Establecer un sistema de KPIs** y tracking para la toma de decisiones.

---

## 📈 Resultados y Hallazgos Clave

Tras procesar y analizar más de 50 campañas históricas, se han obtenido los siguientes KPIs generales:

*   **Open Rate (Apertura) Medio:** 68.9%
*   **CTR (Clics) Medio:** 17.7%

### 🔍 Insights Estratégicos

1.  **Dominio de las Convocatorias:** Las campañas con temática de convocatorias abiertas son las más exitosas, alcanzando un **Open Rate récord del 92.3%**.
2.  **Momento de Envío Óptimo:** El análisis temporal revela que los **Viernes** son los días con mayor tasa de apertura (**94.1%**), seguidos por los Martes.
3.  **Estacionalidad:** Se observa un pico de engagement en el mes de **Abril**, coincidiendo con periodos clave de planificación en el sector cultural.
4.  **Brecha de Engagement:** Existe una asimetría crítica entre públicos. Mientras los **Artistas** mantienen un Open Rate medio del **87.9%**, los **Programadores** se sitúan en un **30.6%**.
5.  **Temáticas Ganadoras:** Las campañas de formación y recursos prácticos (como el *Toolkit*) generan un interés sostenido.

---

## 🖼️ Visualizaciones Destacadas

Los análisis se apoyan en visualizaciones clave que permiten entender el comportamiento de los usuarios de un vistazo:

### 1. Mapa de Calor: Temática vs Público
![Mapa de Calor Temática vs Público](outputs/graficos/heatmap_tematica_publico.png)

### 2. Estacionalidad Mensual
Muestra los picos de apertura y clics a lo largo del año, permitiendo planificar las campañas en los meses de mayor receptividad.
![Estacionalidad Mensual](outputs/graficos/estacionalidad_mensual.png)

### 3. Rendimiento por Día de la Semana
Identifica claramente el Viernes como el día "estrella" para las comunicaciones de enGira!.
![Rendimiento por Día de la Semana](outputs/graficos/rendimiento_dia_semana.png)

### 4. Evolución Anual del Open Rate
Permite visualizar el crecimiento y la consolidación del interés de la audiencia desde 2024.
![Evolución Anual Open Rate](outputs/graficos/evolucion_anual_openrate.png)

---

## 🧰 Herramientas y tecnologías

- **Python:** `pandas`, `numpy`, `matplotlib`, `seaborn` para limpieza y análisis.
- **Jupyter Notebook:** Para el desarrollo iterativo del EDA e insights.
- **Brevo:** Fuente de datos original.
- **Git & GitHub:** Control de versiones y documentación.

---

## 🗂️ Estructura del proyecto

```bash
engira-marketing-analytics/
│
├── notebooks/
│   ├── 02_limpieza_transformacion.ipynb    # Procesamiento del dataset original
│   ├── 03_eda_newsletters.ipynb            # Análisis exploratorio profundo
│   └── 04_insights_segmentacion.ipynb     # Segmentación y conclusiones
│
├── scripts/
│   ├── analisis_insights.py                # Script de generación de informes y gráficos
│   └── limpieza.py                         # Lógica de limpieza modularizada
│
├── outputs/                                # Resultados del análisis (Ignorado en git)
│   ├── graficos/                           # PNGs de visualizaciones
│   ├── tablas/                             # CSVs de estadísticas agrupadas
│   └── informes/                           # Insights textuales resumidos
│
└── docs/
    ├── diccionario_variables.md            # Definición de métricas y origen
    └── estrategia_marketing.md             # Documento de estrategia multicanal
```

---

## 🚀 Próximos Pasos

- **Automatización:** Implementar secuencias de bienvenida basadas en los contenidos con mayor engagement.
- **LinkedIn Strategy:** Desarrollar contenidos específicos para el sector "Programadores" basados en el insight de baja apertura en email.
- **Dashboarding:** Migrar las visualizaciones estáticas a un panel interactivo en Tableau/Power BI.

---

## 👩‍💻 Autora
**Maria Moral** - Especialista en análisis de datos aplicado a la gestión cultural y marketing digital.
