from src.fee import Fee
from src.order import Order
from src.domains import private_key
from brownie import *


def cow_swap():
    # brownie stuff
    network.connect('mainnet')
    account = accounts.add(private_key=private_key)
    sell_token = "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32"  # LDO
    buy_token = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"  # WETH

    sell_token_contract = Contract.from_explorer(sell_token)
    sell_amount = sell_token_contract.balanceOf(account)

    ## TODO GET QUOTE FOR BUY_AMOUNT
    buy_amount = 1  # 0 seems to cause error, 1 wei is the minimum amount, let's assume there's no shennanigans so it
    # should give us the highest amount anyways

    kind = "sell"

    ## fee calc seems to work right
    fee = Fee(sell_token, buy_token, sell_amount, kind, buy_amount)
    fee_amount = fee.get_fee()

    # sell amount less the fees, which imo are always taken out of the sell amount, never the buy
    order = Order(sell_token, buy_token, sell_amount - fee_amount, buy_amount, fee_amount, kind)

    # no need to put the private key here since it's already in the environment variables (a throwaway wallet one ofc)
    order.sign()

    # should return a hex that corresponds to the order id on cow protocol explorer
    print(order.post_order())


if __name__ == "__main__":
    cow_swap()
