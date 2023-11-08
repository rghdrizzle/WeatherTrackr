import logging
import azure.functions as func
import os
from azure.communication.email import EmailClient
import azure.cosmos.exceptions as exceptions
from azure.cosmos import CosmosClient, PartitionKey
import requests

app = func.FunctionApp()

@app.schedule(schedule="*/15 * * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def SendAlert(myTimer: func.TimerRequest) -> None:
    Endpoint = os.getenv("ENDPOINT")
    key=os.getenv("KEY")
    DATABASE_NAME="Cities"
    key_path = PartitionKey(path="/partitionkey")
    client = CosmosClient(url=Endpoint, credential=key)
    database = client.create_database_if_not_exists(id=DATABASE_NAME)
    print("Database\t", database.id)
    container = database.create_container_if_not_exists(
        id="city", partition_key=key_path, offer_throughput=400
    )
    print("Container\t", container.id)
    doc_id ="usercity"
    partition_key="11111"
    response = container.read_item(item=doc_id, partition_key=partition_key)
    print('Item read by Id {0}'.format(doc_id))
    print('city: {0}'.format(response.get('city')))


    city = response.get('city')
    response=requests.get("localhost:8080/weather/"+city)
    weather = response.text['weather'][0]['main']
    
    if myTimer.past_due:
        logging.info('The timer is past due!')
   
    if weather == "Rain":
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


    