# nmlab-fib-cal


## How to run

- Install required python packages
```bash
$ pip3 install -r requirements.txt
```

- Install gRPC dependencies
```bash
# Install protobuf compiler
$ sudo apt-get install protobuf-compiler

# Install buildtools
$ sudo apt-get install build-essential make
```

- Compile protobuf schema to python wrapper
```bash
$ cd gRPC
$ make
```

- Run the MQTT docker container
```bash
$ cd MQTT
$ docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
```

- Migrate Django database tables
```bash
$ cd rest
$ python3 manage.py migrate
```

- Run the shell script
```bash
$ python3 run.py
```

## Using `curl` to perform client request
- [POST] - /rest/fibonacci
```bash
$ curl -X POST --form-string order=10 http://localhost:8000/rest/fibonacci
```
- [GET] - /rest/logs
```bash
$ curl -X GET http://localhost:8000/rest/logs
```

## Note