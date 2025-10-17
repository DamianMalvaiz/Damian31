# spark_mongo.py — helpers para Spark + Mongo con esquema opcional y lecturas estables
import os
from pyspark.sql import SparkSession


def _as_bool(env: str, default: str = "true") -> bool:
    return os.getenv(env, default).strip().lower() in {"1", "true", "t", "yes", "y", "on"}


def get_spark() -> SparkSession:
    """
    Crea / retorna una SparkSession con el conector de Mongo y configuraciones
    que evitan problemas de inferencia de tipos (NullType) y consumos altos de memoria.
    """
    app = os.getenv("SPARK_APP_NAME", "spark-crud")
    master = os.getenv("SPARK_MASTER", "local[*]")
    mongo_uri = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")

    builder = (
        SparkSession.builder
        .appName(app)
        .master(master)
        # Conector Mongo 3.0.x (compatible con Spark 3.2.x)
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1")
        .config("spark.mongodb.read.connection.uri", mongo_uri)
        .config("spark.mongodb.write.connection.uri", mongo_uri)
        # Inferencia robusta para evitar NullType
        .config("spark.mongodb.input.inferSchema.sampleSize", os.getenv("MONGO_INFER_SAMPLE", "1000000"))
        .config("spark.mongodb.input.inferSchema.mapTypes.enabled", "true")
        # Configs suaves para entorno local/Windows
        .config("spark.sql.shuffle.partitions", os.getenv("SPARK_SHUFFLE_PARTS", "4"))
        .config("spark.driver.memory", os.getenv("SPARK_DRIVER_MEMORY", "2g"))
    )

    return builder.getOrCreate()


def read_mongo(db: str, coll: str, pipeline: str | None = None, schema=None):
    """
    Lee desde Mongo. Si se provee 'schema' (StructType), lo usa para evitar NullType.
    'pipeline' debe ser un string JSON válido (arreglo de etapas).
    """
    spark = get_spark()
    reader = (
        spark.read
        .format("mongo")
        .option("database", db)
        .option("collection", coll)
    )
    if pipeline:
        reader = reader.option("pipeline", pipeline)
    if schema is not None:
        return reader.schema(schema).load()
    return reader.load()


def write_mongo(df, db: str, coll: str, mode: str = "append", replace_document: bool = True):
    """
    Escribe un DataFrame de Spark hacia Mongo.
    """
    (
        df.write
        .format("mongo")
        .mode(mode)
        .option("database", db)
        .option("collection", coll)
        .option("replaceDocument", str(replace_document).lower())
        .save()
    )
