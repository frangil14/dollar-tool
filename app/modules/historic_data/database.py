import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional
import logging


class HistoricDataDB:
    """
    Clase para manejar la base de datos SQLite de datos históricos.
    Usa base de datos en memoria para demos y prototipos.
    """
    
    def __init__(self, db_path: str = ":memory:"):
        """
        Inicializar la conexión a la base de datos.
        
        Args:
            db_path: Ruta de la base de datos. ":memory:" para base de datos en RAM
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Para obtener resultados como diccionarios
        self.create_table()
    
    def create_table(self):
        """Crear la tabla de datos históricos si no existe."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS historic_data (
            timestamp DATETIME NOT NULL,
            dolarBlue REAL NOT NULL,
            dolarLemon REAL,
            dolarBinance REAL
        )
        """
        
        self.conn.execute(create_table_sql)
        self.conn.commit()
    
    def insert_data(self, dollar_blue_price: float, lemon_price: Optional[float] = None, 
                   binance_price: Optional[float] = None) -> bool:
        """
        Insertar nuevos datos históricos.
        
        Args:
            dollar_blue_price: Precio del dólar blue
            lemon_price: Precio de Lemon (opcional)
            binance_price: Precio de Binance (opcional)
            
        Returns:
            bool: True si se insertó correctamente
        """
        try:
            insert_sql = """
            INSERT INTO historic_data (timestamp, dolarBlue, dolarLemon, dolarBinance)
            VALUES (?, ?, ?, ?)
            """
            
            now = datetime.now()
            self.conn.execute(insert_sql, (now, dollar_blue_price, lemon_price, binance_price))
            self.conn.commit()
            return True
            
        except Exception as e:
            logging.error(f"Error inserting data: {e}")
            return False
    
    def get_historic_data(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Obtener datos históricos.
        
        Args:
            limit: Número máximo de registros a obtener
            
        Returns:
            List[Dict]: Lista de registros históricos
        """
        try:
            if limit:
                query = "SELECT * FROM historic_data ORDER BY timestamp DESC LIMIT ?"
                cursor = self.conn.execute(query, (limit,))
            else:
                query = "SELECT * FROM historic_data ORDER BY timestamp DESC"
                cursor = self.conn.execute(query)
            
            # Convertir a lista de diccionarios
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except Exception as e:
            logging.error(f"Error getting historic data: {e}")
            return []
    
    def get_latest_data(self) -> Optional[Dict]:
        """
        Obtener el último registro insertado.
        
        Returns:
            Optional[Dict]: Último registro o None si no hay datos
        """
        try:
            query = "SELECT * FROM historic_data ORDER BY timestamp DESC LIMIT 1"
            cursor = self.conn.execute(query)
            row = cursor.fetchone()
            
            return dict(row) if row else None
            
        except Exception as e:
            logging.error(f"Error getting latest data: {e}")
            return None
    
    def get_data_count(self) -> int:
        """
        Obtener el número total de registros.
        
        Returns:
            int: Número de registros
        """
        try:
            cursor = self.conn.execute("SELECT COUNT(*) as count FROM historic_data")
            row = cursor.fetchone()
            return row['count'] if row else 0
            
        except Exception as e:
            logging.error(f"Error getting data count: {e}")
            return 0
    
    def close(self):
        """Cerrar la conexión a la base de datos."""
        if self.conn:
            self.conn.close()


# Instancia global de la base de datos (en memoria para demos)
db = HistoricDataDB(":memory:")
