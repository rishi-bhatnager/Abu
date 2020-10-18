# import plots
# import securitySearch
# import suggestions
# import br_api_tests
# import marketSearch
# import dialogflow
from initPortfolio import Portfolio

class DemoPortfolio:

    @staticmethod
    def getP1():
        p1 = Portfolio(holdings={"ABM": 200, "TSLA": 400, "KO": 76, "GE": 58, "GM": 79,
                    "AAPL": 200, "NCR" : 350, "NOK": 21, "QSR" : 240, "T" : 58,
                    "TAK" : 79, "SPY": 721, "DIA": 270, "FNCL": 32, "F":90,
                    "MMM" : 78, "HON" : 92, "UPS": 68, "UHS": 78, "V": 200, "BLL": 53,
                    "KI": 520, "M": 63, "TAP": 46, "MNST": 79, "NOV": 10})


    @staticmethod
    def getRandomHolding():
        import random
        return random.choice(list(getP1().holdings.keys()))


if __name__ == '__main__':
    DemoPortfolio.getP1()
    DemoPortfolio.getRandomHolding()
    # print(plots.tablePortfolio())
    # plots.assetTypes()
    # plots.assetTypes()
    # plots.industries()
    # plots.sectors()
    # plots.levels()
    # print(plots.portfolioSpecificData("TSLA"))

    # securitySearch.drawTickerPlots("AAPL")
    # securitySearch.drawSectorPlots("Information Technology")
