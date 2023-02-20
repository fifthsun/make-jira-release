FROM public.ecr.aws/docker/library/python:3-slim AS builder
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt --target=/app 
COPY main.py /app
ENV PYTHONPATH /app
CMD ["python3", "/app/main.py"]
