from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from datetime import datetime, timedelta
import pendulum  # For timezone-aware scheduling

LATITUDE = '23.1745'
LONGITUDE = '88.1034'
POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'open_mateo_api'

local_tz = pendulum.timezone("Asia/Kolkata")  # IST timezone

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 6, 11, 9, 30, tzinfo=local_tz),  # Yesterday 9:30 AM IST
}

with DAG(
    dag_id='ETL_Pipeline',
    default_args=default_args,
    schedule='30 9 * * *',  # 9:30 AM IST (since DAG is timezone-aware)
    catchup=False,
    tags=['weather', 'ETL'],
) as dag:

    @task()
    def extract_weather_data():
        http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')
        endpoint = f'/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true'
        response = http_hook.run(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed: {response.status_code}")

    @task()
    def transform_weather_data(weather_data):
        curr_weather = weather_data['current_weather']
        return {
            'latitude': LATITUDE,
            'longitude': LONGITUDE,
            'temperature': curr_weather['temperature'],
            'windspeed': curr_weather['windspeed'],
            'winddirection': curr_weather['winddirection'],
            'weathercode': curr_weather['weathercode']
        }

    @task()
    def load_weather_data(transformed_data):
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                latitude FLOAT,
                longitude FLOAT,
                temperature FLOAT,
                windspeed FLOAT,
                winddirection FLOAT,
                weathercode INT
            )
        """)
        cursor.execute("""
            INSERT INTO weather_data (
                latitude, longitude, temperature,
                windspeed, winddirection, weathercode
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            transformed_data['latitude'],
            transformed_data['longitude'],
            transformed_data['temperature'],
            transformed_data['windspeed'],
            transformed_data['winddirection'],
            transformed_data['weathercode']
        ))
        conn.commit()
        cursor.close()

    weather_data = extract_weather_data()
    transformed = transform_weather_data(weather_data)
    load_weather_data(transformed)
