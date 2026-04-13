
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Robustez para ventanas interactivas
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
except NameError:
    project_root = os.getcwd()

# Definir rutas
data_path = os.path.join(project_root, "data/processed/data_limpia.csv")
outputs_tablas = os.path.join(project_root, "outputs/tablas")
outputs_graficos = os.path.join(project_root, "outputs/graficos")
outputs_informes = os.path.join(project_root, "outputs/informes")

# Configuración visual
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# 1. CARGA DE DATOS
if not os.path.exists(data_path):
    raise FileNotFoundError(f"No se encontró el archivo en {data_path}")

df = pd.read_csv(data_path)
print(f"✅ Datos cargados correctamente ({len(df)} registros).")

# 2. SEGMENTACIÓN
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

# 3. TEMÁTICAS
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
# 4. GUARDADO DE TABLAS
# ==============================
df.groupby('year')[['trackable_open_rate', 'click_rate']].mean().to_csv(os.path.join(outputs_tablas, "stats_por_año.csv"))
df.groupby('month')[['trackable_open_rate', 'click_rate']].mean().to_csv(os.path.join(outputs_tablas, "stats_por_mes.csv"))

weekday_map = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}
df['weekday_name'] = df['weekday'].map(weekday_map)
weekday_stats = df.groupby('weekday_name')[['trackable_open_rate', 'click_rate']].mean().reindex(['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'])
weekday_stats.to_csv(os.path.join(outputs_tablas, "stats_por_dia.csv"))

print(f"📊 Tablas estadísticas guardadas en: {outputs_tablas}")

# ==============================
# 5. VISUALIZACIONES (GUARDAR Y MOSTRAR)
# ==============================

def finalizar_grafico(nombre_archivo):
    path = os.path.join(outputs_graficos, nombre_archivo)
    plt.savefig(path)
    print(f"🖼️ Gráfico guardado: {nombre_archivo}")
    plt.show() # Esto hace que se vea en la ventana interactiva
    plt.close()

# 5.1. Evolución por Año
plt.figure(figsize=(10, 5))
sns.barplot(x='year', y='trackable_open_rate', data=df, hue='year', palette='viridis', legend=False)
plt.title('Evolución del Open Rate por Año')
finalizar_grafico("evolucion_anual_openrate.png")

# 5.2. Estacionalidad Mensual
plt.figure(figsize=(10, 5))
sns.lineplot(x='month', y='trackable_open_rate', data=df, marker='o', label='Open Rate')
sns.lineplot(x='month', y='click_rate', data=df, marker='s', label='Click Rate')
plt.xticks(range(1, 13))
plt.title('Rendimiento Medio por Mes (Estacionalidad)')
finalizar_grafico("estacionalidad_mensual.png")

# 5.3. Rendimiento por Día de la Semana
plt.figure(figsize=(10, 5))
sns.barplot(x='weekday_name', y='trackable_open_rate', data=df, order=['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'], hue='weekday_name', palette='muted', legend=False)
plt.title('Open Rate Medio por Día de la Semana')
finalizar_grafico("rendimiento_dia_semana.png")

# 5.4. Mapa de calor
plt.figure(figsize=(10, 6))
pivot_tematica = df.pivot_table(values='trackable_open_rate', index='tematica_asunto', columns='tipo_publico', aggfunc='mean')
sns.heatmap(pivot_tematica, annot=True, cmap='YlGnBu', fmt=".1f")
plt.title('Open Rate por Temática y Público')
finalizar_grafico("heatmap_tematica_publico.png")

# ==============================
# 6. INFORME FINAL
# ==============================
mejor_dia = weekday_stats['trackable_open_rate'].idxmax()
month_stats = df.groupby('month')['trackable_open_rate'].mean()
mejor_mes = month_stats.idxmax()

insights = [
    f"1. El mejor día para enviar newsletters es el {mejor_dia}.",
    f"2. El mes con mayor engagement histórico es el {mejor_mes}.",
    f"3. Los artistas responden mejor a convocatorias ({df[df['tipo_publico']=='artistas']['trackable_open_rate'].mean():.1f}% OR).",
    f"4. El segmento programadores requiere optimización urgente ({df[df['tipo_publico']=='programadores']['trackable_open_rate'].mean():.1f}% OR)."
]

with open(os.path.join(outputs_informes, "insights_preliminares.txt"), "w") as f:
    f.write("\n".join(insights))

print(f"📝 Informe de insights actualizado en: {outputs_informes}")
print("\n" + "\n".join(insights))
