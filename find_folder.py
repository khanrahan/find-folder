"""
Find Folder

URL:

    https://github.com/khanrahan/find-folder

Description:

    Searches for a subdirectory of the current directory in the Media Hub.  Useful for
    navigating a folder that contains many many subfolders with long names but you have
    a search term that would quickly find the folder you need.

Menus:

    Right-click selected folder in Media Hub Files -> Find... -> Find Folder

To Install:

    For all users, copy this file to:
    /opt/Autodesk/shared/python

    For a specific user, copy this file to:
    /opt/Autodesk/user/<user name>/python
"""

from __future__ import print_function
from PySide2 import QtWidgets, QtCore
import flame
import os

__title__ = "Find Folder"
__version_info__ = (2, 0, 0)
__version__ = ".".join([str(num) for num in __version_info__])
__version_title__ = "{} v{}".format(__title__, __version__)

MESSAGE_PREFIX = "[PYTHON HOOK]"

class FlameButton(QtWidgets.QPushButton):
    """
    Custom Qt Flame Button Widget
    To use:
    button = FlameButton('Button Name', do_when_pressed, window)
    """

    def __init__(self, button_name, do_when_pressed, parent_window, *args, **kwargs):
        super(FlameButton, self).__init__(*args, **kwargs)

        self.setText(button_name)
        self.setParent(parent_window)
        self.setMinimumSize(QtCore.QSize(110, 28))
        self.setMaximumSize(QtCore.QSize(110, 28))
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clicked.connect(do_when_pressed)
        self.setStyleSheet("""
            QPushButton {
                color: #9a9a9a;
                background-color: #424142;
                border-top: 1px inset #555555;
                border-bottom: 1px inset black;
                font: 14px 'Discreet'}
            QPushButton:pressed {
                color: #d9d9d9;
                background-color: #4f4f4f;
                border-top: 1px inset #666666;
                font: italic}
            QPushButton:disabled {
                color: #747474;
                background-color: #353535;
                border-top: 1px solid #444444;
                border-bottom: 1px solid #242424}
            QToolTip {
                color: black;
                background-color: #ffffde;
                border: black solid 1px}""")


class FlameLabel(QtWidgets.QLabel):
    """
    Custom Qt Flame Label Widget
    For different label looks set label_type as: 'normal', 'background', or 'outline'
    To use:
    label = FlameLabel('Label Name', 'normal', window)
    """

    def __init__(self, label_name, label_type, parent_window, *args, **kwargs):
        super(FlameLabel, self).__init__(*args, **kwargs)

        self.setText(label_name)
        self.setParent(parent_window)
        self.setMinimumSize(110, 28)
        self.setMaximumHeight(28)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # Set label stylesheet based on label_type

        if label_type == 'normal':
            self.setStyleSheet("""
                QLabel {
                    color: #9a9a9a;
                    border-bottom: 1px inset #282828;
                    font: 14px 'Discreet'}
                QLabel:disabled {
                    color: #6a6a6a}""")
        elif label_type == 'background':
            self.setAlignment(QtCore.Qt.AlignCenter)
            self.setStyleSheet("""
                QLabel {
                    color: #9a9a9a;
                    background-color: #393939;
                    font: 14px 'Discreet'}
                QLabel:disabled {
                    color: #6a6a6a}""")
        elif label_type == 'outline':
            self.setAlignment(QtCore.Qt.AlignCenter)
            self.setStyleSheet("""
                QLabel {
                    color: #9a9a9a;
                    background-color: #212121;
                    border: 1px solid #404040;
                    font: 14px 'Discreet'}
                QLabel:disabled {
                    color: #6a6a6a}""")


class FlameLineEdit(QtWidgets.QLineEdit):
    """
    Custom Qt Flame Line Edit Widget
    Main window should include this: window.setFocusPolicy(QtCore.Qt.StrongFocus)
    To use:
    line_edit = FlameLineEdit('Some text here', window)
    """

    def __init__(self, text, parent_window, *args, **kwargs):
        super(FlameLineEdit, self).__init__(*args, **kwargs)

        self.setText(text)
        self.setParent(parent_window)
        self.setMinimumHeight(28)
        self.setMinimumWidth(110)
        # self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet("""
            QLineEdit {
                color: #9a9a9a;
                background-color: #373e47;
                selection-color: #262626;
                selection-background-color: #b8b1a7;
                font: 14px 'Discreet'}
            QLineEdit:focus {
                background-color: #474e58}
            QLineEdit:disabled {
                color: #6a6a6a;
                background-color: #373737}
            QToolTip {
                color: black;
                background-color: #ffffde;
                border: black solid 1px}""")


class FlameListWidget(QtWidgets.QListWidget):
    """
    Custom Qt Flame List Widget
    To use:
    list_widget = FlameListWidget(window)
    """

    def __init__(self, parent_window, *args, **kwargs):
        super(FlameListWidget, self).__init__(*args, **kwargs)

        self.setMinimumSize(500, 250)
        self.setParent(parent_window)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        # only want 1 selection possible.  no multi selection.
        #self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setSpacing(3)
        self.setAlternatingRowColors(True)
        self.setUniformItemSizes(True)
        self.setStyleSheet("""
            QListWidget {
                color: #9a9a9a;
                background-color: #2a2a2a;
                alternate-background-color: #2d2d2d;
                outline: none;
                font: 14px "Discreet"}
            QListWidget::item:selected {
                color: #d9d9d9;
                background-color: #474747}""")


class FlameMessageBox(QtWidgets.QMessageBox):
    """
    Custom Qt Flame Message Box
    To use:
    message_box = FlameMessageBox(message)
    message_box.setText("message for user.")
    message_box.setWindowTitle("window title")
    message_box.exec_()
    """

    def __init__(self, *args, **kwargs):
        super(FlameMessageBox, self).__init__(*args, **kwargs)

        # the below has now effect.  should be subclassing QDialog instead.
        self.setMinimumSize(400, 270)
        # Could not get the below working so just doing it at the instance.
        #self.setText(self.message)
        self.button = self.addButton(QtWidgets.QMessageBox.Ok)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.setMinimumSize(QtCore.QSize(80, 28))
        self.setStyleSheet("""
            MessageBox {
                background-color: #313131;
                font: 14px "Discreet"}
            QLabel {
                color: #9a9a9a;
                font: 14px "Discreet"}
            QPushButton {
                color: #9a9a9a;
                background-color: #732020;
                border-top: 1px inset #555555;
                border-bottom: 1px inset black;
                font: 14px "Discreet"}
            QPushButton:pressed {
                color: #d9d9d9;
                background-color: #4f4f4f;
                border-top: 1px inset #666666;
                font: italic}""")


class FindFolder:
    """
    Searches a folder for a subdirectory that matches the search terms.

    On Flame 2021.2 and above, it will navigate in Media Hub to the selection.

    On Flame 2021.1 and below, it will copy the selected subdirectory's path
    to the clipboard for the artist to paste in the Media Hub path bar.
    """

    def __init__(self, selection):
        """Ensure that only 1 folder is selected by the artist."""

        self.message(__version_title__)
        self.message("Script called from {}".format(__file__))

        if len(selection) < 2:
            self.src_path = selection[0].path

            self.dest_folder = ""
            self.dest_path = ""

            self.main_window()
        else:
            msg = FlameMessageBox()
            msg.setText("Please select only 1 folder.")
            msg.setWindowTitle("Error")
            msg.exec_()

    @staticmethod
    def message(string):
        """Print message to shell window and append global MESSAGE_PREFIX."""

        print(" ".join([MESSAGE_PREFIX, string]))


    def get_folders(self):
        """Return all subdirectories in a folder."""
        walker = os.walk(self.src_path)

        root, dirs, files = next(walker)

        results = [d for d in dirs if not d[0] == "."] # results unsorted

        return results

    def main_window(self):
        """
        UI window for artists to enter search terms, view results, then confirm
        the selection.
        """
        def okay_button():
            """Close window and process the artist's selected subdirectory."""

            self.window.close()

            self.dest_folder = self.list_scroll.selectedItems()[0].text()
            self.dest_path = os.path.join(self.src_path, self.dest_folder)

            # introduced in flame 2021.2
            flame.mediahub.files.set_path(self.dest_path)

        def filter_list():
            """
            Updates the results list when anything is typed in the Find bar.
            """
            for num in range(self.list_scroll.count()):
                if self.find.text() in self.list_scroll.item(num).text():
                    self.list_scroll.item(num).setHidden(False)
                else:
                    self.list_scroll.item(num).setHidden(True)

        self.window = QtWidgets.QWidget()

        self.window.setMinimumSize(600, 600)
        self.window.setStyleSheet('background-color: #272727')
        self.window.setWindowTitle(__version_title__)

        # FlameLineEdit class needs this
        self.window.setFocusPolicy(QtCore.Qt.StrongFocus)

        # Center Window
        resolution = QtWidgets.QDesktopWidget().screenGeometry()

        self.window.move((resolution.width() / 2) - (self.window.frameSize().width() / 2),
                         (resolution.height() / 2) - (self.window.frameSize().height() / 2))

        # Label
        self.find_label = FlameLabel("Find", "normal", self.window)

        # Line Edit
        self.find = FlameLineEdit("", self.window)

        self.find.textChanged.connect(filter_list)

        # List Widget
        self.list_scroll = FlameListWidget(self.window)

        self.list_scroll.addItems(self.get_folders())
        self.list_scroll.sortItems()

        self.list_scroll.itemDoubleClicked.connect(okay_button)

        # Buttons
        self.ok_btn = FlameButton('Ok', okay_button, self.window)
        self.ok_btn.setStyleSheet('background: #732020')
        self.ok_btn.setShortcut('Return')

        self.cancel_btn = FlameButton("Cancel", self.window.close, self.window)

        # Layout
        self.grid = QtWidgets.QGridLayout()
        self.grid.setHorizontalSpacing(10)
        self.grid.setVerticalSpacing(10)

        self.grid.addWidget(self.find_label, 0, 0)
        self.grid.addWidget(self.find, 0, 1)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.list_scroll)
        self.hbox.addStretch(1)

        self.hbox2 = QtWidgets.QHBoxLayout()
        self.hbox2.addStretch(1)
        self.hbox2.addWidget(self.cancel_btn)
        self.hbox2.addWidget(self.ok_btn)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.setMargin(20)
        self.vbox.addLayout(self.grid)
        self.vbox.insertSpacing(1, 20)
        self.vbox.addLayout(self.hbox)
        self.vbox.insertSpacing(3, 20)
        self.vbox.addLayout(self.hbox2)

        self.window.setLayout(self.vbox)

        self.window.show()
        return self.window


def scope_folders(selection):
    """Determine if selection is a folder in the Media Hub > Files tab."""

    for item in selection:
        if "FilesFolder" in str(item):
            return True
    return False


def get_mediahub_files_custom_ui_actions():
    """Python hook to add custom item to right click menu in MediaHub."""
    return [{'name': "Find...",
             'actions': [{'name': "Find Folder",
                          'isVisible': scope_folders,
                          'execute': FindFolder,
                          'minimumVersion': "2022"}]}]
