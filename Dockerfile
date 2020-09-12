FROM python:3.8-slim

COPY DNSoverTLS DNSoverTLS
RUN useradd server

USER server

EXPOSE 8053/udp
EXPOSE 8853

ENTRYPOINT ["python", "-m", "DNSoverTLS"]
