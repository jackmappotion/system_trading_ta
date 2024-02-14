class Visualizer:
    @staticmethod
    def draw_signal(fig, signal):
        ax = fig.gca()
        buy_signals = signal["signal"][0 < signal["signal"]]
        ax.scatter(
            buy_signals.index,
            signal.loc[buy_signals.index, "price"],
            s=buy_signals * 100,
            color="r",
            alpha=abs(buy_signals.values) * 1,
        )

        sell_signals = signal["signal"][signal["signal"] < 0]
        ax.scatter(
            sell_signals.index,
            signal.loc[sell_signals.index, "price"],
            s=abs(sell_signals) * 100,
            color="b",
            alpha=abs(sell_signals.values) * 1,
        )
        return fig

    @staticmethod
    def draw_price(fig, signal):
        ax = fig.gca()
        ax.plot(signal.index, signal["price"], color="k", linewidth=0.5)
        return fig
