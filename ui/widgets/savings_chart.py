from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg
)

from matplotlib.figure import Figure


class SavingsChart(
    FigureCanvasQTAgg
):

    def __init__(self):

        self.figure = Figure(
            figsize=(12, 5)
        )

        super().__init__(
            self.figure
        )

    def update_chart(
        self,
        data
    ):

        self.figure.clear()

        ax = self.figure.add_subplot(
            111
        )

        months = [
            "Jan","Fév","Mar","Avr",
            "Mai","Juin","Juil","Août",
            "Sep","Oct","Nov","Déc"
        ]

        labels = [
            months[m - 1]
            for m, _
            in data
        ]

        values = [
            v
            for _, v
            in data
        ]

        bars = ax.bar(
            labels,
            values
        )

        for bar in bars:

            height = bar.get_height()

            ax.text(
                bar.get_x()
                + bar.get_width()/2,
                height,
                f"{height:.0f}€",
                ha="center"
            )

        ax.set_title(
            "Évolution de l'épargne"
        )

        self.figure.tight_layout()

        self.draw()