FROM ubuntu:latest
RUN apt-get update && apt-get -y install gcc libc-dev
COPY ./src/ /work/ipc
WORKDIR /work/ipc
RUN gcc -o ipc ipc.c -lrt
ENTRYPOINT ["./ipc"]
