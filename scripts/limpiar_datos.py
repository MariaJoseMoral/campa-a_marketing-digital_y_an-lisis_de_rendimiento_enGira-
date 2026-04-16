
import pandas as pd
import numpy as np
import os

def clasificar_campaña(nombre):
    """Clasifica la temática de la campaña según palabras clave en el asunto."""
    if not isinstance(nombre, str):
        return "otros"
    
    nombre = nombre.lower()
    if "convocatorias" in nombre:
        return "convocatorias"
    elif "jornadas" in nombre:
        return "jornadas"
    elif "demo" in nombre or 'webinar' in nombre or 'registro' in nombre:
        return "formacion"
    elif "dferia" in nombre or 'madferia' in nombre or 'mercartes' in nombre:
        return "ferias"
    elif "descubre" in nombre or "descobreix" in nombre or 'funcionamiento' in nombre or 'piloto' in nombre or 'destacados' in nombre:
        return "promocion"
    else:
        return "otros"

def clasificar_publico(nombre):
    """Clasifica el público objetivo según palabras clave en el nombre de la campaña."""
    if not isinstance(nombre, str):
        return "all"
        
    nombre = nombre.lower()
    if 'artistas' in nombre or 'convocatorias' in nombre or 'webinar' in nombre or 'diagnostico' in nombre:
        return 'artistas'
    elif 'programadores' in nombre or 'demo' in nombre:
        return 'programadores'
    else:
        return 'all'

def limpiar_y_transformar(raw_path, processed_path):
    """Ejecuta el pipeline de limpieza y transformación de datos."""
    print(f"Cargando datos desde: {raw_path}...")
    
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Archivo no encontrado: {raw_path}")
        
    # Cargar datos (saltando las 3 primeras filas de metadatos del exportador)
    df = pd.read_csv(raw_path, sep=";", engine="python", skiprows=3)
    
    # Eliminar columnas irrelevantes
    df = df.drop(columns=[
        "Name from", "Email from", "Hard bounces", 
        "Soft bounces", "Non delivered", "Delivered", 
        "Unsubscribed", "Complaints"
    ], errors='ignore')
    
    # Normalizar nombres de columnas
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("-", "_")
    
    # Transformar fechas
    df['sending_date'] = pd.to_datetime(df["sending_date"], dayfirst=True, errors="coerce")
    df['year'] = df['sending_date'].dt.year
    df['month'] = df['sending_date'].dt.month
    df['day'] = df['sending_date'].dt.day
    df['weekday'] = df['sending_date'].dt.weekday
    
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
    # Definir rutas relativas a la raíz del proyecto
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        BASE_DIR = os.path.abspath(os.path.join(script_dir, ".."))
    except NameError:
        BASE_DIR = os.getcwd()
        
    RAW_DATA = os.path.join(BASE_DIR, "data", "raw", "data.csv")
    PROCESSED_DATA = os.path.join(BASE_DIR, "data", "processed", "data_limpia.csv")
    
    limpiar_y_transformar(RAW_DATA, PROCESSED_DATA)
