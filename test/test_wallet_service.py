from unittest import TestCase
from wallet_service.wallet_service import ReadUserWalletBalance, CreateInitialOrderId, AddUserWalletBalance
from data_store.data_schemas import TotalDataForTransactionUpdate, OrderDataSchemaToSend

# TODO: Tests are not working due to circular import error


class TestReadUserWallet(TestCase):
    def setUp(self) -> None:
        self.user_id = 9810936621

    def test_call_positive_read_wallet_service(self):
        read_wallet_data = ReadUserWalletBalance(self.user_id)
        print(read_wallet_data.read_wallet_data_for_given_user())


class TestCreateRazorPayOrderId(TestCase):
    def setUp(self) -> None:
        self.user_id = 9810936621
        self.order_data = OrderDataSchemaToSend.parse_obj({"user_id": self.user_id,
                                                           "amount": 100})

    def test_create_new_order_id_positive(self):
        create_order = CreateInitialOrderId(self.order_data)
        result = create_order.get_razorpay_order_for_given_amount()
        print(result)
