import plots
import securitySearch
import suggestions
import br_api_tests
import marketSearch
import dialogflow
from initPortfolio import Portfolio

p1 = Portfolio({"ABM": 200, "TSLA": 400, "KO": 76, "GE": 58, "GM": 79,
                "AAPL": 200, "NCR" : 350, "NOK": 21, "QSR" : 240, "T" : 58,
                "TAK" : 79, "SPY": 721, "DIA": 270, "FNCL": 32, "F":90,
                "MMM" : 78, "HON" : 92, "UPS": 68, "UHS": 78, "V": 200, "BLL": 53,
                "KI": 520, "M": 63, "TAP": 46, "MNST": 79, "NOV": 10})
print(p1.plots.tablePortfolio())
p1.plots.assetTypes()
p1.plots.assetTypes()
p1.plots.industries()
p1.plots.sectors()
p1.plots.levels()
print(p1.plots.portfolioSpecificData("TSLA"))

p1.securitySearch.drawTickerPlots("AAPL")
p1.securitySearch.drawSectorPlots("Information Technology")



