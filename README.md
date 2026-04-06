# Cloud-Based Disaster Recovery and High Availability System

A simple web application that demonstrates disaster recovery workflows and high availability concepts.

This project helps show how a system can reduce downtime and data loss during failures.

## 1. Project Objective

Build a reliable and scalable DR solution that can:

- Monitor service health
- Detect failures quickly
- Trigger failover and recovery actions
- Minimize downtime (low RTO)
- Minimize data loss (low RPO)

## 2. Current Status

This version is a working prototype with:

- Flask backend
- SQLite database
- Backup and recovery simulation
- Dashboard for visibility
- Modular project structure

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
- Database: SQLite
- ORM: Flask-SQLAlchemy
- Auth: Flask-Login
- Frontend: HTML, CSS, JavaScript, Bootstrap

## 6. Project Structure

```text
SGP3/
  app.py
  config.py
  extensions.py
  requirements.txt
  cloud_dr_portal.db
  backups/
    archived/
  models/
    user_model.py
    backup_model.py
    recovery_model.py
  routes/
    auth_routes.py
    dashboard_routes.py
    backup_routes.py
    recovery_routes.py
  services/
    backup_service.py
    recovery_service.py
  templates/
    login.html
    register.html
    dashboard.html
    backups.html
    recovery.html
  static/
    css/styles.css
    js/scripts.js
```

## 7. Getting Started

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

```bat
.\.venv\Scripts\activate.bat
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run Application

Option 1:

```bash
flask --app app.py run --debug
```

Option 2:

```bash
python app.py
```

## 8. Configuration

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

## 9. How to Use

1. Open the app in browser.
2. Register a user or log in.
3. Upload backup files from Backups page.
4. Archive, restore, or purge backups.
5. Open Recovery page and run recovery simulation.
6. View recovery logs and dashboard metrics.

## 10. Missing Components for Production

The current version is a prototype. For industry readiness, add:

- Real health monitoring endpoints and probes
- Automated failover with load balancer or DNS failover
- PostgreSQL with replication and PITR
- Object storage for backups (S3, Azure Blob, GCS)
- Alerting (email, Slack, PagerDuty)
- Centralized logging and observability
- Role-based access control and audit trails
- CI/CD pipeline and infrastructure as code

## 11. Recommended Improvement Plan

### Phase 1 (Now)

- Add tests for backup and recovery workflows
- Add structured logs and request IDs
- Move secrets to environment management
- Add migration support (Flask-Migrate)

### Phase 2 (Next)

- Migrate from SQLite to PostgreSQL
- Move files from local disk to cloud object storage
- Add async jobs for heavy operations
- Add metrics, dashboards, and alerts

### Phase 3 (Production)

- Containerize with Docker
- Deploy with Kubernetes or managed containers
- Use multi-zone architecture
- Implement failover and failback runbooks
- Run periodic disaster recovery drills

## 12. Suggested Cloud Mapping

AWS example:

- App: ECS/Fargate or EKS
- DB: RDS PostgreSQL Multi-AZ
- Storage: S3 with versioning and lifecycle
- Secrets: Secrets Manager
- Monitoring: CloudWatch + Grafana
- Traffic: ALB + Route 53 health-based routing

Equivalent services are available in Azure and GCP.

## 13. Security Best Practices

- Never use default credentials in production
- Enforce strong authentication and authorization
- Enable encryption in transit and at rest
- Keep immutable logs for recovery actions
- Scan dependencies and container images regularly

## 14. Success Metrics

Track these core metrics:

- Recovery Time Objective (RTO)
- Recovery Point Objective (RPO)
- Mean Time To Detect (MTTD)
- Mean Time To Recover (MTTR)
- Backup success and restore success rate

## 15. Future Enhancements

- Real-time notifications and incident response workflows
- Multi-region active-passive setup
- Policy-driven backup retention and cleanup
- Advanced availability dashboards
- Automated rollback in CI/CD deployments