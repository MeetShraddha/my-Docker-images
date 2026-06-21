# Start from a base image that already has Python installed
FROM python:3.11-slim

WORKDIR /home/jovyan/work

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Jupyter Lab port
EXPOSE 8888
# LangGraph CLI dev server port
EXPOSE 2024

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
