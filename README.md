# Digitrails

This project is designed to process and analyze geographical and meteorological data using Apache Airflow, Pandas, and other Python libraries.

## Implementation

1. **Extract**: Data is extracted from various sources such as CSV and JSONL files. This is done using Airflow tasks that read the data into Pandas DataFrames.
2. **Transform**: The extracted data is cleaned and transformed. This includes handling missing values, converting data types, and normalizing data. Pandas is used extensively in this step.
3. **Load**: The transformed data is loaded into a PostgreSQL database. SQLAlchemy is used to handle the database interactions and ensure data integrity.
4. **Scheduling**: Airflow schedules the tasks to run at specified intervals, if needed.

### Key Components

- **Apache Airflow**: Used for orchestrating the data processing tasks.
- **Pandas**: Used for data manipulation and analysis.
- **SQLAlchemy**: Used for data injection as ORM.
- **Docker**: Used for containerizing the application.
- **PostgreSQL**: Used as the database for storing the processed data.

## Setting Up the Environment

### Prerequisites

- **Docker**: Ensure Docker is installed on your system. You can download it from [Docker's official website](https://www.docker.com/products/docker-desktop).
- **Docker Compose**: Ensure Docker Compose is installed. It usually comes with Docker Desktop, but you can also install it separately if needed.
- **Git**: Ensure Git is installed to clone the repository. You can download it from [Git's official website](https://git-scm.com/downloads).
- **Python 3.11**: Ensure Python 3.11 is installed on your system. You can download it from [Python's official website](https://www.python.org/downloads/).

### Steps

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. **Build the Docker image**:
    ```sh
    docker build -t digitrails .
    ```

3. **Start the Docker containers**:
    ```sh
    docker-compose up -d
    ```

4. **Access the Airflow web interface**:
   Open your browser and go to `http://localhost:8080`. Use the default credentials to log in.

## Running the Environment

1. **Trigger the DAG**:
    - Go to the Airflow web interface.
    - Enable and trigger the DAG you want to run.

2. **Monitor the tasks**:
    - Use the Airflow web interface to monitor the progress and logs of the tasks.

## Example Queries

Here are some example SQL queries to get hourly meteorological data per region or province:

### Query 1: Get Weekly Meteo Data Per Region
```sql
SELECT
   r.region_name,
   DATE_TRUNC('week', hd.time) AS week,
   AVG(hd.temperature) AS avg_temperature,
   AVG(hd."precipIntensity") AS avg_precipitation
FROM
   meteo_data m
      JOIN
   city c ON m.city_id = c.id
      JOIN
   region r ON c.region_id = r.id
      JOIN 
   hourly_data hd on hd.meteo_data_id = m.id
GROUP BY
   r.region_name,
   DATE_TRUNC('week',hd.time)
ORDER BY
   r.region_name,
   week;
```

### Query 2: Get Monthly Meteo Data Per Province
```sql
SELECT
   p.province_name,
   DATE_TRUNC('month', hd.time) AS month,
   AVG(hd.temperature) AS avg_temperature,
   AVG(hd."precipIntensity") AS avg_precipitation
FROM
   meteo_data m
      JOIN
   city c ON m.city_id = c.id
      JOIN
   province p ON c.province_id = p.id
      JOIN
   hourly_data hd on hd.meteo_data_id = m.id
GROUP BY
   p.province_name,
   DATE_TRUNC('month',hd.time)
ORDER BY
   p.province_name,
   month;
```
