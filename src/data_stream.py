from config import DataConfig, KafkaConfig, SparkConfig
from logger import get_logger
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import (
    StringType,
    StructField,
    StructType,
    TimestampType
)

logger = get_logger(__name__)


def get_spark_session():

    ''' Get or create a new Spark session '''

    return SparkSession \
        .builder \
        .config('spark.ui.port', SparkConfig.ui_port) \
        .master(SparkConfig.master) \
        .appName(SparkConfig.app_name) \
        .getOrCreate()


def get_calls_dataframe(session):

    ''' Create a new dataframe from the S.F.P.D. incident calls '''

    schema = StructType([
        StructField('address', StringType()),
        StructField('address_type', StringType()),
        StructField('agency_id', StringType()),
        StructField('call_date', TimestampType()),
        StructField('call_date_time', TimestampType()),
        StructField('call_time', StringType()),
        StructField('city', StringType()),
        StructField('common_location', StringType()),
        StructField('crime_id', StringType()),
        StructField('disposition', StringType()),
        StructField('offense_date', TimestampType()),
        StructField('original_crime_type_name', StringType()),
        StructField('report_date', TimestampType()),
        StructField('state', StringType())
    ])

    df = session \
        .readStream \
        .format('kafka') \
        .option('kafka.bootstrap.servers', KafkaConfig.internal_servers) \
        .option('subscribe', KafkaConfig.topic) \
        .option('startingOffsets', SparkConfig.starting_offset) \
        .option('maxOffsetsPerTrigger', SparkConfig.max_offset) \
        .option('stopGracefullyOnShutdown', SparkConfig.stop_gracefully) \
        .load()

    df = df \
        .selectExpr('CAST(value AS STRING)')

    df = df \
        .select(from_json(col('value'), schema).alias('calls')) \
        .select('calls.*')

    return df


def get_codes_dataframe(session):

    ''' Create a new dataframe from the S.F.P.D. incident codes '''

    schema = StructType([
        StructField('description', StringType()),
        StructField('disposition_code', StringType())
    ])

    df = session \
        .read \
        .json(DataConfig.sfdpd_codes, schema=schema)

    df = df \
        .withColumnRenamed('disposition_code', 'disposition')

    return df


def run_spark_job():

    ''' Read and aggregate data from the Kafka stream '''

    # Get a Spark session.
    spark = get_spark_session()

    # Load the dataframes.
    calls_df = get_calls_dataframe(spark)
    codes_df = get_codes_dataframe(spark)

    # Select only the necessary columns.
    calls_df = calls_df \
        .select([
            'call_date_time',
            'disposition',
            'original_crime_type_name'
        ]) \
        .distinct() \
        .withWatermark('call_date_time', '5 minutes')

    # Group and order by original crime.
    calls_df = calls_df \
        .dropna() \
        .select('original_crime_type_name') \
        .groupBy('original_crime_type_name') \
        .agg({'original_crime_type_name': 'count'}) \
        .withColumnRenamed('count(original_crime_type_name)', 'count') \
        .orderBy('count', ascending=False)

    # Print the aggregate table.
    calls_query = calls_df \
        .writeStream \
        .outputMode('complete') \
        .format('console') \
        .start()
    calls_query.awaitTermination()

    # Join both dataframes (incidents and codes).
    join_query = calls_df \
        .join(
            codes_df,
            col('calls_df.disposition') == col('codes_df.disposition'),
            'left_outer'
        )
    join_query.awaitTermination()

    # Close the Spark session.
    spark.stop()


if __name__ == "__main__":
    run_spark_job()
