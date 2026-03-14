# LLM-Observability
Monitor a local LLM API (Ollama) with Flask, Prometheus, and Grafana Cloud, including metrics dashboards, alerts.

# Table of Contents

Overview

Features

Prerequisites

Installation

Flask API Usage

Prometheus Metrics

Grafana Dashboards

Alerts

Project Architecture


# Overview

This project demonstrates full observability for a local LLM API:

Tracks requests, errors, latency, and tokens generated

Visualizes metrics in Grafana Cloud dashboards

Sends alerts for high latency or errors

Optionally collects logs for debugging slow requests

It’s designed to mirror production-level observability for AI services.


# Features

/generate endpoint to send prompts to Ollama

/metrics endpoint for Prometheus

Grafana Cloud dashboards for real-time metrics

Alerts for:

High latency (P95 > threshold)


# Prerequisites

Python 3.11+

Ollama installed locally

Grafana Cloud account (hosted Prometheus + Loki)

curl or Postman (for testing API)

# Installation

Install Python dependencies:
```bash

pip install flask prometheus-client requests
```

Ensure Ollama is running locally:
```bash
ollama run gemma3:1b
```

Configure Grafana Agent for Prometheus metrics inside your prometheus configuration yaml file:

```yaml
remote_write:
  - url: https://<GRAFANA_CLOUD_PROMETHEUS_URL>
    basic_auth:
      username: <USERNAME>
      password: <API_KEY>

```
Run Flask app:
```bash
llm_observability.py
```


# Flask API Usage

the python file is the falsk app , it is responsible for contacting the LLM model and gets the metrics from it and it runs on port 5000

Generate a response:
```bash
curl -X POST http://localhost:5000/generate \
-H "Content-Type: application/json" \
-d '{"prompt":"Explain Kubernetes"}'
```

Returns LLM response as JSON

Updates Prometheus metrics for requests, errors, latency, and tokens

# Prometheus Metrics

the prometheus configuration file is named prometheus.yaml and it has localhost:5000 as a target so that prometheus can read the metrics from the flask app

Metrics exposed at http://localhost:5000/metrics:

llm_requests_total → total requests sent

llm_errors_total → total errors

llm_request_latency_seconds → histogram of request latency

llm_tokens_generated_total → total tokens generated


# Grafana Dashboards

Example panels:

| Metric          | PromQL Query                                                                              | Visualization |
| --------------- | ----------------------------------------------------------------------------------------- | ------------- |
| Requests Total  | `llm_requests_total`                                                                      | Stat          |
| Requests/sec    | `rate(llm_requests_total[1m])`                                                            | Time series   |
| Errors          | `llm_errors_total`                                                                        | Stat          |
| Tokens          | `llm_tokens_generated_total`                                                              | Stat          |
| Latency P95     | `histogram_quantile(0.95, sum(rate(llm_request_latency_seconds_bucket[1m])) by (le))`     | Time series   |



