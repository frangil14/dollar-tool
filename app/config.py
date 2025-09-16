import os

class Config:
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    DOLARHOY_URL = "https://dolarhoy.com/cotizaciondolarblue"
    CRONISTA_URL = "https://www.cronista.com/MercadosOnline/moneda.html?id=ARSB"
    CRIPTOYA_URL = "https://criptoya.com/api/usdt/ars/1"
    
    SCHEDULER_INTERVAL_SECONDS = int(os.environ.get('SCHEDULER_INTERVAL_SECONDS', '30'))