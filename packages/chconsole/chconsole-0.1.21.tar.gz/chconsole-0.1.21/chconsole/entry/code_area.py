import os
from functools import singledispatch

from qtconsole.bracket_matcher import BracketMatcher
from qtconsole.call_tip_widget import CallTipWidget
from qtconsole.completion_widget import CompletionWidget
from qtconsole.kill_ring import QtKillRing
from qtconsole.qt import QtGui, QtCore, QT_API, QT_API_PYSIDE
from qtconsole.util import MetaQObjectHasTraits
from traitlets import Bool

from chconsole.messages import InText, CompleteItems, CallTip
from chconsole.messages import Source, ExportItem, Inspect
from chconsole.standards import DocumentConfig, ViewportFilter, TextAreaFilter
from .code_area_filter import CodeAreaFilter
from .history import History

__author__ = 'Manfred Minimair <manfred@minimair.org>'


@singledispatch
def _post(item, target):
    pass
    #raise NotImplementedError


@_post.register(InText)
def _(item, target):
    target.clear()
    target.insertPlainText(item.text)


@_post.register(CompleteItems)
def _(item, target):
    target.process_complete(item)


@_post.register(CallTip)
def _(item, target):
    if target.textCursor().position() == target.call_tip_position:
        target.call_tip_widget.show_inspect_data(item.content)


def code_area_template(edit_class):
    """
    Template for Entry.
    :param edit_class: QTGui.QTextEdit or QtGui.QPlainTextEdit
    :return: Instantiated class.
    """
    class CodeArea(MetaQObjectHasTraits('NewBase', (DocumentConfig, edit_class), {})):
        """
        Text edit that has two modes, code and chat mode,
        accepting code to be executed or arbitrary text (chat messages).
        """
        name = 'Code'  # name of the widget

        font_changed = QtCore.Signal(QtGui.QFont)          # Signal emitted when the font is changed.

        execute_on_complete_input = Bool(True, config=True,
            help="""Whether to automatically execute on syntactically complete input.

            If False, Shift-Enter is required to submit each execution.
            Disabling this is mainly useful for non-Python kernels,
            where the completion check would be wrong.
            """
        )

        # Whether to automatically show calltips on open-parentheses.
        enable_call_tips = Bool(True, config=True,
                                help="Whether to draw information calltips on open-parentheses.")

        call_tip_widget = None  # CallTipWidget
        _bracket_matcher = None  # BracketMatcher
        call_tip_position = 0  # cursor position where a call tip should be shown

        clear_on_kernel_restart = Bool(True, config=True,
            help="Whether to clear the console when the kernel is restarted")

        please_export = QtCore.Signal(ExportItem)  # tasks for the kernel

        is_complete = None  # function str->(bool, str) that checks whether the input is complete code

        viewport_filter = None
        entry_filter = None
        text_area_filter = None
        release_focus = QtCore.Signal()
        to_next = QtCore.Signal()

        completer = None  # completion object

        kill_ring = None  # QKillRing
        history = None  # History object

        _comment_prefix = '#'  # prefix for line comments

        round_table = None  # RoundTable

        def __init__(self, round_table, is_complete=None, text='', use_ansi=True, comment_prefix='#',
                     parent=None, **kwargs):
            """
            Initialize.
            :param round_table: RoundTable
            :param is_complete: function str->(bool, str) that checks whether the input is complete code
            :param code: True if object should initially expect code to be executed; otherwise arbitrary text.
            :param text: initial text.
            :param parent: parent widget.
            :param kwargs: arguments for LoggingConfigurable
            :return:
            """
            edit_class.__init__(self, text, parent)
            DocumentConfig.__init__(self, **kwargs)

            self.round_table = round_table

            self.use_ansi = use_ansi
            self.highlighter.enable()

            # Call tips
            # forcefully disable calltips if PySide is < 1.0.7, because they crash
            if QT_API == QT_API_PYSIDE:
                import PySide
                if PySide.__version_info__ < (1,0,7):
                    self.log.warn("PySide %s < 1.0.7 detected, disabling calltips" % PySide.__version__)
                    self.enable_call_tips = False
            self.call_tip_widget = CallTipWidget(self)
            self.call_tip_widget.setFont(self.font)
            self.font_changed.connect(self.call_tip_widget.setFont)

            self._bracket_matcher = BracketMatcher(self)
            self.document().contentsChange.connect(self._document_contents_change)

            self.setFrameStyle(QtGui.QFrame.NoFrame)

            self.setAcceptDrops(True)

            self._control = self  # required for completer
            self._clear_temporary_buffer = lambda: None
            self.completer = CompletionWidget(self)
            self.completer.setFont(self.font)
            self.is_complete = is_complete

            self.viewport_filter = ViewportFilter(self)
            self.viewport().installEventFilter(self.viewport_filter)
            self.entry_filter = CodeAreaFilter(self)
            self.installEventFilter(self.entry_filter)
            self.text_area_filter = TextAreaFilter(self)
            self.installEventFilter(self.text_area_filter)

            # Text interaction
            self.setTextInteractionFlags(QtCore.Qt.TextEditable | QtCore.Qt.TextEditorInteraction)
            self.setUndoRedoEnabled(True)
            self.kill_ring = QtKillRing(self)
            self.history = History(self)
            self._comment_prefix = comment_prefix

        def _set_font(self, font):
            DocumentConfig.set_font(self, font)
            if hasattr(self, 'completer') and self.completer:
                self.completer.setFont(font)
            self.font_changed.emit(font)

        @property
        def source(self):
            """
            Get the source from the document edited.
            :return: Source object.
            """
            return Source(self.toPlainText())

        def post(self, item):
            """
            Process the item received.
            :param item: ImportItem for the input area.
            :return:
            """
            _post(item, self)

        @QtCore.Slot()
        def set_focus(self):
            """
            Set the focus to this widget.
            :return:
            """
            self.setFocus()

        # JupyterWidget
        def process_complete(self, items):
            cursor = self.textCursor()
            matches = items.matches
            start = items.start
            end = items.end
            start = max(start, 0)
            end = max(end, start)

            # Move the control's cursor to the desired end point
            cursor_pos = self.textCursor().position()
            if end < cursor_pos:
                cursor.movePosition(QtGui.QTextCursor.Left,
                                    n=(cursor_pos - end))
            elif end > cursor_pos:
                cursor.movePosition(QtGui.QTextCursor.Right,
                                    n=(end - cursor_pos))
            # This line actually applies the move to control's cursor
            self.setTextCursor(cursor)

            offset = end - start
            # Move the local cursor object to the start of the match and
            # complete.
            cursor.movePosition(QtGui.QTextCursor.Left, n=offset)
            self._complete_with_items(cursor, matches)

        # ConsoleWidget
        def _complete_with_items(self, cursor, items):
            """
            Complete code at a given location.
            :param cursor: cursor where completion is performed.
            :param items: list of items that can serve for completion.
            :return:
            """
            self.completer.cancel_completion()

            if len(items) == 1:
                cursor.setPosition(self.textCursor().position(),
                                   QtGui.QTextCursor.KeepAnchor)
                cursor.insertText(items[0])

            elif len(items) > 1:
                current_pos = self.textCursor().position()
                prefix = os.path.commonprefix(items)
                if prefix:
                    cursor.setPosition(current_pos, QtGui.QTextCursor.KeepAnchor)
                    cursor.insertText(prefix)

                cursor.movePosition(QtGui.QTextCursor.Left, n=len(prefix))
                self.completer.show_items(cursor, items)

        # FrontendWidget
        def _auto_call_tip(self):
            """Trigger call tip automatically on open parenthesis

            Call tips can be requested explcitly with `_call_tip`.
            """
            cursor = self.textCursor()
            cursor.movePosition(QtGui.QTextCursor.Left)
            if cursor.document().characterAt(cursor.position()) == '(':
                # trigger auto call tip on open paren
                self._call_tip()

        # FrontendWidget
        def _call_tip(self):
            """Shows a call tip, if appropriate, at the current cursor location."""
            # Decide if it makes sense to show a call tip
            # if not self.enable_calltips or not self.kernel_client.shell_channel.is_alive():
            #     return False
            # cursor_pos = self._get_input_buffer_cursor_pos()
            # code = self.toPlainText()
            # # Send the metadata request to the kernel
            # msg_id = self.kernel_client.inspect(code, cursor_pos)

            if not self.enable_call_tips:
                return False
            cursor_pos = self.textCursor().position()
            self.please_export.emit(Inspect(self.source, cursor_pos))
            return True

        # FrontendWidget
        def _document_contents_change(self, position, removed, added):
            """ Called whenever the document's content changes. Display a call tip
                if appropriate.
            """
            # Calculate where the cursor should be *after* the change:
            position += added

            if position == self.textCursor().position():
                self.call_tip_position = position
                self._auto_call_tip()

    return CodeArea
