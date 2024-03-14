from utility.lambda_invoker import invoke_third_party_url_lambda
from app import get_lambda
from data_store.data_schemas import OrderDataSchemaToSend, TotalDataForTransactionUpdate


# Create order id , update order
class CreateInitialOrderId:
    def __init__(self, order_data: OrderDataSchemaToSend):
        order_data_for_razorpay = order_data.copy(deep=True)
        order_data_for_razorpay.amount = self.convert_to_paise(order_data_for_razorpay.amount)
        self.payload = {
            "action": "CREATE",
            "data": order_data_for_razorpay.dict()
        }

    def convert_to_paise(self, amount):
        return int(amount * 100)

    def convert_to_rupees(self, response):
        response["data"]["amount"] = response["data"]["amount"]/100
        response["data"]["amount_due"] = response["data"]["amount_due"]/100
        return response

    def get_razorpay_order_for_given_amount(self):
        response = invoke_third_party_url_lambda(lambda_client=get_lambda(), function_name="wallet_service", payload=self.payload)
        return self.convert_to_rupees(response)


class ReadUserWalletBalance:
    def __init__(self, user_id):
        self.user_id = user_id
        self.payload = {
            "action": "READ",
            "data": {
                "user_id": self.user_id
            }
        }

    def read_wallet_data_for_given_user(self):
        return invoke_third_party_url_lambda(lambda_client=get_lambda(), function_name="wallet_service",
                                             payload=self.payload)


class AddUserWalletBalance:
    def __init__(self, data_to_add_balance: TotalDataForTransactionUpdate):
        payload_data = data_to_add_balance.dict()
        self.payload = {
            "action": "UPDATE",
            "data": payload_data
        }

    def update_wallet_details_for_user(self):
        return invoke_third_party_url_lambda(lambda_client=get_lambda(), function_name="wallet_service",
                                             payload=self.payload)
