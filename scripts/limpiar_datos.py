
import pandas as pd
import numpy as np
import os
from scripts.utils import clasificar_campaña, clasificar_publico

def limpiar_y_transformar(raw_path, processed_path):
    """Ejecuta el pipeline de limpieza y transformación de datos."""
    print(f"Cargando datos desde: {raw_path}...")
    
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Archivo no encontrado: {raw_path}")
        
    # Cargar datos (saltando las 3 primeras filas de metadatos del exportador)
    df = pd.read_csv(raw_path, sep=";", engine="python", skiprows=3)
    
    # Normalizar nombres de columnas (antes de borrar para evitar errores de case)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("-", "_")
    
    # Eliminar columnas irrelevantes
    cols_to_drop = [
        "name_from", "email_from", "hard_bounces", 
        "soft_bounces", "non_delivered", "delivered", 
        "unsubscribed", "complaints"
    ]
    df = df.drop(columns=cols_to_drop, errors='ignore')
    
    # Transformar fechas
    df['sending_date'] = pd.to_datetime(df["sending_date"], dayfirst=True, errors="coerce")
    df['year'] = df['sending_date'].dt.year
    df['month'] = df['sending_date'].dt.month
    df['day'] = df['sending_date'].dt.day
    
    # Generar nombre del día en español
    weekday_map = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}
    df['weekday'] = df['sending_date'].dt.weekday.map(weekday_map)
    
    # Limpiar strings de texto
    df['subject'] = df['subject'].str.lower().str.strip()
    df['campaign_name'] = df['campaign_name'].str.lower().str.strip()
    
    # Aplicar clasificaciones
    df['tipo_campaña'] = df['subject'].apply(clasificar_campaña)
    df['tipo_publico'] = df['campaign_name'].apply(clasificar_publico)
    
    # Convertir porcentajes a floats
    cols_pct = [
        "non_delivered_rate", "trackable_open_rate", "click_rate",
        "click_to_open_rate", "unsubscription_rate", "delivered_rate",
        "hard_bounces_rate", "soft_bounces_rate", "complaints_rate"
    ]
    
    for col in cols_pct:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace("%", "")
                .str.replace(",", ".")
                .astype(float)
            )
    
    # Asegurar que el directorio de salida existe
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    
    # Guardar datos limpios
    df.to_csv(processed_path, index=False)
    print(f"✅ Datos limpios guardados en: {processed_path}")

if __name__ == "__main__":
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        BASE_DIR = os.path.abspath(os.path.join(script_dir, ".."))
    except NameError:
        BASE_DIR = os.getcwd()
        
    RAW_DATA = os.path.join(BASE_DIR, "data", "raw", "data.csv")
    PROCESSED_DATA = os.path.join(BASE_DIR, "data", "processed", "data_limpia.csv")
    
    limpiar_y_transformar(RAW_DATA, PROCESSED_DATA)
