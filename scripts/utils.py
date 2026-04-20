
import pandas as pd
import numpy as np

def clasificar_campaña(nombre):
    """Clasifica la temática de la campaña según palabras clave en el asunto."""
    if not isinstance(nombre, str):
        return "otros"
    
    nombre = nombre.lower().strip()
    if "convocatorias" in nombre:
        return "convocatorias"
    elif any(x in nombre for x in ["participacion", "participación", "invitación", "invitacio"]):
        return "invitacion"
    elif "jornadas" in nombre:
        return "eventos"
    elif any(x in nombre for x in ["demo", "webinar", "registro"]):
        return "formacion"
    elif any(x in nombre for x in ["dferia", "madferia", "mercartes", "feria"]):
        return "ferias"
    elif any(x in nombre for x in ["descubre", "descobreix", "destacados"]):
        return "promocion"
    elif any(x in nombre for x in ["funcionamiento", "resumen", "fin"]):
        return "informativa"
    else:
        return "otros"

def clasificar_publico(nombre):
    """Clasifica el público objetivo según palabras clave en el nombre de la campaña."""
    if not isinstance(nombre, str):
        return "all"
        
    nombre = nombre.lower().strip()
    if any(x in nombre for x in ['artistas', 'convocatorias', 'webinar', 'diagnostico']):
        return 'artistas'
    elif any(x in nombre for x in ['programadores', 'demo']):
        return 'programadores'
    else:
        return 'all'

def segmentar_rendimiento(row, invalid_campaigns=[]):
    """Categoriza el rendimiento de una campaña según OR y CTR."""
    if row['campaign_name'] in list(invalid_campaigns):
        return 'Volumen insuficiente'
    
    if row['trackable_open_rate'] >= 80 and row['click_rate'] >= 30:
        return 'Top Performance'
    elif row['trackable_open_rate'] >= 60:
        return 'Buen Alcance, Interés Medio'
    elif row['click_rate'] >= 15:
        return 'Alcance Bajo, Alta Conversión'
    else:
        return 'Bajo Rendimiento'

def detectar_tematica_asunto(subject):
    """Detecta la temática específica basada en keywords del asunto."""
    keywords = {
        'convocatoria': ['convocatoria', 'abiertas', 'plazo'],
        'webinar_formacion': ['webinar', 'demo', 'taller', 'programa'],
        'evento_feria': ['feria', 'mercartes', 'madferia', 'dferia'],
        'registro_plataforma': ['registro', 'completa', 'perfil'],
        'descubrimiento': ['descubre', 'descobreix', 'artistas', 'destacado']
    }
    
    subject = str(subject).lower()
    for theme, terms in keywords.items():
        if any(term in subject for term in terms):
            return theme
    return 'otros'
