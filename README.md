# Vehicle Inspection Web App

## Overview
The **Vehicle Inspection Web App** is a web-based application designed to facilitate vehicle inspections, appointments, and report generation. The app provides features for managing customers, appointments, reports, and more, making it a comprehensive tool for vehicle inspection centers.

## Features
- **Appointment Scheduling**: Manage and schedule vehicle inspection appointments.
- **Customer Management**: Store and manage customer details.
- **Report Generation**: Generate detailed vehicle inspection reports.
- **Staff Management**: Handle staff information and roles.
- **PDF Report Creation**: Create and download PDF versions of inspection reports.
- **Branch and Company Management**: Organize branches and manage company information.
- **Blueprint Architecture**: Modular structure with blueprints for various routes.

## Tech Stack
- **Backend**: Python, Flask, Flask-SQLAlchemy
- **Database**: SQLAlchemy ORM (supports various database backends)
- **Frontend**: HTML, CSS, JavaScript (Flask templates)
- **PDF Generation**: WeasyPrint
- **Environment Management**: Python dotenv for environment variable handling
- **Containerization**: Docker

## Installation and Setup

### Prerequisites
- [Python 3.10+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [pip](https://pip.pypa.io/en/stable/installation/)

### Using Docker
1. **Build the Docker image**:
    ```bash
    docker build -t vehicle-inspection-web-app .
    ```

2. **Run the Docker container**:
    ```bash
    docker run -p 5000:5000 vehicle-inspection-web-app
    ```


## Troubleshooting
- **Environment Variables Not Loading**: Ensure the `.env` file is present and correctly configured.
- **Port Issues**: Check if port 5000 is free or modify the port mapping in the `docker run` command.
- **PDF Generation Errors**: Ensure all WeasyPrint dependencies (`libpango`, `libcairo`) are installed and available in your Docker image.


