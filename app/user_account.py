from app import network

EXA = 10**18

class user_account:
    def __init__(self):
        self.address = 0
        self.stakedBALN = 0
        self.iseligible = False
        self.isLP = False
        self.balance = {"available": 0, "staked": 0}
        self.lastBALNdividents = 0
        self.lastBNUSDdividents = 0
        self.lastSICXdividents = 0
        self.totalBALNdividents = 0
        self.totalBNUSDdividents = 0
        self.totalSICXdividents = 0
        self.totalBALNdividents_claimed = 0
        self.totalBNUSDdividents_claimed = 0
        self.totalSICXdividents_claimed = 0
        self.totaldividentsUSD = 0

    def totalDividentsUSD(self, networkInfo):
        totalvalue = (self.totalBALNdividents+self.totalBALNdividents_claimed)*networkInfo["BALN/bnUSD"] \
                     + (self.totalSICXdividents+self.totalSICXdividents_claimed)*networkInfo["sICX/bnUSD"] \
                     + (self.totalBNUSDdividents+self.totalBNUSDdividents_claimed)
        return totalvalue

    def balanceData(self, address):
        balance = {"available": 0, "staked": 0}
        balanceInfo = network.detailsBalanceOf(address)
        balance["available"] = int(balanceInfo["Available balance"], 16) / EXA
        balance["staked"] = int(balanceInfo["Staked balance"], 16) / EXA
        return balance

    def isProvidingLiqBALN(self, address) -> bool:
        isLP = network.isEarningRewards(address, 3) or network.isEarningRewards(address, 4)
        return bool(isLP)

    def updateUser(self, address, day):
        self.address = address
        self.balance = self.balanceData(address)
        self.isLP = self.isProvidingLiqBALN(address)
        self.iseligible = self.isLP or (self.balance["staked"] > 0)

        last_dividents = network.getUserDividends(address, day - 1, day)
        total_dividents = tuple({})
        for x in range(1, day, 50):
            if day < x + 50:
                total_dividents = total_dividents + network.getUserDividends(address, x, day)
            else:
                total_dividents = total_dividents + network.getUserDividends(address, x, x + 49)
        self.lastBALNdividents = int(last_dividents[0][network.BALN_CONTRACT], 16) / EXA
        self.lastBNUSDdividents = int(last_dividents[0][network.BNUSD_CONTRACT], 16) / EXA
        self.lastSICXdividents = int(last_dividents[0][network.SICX_CONTRACT], 16) / EXA
        for x in range(0, len(total_dividents), 2):
            self.totalBALNdividents = self.totalBALNdividents + \
                                      (int(total_dividents[x][network.BALN_CONTRACT], 16)/EXA)
            self.totalBNUSDdividents = self.totalBNUSDdividents + \
                                       (int(total_dividents[x][network.BNUSD_CONTRACT], 16)/EXA)
            self.totalSICXdividents = self.totalSICXdividents + \
                                      (int(total_dividents[x][network.SICX_CONTRACT], 16) /EXA)

        return True

    def updateUserClaim(self, claimData, networkInfo):
        for i in range(len(claimData)-1, -1, -1):
            self.totalBALNdividents_claimed = self.totalBALNdividents_claimed + \
                                              float(claimData[i]["BALN_claimed"])
            self.totalBNUSDdividents_claimed = self.totalBNUSDdividents_claimed + \
                                              float(claimData[i]["bnUSD_claimed"])
            self.totalSICXdividents_claimed = self.totalSICXdividents_claimed + \
                                              float(claimData[i]["sICX_claimed"])

        self.totaldividentsUSD = self.totalDividentsUSD(networkInfo)