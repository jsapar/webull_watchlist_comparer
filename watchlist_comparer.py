from matplotlib.ticker import EngFormatter
import matplotlib.pyplot as plt


class WatchlistComparer:

    wb = None

    def __init__(self, wb):
        self.wb = wb

    # Gets the averages percent gains of the specified watchlsit.
    # Interval - is the length of the time period; d1 = 1 day, m1 = 1 minute
    # Period count - the amount of intervals to be retrieved.
    def get_averaged_watchlist(self, name, interval, period_count):
        # iterate through watchlists
        for watchlist in self.wb.get_watchlists():
            if watchlist['name'] == name:

                # Get a dataframe with the correct dates already in it. Doesn't have to be SPY.
                watchlist_bars = self.wb.get_bars('SPY', interval=interval, count=period_count)
                watchlist_bars = self.__get_percent_change(watchlist_bars)  # clears out all data except dates and close
                for x in range(0, len(watchlist_bars)):
                    watchlist_bars[x] = 0
                ticker_count = 0
                # iterate through each ticker in the watchlist
                for ticker in watchlist['tickerList']:
                    # get bars and convert to percent change bars
                    bars = self.wb.get_bars(stock=ticker['symbol'], interval=interval, count=period_count)
                    if len(bars) - 1 == period_count:
                        bars = self.__get_percent_change(bars)

                        # add percent change to watchlist bars
                        for x in range(0, len(bars)):
                            watchlist_bars[x] += bars[x]
                        ticker_count += 1

                # divide all the values by the amount added
                if ticker_count != 0:
                    for x in range(0, len(watchlist_bars)):
                        watchlist_bars[x] = watchlist_bars[x] / ticker_count
                return watchlist_bars

    # Gets the chart image used for displaying in tkinter.
    def get_tkinter_chart_figure(self, watchlist_name, interval='d1', period_count=30):

        df = self.get_averaged_watchlist(watchlist_name, interval, period_count)

        figure = plt.Figure(figsize=(7, 8), dpi=100)

        # Create axis
        ax = figure.add_subplot()

        # Get SPY percent change bars
        spy = self.wb.get_bars(stock='SPY', interval=interval, count=period_count)
        spy = self.__get_percent_change(spy)

        # Plot SPY and the given watchlist
        df.plot(label=watchlist_name, legend=True, ax=ax)
        spy.plot(label='SPY', legend=True,  ax=ax)

        # Set axis properties
        ax.set_title('Watchlist: ' + watchlist_name + ' vs SPY')
        ax.set_ylabel('Average percent change')
        ax.yaxis.set_major_formatter(EngFormatter(unit='%'))
        ax.set_xlabel('Time interval')

        return figure

    def __get_percent_change(self, bars):
        close = bars['close']
        base_price = close[0]
        for x in range(0, len(close)):
            percent_change = (close[x] - base_price) / base_price * 100
            close[x] = percent_change
        return close

    def get_watchlists(self):
        names = []
        for watchlist in self.wb.get_watchlists():
            if watchlist['name'] != 'My Positions' and watchlist['name'] != 'All Stocks':
                names.append(watchlist['name'])
        return names
