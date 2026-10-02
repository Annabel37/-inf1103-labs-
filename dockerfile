FROM python:3.11-slim

WORKDIR /app

#COPY persistent_auditor.py .
# The program writes inventory.txt into this folder.
# Mount a volume here to keep the file after the container stops.
#ENV DATA_DIR=/app/data
COPY inventory_manager.py .

CMD ["python", "inventory_manager.py"]