from iconsdk.builder.call_builder import CallBuilder
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider


REWARDS_CONTRACT = "cx10d59e8103ab44635190bd4139dbfd682fa2d07e"
BALN_CONTRACT = "cxf61cd5a45dc9f91c15aa65831a30a90d59a09619"
BNUSD_CONTRACT = "cx88fd7df7ddff82f7cc735c871dc519838cb235bb"
SICX_CONTRACT = "cx2609b924e33ef00b648a409245c7ea394c467824"
DEX_CONTRACT = "cxa0af3165c08318e988cb30993b3048335b94af6c"
DIVIDENTS_CONTRACT = "cx203d9cd2a669be67177e997b8948ce2c35caffae"

SICXICX_POOL_ID = 1
EXA = 10**18
APY = 10**16

icon_service = IconService(HTTPProvider("https://ctz.solidwallet.io", 3))


def isEarningRewards(account, id) -> int:
    call = CallBuilder().from_("hx0000000000000000000000000000000000000001")\
                        .to(DEX_CONTRACT)\
                        .method("isEarningRewards")\
                        .params({"_address": account, "_id": id})\
                        .build()
    return int(icon_service.call(call),0)


def getUserDividends(account, start, end) -> tuple:
    call = CallBuilder().from_("hx0000000000000000000000000000000000000001") \
        .to(DIVIDENTS_CONTRACT) \
        .method("getUserDividends") \
        .params({"_account": account, "_start": start, "_end": end}) \
        .build()
    result = icon_service.call(call)
    if result == {}:
        return {"cx0000000000000000000000000000000000000000": "0x0",
                "cxf61cd5a45dc9f91c15aa65831a30a90d59a09619": "0x0",
                "cx88fd7df7ddff82f7cc735c871dc519838cb235bb": "0x0",
                "cx2609b924e33ef00b648a409245c7ea394c467824": "0x0"}, 0
    else:
        return result, 0


def getDay() -> int:
    call = CallBuilder().from_("hx0000000000000000000000000000000000000001")\
                        .to(DIVIDENTS_CONTRACT)\
                        .method("getDay")\
                        .params({})\
                        .build()
    return int(icon_service.call(call), 0)


def getFees() -> dict:
    call = CallBuilder().from_("hx0000000000000000000000000000000000000001")\
                        .to(DIVIDENTS_CONTRACT)\
                        .method("getBalances")\
                        .params({})\
                        .build()
    return icon_service.call(call)


def getPriceByName(name) -> int:
    call = CallBuilder().from_("hx0000000000000000000000000000000000000001")\
                        .to(DEX_CONTRACT)\
                        .method("getPriceByName")\
                        .params({"_name": name})\
                        .build()
    return int(icon_service.call(call), 0)


def detailsBalanceOf(account) -> dict:
    call = CallBuilder().from_("hx0000000000000000000000000000000000000001")\
                        .to(BALN_CONTRACT)\
                        .method("detailsBalanceOf")\
                        .params({"_owner": account})\
                        .build()
    return icon_service.call(call)


def totalStakedBalance() -> int:
    call = CallBuilder().from_("hx0000000000000000000000000000000000000001")\
                        .to(BALN_CONTRACT)\
                        .method("totalStakedBalance")\
                        .params({})\
                        .build()
    return int(icon_service.call(call), 0)


def totalSupply() -> int:
    call = CallBuilder().from_("hx0000000000000000000000000000000000000001")\
                        .to(BALN_CONTRACT)\
                        .method("totalSupply")\
                        .params({})\
                        .build()
    return int(icon_service.call(call), 0)


def priceData() -> dict:
    priceInfo = {"sICX/bnUSD": 0, "BALN/bnUSD": 0}
    sICX_bnUSD = getPriceByName("sICX/bnUSD")
    BALN_bnUSD = getPriceByName("BALN/bnUSD")
    priceInfo["sICX/bnUSD"] = sICX_bnUSD/EXA
    priceInfo["BALN/bnUSD"] = BALN_bnUSD/EXA
    return priceInfo


def feeData() -> dict:
    feeInfo = {"sICX": 0, "BALN": 0, "bnUSD": 0}
    fee_dict = getFees()
    feeInfo["sICX"] = int(fee_dict["sICX"], 16) / EXA
    feeInfo["BALN"] = int(fee_dict["BALN"], 16) / EXA
    feeInfo["bnUSD"] = int(fee_dict["bnUSD"], 16) / EXA
    return feeInfo


def tokenData(BALNprice) -> dict:
    tokenInfo = {"staked": 0, "supply": 0, "marketcap": 0}
    tokenInfo["staked"] = totalStakedBalance() / EXA
    tokenInfo["supply"] = totalSupply() / EXA
    tokenInfo["marketcap"] = tokenInfo["supply"]*BALNprice
    return tokenInfo


def networkData() -> tuple:
    priceInfo = priceData()
    feeInfo = feeData()
    tokenInfo = tokenData(priceInfo["BALN/bnUSD"])
    networkInfo = (priceInfo, feeInfo, tokenInfo)
    return networkInfo
