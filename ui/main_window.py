from PySide6.QtGui import QAction

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QStackedWidget,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QToolBar
)

from ui.pages.dashboard_page import DashboardPage
from ui.pages.transactions_page import TransactionsPage

from services.csv_importer import import_csv
from services.database_service import (
    save_transactions,
)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestion Financière")
        self.resize(1400, 900)

        # =====================
        # TOOLBAR
        # =====================

        toolbar = QToolBar("Principal")

        toolbar.setMovable(False)

        self.addToolBar(toolbar)

        import_action = QAction("📂 Importer CSV", self)

        import_action.triggered.connect(self.import_csv_file)

        toolbar.addAction(import_action)

        # =====================
        # PAGES
        # =====================

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout()

        self.menu = QListWidget()
        self.menu.addItem("📊 Tableau de bord")
        self.menu.addItem("📋 Transactions")
        self.menu.setMaximumWidth(250)

        self.stack = QStackedWidget()

        self.dashboard_page = DashboardPage()
        self.transactions_page = TransactionsPage()

        self.stack.addWidget(self.dashboard_page)

        self.stack.addWidget(self.transactions_page)

        self.menu.currentRowChanged.connect(self.stack.setCurrentIndex)

        self.menu.setCurrentRow(0)

        layout.addWidget(self.menu)
        layout.addWidget(self.stack)
        central_widget.setLayout(layout)

        self.menu.setStyleSheet("""
        QListWidget {
            font-size: 14px;
            padding: 10px;
        }

        QListWidget::item {
            height: 40px;
        }

        QListWidget::item:selected {
            background-color: #2d7ff9;
            color: white;
            border-radius: 6px;
        }
        """)
        
    def import_csv_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner un fichier CSV",
            "",
            "Fichiers CSV (*.csv)"
        )

        if not file_path:
            return

        try:

            transactions = import_csv(
                file_path
            )

            imported, ignored_months = (
                save_transactions(
                    transactions
                )
            )

            message = (
                f"{imported} transactions importées."
            )

            if ignored_months:

                month_names = {
                    1: "Janvier",
                    2: "Février",
                    3: "Mars",
                    4: "Avril",
                    5: "Mai",
                    6: "Juin",
                    7: "Juillet",
                    8: "Août",
                    9: "Septembre",
                    10: "Octobre",
                    11: "Novembre",
                    12: "Décembre"
                }

                months_text = []

                for year, month in sorted(
                    ignored_months
                ):

                    months_text.append(
                        f"{month_names[month]} {year}"
                    )

                message += (
                    "\n\n"
                    "Les mois suivants "
                    "étaient déjà présents "
                    "et n'ont pas été importés :\n\n"
                    + "\n".join(months_text)
                )

            QMessageBox.information(
                self,
                "Import terminé",
                message
            )

            self.dashboard_page.load_years()

            self.dashboard_page.refresh()

            self.transactions_page.load_years()

            self.transactions_page.refresh()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erreur",
                str(e)
            )
    
    def export_csv(self):
        pass