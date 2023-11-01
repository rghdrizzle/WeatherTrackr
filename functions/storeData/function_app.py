import azure.functions as func
import logging
import azure.cosmos.exceptions as exceptions
from azure.cosmos import CosmosClient, PartitionKey

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    city = req.params.get('data')
    ENDPOINT = ""
    KEY=""
    DATABASE_NAME="Cities"
    key_path = PartitionKey(path="/partitionkey")
    client = CosmosClient(url=ENDPOINT, credential=KEY)
    database = client.create_database_if_not_exists(id=DATABASE_NAME)
    print("Database\t", database.id)
    container = database.create_container_if_not_exists(
        id="city", partition_key=key_path, offer_throughput=400
    )
    print("Container\t", container.id)
    doc_id ="usercity"
    partition_key="11111"
    try:
        read_item = container.read_item(item=doc_id, partition_key=partition_key)
        read_item['city'] = city
        response = container.replace_item(item=read_item, body=read_item)
        logging.info('Replaced Item\'s Id is {0}, new city={1}'.format(response['id'], response['city']))
        return func.HttpResponse(f"City '{city}' updated in the database.", status_code=200)
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        return func.HttpResponse(f"An error occurred: {e}", status_code=500)

    







