# config/database_config.py
# Configuración específica de base de datos
# =========================================

import os
from typing import Dict, Any, Optional
from pymongo import MongoClient
from .settings import DatabaseConfig

class DatabaseManager:
    """Gestor centralizado de conexiones a base de datos"""
    
    def __init__(self):
        self._mongo_client: Optional[MongoClient] = None
        self._spark_session = None
        
    def get_mongo_client(self) -> MongoClient:
        """Obtiene cliente MongoDB singleton"""
        if self._mongo_client is None:
            self._mongo_client = MongoClient(
                DatabaseConfig.MONGO_URI,
                serverSelectionTimeoutMS=DatabaseConfig.MONGO_TIMEOUT
            )
            # Test connection
            self._mongo_client.admin.command("ping")
        return self._mongo_client
    
    def get_database(self):
        """Obtiene la base de datos principal"""
        client = self.get_mongo_client()
        return client[DatabaseConfig.MONGO_DB]
    
    def get_collection(self, collection_name: str):
        """Obtiene una colección específica"""
        db = self.get_database()
        return db[collection_name]
    
    def get_spark_session(self):
        """Obtiene sesión Spark (lazy loading)"""
        if not DatabaseConfig.USE_SPARK:
            return None
            
        if self._spark_session is None:
            try:
                from pyspark.sql import SparkSession
                self._spark_session = (
                    SparkSession.builder
                    .appName(DatabaseConfig.SPARK_APP_NAME)
                    .master(DatabaseConfig.SPARK_MASTER)
                    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1")
                    .config("spark.mongodb.read.connection.uri", DatabaseConfig.MONGO_URI)
                    .config("spark.mongodb.write.connection.uri", DatabaseConfig.MONGO_URI)
                    .getOrCreate()
                )
            except ImportError:
                print("⚠️ PySpark no disponible, usando solo MongoDB")
                return None
        return self._spark_session
    
    def close_connections(self):
        """Cierra todas las conexiones"""
        if self._mongo_client:
            self._mongo_client.close()
            self._mongo_client = None
            
        if self._spark_session:
            self._spark_session.stop()
            self._spark_session = None
    
    def test_connections(self) -> Dict[str, Any]:
        """Prueba todas las conexiones"""
        results = {
            "mongodb": False,
            "spark": False,
            "errors": []
        }
        
        # Test MongoDB
        try:
            client = self.get_mongo_client()
            client.admin.command("ping")
            results["mongodb"] = True
        except Exception as e:
            results["errors"].append(f"MongoDB: {str(e)}")
        
        # Test Spark
        try:
            spark = self.get_spark_session()
            if spark:
                results["spark"] = True
            else:
                results["errors"].append("Spark: No disponible")
        except Exception as e:
            results["errors"].append(f"Spark: {str(e)}")
        
        return results

# Instancia global del gestor de BD
db_manager = DatabaseManager()

# Funciones de conveniencia
def get_mongo_client():
    return db_manager.get_mongo_client()

def get_database():
    return db_manager.get_database()

def get_collection(name: str):
    return db_manager.get_collection(name)

def get_spark_session():
    return db_manager.get_spark_session()

__all__ = [
    "DatabaseManager",
    "db_manager",
    "get_mongo_client",
    "get_database", 
    "get_collection",
    "get_spark_session"
]