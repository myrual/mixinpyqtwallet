import requests
import uuid
import base64
import umsgpack
import binascii


def gen_memo_ocean_cancel_order(order_uuid):
    result = {"O":order_uuid}
    return base64.b64encode(umsgpack.packb(result)).decode("utf-8")

def gen_memo_ocean_create_order(asset_id_string, price_string, operation_type, side_operation, order_uuid):
    result = {"S":side_operation, "A":uuid.UUID("{" + asset_id_string + "}").bytes, "P":price_string, "T":operation_type, "O":order_uuid}
    return base64.b64encode(umsgpack.packb(result)).decode("utf-8")

def gen_memo_ocean_bid(asset_id_string, price_string, order_uuid):
    return gen_memo_ocean_create_order(asset_id_string, price_string, "L", "B", order_uuid)
def gen_memo_ocean_ask(asset_id_string, price_string, order_uuid):
    return gen_memo_ocean_create_order(asset_id_string, price_string, "L", "A", order_uuid)


class ocean_order():
    def __init__(self, asset_order):
        self.amount = asset_order.get("amount")
        self.funds  = asset_order.get("funds")
        self.price  = asset_order.get("price")
        self.side   = asset_order.get("side")
class Ocean_pair_price():
    def __init__(self, asset_order_list_result):
        if 'error' in asset_order_list_result:
            return
        asset_order_list = asset_order_list_result.get("data")

        self.market                = asset_order_list.get("market")
        self.event                 = asset_order_list.get("event")
        self.sequence              = asset_order_list.get("sequence")
        self.timestamp             = asset_order_list.get("timestamp")
        self.ask_order_list = []
        self.bid_order_list = []

        data_group = asset_order_list.get("data")
        ask_group_in_data_groups = data_group.get("asks")
        for each in ask_group_in_data_groups:
            self.ask_order_list.append(ocean_order(each))
        bid_group_in_data_groups = data_group.get("bids")
        for each in bid_group_in_data_groups:
            self.bid_order_list.append(ocean_order(each))


def fetchTradePrice(quote_asset_id, target_asset_id):
    url = "https://events.ocean.one/markets/" + target_asset_id + "-" + quote_asset_id+ "/book"
    print(url)
    result_fetchPrice = requests.get(url)
    ocean_response = result_fetchPrice.json()
    this_ocean_pair = Ocean_pair_price(ocean_response)
    return this_ocean_pair
