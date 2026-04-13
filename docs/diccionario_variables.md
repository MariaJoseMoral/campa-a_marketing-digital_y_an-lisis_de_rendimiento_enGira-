# 📖 Diccionario de Variables - Dataset de Campañas enGira!

Dataset final tras limpieza y transformación (`data_limpia.csv`).

| Variable | Descripción | Tipo | Origen |
| :--- | :--- | :--- | :--- |
| `campaign_id` | Identificador único de la campaña en Brevo | int | Original |
| `campaign_name` | Nombre interno de la campaña | string | Original (Limpio) |
| `sending_date` | Fecha de envío de la campaña | datetime | Transformado |
| `subject` | Asunto del e-mail | string | Original (Limpio) |
| `sent` | Número total de e-mails enviados | int | Original |
| `non_delivered_rate` | Porcentaje de e-mails no entregados | float (%) | Limpiado |
| `total_opens` | Número total de aperturas (incluye repetidas) | int | Original |
| `opens` | Número de aperturas únicas | int | Original |
| `trackable_open_rate` | Porcentaje de aperturas únicas (Open Rate) | float (%) | Limpiado |
| `apple_mpp_opens` | Aperturas bajo la política de privacidad de Apple | int | Original |
| `total_clicked` | Número total de clics (incluye repetidos) | int | Original |
| `clicked` | Número de clics únicos | int | Original |
| `click_rate` | Porcentaje de clics únicos sobre entregados (CTR) | float (%) | Limpiado |
| `click_to_open_rate` | Porcentaje de clics únicos sobre aperturas (CTOR) | float (%) | Limpiado |
| `unsubscription_rate` | Porcentaje de bajas de la lista | float (%) | Limpiado |
| `delivered_rate` | Porcentaje de e-mails entregados | float (%) | Limpiado |
| `hard_bounces_rate` | Porcentaje de rebotes permanentes | float (%) | Limpiado |
| `soft_bounces_rate` | Porcentaje de rebotes temporales | float (%) | Limpiado |
| `complaints_rate` | Porcentaje de reportes como spam | float (%) | Limpiado |
| `year`, `month`, `day`, `weekday` | Componentes de la fecha de envío | int | Derivado |
| `tipo_campaña` | Categorización por tipo de acción (convocatoria, formación...) | string | Derivado |
| `tipo_publico` | Segmento objetivo detectado (artistas, programadores, all) | string | Derivado |
| `segmento_rendimiento` | Clasificación por performance (Top, Bajo...) | string | Derivado |
| `tematica_asunto` | Tema principal detectado por palabras clave en subject | string | Derivado |
