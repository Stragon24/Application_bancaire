from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QComboBox,
    QLabel
)

from services.database_service import (
    get_all_categories,
    get_all_labels,
    add_exclusion
)


class AddExclusionDialog(QDialog):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Ajouter une exclusion"
        )

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel("Type")
        )

        self.type_combo = QComboBox()

        self.type_combo.addItems(
            [
                "category",
                "label"
            ]
        )

        layout.addWidget(
            self.type_combo
        )

        layout.addWidget(
            QLabel("Valeur")
        )

        self.value_combo = QComboBox()

        layout.addWidget(
            self.value_combo
        )

        self.save_button = QPushButton(
            "Ajouter"
        )

        layout.addWidget(
            self.save_button
        )

        self.setLayout(layout)

        self.type_combo.currentIndexChanged.connect(
            self.load_values
        )

        self.save_button.clicked.connect(
            self.save
        )

        self.load_values()

    def load_values(self):

        self.value_combo.clear()

        if (
            self.type_combo.currentText()
            == "category"
        ):

            self.value_combo.addItems(
                get_all_categories()
            )

        else:

            self.value_combo.addItems(
                get_all_labels()
            )

    def save(self):

        add_exclusion(
            self.type_combo.currentText(),
            self.value_combo.currentText()
        )

        self.accept()