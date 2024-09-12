# nhl-rivalries

Project documentation here:


##### STEPS

1. Clone repo
```
mkdir nhl-rivalry
cd nhl-rivalry
git clone https://github.com/lksprado/nhl-rivalries.git

```
2. Setting up python version with `pyenv`:
```
pyenv install 3.11.9 &&
pyenv local 3.11.9
```

3. Start Poetry
```
poetry env use 3.11.9 &&
poetry shell
```
4. Install dependancies
```
poetry install
```
5. Execute testing to check if everything is ok
```
poetry run task test
```

5. Execute this to run the code
```
poetry run python main.py
```

6. For the mailing DAG create an account in `mailtrap.io`. Get the credentials in Sending Domains > Integration > SMTP > Python

7. Move `games_of_intest.csv` to `data` folder inside your Airflow enviroment

8. DAG to send game day mail. Beware to insert yuor SMTP credentials bellow.
```
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import pandas as pd
import smtplib
from email.mime.text import MIMEText

# Function to check games and send email
def check_and_send_email():
    # Load the CSV file
    df = pd.read_csv('data/nhl_project/games_of_interest.csv')

    # Parse the 'data' column into datetime
    df['data'] = pd.to_datetime(df['data'])

    # Get today's date (without time)
    today = pd.Timestamp(datetime.now().date())

    # Filter games that match today's date
    games_today = df[df['data'].dt.date == today.date()]

    # If there are games today, send the email
    if not games_today.empty:
        email_body = "Game day\n\n"
        for index, row in games_today.iterrows():
            email_body += f"{row['data']} - {row['game']}\n"
        
        send_email(email_body)

# Function to send email
def send_email(content):
    smtp_server = 'live.smtp.mailtrap.io'
    smtp_port = 'YOUR PORT'
    smtp_username = 'YOUR USER'
    smtp_password = 'YOUR PASSWORD'
    subject = "NHL Game Day Alert"
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = 'mailtrap@demomailtrap.com'
    msg['To'] = 'YOUR EMAIL'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

# Define the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 12),
    'email_on_failure': False,
    'email_on_retry': False
}

with DAG(
    dag_id='game_day_alert',
    default_args=default_args,
    schedule_interval='0 10 * * *',
    catchup=False
) as dag:

    check_for_games = PythonOperator(
        task_id='check_for_games',
        python_callable=check_and_send_email
    )
```