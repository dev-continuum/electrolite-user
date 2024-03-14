from data_store import data_schemas, crud
from vendor_workflow.common_workflows.change_charger_status_common import mark_status


def get_data_communicator(vendor_id, db, sqs):
    return DataCommunicator(vendor_id, db, sqs)


class DataCommunicator:
    def __init__(self, vendor_id, db, sqs):
        self.vendor_id = vendor_id
        self.db = db
        self.sqs = sqs

    def get_one_station_data_from_agg_table(self, station_id):
        return crud.get_one_station_data_from_agg_table(self.db, station_id, self.vendor_id)

    def get_vendor_details_from_vendor_db(self):
        return crud.get_vendor_from_db(self.db, self.vendor_id)

    def set_vendor_transaction_id_to_vendor_db(self, current_transaction_id):
        return crud.set_vendor_transaction_id_to_db(self.db, self.vendor_id, current_transaction_id)

    def update_charger_status_in_agg_table(self, charging_data: data_schemas.ChargingPointDataForUpdate):
        # get data from the agg table
        return mark_status(charger_data=charging_data, db=self.db, sqs=self.sqs)
    def add_new_entry_in_booking_table(self, parsed_data_to_store_in_db):
        return crud.add_new_entry_in_booking_table(self.db, parsed_data_to_store_in_db)

    def update_booking_table(self, data_to_update):
        return crud.update_booking_table(self.db, data_to_update)

    def get_booking_details(self, booking_id: str):
        return crud.get_booking_details(db=self.db, booking_id=booking_id)
