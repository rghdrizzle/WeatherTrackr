import logging
import azure.functions as func
import os
from azure.communication.email import EmailClient
import requests

app = func.FunctionApp()

@app.schedule(schedule="*/15 * * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def SendAlert(myTimer: func.TimerRequest) -> None:
    city = "gaza"
    response=requests.get("localhost:8080/weather/"+city)
    response.text['weather'][0]['main']
    
    if myTimer.past_due:
        logging.info('The timer is past due!')
    name = "Drizzle"

    try:
        connection_string = os.getenv("CONNECTION_STRING")
        client = EmailClient.from_connection_string(connection_string)

        message = {
            "senderAddress": "DoNotReply@ee3c4743-1f91-4f98-b00c-01877bcc7c18.azurecomm.net",
            "recipients":  {
                "to": [{"address": "rockgameplayhakeem@gmail.com" }],
            },
            "content": {
                "subject": "Test Email",
                "plainText": "hello "+name,
            }
        }

        poller = client.begin_send(message)
        result = poller.result()

    except Exception as ex:
        print(ex)