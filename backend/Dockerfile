FROM nvidia/cuda:11.7.0-cudnn8-runtime-ubuntu20.04

WORKDIR /app
RUN apt-get update && apt-get install -y \
    python3-pip ffmpeg

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app/ ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
