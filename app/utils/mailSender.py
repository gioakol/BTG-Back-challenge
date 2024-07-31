from connection import sns_client
from os import getenv
from botocore.exceptions import ClientError



# Send notification email and SMS for subscription or unsubscription.
#
# Parameters:
# * fullName (str): Full name of the client.
# * email (str): Email address of the client.
# * phone (str): Phone number of the client.
# * category (str): Category of the fund (e.g., "FPV" for Voluntary Pension Fund or other categories for Collective Investment Fund).
# * fundName (str): Name of the fund.
# * tipoNotificacion (str): Type of notification, either "subscribed" or "unsubscribed".
#
# Returns:
# * bool: True if both email and SMS notifications were sent successfully, False otherwise.
def sendMailNotificationSubscribe(fullName: str, email: str, phone: str, category: str, fundName: str, tipoNotificacion: str):
    try:
        message = f"Hola {fullName}, gracias por confiar en nosotros, por ello, queremos confirmarte la {"suscripción" if tipoNotificacion == "subscribed" else "baja" } al servicio de {"Fondo voluntario de pensión" if category == "FPV" else "Fondo de inversión colectiva"} '{fundName}' para más información ingresa a nuestro sitio web para más información."
        subject = f"{"Suscripción" if tipoNotificacion == "subscribed" else "Baja" } {"Fondo voluntario de pensión" if category == "FPV" else "Fondo de inversión colectiva"} '{fundName}'"

        responseMail = sns_client.publish(
            TopicArn=getenv("AWS_MAIL_TOPIC_ARN"),
            Message=message,
            Subject=subject
        )

        responsePhone = sns_client.publish(
            PhoneNumber=phone,
            Message=message,
        )
        
        mail_message_id = responseMail.get("MessageId")
        phone_message_id = responsePhone.get("MessageId")

        if not mail_message_id or not phone_message_id:
            return False
        else:
            return True
    except ClientError as ex:
        return False
