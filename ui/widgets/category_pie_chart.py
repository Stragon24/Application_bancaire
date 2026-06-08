from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg
)

from matplotlib.figure import Figure


class CategoryPieChart(
    FigureCanvasQTAgg
):

    def __init__(self):

        self.figure = Figure(
            figsize=(8, 5)
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

        total = sum(
            amount
            for _, amount in data
        )

        labels = []
        values = []

        other_total = 0

        for category, amount in data:

            percent = (
                amount / total * 100
            ) if total else 0

            if percent < 5:

                other_total += amount

            else:

                labels.append(
                    category
                )

                values.append(
                    amount
                )

        if other_total > 0:

            labels.append(
                "Autres"
            )

            values.append(
                other_total
            )

        ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title(
            "Répartition des dépenses"
        )

        self.figure.tight_layout()

        self.draw()