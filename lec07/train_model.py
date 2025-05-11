import pandas as pd
import psycopg2
import psycopg2.extras
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine
import os

def main():
    connection = psycopg2.connect(
        host='postgres',
        user='airflow',
        password='airflow',
        database='airflow'
    )

    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM iris_processed;")
    rows = cursor.fetchall()
    connection.close()

    df = pd.DataFrame(rows, columns=rows[0].keys())

    X = df.drop(columns=['target'])
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    engine = create_engine('postgresql+psycopg2://airflow:airflow@postgres:5432/airflow')
    pd.DataFrame([{'accuracy': accuracy}]).to_sql('iris_model_results', con=engine, if_exists='replace', index=False)

if __name__ == '__main__':
    main()
