How to run a system which leverages Spark, Kafka, and MongoDB to construct a robust network of applications and mine transactions
--------------
START MONGODB
--------------
> Install the MongoDB Community Server (version 7.0.7) and then check its configuration 
> Create a database in MongoDB Compass ('GUI' for MongoDB) - localhost:27017 with the name ITC6107
> Create a collection with the name Blocks
------------
START KAFKA
------------
> Install kafka (version 3.7.0) and save it in yout C: folder
> Inside kafka file, configure server and zookeeper in the config file --> log.dirs=c:/kafka/kafka-logs & dataDir=c:/kafka/zookeeper-data
> Start the zookeeper --> C:\kafka>./bin/zookeeper-server-start.sh config/zookeeper.properties
> Start kafka server --> C:\kafka>.\bin\windows\kafka-server-start.bat .\config\server.properties
> Create a topic with two partitions --> C:\kafka\bin\windows>.\bin\windows\kafka-topics.bat --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 2 --topic Blocks
> Start producer in this topic --> C:\kafka\bin\windows>kafka-console-producer.bat --broker-list localhost:9092 --topic Blocks
> Start consumer in this topic --> C:\kafka\bin\windows>kafka-console-consumer.bat --topic Blocks --bootstrap-server localhost:9092 --from-beginning
------------------------
START PYTHON COMPONENTS
------------------------
Either by running in parallel by 'run' button in Pycharm or each one in a different terminal using the python command
> Run tr-server.python
> Run mine.py
> Run app0.py
> Run app1.py
> Run mongoq.py