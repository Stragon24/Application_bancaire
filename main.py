import sys

from PySide6.QtWidgets import QApplication

from database.database import Base
from database.database import engine

from ui.main_window import MainWindow


def main():

    Base.metadata.create_all(
        bind=engine
    )

    app = QApplication(sys.argv)

    window = MainWindow()

    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()