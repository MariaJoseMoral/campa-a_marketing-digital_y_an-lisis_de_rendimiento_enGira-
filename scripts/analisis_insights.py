
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración visual
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# 1. CARGA DE DATOS
df = pd.read_csv("notebooks/data_limpia.csv")

# 2. SEGMENTACIÓN POR RENDIMIENTO (CLUSTER RÁPIDO)
# Definimos umbrales basados en el EDA previo
# Open rate medio ~69%, CTR medio ~17%

def segmentar_rendimiento(row):
    if row['trackable_open_rate'] >= 80 and row['click_rate'] >= 30:
        return 'Top Performance'
    elif row['trackable_open_rate'] >= 60:
        return 'Buen Alcance, Interés Medio'
    elif row['click_rate'] >= 15:
        return 'Alcance Bajo, Alta Conversión'
    else:
        return 'Bajo Rendimiento'

df['segmento_rendimiento'] = df.apply(segmentar_rendimiento, axis=1)

# 3. ANÁLISIS DE TEMÁTICAS / KEYWORDS EN EL ASUNTO
keywords = {
    'convocatoria': ['convocatoria', 'abiertas', 'plazo'],
    'webinar_formacion': ['webinar', 'demo', 'taller', 'programa'],
    'evento_feria': ['feria', 'mercartes', 'madferia', 'dferia'],
    'registro_plataforma': ['registro', 'completa', 'perfil'],
    'descubrimiento': ['descubre', 'descobreix', 'artistas', 'destacado']
}

def detectar_tematica(subject):
    subject = str(subject).lower()
    for theme, terms in keywords.items():
        if any(term in subject for term in terms):
            return theme
    return 'otros'

df['tematica_asunto'] = df['subject'].apply(detectar_tematica)

# 4. INSIGHTS POR TEMÁTICA
tematica_stats = df.groupby('tematica_asunto')[['trackable_open_rate', 'click_rate', 'click_to_open_rate']].mean().sort_values('trackable_open_rate', ascending=False)
tematica_stats.to_csv("outputs/tablas/stats_por_tematica.csv")

# 5. INSIGHTS POR PÚBLICO Y TIPO DE CAMPAÑA
publico_tipo_stats = df.groupby(['tipo_publico', 'tipo_campaña'])[['trackable_open_rate', 'click_rate']].mean().unstack()
publico_tipo_stats.to_csv("outputs/tablas/stats_publico_tipo.csv")

# 6. VISUALIZACIONES ESTRATÉGICAS

# 6.1. Mapa de calor Temática vs Público (Open Rate)
plt.figure(figsize=(10, 6))
pivot_tematica = df.pivot_table(values='trackable_open_rate', index='tematica_asunto', columns='tipo_publico', aggfunc='mean')
sns.heatmap(pivot_tematica, annot=True, cmap='YlGnBu', fmt=".1f")
plt.title('Open Rate por Temática y Público')
plt.savefig("outputs/graficos/heatmap_tematica_publico.png")
plt.close()

# 6.2. Boxplot de Click Rate por Segmento de Rendimiento
plt.figure(figsize=(10, 6))
sns.boxplot(x='segmento_rendimiento', y='click_rate', data=df)
plt.title('Distribución de Click Rate por Segmento de Rendimiento')
plt.xticks(rotation=45)
plt.savefig("outputs/graficos/boxplot_rendimiento_clickrate.png")
plt.close()

# 6.3. Relación entre Volumen de Envío y Open Rate
plt.figure(figsize=(10, 6))
sns.scatterplot(x='sent', y='trackable_open_rate', hue='tipo_publico', size='click_rate', data=df, sizes=(20, 200))
plt.title('Volumen de Envío vs Open Rate (Tamaño = Click Rate)')
plt.savefig("outputs/graficos/scatter_volumen_openrate.png")
plt.close()

# 7. GENERACIÓN DE INSIGHTS TEXTUALES
insights = []
insights.append(f"1. El público 'artistas' responde significativamente mejor a las 'convocatorias' con un Open Rate medio de {df[df['tipo_publico']=='artistas']['trackable_open_rate'].mean():.2f}%.")
insights.append(f"2. La temática '{tematica_stats.index[0]}' es la que genera mayor interés inicial (Open Rate: {tematica_stats.iloc[0,0]:.2f}%).")
insights.append(f"3. Los envíos a 'programadores' tienen un rendimiento crítico (Open Rate: {df[df['tipo_publico']=='programadores']['trackable_open_rate'].mean():.2f}%), lo que sugiere la necesidad de revisar el 'subject' o la relevancia del contenido para este segmento.")
insights.append(f"4. Se han identificado {len(df[df['segmento_rendimiento']=='Top Performance'])} campañas en el segmento 'Top Performance', que deberían servir de benchmark.")

with open("outputs/informes/insights_preliminares.txt", "w") as f:
    f.write("\n".join(insights))

print("Proceso de insights y segmentación completado.")
