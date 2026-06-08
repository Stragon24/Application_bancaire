from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from services.database_service import (
    get_transactions_by_period,
    get_available_years
)


class TransactionsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        filter_layout = QHBoxLayout()

        filter_layout.addWidget(
            QLabel("Année :")
        )

        self.year_combo = QComboBox()

        filter_layout.addWidget(
            self.year_combo
        )

        filter_layout.addWidget(
            QLabel("Mois :")
        )

        self.month_combo = QComboBox()

        self.month_combo.addItems([
            "Janvier",
            "Février",
            "Mars",
            "Avril",
            "Mai",
            "Juin",
            "Juillet",
            "Août",
            "Septembre",
            "Octobre",
            "Novembre",
            "Décembre"
        ])

        filter_layout.addWidget(
            self.month_combo
        )

        filter_layout.addStretch()

        layout.addLayout(
            filter_layout
        )

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "Date",
            "Libellé",
            "Catégorie",
            "Compte",
            "Montant"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(
            self.table
        )

        self.setLayout(layout)

        self.load_years()

        self.year_combo.currentIndexChanged.connect(
            self.refresh
        )

        self.month_combo.currentIndexChanged.connect(
            self.refresh
        )

        self.refresh()

    def load_years(self):

        years = get_available_years()

        self.year_combo.clear()

        for year in years:
            self.year_combo.addItem(
                str(year)
            )

    def refresh(self):

        if self.year_combo.count() == 0:
            return

        year = int(
            self.year_combo.currentText()
        )

        month = (
            self.month_combo.currentIndex()
            + 1
        )

        transactions = (
            get_transactions_by_period(
                year,
                month
            )
        )

        self.table.setRowCount(
            len(transactions)
        )

        for row, t in enumerate(transactions):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(t.date)
                )
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    t.label
                )
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    t.category
                )
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    t.account_label
                )
            )

            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    f"{t.amount:.2f}"
                )
            )