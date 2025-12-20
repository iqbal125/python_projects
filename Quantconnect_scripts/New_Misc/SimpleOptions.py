from AlgorithmImports import *

class SimpleOptionsAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)  # Set Start Date
        self.SetEndDate(2024, 1, 1)    # Set End Date
        self.SetCash(100000)           # Set Strategy Cash
        
        equity = self.AddEquity("SPY", Resolution.Minute)
        option = self.AddOption("SPY", Resolution.Minute)
        self.symbol = option.Symbol
        
        # set our strike/expiry filter for this option chain
        option.SetFilter(-2, 2, timedelta(30), timedelta(60))
        
        # indicators
        self.fast = self.SMA(equity.Symbol, 50, Resolution.Daily)
        self.slow = self.SMA(equity.Symbol, 200, Resolution.Daily)

    def OnData(self, slice):
        if slice.OptionChains:
            chains = slice.OptionChains.Values
            for chain in chains:
                # find the call option contract with the furthest expiration
                contract = sorted(chain, key=lambda x: x.Expiry, reverse=True)[0]
                
                if not self.Portfolio.Invested:
                    if self.fast > self.slow:
                        self.Buy(contract.Symbol, 1)  # buy 1 contract of the call option
                
                if self.fast < self.slow:
                    self.Liquidate()  # liquidate if fast SMA crosses below slow SMA
