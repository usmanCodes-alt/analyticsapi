# AnalyticsAPI

AnalyticsAPI is a simple RESTful API for storing and retrieving time-series data related to web events. It allows you to track web activity and provides endpoints for analyzing these events over time. This project is designed to be deployed using Docker for easy scalability and deployment.

## Features

- Store event data as time-series entries.
- Retrieve event data based on filters like date ranges.
- Easily deploy using Docker.

## Requirements

Before running the project, ensure you have the following installed on your machine:

- Docker (for containerization)
- Python 3.x (for development purposes, if not using Docker)

## Setup and Installation

### Docker

1. Clone the repository:

   ```bash
   git clone https://github.com/usmanCodes-alt/analyticsapi.git
   cd analyticsapi
   ```

2. Build the Docker image:

   ```bash
   docker build -t analytics-api .
   ```

3. Run the Docker container:

   ```bash
   docker run -p 8000:8000 analytics-api
   ```

This will start the API at `http://localhost:8000`.

### Without Docker (for local development)

1. Clone the repository:

   ```bash
   git clone https://github.com/usmanCodes-alt/analyticsapi.git
   cd analyticsapi
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python app.py
   ```

This will start the API at `http://localhost:8000`.

## Usage

The API provides the following endpoints:

### 1. **POST /events**

Store an event with time-series data.

**Request Body:**

```json
{
  "event_type": "page_view",
  "timestamp": "2025-04-08T10:00:00Z",
  "user_id": "12345"
}
```
