







# Chat-transportation.

Real-time WebSocket gateway for the distributed chat platform

The transportation microservice responsible for managing WebSocket connections, authenticating users via one-time passes, and bridging real-time traffic between clients and RabbitMQ.

## 🚀 Overview

Chat-transportation acts as the entry point for all WebSocket traffic in the system.

It provides a lightweight, high-performance gateway whose only goal is to reliably move messages in and out, while keeping all heavy lifting (database writes, validation, authorization, business logic) in other specialized services.

The service ensures:

- correct authentication flow (headers don’t exist in WebSocket frames, so JWT is exchanged for a one-time pass)

- stable management of WebSocket sessions

- dispatching messages from RabbitMQ to connected clients

- publishing client messages back into RabbitMQ

- per-user ephemeral queues that are automatically removed when the user disconnects

Chat-transportation is intentionally kept thin by design to guarantee speed, isolation, and scalability.

## 🧩 Features

1) One-time pass (OTP) endpoint
 - Obtains a short-lived token from the authentication service.
 - Used to authenticate WebSocket connections safely and without headers.

2) WebSocket hub management
 - Tracks connected users, attaches them to their transient queues, and dispatches messages to active sessions.

3) Per-user ephemeral queues
 - One queue per connected user.
 - Automatically deleted when the user disconnects — no garbage left behind.

4) Clean separation of concerns
 - Chat-auth only transports data.
 - Business logic, authorization, storage, validation — handled elsewhere.

Clean Architecture (4-layer structure)

**Domain** — pure entities and value objects

**Application** — orchestration and business flow

**Interface Adapters** — minimal transport layer

**Infrastructure** — RabbitMQ, frameworks, I/O

## ⚙️ Usage

1) Clone the repository.
2) Create .env file in the backend directory using the env_example.txt as an example.
3) ```docker-compose up --build``` in the directory where docker-compose.yaml file is located.
4) The application will be available on **http://localhost:8001**

## 📘 Docs.

Available at the standard FastAPI docs endpoint **http://localhost:8001/docs**

## 🔗 Back to the Main Index Repository.

https://github.com/aleksandrshaulskyi/chat-index
