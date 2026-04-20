
import os
from datetime import datetime

def enviar_resumen_notificacion(base_dir):
    """
    Simula el envío de notificaciones por correo electrónico con un resumen de los insights.
    """
    print("--- PASO 3: Simulación de Envío de Notificaciones ---")
    
    informe_path = os.path.join(base_dir, "outputs", "informes", "insights_finales.txt")
    recomendaciones_path = os.path.join(base_dir, "outputs", "informes", "recomendaciones_estrategicas.txt")
    log_path = os.path.join(base_dir, "outputs", "informes", "notificaciones_enviadas.txt")
    
    if not os.path.exists(informe_path):
        print(f"⚠️ No se encontró el informe en {informe_path}. Abortando notificación.")
        return

    # Leer contenido
    with open(informe_path, "r", encoding="utf-8") as f:
        insights = f.read()
    
    recomendaciones = ""
    if os.path.exists(recomendaciones_path):
        with open(recomendaciones_path, "r", encoding="utf-8") as f:
            recomendaciones = f.read()

    # Formatear el "correo"
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje = f"""
============================================================
📧 ASUNTO: Resumen Ejecutivo - Análisis de Marketing Digital enGira
FECHA: {ahora}
============================================================

Hola equipo,

Aquí tenéis el resumen actualizado de los últimos insights generados por el pipeline:

{insights}

--- RECOMENDACIONES CLAVE ---
{recomendaciones}

Atentamente,
El Sistema de Análisis Automático enGira 🚀
============================================================
"""

    # Simular envío (imprimir en consola)
    print("📤 Enviando notificación a los stakeholders...")
    print(mensaje)
    
    # Registrar en log
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n--- ENVÍO REALIZADO EL {ahora} ---\n")
            f.write(mensaje)
        print(f"✅ Notificación registrada en: {log_path}")
    except Exception as e:
        print(f"❌ Error al guardar el log de notificaciones: {e}")

if __name__ == "__main__":
    # Para pruebas directas
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    enviar_resumen_notificacion(BASE_DIR)
