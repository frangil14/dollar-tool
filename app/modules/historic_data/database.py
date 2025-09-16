import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import logging


class HistoricDataDB:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_table()
    
    def create_table(self):
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
        try:
            if limit:
                query = "SELECT * FROM historic_data ORDER BY timestamp DESC LIMIT ?"
                cursor = self.conn.execute(query, (limit,))
            else:
                query = "SELECT * FROM historic_data ORDER BY timestamp DESC"
                cursor = self.conn.execute(query)
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except Exception as e:
            logging.error(f"Error getting historic data: {e}")
            return []
    
    def get_latest_data(self) -> Optional[Dict]:
        try:
            query = "SELECT * FROM historic_data ORDER BY timestamp DESC LIMIT 1"
            cursor = self.conn.execute(query)
            row = cursor.fetchone()
            
            return dict(row) if row else None
            
        except Exception as e:
            logging.error(f"Error getting latest data: {e}")
            return None
    
    def get_data_count(self) -> int:
        try:
            cursor = self.conn.execute("SELECT COUNT(*) as count FROM historic_data")
            row = cursor.fetchone()
            return row['count'] if row else 0
            
        except Exception as e:
            logging.error(f"Error getting data count: {e}")
            return 0
    
    def close(self):
        if self.conn:
            self.conn.close()


db = HistoricDataDB(":memory:")
