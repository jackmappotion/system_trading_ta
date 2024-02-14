from .._visualizer import Visualizer


class BollingerBandVisualizer(Visualizer):
    @staticmethod
    def draw_band(fig, signal):
        ax = fig.gca()
        ax.plot(signal.index, signal["ma_price"], color="g", linewidth=5, alpha=0.5)
        ax.fill_between(
            signal.index, signal["ma_price"], signal["upper_band"], color="r", alpha=0.5
        )
        ax.fill_between(
            signal.index, signal["ma_price"], signal["lower_band"], color="b", alpha=0.5
        )
        return fig
