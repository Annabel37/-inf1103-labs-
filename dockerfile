FROM python:3.11-slim

WORKDIR /app

#COPY persistent_auditor.py .
# The program writes inventory.txt into this folder.
# Mount a volume here to keep the file after the container stops.
#ENV DATA_DIR=/app/data
COPY persistent_auditor.py .

CMD ["python", "persistent_auditor.py"]