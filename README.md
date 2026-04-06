# Cloud-Based Disaster Recovery and High Availability System

A simple web application that demonstrates disaster recovery workflows and high availability concepts.

This project helps show how a system can reduce downtime and data loss during failures.

**🚀 Live Demo:** [http://15.206.172.53:5000/auth/login](http://15.206.172.53:5000/auth/login) *(Currently hosted on an AWS EC2 instance)*

## 1. Project Objective

Build a reliable and scalable DR solution that can:

- Monitor service health
- Detect failures quickly
- Trigger failover and recovery actions
- Minimize downtime (low RTO)
- Minimize data loss (low RPO)

## 2. Current Status & AWS Deployment

This version is a fully functional prototype that has been successfully deployed to the cloud.

**Current Live Deployment:** The application is currently accessible via a standalone AWS EC2 instance. This "Phase 1" deployment serves to validate the application logic, database models, and backup simulation workflows in a live cloud environment.

**High Availability Test Environment (Architected):** A robust High Availability (HA) test architecture has been designed and provisioned, which includes:
- **Application Load Balancer (ALB)** to distribute traffic.
- **Auto Scaling Group (ASG)** configured with a minimum of 2 EC2 instances across multiple Availability Zones.
- *Note: The live demo is currently running on a single EC2 instance while the backend is being refactored to support distributed, stateless operation (e.g., migrating from local SQLite to RDS) before deploying to the full ASG environment.*

## 3. Key Features Implemented

- User authentication (login, register, logout)
- Backup upload and metadata tracking
- Archive and restore backup workflow
- Soft delete and recover-from-trash flow
- Recovery simulation with event logs
- Dashboard with backup and recovery counters

## 4. System Design (Current)

The app currently runs as a single Flask service with modular layers:

- Routes: request handling
- Services: backup/recovery business logic
- Models: database entities
- Templates and static assets: user interface

Logical DR roles represented in the project:

- Primary system
- Backup/standby storage and workflows
- Recovery controller logic (simulated)

## 5. Tech Stack

- Backend: Python, Flask
- Database: SQLite (Transitioning to PostgreSQL/Amazon RDS)
- ORM: Flask-SQLAlchemy
- Auth: Flask-Login
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Cloud Infrastructure: AWS (EC2, ALB, Auto Scaling Groups)

## 6. Getting Started (Local Development)

### Prerequisites

- Python 3.10 or above
- pip

### Installation

```bash
python -m venv .venv
```

Activate virtual environment:

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

CMD:

```dos
.\.venv\Scripts\activate.bat
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run Application

```bash
flask --app app.py run --debug
```

## 7. Configuration

Set environment variables before running in real environments:

- SECRET_KEY
- DATABASE_URL
- ADMIN_DEFAULT_USERNAME
- ADMIN_DEFAULT_PASSWORD

PowerShell example:

```powershell
$env:SECRET_KEY="replace-this-secret"
$env:DATABASE_URL="sqlite:///cloud_dr_portal.db"
$env:ADMIN_DEFAULT_USERNAME="admin"
$env:ADMIN_DEFAULT_PASSWORD="change-this-password"
```

## 8. How to Use

- Open the app in the browser via the live IP or localhost.
- Register a user or log in.
- Upload backup files from the Backups page.
- Archive, restore, or purge backups.
- Open the Recovery page and run a recovery simulation.
- View recovery logs and dashboard metrics.

## 9. Recommended Improvement Plan (The Path to True HA)

To fully utilize the mocked Auto Scaling Group and Load Balancer test environment, the following transitions are actively planned:

Phase 1: Decoupling State (In Progress)

- Database Migration: Replace the local sqlite:///cloud_dr_portal.db with an Amazon RDS (PostgreSQL/MySQL) instance so multiple EC2s can share the same user data.
- Shared Storage: Refactor backup_service.py to upload files to an Amazon S3 bucket rather than the local EC2 disk.

Phase 2: Production Web Server

- Wrap the Flask application in a production WSGI server (Gunicorn) and set up a reverse proxy (Nginx) to handle incoming HTTP requests securely on port 80.

Phase 3: The HA Cutover

- Create an Amazon Machine Image (AMI) of the stateless EC2 configuration.
- Attach the Load Balancer and execute the Auto Scaling Group deployment to achieve a multi-AZ, fault-tolerant infrastructure.

## 10. Security Best Practices

- Never use default credentials in production
- Enforce strong authentication and authorization
- Enable encryption in transit and at rest
- Keep immutable logs for recovery actions
- Scan dependencies and container images regularly

## 11. Success Metrics

Track these core metrics:

- Recovery Time Objective (RTO)
- Recovery Point Objective (RPO)
- Mean Time To Detect (MTTD)
- Mean Time To Recover (MTTR)
- Backup success and restore success rate

## 12. Team Members

- Aarya Shah - [GitHub](https://github.com/shahaarya465)
- Aditya Patel - [GitHub](https://github.com/adityapatel007-byte)