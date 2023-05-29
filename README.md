# IoT Processing Architecture

A simple scalable architecture of an IoT data processing pipeline, using
common components.

Made as a final project for my Electrical Engineering bachelor's degree at
Universidade Federal de Santa Catarina (UFSC).

## Project structure

This project can be divided into Infrastructure (`/infrastructure`) and Microservices (`/microservices`).

### Infrastructure

Written in Terraform, this folder contains all files related to infratructure
deployment.

### Microservices

Written in Python, this folder contains all code related to application servers.

## How to use

TODO: write installation steps


## Sample payload
```
{'unit_id':123,'created_at':'2022-05-18T11:40:22.519222','is_defective': true,'machine_id':123,'machine_temperature':110.0,'machine_pressure':1.2}
```

With `mosquitto` installed, to send a payload to the app use:

```
mosquitto_pub -p 1883 -h localhost -m "{'unit_id':123,'created_at':'2022-05-18T11:39:22.519222','is_defective': true,'machine_id':123,'machine_temperature':110.0,'machine_pressure':1.2}" -t payloads
```

