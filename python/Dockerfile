FROM ubuntu:latest
RUN apt-get update -y \
    && apt-get install -y python3
COPY ./src/ /app/
ENTRYPOINT ["python3", "/app/ipc-test.py"]
