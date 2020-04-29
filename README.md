# SF Crime Statistics with Spark Streaming

In this project, we will be provided with a real-world dataset, extracted from Kaggle, on San Francisco crime incidents, and you will provide statistical analyses of the data using Apache Spark Structured Streaming.

## Table of contents

- [Structure](#structure)
- [Requirements](#requirements)
- [Getting started](#getting-started)
  - [Cloning the repository](#cloning-the-repository)
  - [Terminal 1: Architecture](#terminal-1-architecture)
  - [Terminal 2: Producer](#terminal-2-producer)
  - [Terminal 3: Consumer](#terminal-3-consumer)
  - [Screenshots](#screenshots)
- [Stopping the solution](#stopping-the-solution)
- [Questions](#questions)

---

## Structure<a name="structure"></a>

This tree shows the repository structure.

```
.
├── docker
│   ├── producer
│   │   └── Dockerfile
│   └── spark
│       └── Dockerfile
├── images
│   ├── architecture.png
│   ├── iterm.jpg
│   ├── query.png
│   ├── spark-job-dag.png
│   ├── spark-jobs.png
│   └── spark-nodes.png
├── src
│   ├── config
│   │   ├── config.ini
│   │   └── logging.ini
│   ├── data
│   │   ├── police-department-calls-for-service.json
│   │   └── radio_code.json
│   ├── config.py
│   ├── consumer_server.py
│   ├── data_stream.py
│   ├── kafka_server.py
│   ├── logger.py
│   └── producer_server.py
├── .editorconfig
├── .gitignore
├── docker-compose.yaml
├── README.md
├── run_consumer.sh
└── run_producer.sh
```

---

## Requirements<a name="requirements"></a>

The application we're building is quite memory and CPU demanding, so you must æhave a decent computer with at least **16GB RAM** and **4-core CPU**.

All the services and frameworks we need will to run the application are containerized, so the only tool you must have propery installed is Docker Engine / Desktop + Docker Compose.

---

## Getting started<a name="getting-started"></a>

We will need multiple terminal sessions in order to run the application:

- A session to run the architecture of the solution, consisting in:
  - Apache Zookeeper
  - A 2-node Apache Kafka cluster
  - A 3-node Apache Spark cluster
- A session to run the simulator that produces the events
- A session to run the server that consumes these events

<img src="images/architecture.png" width="820" alt="Architecture">

This image shows how the container architecture is deployed. Let's go to run this all!

### Cloning the repository<a name="cloning-the-repository"></a>

The first step is to clone this repository. Just type the following command in your terminal:

```bash
# Clone the repository...
$ git clone https://github.com/vermicida/data-streaming-spark.git

# ...and move to its directory
$ cd data-streaming-spark
```

### Terminal 1: Architecture<a name="terminal-1-architecture"></a>

Open a new terminal session, or use the one you just used to clone the respository. From the root folder of the project, run the following command:

```bash
$ docker-compose up --force-recreate --build
```

Docker will run the services defined in the file `docker-compose.yaml`. If any of the images isn't found locally, Docker will download it. This process take awhile, so be patient; 10-15 minutes based on your internet connection and hardware.

### Terminal 2: Producer<a name="terminal-2-producer"></a>

Once the architecture is ready, we can run the producer. The code is hosted inside a container called `producer`, so we can run a command within that container in order to start the producer.

The command is wrapped in a script file to ease the task. Open a new terminal session and run the command below:

```bash
$ ./run_producer.sh
```

It instantiate a `KafkaProducer` that will be pushing a new message to the Kafka's cluster every 2 seconds.

### Terminal 3: Consumer<a name="terminal-3-consumer"></a>

Now we can start our consumer. Just as we did with the producer, we will run a script that submits the consumer application to the Spark's cluster for us. In this case, the code is hosted inside the Spark's master node container.

Type command in a new terminal sessión:

```bash
$ ./run_consumer.sh
```

In a few seconds, the consumer application will start processing the messages from the Kafka topic in small batches (windowed).

### Screenshots<a name="screenshots"></a>

Below are some screenshots of the application and its monitoring.

These are the terminal session:

- Upper left: Terminal 1, `docker-compose` task.
- Lower left: Terminal 2, `run_producer.sh` script.
- Right: Terminal 3, `run_consumer.sh` script.

<img src="images/iterm.png" width="880" alt="iTerm">

Once the consumer is running, we can navigate `http://localhost:8080` in a web browser to see Spark UI. This console shows tons of info regarding the jobs running in the cluster.

Here you can check out the nodes of the cluster:

<img src="images/spark-nodes.png" width="880" alt="Spark nodes">

Click on an application to see their jobs:

<img src="images/spark-jobs.png" width="880" alt="Jobs">

Also you can get details of every single job, such as its DAG or its logs:

<img src="images/spark-job-dag.png" width="880" alt="Job DAG">

A closer view of the terminal where Spark prints the aggregate table we're building, updated after every batch processed.

<img src="images/query.png" width="320" alt="Query">

And last but not least, the JSON object representing the progress report:

```json
{
  "id" : "e292e447-66f3-43d2-88ec-6dcfef0d0b09",
  "runId" : "118b6a03-8b0a-4ac2-b645-7c79692b20af",
  "name" : null,
  "timestamp" : "2020-04-28T22:54:38.952Z",
  "batchId" : 4,
  "numInputRows" : 30,
  "inputRowsPerSecond" : 0.49206948021060576,
  "processedRowsPerSecond" : 0.5643234702131261,
  "durationMs" : {
    "addBatch" : 52778,
    "getBatch" : 3,
    "getEndOffset" : 1,
    "queryPlanning" : 109,
    "setOffsetRange" : 14,
    "triggerExecution" : 53161,
    "walCommit" : 99
  },
  "eventTime" : {
    "avg" : "2018-12-31T21:51:34.000Z",
    "max" : "2018-12-31T21:59:00.000Z",
    "min" : "2018-12-31T21:41:00.000Z",
    "watermark" : "2018-12-31T23:52:00.000Z"
  },
  "stateOperators" : [ {
    "numRowsTotal" : 84,
    "numRowsUpdated" : 34,
    "memoryUsedBytes" : 144380,
    "customMetrics" : {
      "loadedMapCacheHitCount" : 6000,
      "loadedMapCacheMissCount" : 0,
      "stateOnCurrentVersionSizeBytes" : 50980
    }
  }, {
    "numRowsTotal" : 160,
    "numRowsUpdated" : 30,
    "memoryUsedBytes" : 119812,
    "customMetrics" : {
      "loadedMapCacheHitCount" : 800,
      "loadedMapCacheMissCount" : 0,
      "stateOnCurrentVersionSizeBytes" : 52700
    }
  } ],
  "sources" : [ {
    "description" : "KafkaV2[Subscribe[san-francisco.police-department.calls]]",
    "startOffset" : {
      "san-francisco.police-department.calls" : {
        "0" : 134
      }
    },
    "endOffset" : {
      "san-francisco.police-department.calls" : {
        "0" : 164
      }
    },
    "numInputRows" : 30,
    "inputRowsPerSecond" : 0.49206948021060576,
    "processedRowsPerSecond" : 0.5643234702131261
  } ],
  "sink" : {
    "description" : "org.apache.spark.sql.execution.streaming.ConsoleSinkProvider@5880d11"
  }
}
```

Everything works like a charm!

---

## Stopping the solution<a name="stopping-the-solution"></a>

To stop all the running processes we will go in reverse order:

- In **Terminal 3**, hit `Ctrl` + `C`.
- In **Terminal 2**, hit `Ctrl` + `C`.
- In **Terminal 1**, hit `Ctrl` + `C`. When Docker Compose stops all the services, make sure to also remove the containers running the following command:

```bash
$ docker-compose down
```

---

## Questions<a name="questions"></a>

These are my answers to the Udacity's questions:

**1. How did changing values on the SparkSession property parameters affect the throughput and latency of the data?**

The table below resumes some of the properties that can be tweaked for a better the throughput and latency:

| Property | Meaning |
|:-|:-|
| spark.driver.cores | Number of cores to use for the driver process, only in cluster mode |
| spark.driver.memory | Amount of memory to use for the driver process |
| spark.executor.cores | The number of cores to use on each executor |
| spark.executor.memory | Amount of memory to use per executor process |
| spark.streaming.kafka.maxRatePerPartition | Maximum rate (number of records per second) at which data will be read from each Kafka partition when using the new Kafka direct stream API |

**2. What were the 2-3 most efficient SparkSession property key/value pairs? Through testing multiple variations on values, how can you tell these were the most optimal?**

I don't have a magic number, but these are the values I used:

| Property | Meaning | Value |
|:-|:-|:-|
| `spark.default.parallelism` | Default number of partitions in RDDs returned by transformations like join, reduceByKey, and parallelize when not set by user | 4 |
| `spark.streaming.kafka.maxRatePerPartition` | Maximum rate (number of records per second) at which data will be read from each Kafka partition when using the new Kafka direct stream API | N/A (producer is pushing a message every 2 seconds) |
