
import os
import sys
from scripts.limpiar_datos import limpiar_y_transformar
from scripts.analisis_insights import generar_insights

def run_pipeline():
    """
    Orquestador principal del proyecto de análisis de marketing digital.
    """
    print("🚀 Iniciando Pipeline de Análisis enGira!...\n")
    
    # 1. Configurar rutas
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RAW_DATA = os.path.join(BASE_DIR, "data", "raw", "data.csv")
    PROCESSED_DATA = os.path.join(BASE_DIR, "data", "processed", "data_limpia.csv")
    
    try:
        # Paso 1: Limpieza y Transformación
        print("--- PASO 1: Limpieza y Transformación ---")
        limpiar_y_transformar(RAW_DATA, PROCESSED_DATA)
        print()
        
        # Paso 2: Análisis y Generación de Insights
        print("--- PASO 2: Análisis y Generación de Insights ---")
        generar_insights(BASE_DIR, show_plots=False)
        print()
        
        print("✨ Pipeline finalizado con éxito.")
        print(f"📁 Resultados disponibles en la carpeta 'outputs/'.")
        
    except Exception as e:
        print(f"❌ Error durante la ejecución del pipeline: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
