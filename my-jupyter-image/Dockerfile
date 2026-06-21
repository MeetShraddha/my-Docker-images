# Start from a base image that already has Python installed
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /home/jovyan/work

# Copy a requirements file into the container
COPY requirements.txt .

# Install Jupyter and any libraries you listed
RUN pip install --no-cache-dir -r requirements.txt

# Tell Docker this container listens on port 8888
EXPOSE 8888

# The command that runs when the container starts
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]