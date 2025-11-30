# Chat-auth.

The transportation microservice for the distributed chat system.

## Brief.

This microservice is generally responsibe for the websockets
connections management and transmitting received messages to
the RabbitMQ / dispatching the received messages from RabbitMQ
back to users.

## Stage.
This service is in the stage of active development. Updates are released multiple times a week.

## Features.
This microservice is a thin layer by design. It's main purpose is to decouple
the database operations, verifications and all the other heavy lifting from transportation operations.

1) Provides the method for receiving a one time pass using JWT issued by the authentication service.
The pass is needed for the correct authentication upon connecting to the websocket endpoint as websocket
messages do not have headers.
2) Manages connections to the websocket hub in order to correctly dispatch messages.
3) Uses ephemeral one-per-user queue that is deleted upon disconnecting from the websocket endpoint.

## Architecture.

This microservice is built using the Clean Architecture approach.
It consists of 4 layers which are:

1) Domain (entities, value objects)
2) Application layer (domain entities orchestration and business logic)
3) Interface adapters (thin transport layer that incapsulates the internal logic)
4) Infrastructure (frameworks, databases, etc.)

## Usage.

1) Clone the repository.
2) Create .env file in the backend directory using the env_example.txt as an example.
3) ```docker-compose up --build``` in the directory where docker-compose.yaml file is located.
4) The application will be available on **http://localhost:8001**

## Recent updates.

**30.11.2025**

**Major**

1) Added logging using probably the most classic stack for such purposes - ELK and Filebeat.

> Note that in probably 90% of times I would stick to Open Telemetry | Prometheus | Grafana | Loki stack.
> It's much easier, more modern and in the most cases you would already use it
> as your monitoring/tracing solution.

## Docs.

Available at the standard FastAPI docs endpoint **http://localhost:8001/docs**

## Back to Index repository of the whole chat system.

https://github.com/aleksandrshaulskyi/chat-index
