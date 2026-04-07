# 🎭 enGira! · Análisis de campañas y estrategia de marketing digital

## 📌 Descripción del proyecto

Este proyecto tiene como objetivo analizar el rendimiento histórico de las campañas de **newsletter enviadas desde el lanzamiento de la plataforma enGira!** para extraer patrones de comportamiento y convertirlos en **insights accionables** que sirvan de base para una futura **campaña de marketing digital multicanal**.

La campaña estará orientada a dos grandes públicos:

- **Programadores/as de teatro**
- **Artistas / compañías escénicas**

Y persigue tres objetivos principales:

- **Atraer la atención de programadores/as de teatros**
- **Promocionar los programas de acompañamiento** (servicio de pago) entre artistas
- **Aumentar el número de registros en la plataforma** y el número de seguidores en redes sociales

---

## 🎯 Objetivos del proyecto

### Objetivo general
Diseñar una estrategia de marketing digital **basada en datos** para mejorar la captación, activación y conversión de usuarios en la plataforma **enGira!**.

### Objetivos específicos
- Analizar el rendimiento histórico de las campañas de e-mail marketing enviadas desde **Brevo**
- Detectar patrones de comportamiento y variables de éxito
- Segmentar audiencias y definir mensajes clave por público
- Diseñar una estrategia de campaña para:
  - **Instagram**
  - **LinkedIn**
  - **E-mail marketing**
  - **Sección Noticias / Blog** de la web de enGira!
- Definir un sistema de **KPIs**, **tracking** y visualización de resultados

---

## 🧰 Herramientas y tecnologías

Este proyecto se apoya en un stack de análisis y visualización de datos orientado a marketing:

- **Python**
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `seaborn`
- **SQL** *(si se integran varias fuentes de datos)*
- **Tableau** / **Power BI**
- **Jupyter Notebook**
- **Git & GitHub**
- **Brevo** (fuente de datos principal en esta fase)

---

## 🔍 Enfoque metodológico

El proyecto se estructura en cuatro grandes bloques:

1. **Análisis de campañas históricas**
2. **Definición estratégica**
3. **Diseño de campaña multicanal**
4. **Medición y optimización**

La lógica de trabajo parte de una idea clave:

> Antes de diseñar nuevas campañas, conviene entender qué ha funcionado ya y qué patrones de comportamiento existen en la base de usuarios actual.

---

## 📊 Métricas de interés

Durante el análisis se trabajará principalmente con métricas de e-mail marketing como:

- **Open Rate**
- **CTR**
- **Click-to-Open Rate (CTOR)**
- **Bounce Rate**
- **Unsubscribe Rate**
- **Conversiones** *(si la trazabilidad lo permite)*

Más adelante se incorporarán métricas relacionadas con:

- crecimiento de usuarios registrados
- tráfico web
- rendimiento en Instagram y LinkedIn
- captación de leads / solicitudes de acompañamiento

---

## 🗂️ Estructura del proyecto

```bash
engira-marketing-analytics/
│
├── README.md
├── .gitignore
│
├── data/
│   ├── raw/                # Exportaciones originales de Brevo
│   ├── interim/            # Datos intermedios / transformados
│   └── processed/          # Dataset final limpio para análisis
│
├── notebooks/
│   ├── 01_exploracion_datos.ipynb
│   ├── 02_limpieza_transformacion.ipynb
│   ├── 03_eda_newsletters.ipynb
│   └── 04_insights_segmentacion.ipynb
│
├── scripts/
│   ├── limpieza.py
│   ├── transformacion.py
│   └── analisis.py
│
├── outputs/
│   ├── graficos/
│   ├── tablas/
│   ├── informes/
│   └── dashboards/
│
└── docs/
    ├── backlog_proyecto.md
    ├── diccionario_variables.md
    └── estrategia_marketing.md
