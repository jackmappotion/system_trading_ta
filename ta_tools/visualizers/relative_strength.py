import matplotlib.gridspec as gridspec
from .._visualizer import Visualizer


class RelativeStrengthVisualizer:
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
        gs = gridspec.GridSpec(3, 1, figure=fig)
        ax = fig.add_subplot(gs[:2, :])
        ax.plot(signal.index, signal["price"], color="k", linewidth=0.5)
        return fig

    @staticmethod
    def draw_rsi(fig, signal):
        gs = gridspec.GridSpec(3, 1, figure=fig)
        ax_2 = fig.add_subplot(gs[2, :])
        ax_2.plot(signal.index, signal["rsi"], color="purple", label="RSI")
        ax_2.axhline(70, linestyle="--", color="red", label="Overbought")
        ax_2.axhline(30, linestyle="--", color="green", label="Oversold")
        ax_2.set_title("Relative Strength Index (RSI)")
        ax_2.legend()
