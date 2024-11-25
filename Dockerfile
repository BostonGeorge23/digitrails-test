FROM apache/airflow:2.10.3-python3.11

USER root

# Install any additional packages you need here
RUN apt-get update && apt-get install -y vim\
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy DAGs, plugins, and other necessary files
COPY dags /opt/airflow/dags