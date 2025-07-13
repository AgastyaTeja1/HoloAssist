# HoloAssist

**Seamless multimodal repair assistant** that overlays step-by-step guidance on live camera and voice streams in real time.

---

## Overview

HoloAssist combines Vision Transformers (ViT), GPT-4o, LangGraph orchestration, WebRTC streaming, and on-device inference (TensorFlow.js + WebGPU) to guide users through complex repairs. Capture video and audio in the browser; frames are analyzed on the backend (PyTorch ViT, Whisper STT, GPT-4o) and instructions are rendered as interactive overlays via Next.js.

---

## Features

- **Real-time object recognition** with ViT  
- **Natural language reasoning** via GPT-4o  
- **Workflow orchestration** with LangGraph  
- **Low-latency streaming** using WebRTC (aiortc)  
- **On-device inference** in browser (TensorFlow.js + WebGPU)  
- **Responsive web UI** built on Next.js  
- **Scalable deployment** on AWS EKS & GCP GKE with GPU autoscaling  
- **CI/CD** via GitHub Actions, multi-arch Docker images  
- **Observability**: Prometheus metrics, Grafana dashboards, Sentry error tracking  
- **Secrets management**: Vault CSI driver in Kubernetes  

---

## Tech Stack

| Layer            | Tools & Libraries                                              |
| ---------------- | -------------------------------------------------------------- |
| **Backend**      | FastAPI, aiortc, PyTorch (ViT), Whisper, LangChain/LangGraph |
| **Frontend**     | Next.js, React, Canvas/Three.js, WebRTC client                |
| **On-device ML** | TensorFlow.js, WebGPU                                         |
| **Streaming**    | WebRTC (aiortc), MediaRecorder                                |
| **Container**    | Docker, NVIDIA CUDA base images                               |
| **Orchestration**| Kubernetes (EKS, GKE), Helm charts (optional)                 |
| **Infra as Code**| Terraform (AWS, GCP)                                          |
| **CI/CD**        | GitHub Actions, Docker Buildx, ECR & GCR                      |
| **Monitoring**   | Prometheus, Grafana, Sentry                                   |
| **Secrets**      | HashiCorp Vault CSI driver                                    |

---

## Prerequisites

- **Local development:** Docker & Docker Compose  
- **Kubernetes:** `kubectl` configured for your cluster  
- **Cloud accounts:** AWS & GCP CLI authenticated  
- **GPU support:** NVIDIA drivers & device plugin  

---

## Installation & Quickstart

1. **Clone the repo**  
   ```bash
   git clone https://github.com/AgastyaTeja1/holoassist.git
   cd holoassist
    ```
2. **Local development (Docker Compose)**
    ```bash
    cd deploy
    docker-compose up --build
    ```
- **Backend:** http://localhost:8000

- **Frontend:** http://localhost:3000

3. **Kubernetes deployment**

- **AWS EKS**
    ```bash
    cd deploy/terraform/aws
    terraform init && terraform apply
    aws eks update-kubeconfig --name <cluster_name> --region <region>
    kubectl apply -f ../k8s/
    ```

- **GCP GKE**
    ```bash
    cd deploy/terraform/gcp
    terraform init && terraform apply
    gcloud container clusters get-credentials <cluster_name> --region <region>
    kubectl apply -f ../k8s/
    ```

4. **Scale GPU workers**
    ```bash
    kubectl scale deployment holoassist-backend --replicas=3
    ```
---

## Architecture Diagram

Browser (Next.js)
  ├─ getUserMedia → MediaRecorder → WebSocket → FastAPI + aiortc
  ├─ Canvas overlays ← WebSocket responses
  └─ TensorFlow.js inference (optional quick checks)
  
FastAPI Server
  ├─ /offer (SDP handshake via aiortc)
  ├─ /ws (binary frames & audio chunks)
  │   ├─ vision.predict_component (PyTorch ViT)
  │   ├─ audio_stt.transcribe_audio (Whisper)
  │   └─ langchain_flow.generate_steps (GPT-4o via LangGraph)
  └─ Returns JSON with overlay instructions

---

## Monitoring & Logging
- **Prometheus:** kubectl port-forward svc/prometheus 9090

- **Grafana:** kubectl port-forward svc/grafana 3001

- **Sentry:** Errors tracked automatically (set SENTRY_DSN secret)

---

## Secrets Management
Vault CSI injects secrets into pods—no hard-coded credentials.

- **Example annotation on Deployment:**
    ```bash
    metadata:
    annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "holoassist-backend"
        vault.hashicorp.com/agent-inject-secret-openai: "secret/data/openai"
    ```

---

## Contributing
1. Fork the repo

2. Create a feature branch (git checkout -b feat/xyz)

3. Commit & push (git push origin feat/xyz)

4. Open a Pull Request—CI will run tests & linting


