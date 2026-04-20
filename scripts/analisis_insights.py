
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Añadir la raíz del proyecto al sys.path para permitir importaciones de 'scripts'
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from scripts.utils import segmentar_rendimiento, detectar_tematica_asunto

def generar_insights(project_root, show_plots=True):
    """
    Realiza el análisis de datos, genera visualizaciones y guarda informes.
    """
    # Definir rutas
    data_path = os.path.join(project_root, "data/processed/data_limpia.csv")
    outputs_tablas = os.path.join(project_root, "outputs/tablas")
    outputs_graficos = os.path.join(project_root, "outputs/graficos")
    outputs_informes = os.path.join(project_root, "outputs/informes")

    # Asegurar directorios
    for d in [outputs_tablas, outputs_graficos, outputs_informes]:
        os.makedirs(d, exist_ok=True)

    # Configuración visual
    sns.set(style="whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)

    # 1. CARGA DE DATOS
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"No se encontró el archivo en {data_path}")

    df = pd.read_csv(data_path)
    print(f"✅ Datos cargados correctamente ({len(df)} registros).")

    # 2. FILTRADO Y SEGMENTACIÓN
    # Identificar campañas con volumen insuficiente (<50 envíos)
    invalid_campaigns = df[df['sent'] < 50]['campaign_name'].unique()
    
    # Aplicar segmentación de rendimiento
    df['segmento_rendimiento'] = df.apply(lambda row: segmentar_rendimiento(row, invalid_campaigns), axis=1)

    # Aplicar detección de temática específica del asunto
    df['tematica_asunto'] = df['subject'].apply(detectar_tematica_asunto)

    # --- NUEVAS MÉTRICAS DE NEGOCIO ---
    # 2.1. Engagement Score
    df['engagement_score'] = (df['trackable_open_rate'] * 0.3) + (df['click_rate'] * 0.7)

    # 2.2. Outliers de Éxito (Click Rate > media + 2*std)
    umbral_click = df['click_rate'].mean() + (2 * df['click_rate'].std())
    campanas_top = df[df['click_rate'] > umbral_click][['subject', 'tipo_campaña', 'sending_date', 'click_rate', 'engagement_score']]
    campanas_top.sort_values('engagement_score', ascending=False).to_csv(os.path.join(outputs_tablas, "campañas_top.csv"), index=False)

    # 2.3. Correlación Volumen vs Open Rate
    correlacion_vol = df['sent'].corr(df['trackable_open_rate'])

    # ==============================
    # 3. GUARDADO DE TABLAS
    # ==============================
    # Estadísticas anuales y mensuales
    df.groupby('year')[['trackable_open_rate', 'click_rate', 'engagement_score']].mean().to_csv(os.path.join(outputs_tablas, "stats_por_año.csv"))
    df.groupby('month')[['trackable_open_rate', 'click_rate', 'engagement_score']].mean().to_csv(os.path.join(outputs_tablas, "stats_por_mes.csv"))

    # Rendimiento por día de la semana
    # La columna 'weekday' ya contiene los nombres en español según la inspección de datos
    df['weekday_name'] = df['weekday']
    weekday_stats = df.groupby('weekday_name')[['trackable_open_rate', 'click_rate', 'engagement_score']].mean().reindex(['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'])
    # Eliminar filas con NaN si algún día no tiene datos
    weekday_stats = weekday_stats.dropna(subset=['engagement_score'])
    weekday_stats.to_csv(os.path.join(outputs_tablas, "stats_por_dia.csv"))

    # Estadísticas por temática y público
    df.groupby('tipo_campaña')[['trackable_open_rate', 'click_rate', 'engagement_score']].mean().sort_values('engagement_score', ascending=False).to_csv(os.path.join(outputs_tablas, "stats_por_tematica.csv"))
    df.groupby('tipo_publico')[['trackable_open_rate', 'click_rate', 'engagement_score']].mean().to_csv(os.path.join(outputs_tablas, "stats_publico_tipo.csv"))

    print(f"📊 Tablas estadísticas guardadas en: {outputs_tablas}")

    # ==============================
    # 4. VISUALIZACIONES
    # ==============================
    # (El resto de visualizaciones se mantienen, añadimos una nueva para Engagement)
    
    def finalizar_grafico(nombre_archivo):
        path = os.path.join(outputs_graficos, nombre_archivo)
        plt.savefig(path)
        print(f"🖼️ Gráfico guardado: {nombre_archivo}")
        if show_plots:
            plt.show()
        plt.close()

    # 4.1. Engagement Score por Temática
    plt.figure(figsize=(10, 5))
    sns.barplot(x='engagement_score', y='tipo_campaña', data=df, hue='tipo_campaña', palette='magma', legend=False)
    plt.title('Engagement Score Medio por Temática de Campaña')
    finalizar_grafico("engagement_por_tematica.png")

    # 4.2. Evolución por Año
    # ... (mantener previos o simplificar si es necesario)

    # 4.2. Estacionalidad Mensual
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='month', y='trackable_open_rate', data=df, marker='o', label='Open Rate')
    sns.lineplot(x='month', y='click_rate', data=df, marker='s', label='Click Rate')
    plt.xticks(range(1, 13))
    plt.title('Rendimiento Medio por Mes (Estacionalidad)')
    finalizar_grafico("estacionalidad_mensual.png")

    # 4.3. Rendimiento por Día de la Semana
    plt.figure(figsize=(10, 5))
    sns.barplot(x='weekday_name', y='trackable_open_rate', data=df, order=['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'], hue='weekday_name', palette='muted', legend=False)
    plt.title('Open Rate Medio por Día de la Semana')
    finalizar_grafico("rendimiento_dia_semana.png")

    # 4.4. Rendimiento por Segmento de Público (Boxplot)
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='tipo_publico', y='click_rate', data=df, hue='tipo_publico', palette='Set3', legend=False)
    plt.title('Distribución de Click Rate por Público')
    finalizar_grafico("boxplot_rendimiento_clickrate.png")

    # 4.5. Mapa de calor: Temática vs Público
    plt.figure(figsize=(10, 6))
    pivot_tematica = df.pivot_table(values='trackable_open_rate', index='tematica_asunto', columns='tipo_publico', aggfunc='mean')
    sns.heatmap(pivot_tematica, annot=True, cmap='YlGnBu', fmt=".1f")
    plt.title('Open Rate por Temática de Asunto y Público')
    finalizar_grafico("heatmap_tematica_publico.png")

    # 4.6. Scatter plot: Volumen vs Open Rate
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='sent', y='trackable_open_rate', data=df, hue='tipo_publico', size='click_rate', sizes=(20, 200))
    plt.title('Relación Volumen de Envío vs Open Rate')
    finalizar_grafico("scatter_volumen_openrate.png")

    # ==============================
    # 5. INFORME Y RECOMENDACIONES
    # ==============================
    mejor_dia = weekday_stats['engagement_score'].idxmax()
    mejor_tematica = df.groupby('tipo_campaña')['engagement_score'].mean().idxmax()
    mejor_mes = df.groupby('month')['engagement_score'].mean().idxmax()
    
    # Análisis de correlación para recomendaciones
    correlacion_msg = "Existe una correlación negativa moderada" if correlacion_vol < -0.3 else "No hay una correlación clara"
    if correlacion_vol > 0.3: correlacion_msg = "Existe una correlación positiva"

    top_perf_count = len(df[df['segmento_rendimiento'] == 'Top Performance'])
    
    # 5.1. Informe de Insights (Existente)
    insights = [
        "--- INFORME ESTRATÉGICO MARKETING DIGITAL ---",
        f"1. El mejor día para maximizar el engagement es el {mejor_dia}.",
        f"2. El mes con mayor engagement histórico es el mes {mejor_mes}.",
        f"3. La temática con mejor desempeño (Engagement Score) es: {mejor_tematica}.",
        f"4. Correlación Volumen-Apertura: {correlacion_vol:.2f} ({correlacion_msg}).",
        f"5. Se han identificado {top_perf_count} campañas de 'Top Performance'.",
        f"6. {len(campanas_top)} campañas son consideradas 'Outliers de Éxito' (>2 std en Click Rate)."
    ]

    with open(os.path.join(outputs_informes, "insights_finales.txt"), "w") as f:
        f.write("\n".join(insights))

    # 5.2. Recomendaciones Automatizadas (Nuevo)
    recomendaciones = [
        "--- RECOMENDACIONES ESTRATÉGICAS BASADAS EN DATOS ---",
        f"- PRIORIZACIÓN: Enfocar esfuerzos en la temática '{mejor_tematica}', que lidera el engagement score.",
        f"- CALENDARIO: Programar envíos preferentemente los {mejor_dia} para optimizar la tasa de apertura y clics.",
        f"- VOLUMEN: {'Reducir el tamaño de las listas para aumentar el OR' if correlacion_vol < -0.4 else 'El volumen de envío no parece penalizar drásticamente la apertura'}.",
        f"- CONTENIDO: Analizar los asuntos de las {len(campanas_top)} campañas top para replicar patrones de éxito.",
        "- SEGMENTACIÓN: Los artistas muestran mayor receptividad inicial; los programadores requieren contenido más orientado a la conversión directa (click rate)."
    ]

    with open(os.path.join(outputs_informes, "recomendaciones_estrategicas.txt"), "w") as f:
        f.write("\n".join(recomendaciones))

    print(f"📝 Informes actualizados en: {outputs_informes}")
    print("\n" + "\n".join(insights))
    print("\n" + "\n".join(recomendaciones))

if __name__ == "__main__":
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(script_dir, ".."))
    except NameError:
        project_root = os.getcwd()
    
    generar_insights(project_root, show_plots=True)
