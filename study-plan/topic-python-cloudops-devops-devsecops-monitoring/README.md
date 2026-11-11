# Python for CloudOps + DevOps + DevSecOps + Monitoring

A beginner-to-intermediate study plan for using **Python** to automate cloud operations, build DevOps pipelines, implement DevSecOps security practices, and construct observability stacks.

---

## Prerequisites

### Tools to Install

| Tool | Purpose | Install |
|------|---------|---------|
| Python 3.10+ | Core language | https://www.python.org/downloads/ |
| pip + virtualenv | Dependency management | `pip install virtualenv` |
| Docker Desktop | Container management (Phase 3) | https://www.docker.com/products/docker-desktop/ |
| kubectl | Kubernetes CLI (Phase 3) | https://kubernetes.io/docs/tasks/tools/ |
| AWS CLI | Cloud automation (Phase 2) | https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html |
| Git | Version control | https://git-scm.com/ |

### Prior Knowledge Assumed
- Basic Python (variables, functions, loops, dictionaries)
- Basic Linux/terminal familiarity (cd, ls, cat, grep)
- Conceptual understanding of cloud computing (VMs, object storage, containers)

### Accounts to Create (free tiers available)
- AWS Free Tier account (Phase 2): https://aws.amazon.com/free/
- Docker Hub account (Phase 3): https://hub.docker.com/
- Grafana Cloud free account (Phase 5): https://grafana.com/products/cloud/

---

## Recommended Resources

### 📋 Official Documentation

| Resource | URL |
|----------|-----|
| Python 3.10 Official Docs | https://docs.python.org/3.10/ |
| Python Packaging User Guide | https://packaging.python.org/ |
| AWS boto3 Documentation | https://boto3.amazonaws.com/v1/documentation/api/latest/index.html |
| Azure SDK for Python | https://learn.microsoft.com/en-us/azure/developer/python/ |
| Google Cloud Python Client Libraries | https://cloud.google.com/python/docs/reference |
| Docker SDK for Python | https://docker-py.readthedocs.io/en/stable/ |
| Kubernetes Python Client | https://github.com/kubernetes-client/python |
| Prometheus Python Client | https://github.com/prometheus/client_python |
| OpenTelemetry Python | https://opentelemetry-python.readthedocs.io/ |

### 📚 Core Documentation by Domain

| Domain | Resource | URL |
|--------|----------|-----|
| CloudOps | boto3 Quickstart | https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html |
| CloudOps | AWS SDK Examples (Python) | https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python |
| DevOps | Docker SDK for Python Reference | https://docker-py.readthedocs.io/en/stable/api.html |
| DevOps | Kubernetes Python Client Wiki | https://github.com/kubernetes-client/python/tree/master/kubernetes/docs |
| DevOps | PyGitHub Documentation | https://pygithub.readthedocs.io/ |
| DevSecOps | Bandit Documentation | https://bandit.readthedocs.io/en/latest/ |
| DevSecOps | pip-audit Documentation | https://pypi.org/project/pip-audit/ |
| DevSecOps | OWASP Python Security | https://cheatsheetseries.owasp.org/cheatsheets/Python_Security_Cheat_Sheet.html |
| DevSecOps | HashiCorp Vault Python Client | https://hvac.readthedocs.io/en/stable/ |
| Monitoring | Prometheus Client Python | https://github.com/prometheus/client_python/blob/master/README.md |
| Monitoring | OpenTelemetry Python Docs | https://opentelemetry-python.readthedocs.io/en/latest/ |
| Monitoring | Grafana HTTP API | https://grafana.com/docs/grafana/latest/developers/http_api/ |

### 🎓 Training & Courses

| Resource | URL |
|----------|-----|
| Python for DevOps (book by O'Reilly) | https://www.oreilly.com/library/view/python-for-devops/9781492057680/ |
| AWS Python SDK Tutorial (official) | https://aws.amazon.com/developer/language/python/ |
| Real Python — Automation Topics | https://realpython.com/tutorials/devops/ |
| CloudAcademy — Python for AWS | — search: "Cloud Academy Python AWS automation" |
| Udemy — Python for Cloud & DevOps | — search: "Udemy Python DevOps automation" |
| OpenTelemetry YouTube Demos | https://www.youtube.com/@opentelemetry |

### 📝 Cheat Sheets & Quick Reference

| Resource | URL |
|----------|-----|
| boto3 Cheat Sheet | https://www.pythonsheets.com/notes/python-aws.html |
| Python subprocess Quick Ref | https://docs.python.org/3/library/subprocess.html |
| Docker SDK for Python Quick Ref | https://docker-py.readthedocs.io/en/stable/containers.html |
| Click CLI Framework Cheat Sheet | https://click.palletsprojects.com/en/8.x/quickstart/ |
| Prometheus Data Model | https://prometheus.io/docs/concepts/data_model/ |
| OpenTelemetry Semantic Conventions | https://opentelemetry.io/docs/specs/semconv/ |

### 🛠️ Key Docs by Phase/Feature

| Phase | Feature | URL |
|-------|---------|-----|
| Phase 1 | subprocess module | https://docs.python.org/3/library/subprocess.html |
| Phase 1 | pathlib module | https://docs.python.org/3/library/pathlib.html |
| Phase 1 | python-dotenv | https://saurabh-kumar.com/python-dotenv/ |
| Phase 1 | Click CLI | https://click.palletsprojects.com/en/8.x/ |
| Phase 1 | structlog | https://www.structlog.org/en/stable/ |
| Phase 2 | boto3 EC2 | https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html |
| Phase 2 | boto3 S3 | https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html |
| Phase 2 | boto3 CloudWatch | https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html |
| Phase 2 | Azure Identity SDK | https://learn.microsoft.com/en-us/python/api/azure-identity/ |
| Phase 2 | GCP Resource Manager | https://cloud.google.com/resource-manager/docs/libraries |
| Phase 3 | Docker SDK containers | https://docker-py.readthedocs.io/en/stable/containers.html |
| Phase 3 | Kubernetes Python Client | https://github.com/kubernetes-client/python/tree/master/kubernetes |
| Phase 3 | PyGitHub Workflows | https://pygithub.readthedocs.io/en/latest/github_objects/WorkflowRun.html |
| Phase 4 | Bandit CLI Reference | https://bandit.readthedocs.io/en/latest/man/bandit.html |
| Phase 4 | pip-audit CLI | https://pypi.org/project/pip-audit/ |
| Phase 4 | HVAC Vault client | https://hvac.readthedocs.io/en/stable/usage/secrets_engines/kv_v2.html |
| Phase 4 | detect-secrets | https://github.com/Yelp/detect-secrets |
| Phase 5 | prometheus_client Python | https://github.com/prometheus/client_python |
| Phase 5 | OpenTelemetry SDK setup | https://opentelemetry-python.readthedocs.io/en/latest/getting-started.html |
| Phase 5 | Grafana API Auth | https://grafana.com/docs/grafana/latest/developers/http_api/auth/ |
| Phase 5 | PagerDuty Events v2 API | https://developer.pagerduty.com/docs/ZG9jOjExMDI5NTgw-events-api-v2-overview |
| Phase 5 | Slack Incoming Webhooks | https://api.slack.com/messaging/webhooks |

### 🧪 Practice & Sandboxes

| Resource | URL |
|----------|-----|
| Katacoda Python DevOps Labs | — search: "Katacoda Python DevOps" |
| Play-with-Docker (free browser Docker) | https://labs.play-with-docker.com/ |
| Killercoda Kubernetes Labs | https://killercoda.com/playgrounds/scenario/kubernetes |
| AWS CloudShell (browser terminal) | https://aws.amazon.com/cloudshell/ |
| Localstack (AWS local emulator) | https://localstack.cloud/ |
| Minikube (local Kubernetes) | https://minikube.sigs.k8s.io/docs/start/ |
| Grafana Play (live demo) | https://play.grafana.org/ |

### 🏘️ Community & Support

| Resource | URL |
|----------|-----|
| Python DevOps Subreddit | https://www.reddit.com/r/devops/ |
| boto3 GitHub Issues | https://github.com/boto/boto3/issues |
| OpenTelemetry Slack | https://cloud-native.slack.com/ (CNCF Slack — #otel-python) |
| Stack Overflow — boto3 tag | https://stackoverflow.com/questions/tagged/boto3 |
| Stack Overflow — devops+python | https://stackoverflow.com/questions/tagged/python+devops |
| Awesome Python DevOps (curated list) | — search: "awesome-python-devops github" |
| Python Discord — devops channel | https://discord.gg/python |

---

## Study Plan Overview

| Phase | Title | Lessons | Est. Time |
|-------|-------|---------|-----------|
| 1 | Python Automation Foundations | 5 | 4–5 hrs |
| 2 | Cloud Automation (CloudOps) | 5 | 6–8 hrs |
| 3 | CI/CD & Container Automation (DevOps) | 5 | 5–7 hrs |
| 4 | Security Automation (DevSecOps) | 5 | 5–6 hrs |
| 5 | Monitoring, Observability & Alerting | 6 | 8–10 hrs |
| Capstone | Python Ops Automation Platform | 1 | 6–10 hrs |

**Total: 26 lessons + 1 capstone | ~34–46 hours**

---

## Lesson Index

### Phase 1 — Python Automation Foundations
| Lesson | Title | Notebook |
|--------|-------|---------|
| 1.1 | DevOps Environment Setup | [phase-1-python-automation-foundations/lesson-1.1-devops-environment-setup.ipynb](phase-1-python-automation-foundations/lesson-1.1-devops-environment-setup.ipynb) |
| 1.2 | OS & Process Automation | [phase-1-python-automation-foundations/lesson-1.2-os-process-automation.ipynb](phase-1-python-automation-foundations/lesson-1.2-os-process-automation.ipynb) |
| 1.3 | Configuration Management | [phase-1-python-automation-foundations/lesson-1.3-configuration-management.ipynb](phase-1-python-automation-foundations/lesson-1.3-configuration-management.ipynb) |
| 1.4 | CLI Tools for Ops | [phase-1-python-automation-foundations/lesson-1.4-cli-tools.ipynb](phase-1-python-automation-foundations/lesson-1.4-cli-tools.ipynb) |
| 1.5 | Logging & Structured Logging | [phase-1-python-automation-foundations/lesson-1.5-logging-structured.ipynb](phase-1-python-automation-foundations/lesson-1.5-logging-structured.ipynb) |

### Phase 2 — Cloud Automation (CloudOps)
| Lesson | Title | Notebook |
|--------|-------|---------|
| 2.1 | AWS boto3 Basics & Authentication | [phase-2-cloud-automation-cloudops/lesson-2.1-boto3-basics.ipynb](phase-2-cloud-automation-cloudops/lesson-2.1-boto3-basics.ipynb) |
| 2.2 | AWS EC2, S3 & CloudWatch | [phase-2-cloud-automation-cloudops/lesson-2.2-ec2-s3-cloudwatch.ipynb](phase-2-cloud-automation-cloudops/lesson-2.2-ec2-s3-cloudwatch.ipynb) |
| 2.3 | Azure SDK for Python | [phase-2-cloud-automation-cloudops/lesson-2.3-azure-sdk.ipynb](phase-2-cloud-automation-cloudops/lesson-2.3-azure-sdk.ipynb) |
| 2.4 | GCP SDK for Python | [phase-2-cloud-automation-cloudops/lesson-2.4-gcp-sdk.ipynb](phase-2-cloud-automation-cloudops/lesson-2.4-gcp-sdk.ipynb) |
| 2.5 | Multi-Cloud Patterns | [phase-2-cloud-automation-cloudops/lesson-2.5-multi-cloud-patterns.ipynb](phase-2-cloud-automation-cloudops/lesson-2.5-multi-cloud-patterns.ipynb) |

### Phase 3 — CI/CD & Container Automation (DevOps)
| Lesson | Title | Notebook |
|--------|-------|---------|
| 3.1 | Docker SDK for Python | [phase-3-cicd-container-automation/lesson-3.1-docker-sdk.ipynb](phase-3-cicd-container-automation/lesson-3.1-docker-sdk.ipynb) |
| 3.2 | Kubernetes Python Client | [phase-3-cicd-container-automation/lesson-3.2-kubernetes-client.ipynb](phase-3-cicd-container-automation/lesson-3.2-kubernetes-client.ipynb) |
| 3.3 | GitHub Actions & PyGitHub | [phase-3-cicd-container-automation/lesson-3.3-github-actions-pygithub.ipynb](phase-3-cicd-container-automation/lesson-3.3-github-actions-pygithub.ipynb) |
| 3.4 | Pipeline Scripting Patterns | [phase-3-cicd-container-automation/lesson-3.4-pipeline-scripting-patterns.ipynb](phase-3-cicd-container-automation/lesson-3.4-pipeline-scripting-patterns.ipynb) |
| 3.5 | GitOps & Helm Automation | [phase-3-cicd-container-automation/lesson-3.5-gitops-helm-automation.ipynb](phase-3-cicd-container-automation/lesson-3.5-gitops-helm-automation.ipynb) |

### Phase 4 — Security Automation (DevSecOps)
| Lesson | Title | Notebook |
|--------|-------|---------|
| 4.1 | Static Analysis & Dependency Scanning | [phase-4-security-automation-devsecops/lesson-4.1-static-analysis.ipynb](phase-4-security-automation-devsecops/lesson-4.1-static-analysis.ipynb) |
| 4.2 | Container & Image Security | [phase-4-security-automation-devsecops/lesson-4.2-container-security.ipynb](phase-4-security-automation-devsecops/lesson-4.2-container-security.ipynb) |
| 4.3 | Secrets Management | [phase-4-security-automation-devsecops/lesson-4.3-secrets-management.ipynb](phase-4-security-automation-devsecops/lesson-4.3-secrets-management.ipynb) |
| 4.4 | Compliance as Code | [phase-4-security-automation-devsecops/lesson-4.4-compliance-as-code.ipynb](phase-4-security-automation-devsecops/lesson-4.4-compliance-as-code.ipynb) |
| 4.5 | Security Gates in CI/CD | [phase-4-security-automation-devsecops/lesson-4.5-security-gates-cicd.ipynb](phase-4-security-automation-devsecops/lesson-4.5-security-gates-cicd.ipynb) |

### Phase 5 — Monitoring, Observability & Alerting
| Lesson | Title | Notebook |
|--------|-------|---------|
| 5.1 | Prometheus Custom Metrics & Exporters | [phase-5-monitoring-observability-alerting/lesson-5.1-prometheus-custom-metrics.ipynb](phase-5-monitoring-observability-alerting/lesson-5.1-prometheus-custom-metrics.ipynb) |
| 5.2 | OpenTelemetry Python | [phase-5-monitoring-observability-alerting/lesson-5.2-opentelemetry-python.ipynb](phase-5-monitoring-observability-alerting/lesson-5.2-opentelemetry-python.ipynb) |
| 5.3 | Cloud-Native Monitoring | [phase-5-monitoring-observability-alerting/lesson-5.3-cloud-native-monitoring.ipynb](phase-5-monitoring-observability-alerting/lesson-5.3-cloud-native-monitoring.ipynb) |
| 5.4 | Structured Logging & Log Aggregation | [phase-5-monitoring-observability-alerting/lesson-5.4-structured-logging-aggregation.ipynb](phase-5-monitoring-observability-alerting/lesson-5.4-structured-logging-aggregation.ipynb) |
| 5.5 | Alerting & Incident Automation | [phase-5-monitoring-observability-alerting/lesson-5.5-alerting-incident-automation.ipynb](phase-5-monitoring-observability-alerting/lesson-5.5-alerting-incident-automation.ipynb) |
| 5.6 | Dashboards as Code | [phase-5-monitoring-observability-alerting/lesson-5.6-dashboards-as-code.ipynb](phase-5-monitoring-observability-alerting/lesson-5.6-dashboards-as-code.ipynb) |

### Capstone
| | Title | Notebook |
|-|-------|---------|
| Final | Python Ops Automation Platform | [capstone/capstone-project.ipynb](capstone/capstone-project.ipynb) |

---

## Capstone Overview

Build a Python-based **Ops Automation Platform** that ties together all five phases:

1. **CloudOps module** — Inventory and health-check AWS EC2 instances and S3 buckets using boto3
2. **Container security module** — Run Trivy container scans via subprocess; parse and report CVEs
3. **Prometheus exporter** — Export custom metrics (resource count, scan results, health scores) via HTTP
4. **Alerting module** — Send Slack webhook alerts when health thresholds are breached
5. **CLI interface** — Package everything as a Click CLI: `ops-bot inventory`, `ops-bot scan`, `ops-bot report`
6. **Deployment** — Containerize the platform with Docker and provide a `docker-compose.yml`

**Capstone directory:** `capstone/`

---

## How to Use These Notebooks

1. Install Jupyter: `pip install jupyterlab`
2. Create a virtual environment: `python -m venv .venv && source .venv/bin/activate` (Linux/macOS) or `.venv\Scripts\activate` (Windows)
3. Launch Jupyter Lab: `jupyter lab`
4. Open Phase 1 notebooks and run cells **top to bottom**
5. Complete exercises before advancing to the next lesson
6. **Do the Capstone only after completing all 5 phases**

> **Tip:** Install all dependencies for a lesson at the top of each notebook before running the rest.
