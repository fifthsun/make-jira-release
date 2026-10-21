# Built only by .github/workflows/publish-image.yml and published to GHCR; callers pull that
# image (see action.yml) and never build this file. Docker Hub, not public.ecr.aws: anonymous
# ECR pulls from shared GitHub runner IPs hit "429 toomanyrequests: Data limit exceeded".
FROM python:3-slim AS builder
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt --target=/app 
COPY main.py /app
ENV PYTHONPATH /app
CMD ["python3", "/app/main.py"]
