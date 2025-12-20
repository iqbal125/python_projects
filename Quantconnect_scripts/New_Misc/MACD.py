from AlgorithmImports import *

class MACDAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2020, 1, 1)  # Set Start Date
        self.SetEndDate(2020, 12, 31)  # Set End Date
        self.SetCash(100000)  # Set Strategy Cash
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        # Create MACD indicator
        # MACD(fast period, slow period, signal period, type of moving average)
        self.macd = self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Exponential, Resolution.Daily, Field.Close)
        
        # Create a chart with two series: MACD line and MACD signal line
        macdPlot = Chart('MACD Plot')
        macdPlot.AddSeries(Series('MACD', SeriesType.Line, '$', Color.Blue))
        macdPlot.AddSeries(Series('Signal', SeriesType.Line, '$', Color.Orange))
        self.AddChart(macdPlot)

    def OnData(self, data):
        if not self.macd.IsReady:
            return
        
        # Plot MACD and Signal Line
        self.Plot('MACD Plot', 'MACD', self.macd.Current.Value)
        self.Plot('MACD Plot', 'Signal', self.macd.Signal.Current.Value)
        
        # Trading logic
        if not self.Portfolio.Invested:
            if self.macd.Current.Value > self.macd.Signal.Current.Value:
                self.SetHoldings(self.symbol, 1)  # Buy full position
        elif self.macd.Current.Value < self.macd.Signal.Current.Value:
            self.Liquidate(self.symbol)  # Sell all holdings
