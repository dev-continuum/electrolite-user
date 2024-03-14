import json


def invoke_third_party_url_lambda(lambda_client, function_name, payload):
    result = lambda_client.invoke(FunctionName=function_name, Payload=json.dumps(payload))
    result_to_return = json.loads(result["Payload"].read().decode())
    return {"status_code": result_to_return["status_code"],
            "message": result_to_return["message"],
            "data": result_to_return["data"]}


def invoke_caching_service_lambda(lambda_client, function_name, payload):
    result = lambda_client.invoke(FunctionName=function_name, Payload=json.dumps(payload))
    result_to_return = result["Payload"].read().decode()
    return result_to_return
