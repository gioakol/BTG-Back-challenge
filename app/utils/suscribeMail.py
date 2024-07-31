from os import getenv
from connection import sns_client
from app.database.clients import getClientById
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError



# Subscribe a client's email to the SNS topic.
#
# Parameters:
# * idClient (str): The unique identifier of the client.
#
# Returns:
# * JSONResponse: Response from SNS subscription request if the email is valid.
#                 Error response with status code 404 if the client or email is not found.
#                 Error response with status code 500 if a ClientError occurs.
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
    

# Validate if a client's email is subscribed to the SNS topic.
#
# Parameters:
# * idClient (str): The unique identifier of the client.
#
# Returns:
# * JSONResponse: List of subscriptions matching the client's email.
#                 Error response with status code 404 if the client or email is not found.
#                 Error response with status code 500 if a ClientError occurs.
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
   