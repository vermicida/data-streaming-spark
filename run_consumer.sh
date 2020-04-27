#! /bin/bash

docker exec -it spark_master spark-submit \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5 \
    /opt/app/data_stream.py
