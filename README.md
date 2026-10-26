# LeaklyTex
AI-assisted wastewater pipeline leak prediction and monitoring system
# LeaklyTex

### Know your pipes. Act before failure.

**LeaklyTex** is an AI-assisted wastewater pipeline health monitoring and predictive maintenance project designed to help identify potentially problematic pipe conditions and prioritize maintenance inspections.

## Problem Statement

Wastewater pipelines in commercial buildings, hospitals, shopping malls, and other facilities can develop faults that are difficult to identify through routine visual inspection. Undetected pipeline problems may contribute to leakage, unpleasant odours, infrastructure damage, and maintenance challenges.

LeaklyTex explores how data-driven prediction and a monitoring dashboard can help maintenance teams assess pipe conditions and identify assets that may require attention.

## Objectives

- Monitor and organize pipeline asset information.
- Use machine learning to support pipe-condition prediction.
- Present pipeline condition information through a dashboard.
- Help prioritize inspections and preventive maintenance.
- Establish a foundation for future integration with environmental and hardware sensors.

## Key Features

- **Pipeline monitoring dashboard:** A centralized interface for viewing pipeline assets and their reported condition.
- **AI-assisted prediction:** A backend API that uses a trained machine-learning model to predict pipe condition from supported input features.
- **Database integration:** PostgreSQL for structured application data.
- **REST API:** FastAPI-based backend services.
- **Interactive frontend:** A React and Vite web interface.
- **Extensible architecture:** Designed to support future sensor integration and additional predictive analytics.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React, Vite, CSS |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| Database migrations | Alembic |
| Machine learning | Trained model using joblib |
| Testing | Pytest |

## System Architecture

1. **Input data:** Pipeline asset details and supported condition-related features.
2. **Backend API:** FastAPI validates requests and coordinates application logic.
3. **Prediction layer:** The trained model generates a pipe-condition prediction from supported inputs.
4. **Database:** PostgreSQL stores structured application information.
5. **Dashboard:** The frontend presents monitoring information to users.

## Project Status

LeaklyTex is a developing prototype.

The current machine-learning prediction workflow is data-driven. It should not be interpreted as proof of a physical leak or as a substitute for on-site inspection. Live hardware sensor integration and real-world validation must be completed and verified before the system can be used for operational safety decisions.

## Getting Started

### Prerequisites

- Python installed
- PostgreSQL installed and running
- Node.js and npm installed

### 1. Clone the repository

```bash
git clone https://github.com/sec24cs210-del/LeaklyTex.git
cd LeaklyTex
```

### 2. Configure the backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure your local environment variables using the provided `.env.example` file. Do not commit credentials or secrets.

Create the required PostgreSQL database and configure its connection settings before starting the backend.

### 3. Run database migrations

From the `backend` directory, run:

```bash
alembic upgrade head
```

### 4. Start the backend

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API documentation.

### 5. Start the frontend

Open a second Terminal window:

```bash
cd ~/leaklytex/frontend
npm install
npm run dev
```

Open the local URL printed by Vite in your browser.

> Setup commands may require adjustment to match the current environment configuration and database settings.

## Future Enhancements

- Integrate ESP32 and environmental sensors.
- Incorporate validated pressure, flow, vibration, and gas-monitoring data where appropriate.
- Improve prediction evaluation using independent test datasets.
- Add maintenance history, alerts, and location-based asset visualization.
- Validate the system under real-world pipeline conditions.

## Intended Impact

LeaklyTex aims to support safer infrastructure management, more proactive maintenance, and responsible use of AI for wastewater pipeline monitoring.

## Disclaimer

This project is a prototype for educational and development purposes. Predictions are not guaranteed to identify actual leaks or hazardous conditions. Physical inspection and appropriate safety procedures remain essential.

---

**Developed as a student engineering project.**

