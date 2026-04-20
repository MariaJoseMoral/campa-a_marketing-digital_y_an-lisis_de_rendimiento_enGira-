
import pandas as pd
import numpy as np
import os
import logging
from scripts.utils import clasificar_campaña, clasificar_publico

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataCleaner:
    """
    Clase para gestionar la carga, limpieza y transformación de datos de marketing.
    """
    
    def __init__(self, raw_path, processed_path):
        self.raw_path = raw_path
        self.processed_path = processed_path
        self.df = None
        
    def load_data(self):
        """Carga los datos desde el archivo CSV raw."""
        logger.info(f"Cargando datos desde: {self.raw_path}...")
        
        if not os.path.exists(self.raw_path):
            error_msg = f"Archivo no encontrado: {self.raw_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
            
        # Cargar datos (saltando las 3 primeras filas de metadatos del exportador)
        self.df = pd.read_csv(self.raw_path, sep=";", engine="python", skiprows=3)
        return self.df

    def clean_data(self):
        """Realiza la limpieza básica de columnas y tipos de datos."""
        if self.df is None:
            self.load_data()
            
        logger.info("Normalizando nombres de columnas y eliminando irrelevantes...")
        
        # Normalizar nombres de columnas
        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("-", "_")
        )
        
        # Eliminar columnas irrelevantes
        cols_to_drop = [
            "name_from", "email_from", "hard_bounces", 
            "soft_bounces", "non_delivered", "delivered", 
            "unsubscribed", "complaints"
        ]
        self.df = self.df.drop(columns=cols_to_drop, errors='ignore')
        
        # Limpiar strings de texto
        self.df['subject'] = self.df['subject'].str.lower().str.strip()
        self.df['campaign_name'] = self.df['campaign_name'].str.lower().str.strip()
        
        # Convertir porcentajes a floats
        cols_pct = [
            "non_delivered_rate", "trackable_open_rate", "click_rate",
            "click_to_open_rate", "unsubscription_rate", "delivered_rate",
            "hard_bounces_rate", "soft_bounces_rate", "complaints_rate"
        ]
        
        for col in cols_pct:
            if col in self.df.columns:
                self.df[col] = (
                    self.df[col]
                    .astype(str)
                    .str.replace("%", "")
                    .str.replace(",", ".")
                    .astype(float)
                )
        
        return self.df

    def transform_data(self):
        """Aplica transformaciones temporales y clasificaciones de negocio."""
        if self.df is None:
            self.clean_data()
            
        logger.info("Transformando fechas y aplicando clasificaciones...")
        
        # Transformar fechas
        self.df['sending_date'] = pd.to_datetime(self.df["sending_date"], dayfirst=True, errors="coerce")
        self.df['year'] = self.df['sending_date'].dt.year
        self.df['month'] = self.df['sending_date'].dt.month
        self.df['day'] = self.df['sending_date'].dt.day
        
        # Generar nombre del día en español
        weekday_map = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}
        self.df['weekday'] = self.df['sending_date'].dt.weekday.map(weekday_map)
        
        # Aplicar clasificaciones de scripts.utils
        self.df['tipo_campaña'] = self.df['subject'].apply(clasificar_campaña)
        self.df['tipo_publico'] = self.df['campaign_name'].apply(clasificar_publico)
        
        # Redondear todos los floats a 2 decimales
        float_cols = self.df.select_dtypes(include=['float64', 'float32']).columns
        self.df[float_cols] = self.df[float_cols].round(2)
        
        return self.df

    def save_data(self):
        """Guarda el DataFrame procesado en la ruta de salida."""
        if self.df is None:
            self.transform_data()
            
        logger.info(f"Guardando datos procesados en: {self.processed_path}...")
        
        # Asegurar que el directorio de salida existe
        os.makedirs(os.path.dirname(self.processed_path), exist_ok=True)
        
        self.df.to_csv(self.processed_path, index=False)
        logger.info("✅ Proceso de limpieza finalizado con éxito.")
        
    def run(self):
        """Ejecuta el flujo completo de limpieza y transformación."""
        self.load_data()
        self.clean_data()
        self.transform_data()
        self.save_data()

def limpiar_y_transformar(raw_path, processed_path):
    """
    Función envoltorio para mantener compatibilidad con pipeline.py.
    """
    cleaner = DataCleaner(raw_path, processed_path)
    cleaner.run()

if __name__ == "__main__":
    # Configuración de rutas para ejecución directa
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        BASE_DIR = os.path.abspath(os.path.join(script_dir, ".."))
    except NameError:
        BASE_DIR = os.getcwd()
        
    RAW_DATA = os.path.join(BASE_DIR, "data", "raw", "data.csv")
    PROCESSED_DATA = os.path.join(BASE_DIR, "data", "processed", "data_limpia.csv")
    
    limpiar_y_transformar(RAW_DATA, PROCESSED_DATA)
