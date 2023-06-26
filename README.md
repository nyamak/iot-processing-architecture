# IoT Processing Architecture

A simple scalable architecture of an IoT data processing pipeline, using
common components.

Made as a final project for my Electrical Engineering bachelor's degree at
Universidade Federal de Santa Catarina (UFSC).

## Project structure

This project can be divided into Infrastructure (`/infrastructure`),
Microservices (`/microservices`) and Testing (`/testing`).

### Infrastructure

Written in Terraform, this folder contains all files related to infratructure
deployment.

### Microservices

Written in Python, this folder contains all code related to application servers.

### Testing

This folder contains all code related to load testing, written using
[Locust.io](locust.io).

## How to use

### Setup
To start, you need to have the latest version of Terraform (`v1.4.6` as of the
writing of this document) and a free-tier [Sendgrid](https://app.sendgrid.com/)
account, with an [API key](https://docs.sendgrid.com/ui/account-and-settings/api-keys)
and a [verified email](https://docs.sendgrid.com/ui/sending-email/sender-verification).

### Deployment
If you simply want to deploy the latest version of this application using
Kubernetes, you may update your .kubeconfig file with the desired context
and add its name on `./infrastructure/providers.tf`, under both `config_context`
parameters. You may use `minikube` for local deployment or your cloud provider
of choice.

After, you may simply go to the `.\infrastructure` folder (`cd infrastructure`)
and execute `terraform init`, followed by `terraform apply`, setting you correct
credentials and variables.


### Load testing
To execute the load tests, you must first install the requirements with:
```
cd testing
pip install -r requirements.txt
```

Then you must update create a `.env` file, replacing any values in the
`.env.example` file.

To execute the load tests, run the following line:
```
locust -f load_testing.py
```

Access the URL shown in the command line and set the parameters.


## Sample payload
```
{'unit_id':123,'created_at':'2022-05-18T11:40:22.519222','is_defective': true,'machine_id':123,'machine_temperature':110.0,'machine_pressure':1.2}
```

With `mosquitto` installed, to send a payload to the app use:

```
mosquitto_pub -p 1883 -h localhost -m "{'unit_id':123,'created_at':'2022-05-18T11:39:22.519222','is_defective': true,'machine_id':123,'machine_temperature':110.0,'machine_pressure':1.2}" -t payloads
```

