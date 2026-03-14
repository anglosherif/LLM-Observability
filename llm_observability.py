from flask import Flask, request, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import requests
import time

app = Flask(__name__)

# Metrics
REQUEST_COUNT = Counter(
    'llm_requests_total',
    'Total LLM requests'
)

ERROR_COUNT = Counter(
    'llm_errors_total',
    'Total LLM errors'
)

LATENCY = Histogram(
    'llm_request_latency_seconds',
    'LLM request latency'
)

TOKENS = Counter(
    'llm_tokens_generated_total',
    'Total tokens generated'
)

@app.route("/generate", methods=["POST"])
def generate():

    prompt = request.json.get("prompt")

    REQUEST_COUNT.inc()

    start = time.time()

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma3:1b",
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()

        latency = time.time() - start
        LATENCY.observe(latency)

        tokens = len(data["response"].split())
        TOKENS.inc(tokens)

        return jsonify(data)

    except Exception as e:
        ERROR_COUNT.inc()
        return {"error": str(e)}, 500


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


app.run(port=5000)
