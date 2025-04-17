# import boto3
# import io
# import sys
# import base64
# from logging import Logger

# rek_client = boto3.client('rekognition')
# logger = Logger(name='FaceLivenessLambdaFunction')

# class FaceLivenessError(Exception):
#     '''
#     Represents an error due to Face Liveness Issue.
#     '''
#     pass


# def get_session_results(session_id):
#     '''
#     Get Session result.
#     '''
#     try:
#         response = rek_client.get_face_liveness_session_results(SessionId=session_id)
#         imageStream = io.BytesIO(response['ReferenceImage']['Bytes'])
#         referenceImage = base64.b64encode(imageStream.getvalue())
#         response['ReferenceImage']['Bytes'] = referenceImage

#         return response
#     except rek_client.exceptions.AccessDeniedException:
#         logger.error('Access Denied Error')
#         raise FaceLivenessError('AccessDeniedError')
#     except rek_client.exceptions.InternalServerError:
#         logger.error('InternalServerError')
#         raise FaceLivenessError('InternalServerError')
#     except rek_client.exceptions.InvalidParameterException:
#         logger.error('InvalidParameterException')
#         raise FaceLivenessError('InvalidParameterException')
#     except rek_client.exceptions.SessionNotFoundException:
#         logger.error('SessionNotFound')
#         raise FaceLivenessError('SessionNotFound')
#     except rek_client.exceptions.ThrottlingException:
#         logger.error('ThrottlingException')
#         raise FaceLivenessError('ThrottlingException')
#     except rek_client.exceptions.ProvisionedThroughputExceededException:
#         logger.error('ProvisionedThroughputExceededException')
#         raise FaceLivenessError('ProvisionedThroughputExceededException')
   

# def lambda_handler(event, context):
#     output = get_session_results(event['sessionid'])
#     return {
#         'statusCode': 200,
#         'body': (output)
#     }


# if __name__ == "__main__":
#     session_id = sys.argv[1]
#     status = get_session_results(session_id)

import boto3
import io
import base64
from logging import Logger

# Initialize Rekognition client
rek_client = boto3.client('rekognition')
logger = Logger(name='FaceLivenessLambdaFunction')

class FaceLivenessError(Exception):
    '''
    Represents an error due to Face Liveness Issue.
    '''
    pass


def get_session_results(session_id):
    '''
    Get Session result.
    '''
    try:
        # Retrieve the session results from Rekognition
        response = rek_client.get_face_liveness_session_results(SessionId=session_id)

        # ✅ Confidence score threshold check (92.0)
        confidence = response.get("Confidence", 0)
        if confidence < 92.0 or response.get("Status") != "SUCCEEDED":
            logger.error(f"Liveness confidence too low: {confidence} or status not SUCCEEDED.")
            raise FaceLivenessError("Liveness check failed. Confidence too low or session not succeeded.")

        # Convert the ReferenceImage to base64
        imageStream = io.BytesIO(response['ReferenceImage']['Bytes'])
        referenceImage = base64.b64encode(imageStream.getvalue()).decode("utf-8")
        response['ReferenceImage']['Bytes'] = referenceImage

        return response

    except rek_client.exceptions.AccessDeniedException:
        logger.error('Access Denied Error')
        raise FaceLivenessError('AccessDeniedError')
    except rek_client.exceptions.InternalServerError:
        logger.error('InternalServerError')
        raise FaceLivenessError('InternalServerError')
    except rek_client.exceptions.InvalidParameterException:
        logger.error('InvalidParameterException')
        raise FaceLivenessError('InvalidParameterException')
    except rek_client.exceptions.SessionNotFoundException:
        logger.error('SessionNotFound')
        raise FaceLivenessError('SessionNotFound')
    except rek_client.exceptions.ThrottlingException:
        logger.error('ThrottlingException')
        raise FaceLivenessError('ThrottlingException')
    except rek_client.exceptions.ProvisionedThroughputExceededException:
        logger.error('ProvisionedThroughputExceededException')
        raise FaceLivenessError('ProvisionedThroughputExceededException')


def lambda_handler(event, context):
    '''
    Main Lambda function handler.
    '''
    try:
        # Extract the session ID from the event
        session_id = event['sessionid']
        
        # Get the session results using the get_session_results function
        output = get_session_results(session_id)

        # Return the response with the session result
        return {
            'statusCode': 200,
            'body': output
        }

    except FaceLivenessError as e:
        # Catch and log any FaceLivenessError exceptions
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 400,
            'body': str(e)
        }
    except Exception as e:
        # Catch any other unexpected errors
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': "An unexpected error occurred."
        }


if __name__ == "__main__":
    session_id = input("Enter session ID: ")
    try:
        # Test the get_session_results function with the provided session ID
        result = get_session_results(session_id)
        print("Session result:", result)
    except Exception as e:
        print(f"Error: {str(e)}")
