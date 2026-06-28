# Containerization — Deployment Runbook

## 1. What You're Deploying

Packaging your AI services (FastAPI + RAG pipeline + vector DB + cache) into reproducible containers. You know Docker. The AI twist: large model files, GPU passthrough, pip layer caching for ML dependencies, and startup time optimization.

**AI-specific challenge:** ML Python packages (torch, transformers, sentence-transformers) are 2-5GB. Naive Dockerfiles produce 10GB+ images with 30-minute builds. Model files add another 1-15GB. You need multi-stage builds, proper layer ordering, and a model-loading strategy.

## 2. Prerequisites & Dependencies

```bash
# Verify Docker with GPU support
docker --version          # 24.0+
nvidia-smi               # GPU available
docker run --gpus all nvidia/cuda:12.1-base nvidia-smi  # GPU in Docker
```

| Requirement | Why |
|-------------|-----|
| Docker 24.0+ | BuildKit by default, better layer caching |
| NVIDIA Container Toolkit | GPU passthrough for local inference |
| Module 5 Topic 1 complete | FastAPI app ready to containerize |
| `.dockerignore` configured | Prevent copying venv, __pycache__, .git |

## 3. Step-by-Step Procedure

### 3.1 .dockerignore (Critical for AI Projects)

```dockerignore
# .dockerignore
.git
.venv
__pycache__
*.pyc
.env
.env.*
models/          # Don't bake models into image!
data/raw/
*.ipynb
.mypy_cache
.pytest_cache
node_modules
```

### 3.2 Multi-Stage Dockerfile for AI Service

```dockerfile
# Dockerfile
# Stage 1: Dependencies (cached layer — changes rarely)
FROM python:3.11-slim AS dependencies

WORKDIR /app

# System deps for ML packages (numpy, scipy, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (layer caching!)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Application (changes frequently)
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy installed packages from dependencies stage
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Runtime system deps only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY app/ ./app/
COPY prompts/ ./prompts/

# Non-root user
RUN useradd -m -r appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

### 3.3 GPU-Enabled Dockerfile (Local Inference)

```dockerfile
# Dockerfile.gpu — for running local models (vLLM, HuggingFace)
FROM nvidia/cuda:12.1-runtime-ubuntu22.04 AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 python3-pip curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ML dependencies (large layer — keep stable)
COPY requirements-gpu.txt .
RUN pip install --no-cache-dir -r requirements-gpu.txt

COPY app/ ./app/
COPY prompts/ ./prompts/

# Model directory mount point
VOLUME /models

ENV MODEL_PATH=/models
ENV CUDA_VISIBLE_DEVICES=0

HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

### 3.4 Requirements Split Strategy

```txt
# requirements.txt — API dependencies (small, changes often)
fastapi==0.115.0
uvicorn[standard]==0.30.0
pydantic==2.9.0
langchain-core==0.3.0
langchain-openai==0.2.0
langgraph==0.2.0
sse-starlette==2.1.0
redis==5.0.0
httpx==0.27.0
```

```txt
# requirements-gpu.txt — includes heavy ML deps (large, changes rarely)
-r requirements.txt
torch==2.4.0
transformers==4.44.0
sentence-transformers==3.0.0
vllm==0.6.0
accelerate==0.34.0
```

### 3.5 Docker Compose for Local Development

```yaml
# docker-compose.yml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - VECTOR_DB_URL=http://chromadb:8001
      - REDIS_URL=redis://redis:6379
    depends_on:
      chromadb:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./prompts:/app/prompts  # Hot-reload prompts without rebuild

  chromadb:
    image: chromadb/chroma:0.5.5
    ports:
      - "8001:8000"
    volumes:
      - chroma_data:/chroma/chroma
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - redis_data:/data

  # Optional: Prometheus for metrics
  prometheus:
    image: prom/prometheus:v2.53.0
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml

volumes:
  chroma_data:
  redis_data:
```

### 3.6 GPU Docker Compose (Local Inference)

```yaml
# docker-compose.gpu.yml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.gpu
    ports:
      - "8000:8000"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    volumes:
      - ./models:/models  # Mount model files, don't bake into image
    environment:
      - MODEL_PATH=/models/mistral-7b-instruct
      - CUDA_VISIBLE_DEVICES=0
```

### 3.7 Model File Strategy

```bash
# NEVER bake models into Docker image. Options:

# Option 1: Volume mount (local dev / single server)
docker run -v /host/models:/models my-ai-service

# Option 2: Download at startup (cloud / ephemeral containers)
# In your app startup:
```

```python
# app/model_loader.py
import os
from huggingface_hub import snapshot_download

async def ensure_model_available():
    """Download model on first startup, cached on volume for subsequent starts."""
    model_path = os.environ["MODEL_PATH"]
    if not os.path.exists(os.path.join(model_path, "config.json")):
        snapshot_download(
            repo_id="mistralai/Mistral-7B-Instruct-v0.3",
            local_dir=model_path,
            token=os.environ.get("HF_TOKEN")
        )
```

## 4. Configuration Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_PATH` | Directory containing model files | `/models` |
| `HF_TOKEN` | HuggingFace token for gated models | (optional) |
| `CUDA_VISIBLE_DEVICES` | Which GPUs to use | `0` |
| `DOCKER_BUILDKIT` | Enable BuildKit (better caching) | `1` |
| `COMPOSE_PROFILES` | Select service profiles | `default` |

## 5. Verification & Smoke Tests

```bash
# Build and verify image size
docker build -t ai-service . && docker images ai-service
# Target: < 2GB for API-only, < 8GB for GPU inference

# Run and test
docker compose up -d
docker compose ps  # All services "healthy"

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/ready

# Check GPU access (if using GPU image)
docker compose -f docker-compose.gpu.yml exec api python -c "import torch; print(torch.cuda.is_available())"

# Verify layer caching (second build should be fast)
docker build -t ai-service .  # Should see "CACHED" for dependencies layer
```

## 6. Monitoring & Alerting

| Metric | Alert Threshold | Why |
|--------|----------------|-----|
| Container restart count | > 2 in 5 min | OOM or crash loop |
| Memory usage | > 85% of limit | Need to increase or optimize |
| GPU memory usage | > 90% | Model too large for GPU |
| Image pull time | > 5 min | Image too large, optimize layers |
| Startup time | > 120s | Model loading too slow |

## 7. Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| OOM killed on startup | Loading embeddings model into memory | Increase memory limit or use lazy loading |
| `nvidia-smi` not found in container | NVIDIA Container Toolkit not installed | Install toolkit, verify with `docker run --gpus all` |
| Build takes 20+ minutes | Pip installing on every code change | Reorder Dockerfile: COPY requirements.txt BEFORE COPY app/ |
| Image is 10GB+ | Including model files or build tools in final stage | Multi-stage build, mount models as volume |
| "No space left on device" | Docker cache full | `docker system prune -a`, increase disk allocation |
| Torch can't find CUDA | CUDA version mismatch | Match torch version to base image CUDA version |

## 8. Security & Compliance

- Run as non-root user (already in Dockerfile)
- Scan images: `docker scout cves ai-service`
- Never include API keys in image (use runtime env vars)
- Use specific image tags, never `latest` in production
- Mount secrets as read-only volumes, not environment variables for sensitive data

## 9. Cost Management

- Multi-stage builds reduce image size → faster pulls → lower storage costs
- Use `python:3.11-slim` not `python:3.11` (saves ~800MB)
- Share base layers across services (use same base image)
- GPU containers cost significantly more — only use when serving local models
- Consider CPU inference for small models (< 1B params) to avoid GPU costs

## 10. Maintenance & Updates

- **Dependency updates:** Update `requirements.txt`, rebuild. Layer cache invalidates automatically
- **Model updates:** Replace files in mounted volume, restart container
- **Base image updates:** Schedule monthly rebuilds for security patches
- **Scaling:** Docker Compose for dev, graduate to Kubernetes for production multi-node
- **Cleanup:** Schedule `docker system prune` weekly to reclaim space
