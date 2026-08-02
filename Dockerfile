# Sprint 75 task 53 — minimal Dockerfile to run the cloud server elsewhere.
FROM python:3.11-slim

WORKDIR /app
COPY superninja_cloud_command_server.py sn_logging.py sn_nl_translator.py ./
RUN pip install --no-cache-dir requests

EXPOSE 8791
ENV PORT=8791
CMD ["python", "superninja_cloud_command_server.py"]
