from qtconsole.qt import QtGui
from chconsole.launch import start_chconsole, Launch
from chconsole.connect import Curie


__author__ = 'Manfred Minimair <manfred@minimair.org>'


class _CurieEntry(QtGui.QLineEdit):
    def __init__(self):
        super(_CurieEntry, self).__init__()

        self.setPlaceholderText('Enter launch information')


class _UserNameEntry(QtGui.QLineEdit):
    def __init__(self):
        super(_UserNameEntry, self).__init__()

        self.setPlaceholderText('Enter chat user name')


class LaunchWidget(QtGui.QWidget):

    def __init__(self, kernel_gate, gate_tunnel_user,
                 request_user_name=True, parent=None):
        """
        Initialize.
        :param kernel_gate: url of kernel gate.
        :param gate_tunnel_user: user name to tunnel through gate to kernel.
        :param request_user_name:
               whether user should enter a user name for chat.
        """
        super(LaunchWidget, self).__init__(parent)

        self.kernel_gate = kernel_gate
        self.gate_tunnel_user = gate_tunnel_user
        self.request_user_name = request_user_name
        self.setWindowTitle('Chat Console')
        self.notify = QtGui.QLabel('Connect with Chat Console' + ' ' * 60)
        self.input_user = _UserNameEntry()
        self.input_curie = _CurieEntry()
        self.button = QtGui.QPushButton('Submit')
        self.button.clicked.connect(self.finished)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.notify)
        layout.addWidget(self.input_user)
        layout.addWidget(self.input_curie)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.show()

    def finished(self):
        if self.request_user_name and not self.input_user.text():
            msg = QtGui.QMessageBox(self)
            msg.setWindowTitle('Chat Console')
            msg.setText('Please enter your chat user name.')
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
            msg.show()
        else:
            user_name = self.input_user.text().strip()
            curie = self.kernel_gate + '/' + self.input_curie.text().strip()
            if Curie.valid(curie):
                try:
                    launch = Launch(self.gate_tunnel_user,
                                    curie, user_name)
                    start_chconsole(launch)
                except Exception:
                    msg = QtGui.QMessageBox(self)
                    msg.setWindowTitle('Chat Console')
                    msg.setText('Remote connection cannot be established.')
                    msg.setStandardButtons(QtGui.QMessageBox.Ok)
                    msg.show()
            else:
                msg = QtGui.QMessageBox(self)
                msg.setWindowTitle('Chat Console')
                msg.setText('Invalid launch information.')
                msg.setStandardButtons(QtGui.QMessageBox.Ok)
                msg.show()
