FROM apache/airflow:2.6.0-python3.8

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY airflow.cfg /opt/airflow/airflow.cfg
COPY entrypoint.sh /opt/airflow/entrypoint.sh

ENTRYPOINT ["/opt/airflow/entrypoint.sh"]

