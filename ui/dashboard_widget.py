from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout
)


class DashboardWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QGridLayout()

        self.balance_label = QLabel()
        self.transactions_label = QLabel()

        self.revenues_label = QLabel()
        self.expenses_label = QLabel()

        layout.addWidget(
            self.balance_label,
            0,
            0
        )

        layout.addWidget(
            self.transactions_label,
            0,
            1
        )

        layout.addWidget(
            self.revenues_label,
            1,
            0
        )

        layout.addWidget(
            self.expenses_label,
            1,
            1
        )

        self.setLayout(layout)

    def update_stats(self, stats):

        self.balance_label.setText(
            f"Solde : {stats['balance']:.2f} €"
        )

        self.transactions_label.setText(
            f"Transactions : {stats['total_transactions']}"
        )

        self.revenues_label.setText(
            f"Revenus du mois : {stats['monthly_revenues']:.2f} €"
        )

        self.expenses_label.setText(
            f"Dépenses du mois : {stats['monthly_expenses']:.2f} €"
        )