from .._visualizer import Visualizer


class MovingAverageVisualizer(Visualizer):
    @staticmethod
    def draw_ma(fig, signal):
        ax = fig.gca()
        ax.plot(signal.index, signal["short_ma"], linewidth=5, alpha=0.5)
        ax.plot(signal.index, signal["long_ma"], linewidth=5, alpha=0.5)
        return fig
