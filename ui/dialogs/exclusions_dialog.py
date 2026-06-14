from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)

from services.database_service import (
    get_user_exclusions,
    delete_exclusion
)

from ui.dialogs.add_exclusion_dialog import (
    AddExclusionDialog
)


class ExclusionsDialog(QDialog):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Configuration des exclusions"
        )

        self.resize(800, 500)

        layout = QVBoxLayout()

        self.table = QTableWidget()

        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels(
            [
                "Type",
                "Valeur"
            ]
        )

        layout.addWidget(
            self.table
        )

        self.add_button = QPushButton(
            "Nouveau"
        )

        self.delete_button = QPushButton(
            "Supprimer"
        )

        layout.addWidget(
            self.add_button
        )

        layout.addWidget(
            self.delete_button
        )

        self.setLayout(layout)

        self.add_button.clicked.connect(
            self.add_exclusion
        )

        self.delete_button.clicked.connect(
            self.delete_selected
        )

        self.refresh()

    def refresh(self):

        exclusions = get_user_exclusions()

        self.table.setRowCount(
            len(exclusions)
        )

        for row, exclusion in enumerate(
            exclusions
        ):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    exclusion.exclusion_type
                )
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    exclusion.value
                )
            )

            self.table.item(
                row,
                0
            ).setData(
                1000,
                exclusion.id
            )

    def add_exclusion(self):

        dialog = AddExclusionDialog()

        if dialog.exec():

            self.refresh()

    def delete_selected(self):

        row = self.table.currentRow()

        if row < 0:
            return

        exclusion_id = (
            self.table.item(
                row,
                0
            )
            .data(1000)
        )

        delete_exclusion(
            exclusion_id
        )

        self.refresh()