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

from PySide2 import QtWidgets, QtCore
import flame
import os

__title__ = "Find Folder"
__version_info__ = (2, 0, 0)
__version__ = ".".join([str(num) for num in __version_info__])
__version_title__ = "{} v{}".format(__title__, __version__)

MESSAGE_PREFIX = "[PYTHON HOOK]"


class FlameButton(QtWidgets.QPushButton):
    '''
    Custom Qt Flame Button Widget v2.1

    button_name: button text [str]
    connect: execute when clicked [function]
    button_color: (optional) normal, blue [str]
    button_width: (optional) default is 150 [int]
    button_max_width: (optional) default is 150 [int]

    Usage:

        button = FlameButton(
            'Button Name', do_something__when_pressed, button_color='blue')
    '''

    def __init__(self, button_name, connect, button_color='normal', button_width=150,
                 button_max_width=150):
        super(FlameButton, self).__init__()

        self.setText(button_name)
        self.setMinimumSize(QtCore.QSize(button_width, 28))
        self.setMaximumSize(QtCore.QSize(button_max_width, 28))
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clicked.connect(connect)
        if button_color == 'normal':
            self.setStyleSheet('''
                QPushButton {
                    color: rgb(154, 154, 154);
                    background-color: rgb(58, 58, 58);
                    border: none;
                    font: 14px "Discreet"}
                QPushButton:hover {
                    border: 1px solid rgb(90, 90, 90)}
                QPushButton:pressed {
                    color: rgb(159, 159, 159);
                    background-color: rgb(66, 66, 66);
                    border: 1px solid rgb(90, 90, 90)}
                QPushButton:disabled {
                    color: rgb(116, 116, 116);
                    background-color: rgb(58, 58, 58);
                    border: none}
                QToolTip {
                    color: rgb(170, 170, 170);
                    background-color: rgb(71, 71, 71);
                    border: 10px solid rgb(71, 71, 71)}''')
        elif button_color == 'blue':
            self.setStyleSheet('''
                QPushButton {
                    color: rgb(190, 190, 190);
                    background-color: rgb(0, 110, 175);
                    border: none;
                    font: 12px "Discreet"}
                QPushButton:hover {
                    border: 1px solid rgb(90, 90, 90)}
                QPushButton:pressed {
                    color: rgb(159, 159, 159);
                    border: 1px solid rgb(90, 90, 90)
                QPushButton:disabled {
                    color: rgb(116, 116, 116);
                    background-color: rgb(58, 58, 58);
                    border: none}
                QToolTip {
                    color: rgb(170, 170, 170);
                    background-color: rgb(71, 71, 71);
                    border: 10px solid rgb(71, 71, 71)}''')


class FlameLabel(QtWidgets.QLabel):
    '''
    Custom Qt Flame Label Widget v2.1

    label_name:  text displayed [str]
    label_type:  (optional) select from different styles:
                 normal, underline, background. default is normal [str]
    label_width: (optional) default is 150 [int]

    Usage:

        label = FlameLabel('Label Name', 'normal', 300)
    '''

    def __init__(self, label_name, label_type='normal', label_width=150):
        super(FlameLabel, self).__init__()

        self.setText(label_name)
        self.setMinimumSize(label_width, 28)
        self.setMaximumHeight(28)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # Set label stylesheet based on label_type

        if label_type == 'normal':
            self.setStyleSheet('''
                QLabel {
                    color: rgb(154, 154, 154);
                    font: 14px "Discreet"}
                QLabel:disabled {
                    color: rgb(106, 106, 106)}''')
        elif label_type == 'underline':
            self.setAlignment(QtCore.Qt.AlignCenter)
            self.setStyleSheet('''
                QLabel {
                    color: rgb(154, 154, 154);
                    border-bottom: 1px inset rgb(40, 40, 40);
                    font: 14px "Discreet"}
                QLabel:disabled {
                    color: rgb(106, 106, 106)}''')
        elif label_type == 'background':
            self.setStyleSheet('''
                QLabel {
                    color: rgb(154, 154, 154);
                    background-color: rgb(30, 30, 30);
                    padding-left: 5px;
                    font: 14px "Discreet"}
                QLabel:disabled {
                    color: rgb(106, 106, 106)}''')


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
    """Searches for a subdirectory.

    Find matching subdirectories based on a search string, then navigate to the
    destination subdirectory the artist chooses.
    """

    def __init__(self, selection):
        """Ensure that only 1 folder is selected by the artist."""

        self.message(__version_title__)
        self.message("Script called from {}".format(__file__))

        if len(selection) < 2:
            self.src_path = selection[0].path

            self.dest_folder = ''
            self.dest_path = ''

            self.main_window()
        else:
            msg = FlameMessageBox()
            msg.setText('Please select only 1 folder.')
            msg.setWindowTitle('Error')
            msg.exec_()

    @staticmethod
    def message(string):
        """Print message to shell window and append global MESSAGE_PREFIX."""

        print(" ".join([MESSAGE_PREFIX, string]))


    def get_folders(self):
        """Return all subdirectories in a folder."""
        walker = os.walk(self.src_path)

        root, dirs, files = next(walker)
        del root
        del files

        results = [d for d in dirs if d[0] != '.']  # results unsorted

        return results

    def main_window(self):
        """Enter search terms, view results, then confirm the selection."""

        def okay_button():
            """Close window and process the artist's selected subdirectory."""
            self.window.close()

            self.dest_folder = self.list_scroll.selectedItems()[0].text()
            self.dest_path = os.path.join(self.src_path, self.dest_folder)

            # introduced in flame 2021.2
            flame.mediahub.files.set_path(self.dest_path)

        def filter_list():
            """Updates the results list when anything is typed in the Find bar."""
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

        self.window.move(
                (resolution.width() / 2) - (self.window.frameSize().width() / 2),
                (resolution.height() / 2) - (self.window.frameSize().height() / 2))

        # Label
        self.find_label = FlameLabel('Find')

        # Line Edit
        self.find = FlameLineEdit('', self.window)

        self.find.textChanged.connect(filter_list)

        # List Widget
        self.list_scroll = FlameListWidget(self.window)

        self.list_scroll.addItems(self.get_folders())
        self.list_scroll.sortItems()

        self.list_scroll.itemDoubleClicked.connect(okay_button)

        # Buttons
        self.ok_btn = FlameButton('Ok', okay_button, button_color='blue')
        self.ok_btn.setAutoDefault(True)  # doesnt make Enter key work

        self.cancel_btn = FlameButton('Cancel', self.window.close)

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
    valid_objects = (flame.PyMediaHubFilesFolder)

    return all(isinstance(item, valid_objects) for item in selection)


def get_mediahub_files_custom_ui_actions():
    """Python hook to add custom item to right click menu in MediaHub."""
    return [{'name': 'Find...',
             'actions': [{'name': 'Find Folder',
                          'isVisible': scope_folders,
                          'execute': FindFolder,
                          'minimumVersion': '2022'}]}]
