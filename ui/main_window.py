from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox
)

from ui.transactions_view import TransactionsView

from services.csv_importer import import_csv
from services.database_service import (
    save_transactions,
    is_file_already_imported,
    register_imported_file
)

from services.database_service import (
    save_transactions,
    is_file_already_imported,
    register_imported_file,
    get_all_transactions
    )

from services.file_service import compute_file_hash

from database.database import SessionLocal

from ui.dashboard_widget import DashboardWidget

from services.database_service import (
    get_dashboard_stats
)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestion Financière")
        self.resize(1400, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.dashboard = DashboardWidget()
        
        layout.addWidget(
            self.dashboard
        )

        self.refresh_dashboard()

        self.import_csv_button = QPushButton(
            "Importer un relevé CSV"
        )

        self.import_csv_button.clicked.connect(
            self.import_csv_file
        )

        layout.addWidget(
            self.import_csv_button
        )

        self.transactions_view = TransactionsView()

        layout.addWidget(
            self.transactions_view
        )

        self.load_saved_transactions()

        central_widget.setLayout(layout)

    def refresh_dashboard(self):

        stats = get_dashboard_stats()

        self.dashboard.update_stats(
            stats
        )

    def load_saved_transactions(self):

        transactions = get_all_transactions()

        self.transactions_view.load_transactions(
            transactions
        )

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

            session = SessionLocal()

            file_hash = compute_file_hash(
                file_path
            )

            if is_file_already_imported(
                session,
                file_hash
            ):

                QMessageBox.warning(
                    self,
                    "Import refusé",
                    "Ce fichier a déjà été importé."
                )

                session.close()
                return

            transactions = import_csv(
                file_path
            )

            imported = save_transactions(
                transactions
            )

            register_imported_file(
                session,
                file_path,
                file_hash
            )

            session.close()

            self.transactions_view.load_transactions(
                transactions
            )
            
            QMessageBox.information(
                self,
                "Import terminé",
                f"{imported} transactions importées."
            )

            self.refresh_dashboard()
            
        except Exception as e:

            QMessageBox.critical(
                self,
                "Erreur",
                str(e)
            )
    
    