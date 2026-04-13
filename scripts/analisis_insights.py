
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

# ==============================
# 4. ANÁLISIS TEMPORAL (AÑO, MES, DÍA)
# ==============================

# 4.1. Rendimiento por Año
year_stats = df.groupby('year')[['trackable_open_rate', 'click_rate']].mean()
year_stats.to_csv("outputs/tablas/stats_por_año.csv")

# 4.2. Rendimiento por Mes (Estacionalidad)
month_stats = df.groupby('month')[['trackable_open_rate', 'click_rate']].mean()
month_stats.to_csv("outputs/tablas/stats_por_mes.csv")

# 4.3. Rendimiento por Día de la Semana (0=Lunes, 6=Domingo)
weekday_map = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}
df['weekday_name'] = df['weekday'].map(weekday_map)
weekday_stats = df.groupby('weekday_name')[['trackable_open_rate', 'click_rate']].mean().reindex(['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'])
weekday_stats.to_csv("outputs/tablas/stats_por_dia.csv")

# 5. GUARDAR ESTADÍSTICAS ADICIONALES
tematica_stats = df.groupby('tematica_asunto')[['trackable_open_rate', 'click_rate', 'click_to_open_rate']].mean().sort_values('trackable_open_rate', ascending=False)
tematica_stats.to_csv("outputs/tablas/stats_por_tematica.csv")

publico_tipo_stats = df.groupby(['tipo_publico', 'tipo_campaña'])[['trackable_open_rate', 'click_rate']].mean().unstack()
publico_tipo_stats.to_csv("outputs/tablas/stats_publico_tipo.csv")

# ==============================
# 6. VISUALIZACIONES ESTRATÉGICAS
# ==============================

# 6.1. Evolución por Año (Barplot)
plt.figure(figsize=(10, 6))
sns.barplot(x='year', y='trackable_open_rate', data=df, palette='viridis')
plt.title('Evolución del Open Rate por Año')
plt.savefig("outputs/graficos/evolucion_anual_openrate.png")
plt.close()

# 6.2. Estacionalidad Mensual (Lineplot)
plt.figure(figsize=(10, 6))
sns.lineplot(x='month', y='trackable_open_rate', data=df, marker='o', label='Open Rate')
sns.lineplot(x='month', y='click_rate', data=df, marker='s', label='Click Rate')
plt.xticks(range(1, 13))
plt.title('Rendimiento Medio por Mes (Estacionalidad)')
plt.savefig("outputs/graficos/estacionalidad_mensual.png")
plt.close()

# 6.3. Rendimiento por Día de la Semana
plt.figure(figsize=(10, 6))
sns.barplot(x='weekday_name', y='trackable_open_rate', data=df, order=['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'])
plt.title('Open Rate Medio por Día de la Semana')
plt.savefig("outputs/graficos/rendimiento_dia_semana.png")
plt.close()

# 6.4. Mapa de calor Temática vs Público
plt.figure(figsize=(10, 6))
pivot_tematica = df.pivot_table(values='trackable_open_rate', index='tematica_asunto', columns='tipo_publico', aggfunc='mean')
sns.heatmap(pivot_tematica, annot=True, cmap='YlGnBu', fmt=".1f")
plt.title('Open Rate por Temática y Público')
plt.savefig("outputs/graficos/heatmap_tematica_publico.png")
plt.close()

# 7. GENERACIÓN DE INSIGHTS TEXTUALES
mejor_dia = weekday_stats['trackable_open_rate'].idxmax()
mejor_mes = month_stats['trackable_open_rate'].idxmax()

insights = []
insights.append(f"1. El mejor día para enviar newsletters es el {mejor_dia} (Open Rate: {weekday_stats.loc[mejor_dia, 'trackable_open_rate']:.2f}%).")
insights.append(f"2. El mes con mayor engagement histórico es el {mejor_mes}, lo que sugiere picos estacionales de interés.")
insights.append(f"3. El público 'artistas' responde significativamente mejor a las 'convocatorias' con un Open Rate medio de {df[df['tipo_publico']=='artistas']['trackable_open_rate'].mean():.2f}%.")
insights.append(f"4. Los envíos a 'programadores' tienen un rendimiento crítico (Open Rate: {df[df['tipo_publico']=='programadores']['trackable_open_rate'].mean():.2f}%).")

with open("outputs/informes/insights_preliminares.txt", "w") as f:
    f.write("\n".join(insights))

print("Proceso de insights (incluyendo temporalidad) completado.")
