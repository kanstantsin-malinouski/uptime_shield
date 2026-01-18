# Uptime Shield: Distributed Website Monitoring System

**Uptime Shield** is a high-performance, distributed system designed to monitor the availability and response time of various websites in real-time. This project demonstrates core principles of **distributed computing** and **parallel processing** using a Master-Worker architecture.

---

## 🏗 System Architecture

The project is built on a microservices architecture to ensure high availability and horizontal scalability.

* **Web Dashboard (Master):** A Flask-based interface that allows users to add URLs. It acts as a producer by sending check-tasks to the message broker.
* **RabbitMQ (Message Broker):** Orchestrates task distribution. It ensures that tasks are reliably delivered to workers and handles the load balancing.
* **Distributed Workers:** Independent Python nodes that pull tasks from RabbitMQ, perform asynchronous HTTP checks, and measure latency.
* **Redis (Shared Result Store):** An in-memory database used for real-time synchronization of results between workers and the dashboard.



---

## 🚀 Key Features

* **Parallel Processing:** Multiple worker containers process website checks simultaneously, significantly reducing total execution time.
* **Horizontal Scalability:** You can increase the number of workers dynamically to handle a larger volume of URLs.
* **Fault Tolerance:** If a worker container crashes, RabbitMQ keeps the task in the queue until another worker is ready to process it.
* **Live Updates:** The dashboard uses asynchronous polling to show status changes and latency updates every 2 seconds.
* **Automated Scheduling:** Includes a background thread that automatically triggers re-checks for all monitored sites every 30 seconds.

---

## 🛠 Tech Stack

| Technology | Role |
| :--- | :--- |
| **Python 3.9** | Core programming language |
| **Flask** | Web framework for the Dashboard |
| **RabbitMQ** | Distributed message broker (AMQP) |
| **Redis** | In-memory key-value storage for results |
| **Docker / Compose** | Containerization and orchestration |
| **Tailwind CSS** | Modern UI styling |

---

## 🚦 Getting Started

### Prerequisites
* Installed **Docker** and **Docker Compose**.

### Installation & Launch
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kanstantsin-malinouski/uptime_shield.git
    cd uptime_shield
    ```

2.  **Build and run the containers:**
    ```bash
    docker-compose up --build
    ```

3.  **Access the Dashboard:**
    Open your browser and go to `http://localhost:5000`.

---

## 📈 Scalability Demonstration

To prove the distributed nature of the system during a presentation, you can scale the worker nodes on the fly using this command:

```bash
docker-compose up --scale worker=5 -d
```


## Project Structure
```
uptime_project/
├── docker-compose.yml       # Orchestration file
├── web_app/                 # Dashboard & Task Producer
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── templates/
│       └── index.html       # UI with Tailwind CSS
└── worker/                  # Task Consumer
    ├── worker.py
    ├── Dockerfile
    └── requirements.txt

```
