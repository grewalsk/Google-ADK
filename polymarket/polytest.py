from py_clob_client.clob_types import TradeParams

resp = client.get_trades(
    TradeParams(
        maker_address=client.get_address(),
        market="0xbd31dc8a20211944f6b70f31557f1001557b59905b7738480ca09bd4532f84af",
    ),
)
print(resp)
print("Done!")