from botocore.exceptions import ClientError
from utility.custom_logger import logger
from fastapi import status, HTTPException


def publish_mobile_sms(sns, current_user, phonenumber, current_otp):
    try:
        response = sns.publish(
            PhoneNumber=phonenumber, Message="{} is the OTP to verify your mobile number for Electrolite. "
                                             "OTPs are SECRET. DO NOT share with anyone".format(current_otp),
            MessageAttributes={
                'AWS.SNS.SMS.SMSType': {
                    'DataType': 'String',
                    'StringValue': 'Transactional'  # or 'Transactional'
                }
            }
        )
        message_id = response['MessageId']
    except ClientError:
        logger.exception(f"error in sending otp to {current_user.phonenumber}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Error in sending OTP")

    else:
        return response
