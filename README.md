# WeatherTrackr
A weather tracker website to track weeathers of you and also allows alerts you whenever a certain weather threshold is met using serverless function

## Architecture
<img src="https://github.com/rghdrizzle/WeatherTrackr/blob/main/arch.png">

## Tools used
- Azure Function
- Azure Communication Service (Email)
- Azure CosmosDB
- Python and Golang for backend
- HTML and js for frontend
- Azure Web Apps
- Azure Container Apps and Registry
- Azure Container Instance

## The Idea
The idea is about creating a weather alert system so that I can get notified when it is gonna rain in the city I registered the notification system for. I made the alerting system personalised to only send it to me so technically this isnt a service where every one can use it for getting notified to their own email. The whole process should be automated and I should work with azure services. The whole idea of this project is to work with azure services more than actually building the product.

## Frontend
The frontend was done using the obvious classic trio , Html , css and Javascript. The js function calls to the backend of the application whenever the user enters a city and takes that data returned by the backend and display it to the user. I then created a Dockerfile to build and run the frontend using nginx. Then I deployed the frontend to Azure Web Apps. The web apps builds the image from the repositry where the image resides in and runs it in a virtual machine which can be accessable from the internet (I enabled ingress for webapps ). I created a page where the user can regisiter the city's name so that he gets notified if its going to rain or not in that city to his email. <br>
This is how the frontend looks after deployment:
<img src="https://github.com/rghdrizzle/WeatherTrackr/blob/main/Screenshot%20(201).png">

## Backend
The backend consists of a weather fetcher , alert system and a function to store the city name to the database. The function which fetches the weather for a particulat city is implemeneted using Golang. It is then deployed to Azure containers after building the docker image for the application. I deployed it to Azure container Instance as a dev/testing enviornment and Container Apps as the production environment. The web app fetches the weather data from the application in the backend. Next the function for storing the city's name. This function gets the value of the string entered by the user and then stores that string to Cosmos DB by using the Azure sdk. Next is the main part of this whole project , the alert system. I used Azure functions to respond to Time triggers (every 24 hrs at 8:00 am). The function fetches the city name from the Cosmos Db and then calls the backend application running in Azure container apps to get the weather data and if the it is raining it will send a message to my email. For the email communication I used Azure Communication service. So basiscally everytime it rains this function will send me an email using the communication service from Azure and tada I get notified. All the required images are stored in Azure container registry.

## Outputs
### Backend running in production:
<img src="https://github.com/rghdrizzle/WeatherTrackr/blob/main/Screenshot%20(198).png">

### Backend running in dev/test environment 
<img src="https://github.com/rghdrizzle/WeatherTrackr/blob/main/Screenshot%20(194).png">

#### Frontend ( displaying weather for requested city )
<img src="https://github.com/rghdrizzle/WeatherTrackr/blob/main/Screenshot%20(202).png">

### Subsribing a city for weather alert
<img src="https://github.com/rghdrizzle/WeatherTrackr/blob/main/Screenshot%20(203).png">

### Email(alert) sent once its raining in the city (registered city)
<img src="https://github.com/rghdrizzle/WeatherTrackr/blob/main/Screenshot%20(195).png">

### Images of the services deployed in Azure
<img src="https://github.com/rghdrizzle/WeatherTrackr/blob/main/Screenshot%20(196).png">
<img src="https://github.com/rghdrizzle/WeatherTrackr/blob/main/Screenshot%20(197).png">
<img src="https://github.com/rghdrizzle/WeatherTrackr/blob/main/Screenshot%20(199).png">
<img src="https://github.com/rghdrizzle/WeatherTrackr/blob/main/Screenshot%20(204).png">
<img src="https://github.com/rghdrizzle/WeatherTrackr/blob/main/Screenshot%20(205).png">
<img src="https://github.com/rghdrizzle/WeatherTrackr/blob/main/Screenshot%20(206).png>


## Thank you for reading


### Links used when Faced a problem or simply to refer the documents:
- CORs error : https://www.stackhawk.com/blog/golang-cors-guide-what-it-is-and-how-to-enable-it/ https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors
- Azure SDK python: https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cosmos/azure-cosmos/samples/document_management.py#L86-L93
  https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/quickstart-python?tabs=azure-portal%2Cconnection-string%2Cwindows%2Csign-in-azure-cli%2Csync
  https://stackoverflow.com/questions/69373097/confusing-partitioning-key-of-cosmosdb
- To recieve data from js: https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=asgi%2Capplication-level&pivots=python-mode-decorators
- To fix ECONNREFUSED error: https://stackoverflow.com/questions/71532944/unable-to-debug-python-azure-function-in-vs-code-ide-getting-connect-econnrefus
- To fix an error with time_trigger function: https://learn.microsoft.com/en-us/answers/questions/698846/listener-for-azure-function-was-unable-to-start-er
- Python http request module : https://pypi.org/project/requests/
- Azure time trigger cheat sheet: https://arminreiter.com/2017/02/azure-functions-time-trigger-cron-cheat-sheet/
