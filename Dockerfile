# Docker Hub, not public.ecr.aws: anonymous ECR pulls from shared GitHub runner IPs hit
# "429 toomanyrequests: Data limit exceeded", and a docker/login-action step in the caller
# can only lift Docker Hub's limit. Callers should log into Docker Hub before using this action.
FROM python:3-slim AS builder
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt --target=/app 
COPY main.py /app
ENV PYTHONPATH /app
CMD ["python3", "/app/main.py"]
