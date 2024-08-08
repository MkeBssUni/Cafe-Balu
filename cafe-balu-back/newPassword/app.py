import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, __):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "PATCH, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token"
    }
    client = boto3.client('cognito-idp', region_name='us-east-2')
    user_pool_id = "us-east-2_Yxnt4eRMp"
    client_id = "5ffukkqllrcqtlffpbq1pjuuqc"
    try:
        body_parameters = json.loads(event["body"])
        username = body_parameters.get('username')
        current_password = body_parameters.get('current_password')
        new_password = body_parameters.get('new_password')

        # Autentica al usuario con la contraseña actual
        response = client.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow='ADMIN_USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': current_password
            }
        )

        # Verifica si se requiere un desafío para una nueva contraseña
        if 'ChallengeName' in response and response['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
            client.respond_to_auth_challenge(
                ClientId=client_id,
                ChallengeName='NEW_PASSWORD_REQUIRED',
                Session=response['Session'],
                ChallengeResponses={
                    'USERNAME': username,
                    'NEW_PASSWORD': new_password,
                    'email_verified': 'true'
                }
            )
            return {
                'statusCode': 200,
                "headers": headers,
                'body': json.dumps({"message": "Password changed successfully."})
            }
        elif 'AuthenticationResult' in response:
            # El usuario se autentica correctamente, ahora cambiamos la contraseña
            access_token = response['AuthenticationResult']['AccessToken']
            client.change_password(
                AccessToken=access_token,
                PreviousPassword=current_password,
                ProposedPassword=new_password
            )
            return {
                'statusCode': 200,
                "headers": headers,
                'body': json.dumps({"message": "Password updated successfully."})
            }
        else:
            return {
                'statusCode': 400,
                "headers": headers,
                'body': json.dumps({"error_message": "Unexpected response during authentication."})
            }

    except ClientError as e:
        return {
            'statusCode': 400,
            "headers": headers,
            'body': json.dumps({"error_message": e.response['Error']['Message']})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            "headers": headers,
            'body': json.dumps({"error_message": str(e)})
        }
