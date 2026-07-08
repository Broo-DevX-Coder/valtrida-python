"""
Use the function of popup message box to show the message to user and execute the function when user click the button.
The function is called pup_message, it takes 4 parameters:
- title: the title of the message box
- text: the text of the message box
- function: the function to execute when user click the button
- type_: the type of the message box, it can be "info", "warning" or "error", default is "info"
exemple:
pup_message(
    title="Error",
    text="An error occurred while processing your request.",
    function=handle_error,
    type_="error"
)
"""

# ==================================================================
# Import nessary modules
# ==================================================================

# == Libs ==
from typing import Callable
from PySide2.QtWidgets import QMessageBox

# == local ==
from Styles.qss import QSS


# ==================================================================
# Functions
# ==================================================================
def pup_message(
    title: str,
    text: str,
    function: Callable[[], None] | any,
    type_: str = "info"
):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)

    if type_ == "error":
        icon = QMessageBox.Critical
    elif type_ == "warning":
        icon = QMessageBox.Warning
    else:
        icon = QMessageBox.Information

    msg.setIcon(icon)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setStyleSheet(QSS["POPUP_W"])

    result = msg.exec_()  # use exec() if PyQt6/PySide6
    if result == QMessageBox.Ok:
        if isinstance(function,Callable):
            function()

