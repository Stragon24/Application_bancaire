from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg
)

from matplotlib.figure import Figure


class MonthlyChart(
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

        month_names = [
            "Jan",
            "Fév",
            "Mar",
            "Avr",
            "Mai",
            "Juin",
            "Juil",
            "Août",
            "Sep",
            "Oct",
            "Nov",
            "Déc"
        ]

        labels = [
            month_names[m - 1]
            for m, _ in data
        ]

        values = [
            amount
            for _, amount in data
        ]

        bars = ax.bar(
            labels,
            values
        )

        for bar in bars:

            height = bar.get_height()

            ax.text(
                bar.get_x()
                + bar.get_width() / 2,
                height,
                f"{height:.0f} €",
                ha="center",
                va="bottom"
            )

        ax.set_title(
            "Dépenses mensuelles"
        )

        ax.set_ylabel(
            "Montant (€)"
        )

        ax.margins(
            y=0.15
        )

        self.figure.tight_layout()

        self.draw()