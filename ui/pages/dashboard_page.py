from datetime import date

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QListWidget,
    QListWidgetItem,
    QPushButton
)

from services.database_service import (
    get_available_years,
    get_dashboard_month_stats,
    get_category_expenses_month,
    get_monthly_expenses_year
)

from ui.widgets.monthly_chart import MonthlyChart
from ui.widgets.category_pie_chart import CategoryPieChart


class DashboardPage(QWidget):

    def __init__(self):

        super().__init__()

        main_layout = QVBoxLayout()

        self.hide_internal_transfers = False

        self.transfer_button = QPushButton(
            "Enlever les virements internes"
        )

        self.transfer_button.clicked.connect(
            self.toggle_internal_transfers
        )

        main_layout.insertWidget(
            0,
            self.transfer_button
        )

        # =====================
        # FILTRES
        # =====================

        filters_layout = QHBoxLayout()

        filters_layout.addWidget(
            QLabel("Année")
        )

        self.year_combo = QComboBox()

        filters_layout.addWidget(
            self.year_combo
        )

        filters_layout.addWidget(
            QLabel("Mois")
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

        filters_layout.addWidget(
            self.month_combo
        )

        filters_layout.addStretch()

        main_layout.addLayout(
            filters_layout
        )

        # =====================
        # KPI
        # =====================

        cards_layout = QHBoxLayout()

        self.balance_label = self.create_card()
        self.revenues_label = self.create_card()
        self.expenses_label = self.create_card()

        cards_layout.addWidget(
            self.balance_label
        )

        cards_layout.addWidget(
            self.revenues_label
        )

        cards_layout.addWidget(
            self.expenses_label
        )

        main_layout.addLayout(
            cards_layout
        )

        # =====================
        # CAMEMBERT
        # =====================

        pie_layout = QHBoxLayout()

        self.category_chart = (
            CategoryPieChart()
        )

        self.category_chart.setMinimumHeight(
            450
        )

        pie_layout.addWidget(
            self.category_chart,
            3
        )

        self.other_categories = QListWidget()
        self.other_categories.setMinimumWidth(300)

        pie_layout.addWidget(
            self.other_categories,
            1
        )

        main_layout.addLayout(
            pie_layout
        )

        # =====================
        # GRAPHIQUE
        # =====================

        self.monthly_chart = MonthlyChart()

        self.monthly_chart.setMinimumHeight(
            400
        )

        main_layout.addWidget(
            self.monthly_chart
        )

        self.setLayout(main_layout)

        self.load_years()

        self.year_combo.currentIndexChanged.connect(
            self.refresh
        )

        self.month_combo.currentIndexChanged.connect(
            self.refresh
        )

        today = date.today()

        self.month_combo.setCurrentIndex(
            today.month - 1
        )

        self.refresh()

    def create_card(self):

        label = QLabel()

        label.setStyleSheet("""
        QLabel {
            border: 1px solid #cccccc;
            border-radius: 10px;
            padding: 15px;
            font-size: 18px;
            font-weight: bold;
        }
        """)

        return label

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

        stats = get_dashboard_month_stats(
            year,
            month,
            self.hide_internal_transfers
        )

        self.balance_label.setText(
            f"Solde\n{stats['balance']:.2f} €"
        )

        self.revenues_label.setText(
            f"Revenus\n{stats['revenues']:.2f} €"
        )

        self.expenses_label.setText(
            f"Dépenses\n{stats['expenses']:.2f} €"
        )

        categories = (
            get_category_expenses_month(
                year,
                month,
                self.hide_internal_transfers
            )
        )

        self.category_chart.update_chart(
            categories
        )

        total = sum(
            amount
            for _, amount in categories
        )

        self.other_categories.clear()

        self.other_categories.addItem(
            "=== Catégories affichées ==="
        )

        small_categories = []

        for cat, amount in sorted(
            categories,
            key=lambda x: x[1],
            reverse=True
        ):

            percent = (
                amount / total * 100
            ) if total else 0

            if percent >= 5:

                self.other_categories.addItem(
                    f"{cat} : {amount:.2f} € ({percent:.1f}%)"
                )

            else:

                small_categories.append(
                    (
                        cat,
                        amount,
                        percent
                    )
                )

        if small_categories:

            self.other_categories.addItem("")
            self.other_categories.addItem(
                "=== Regroupées dans 'Autres' ==="
            )

            for cat, amount, percent in small_categories:

                self.other_categories.addItem(
                    f"{cat} : {amount:.2f} € ({percent:.1f}%)"
                )

        self.monthly_chart.update_chart(
            get_monthly_expenses_year(
                year,
                self.hide_internal_transfers
            )
        )

    def toggle_internal_transfers(self):

        self.hide_internal_transfers = (
            not self.hide_internal_transfers
        )

        if self.hide_internal_transfers:

            self.transfer_button.setText(
                "Rajouter les virements internes"
            )

        else:

            self.transfer_button.setText(
                "Enlever les virements internes"
            )

        self.refresh()