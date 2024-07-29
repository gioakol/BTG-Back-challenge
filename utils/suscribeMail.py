from os import getenv
from connection import sns_client
from database.clients import getClientById
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError

def subscribeClientMail(idClient: str):
    try:
        client_data = getClientById(idClient)

        email = client_data.get('email', '')

        if email != "":
            response = sns_client.subscribe(
                TopicArn=getenv("AWS_MAIL_TOPIC_ARN"),
                Protocol="email",
                Endpoint=email,
                ReturnSubscriptionArn=True
            )

            return JSONResponse(response, status_code = 200)
        else:
            return JSONResponse(content={"message": "El cliente al que intenta acceder no se encuentra."}, status_code=404)
    except ClientError as ex:
        return JSONResponse(content = ex.response["Error"], status_code = 500)
    

def validateSubscribe(idClient: str):
    try:
        client_data = getClientById(idClient)

        email = client_data.get('email', '')

        if email != "":
            response = sns_client.list_subscriptions_by_topic(
                TopicArn=getenv("AWS_MAIL_TOPIC_ARN")
            )

            EMAIL = email

            SUBSCRIPTIONS = response["Subscriptions"]

            result = list(filter(lambda subs: subs["Endpoint"] == EMAIL, SUBSCRIPTIONS))

            return JSONResponse(result, status_code = 200)
        else:
            return JSONResponse(content={"message": "El cliente al que intenta acceder no se encuentra."}, status_code=404)
    except ClientError as ex:
        return JSONResponse(content = ex.response["Error"], status_code = 500)

    