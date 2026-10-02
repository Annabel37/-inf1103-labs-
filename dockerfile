FROM python:3.11-slim

WORKDIR /app

#COPY persistent_auditor.py .
# The program writes inventory.txt into this folder.
# Mount a volume here to keep the file after the container stops.
#ENV DATA_DIR=/app/data
COPY inventory_manager.py .
# New line: put a copy of the current data in the image
COPY inventory.json .

CMD ["python", "inventory_manager.py"]