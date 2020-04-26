from config import DataConfig, KafkaConfig, SparkConfig
from logger import get_logger
import pyspark.sql.functions as psf
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructField, StructType, TimestampType
from dateutil.parser import parse as parse_date

logger = get_logger(__name__)


def run_spark_job():

    spark = SparkSession \
        .builder \
        .config('spark.ui.port', 3000) \
        .master(SparkConfig.master) \
        .appName(SparkConfig.app_name) \
        .getOrCreate()

    # TBD

    spark.stop()


if __name__ == '__main__':
    run_spark_job()
