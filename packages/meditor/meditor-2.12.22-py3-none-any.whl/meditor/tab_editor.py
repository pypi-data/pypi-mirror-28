
import os.path
import logging

from PyQt5 import QtCore, QtGui, QtWidgets

from .editor import Editor
from . import __default_basename__, __monospace__


logger = logging.getLogger(__name__)


FILTER = [
    'All support files (*.rst *.md *.txt);;',
    'reStructuredText files (*.rst *.rest);;',
    'Markdown files (*.md *.markdown);;',
    'Text files (*.txt)',
]


class TabEditor(QtWidgets.QTabWidget):
    statusChanged = QtCore.pyqtSignal(int, 'QString')
    previewRequest = QtCore.pyqtSignal(int, 'QString')
    modificationChanged = QtCore.pyqtSignal(int, bool)
    verticalScrollBarChanged = QtCore.pyqtSignal(int, int)
    filenameChanged = QtCore.pyqtSignal('QString', 'QString')
    fileLoaded = QtCore.pyqtSignal(int)
    _actions = None
    _enable_lexer = True
    _find_dialog = None
    _settings = None
    _wrap_mode = 0
    _one_editor = False
    _editor_font = None

    def __init__(self, settings, find_dialog, parent=None):
        super(TabEditor, self).__init__(parent)
        self._settings = settings
        self._find_dialog = find_dialog

        self.setMovable(True)
        self.setTabsClosable(True)
        self.setDocumentMode(True)
        self.setTabBarAutoHide(True)
        self.tabBarClicked.connect(self._onTabClicked)
        self.tabCloseRequested.connect(self._onTabCloseRequested)

        self._wrap_mode = self._settings.value('editor/wrap_mode', 0, type=int)
        self._one_editor = self._settings.value('editor/one_editor', False, type=bool)

        self._actions = {}
        action = QtWidgets.QAction(self.tr('&Open'), self)
        action.setShortcut(QtGui.QKeySequence.Open)
        action.triggered.connect(self._onOpen)
        action.setIcon(QtGui.QIcon.fromTheme('document-open'))
        self._actions['open'] = action

        action = QtWidgets.QAction(self.tr('&Save'), self)
        action.setShortcut(QtGui.QKeySequence.Save)
        action.triggered.connect(self._onSave)
        action.setIcon(QtGui.QIcon.fromTheme('document-save'))
        self._actions['save'] = action

        action = QtWidgets.QAction(self.tr('Save as...'), self)
        action.setShortcut(QtGui.QKeySequence.SaveAs)
        action.triggered.connect(self._onSaveAs)
        action.setIcon(QtGui.QIcon.fromTheme('document-save-as'))
        self._actions['save_as'] = action

        action = QtWidgets.QAction(self.tr('Close all'), self)
        action.triggered.connect(self._onCloseAll)
        self._actions['close_all'] = action

        action = QtWidgets.QAction(self.tr('Default font'), self)
        action.triggered.connect(self._onDefaultFont)
        self._actions['default_font'] = action

        action = QtWidgets.QAction(self.tr('One editor'), self, checkable=True)
        action.triggered.connect(self._onOneEditor)
        action.setChecked(self._one_editor)
        self._actions['one_editor'] = action

        self._actions.update(Editor.createAction(self, self._onAction))
        self.action('wrap_line').setChecked(self._wrap_mode > 0)

        value = self._settings.value('editor/font', __monospace__, type=str)
        self._editor_font = QtGui.QFont()
        self._editor_font.fromString(value)
        self.do_set_font(self._editor_font)
        logger.info('editor font: %s' % (self._editor_font.toString()))

        value = self._settings.value('editor/opened_files', type=str)
        for v in value.split(';')[::-1]:
            filepath, _, zoom = v.rpartition(':')
            if not os.path.exists(filepath):
                continue
            index = self.open(os.path.abspath(filepath))
            self.widget(index).zoomTo(int(zoom) if zoom else 0)
            if self._one_editor:
                break
        if self.count() == 0:
            self.new('.rst')

    def closeEvent(self, event):
        for x in range(self.count()):
            if not self._saveAndContinue(x):
                event.ignore()
                return

        self._settings.setValue('editor/font', self._editor_font.toString())
        opened = []
        for x in range(self.count()):
            editor = self.widget(x)
            opened.append('%s:%s' % (editor.getFileName(), editor.zoom()))
        self._settings.setValue('editor/opened_files', ';'.join(opened))
        self._settings.setValue('editor/wrap_mode', self._wrap_mode)
        self._settings.setValue('editor/one_editor', self._one_editor)

    def _onStatusChanged(self, status):
        widget = self.sender()
        index = self.indexOf(widget)
        if index < 0:
            return
        self.statusChanged.emit(index, status)

    def _onInputPreview(self):
        widget = self.sender()
        index = self.indexOf(widget)
        if index < 0:
            return
        self.previewRequest.emit(index, 'input')

    def _onModificationChanged(self, value):
        widget = self.sender()
        index = self.indexOf(widget)
        if index < 0:
            return
        widget.do_modification_changed(value, self)
        self.updateTitle(index)
        self.modificationChanged.emit(index, value)

    def _onCopyAvailable(self, value):
        widget = self.currentWidget()
        widget and widget.do_copy_available(value, self)

    def _onFilesDropped(self, value):
        for fname in value.split(';'):
            self.loadFile(fname)

    def _onVerticalScrollBarChanged(self, value):
        index = self.currentIndex()
        if index < 0:
            return
        self.verticalScrollBarChanged.emit(index, value)

    def _onTabClicked(self, index):
        widget = self.widget(index)
        if not widget:
            return
        widget.setFocus(QtCore.Qt.TabFocusReason)
        self.fileLoaded.emit(index)
        self.statusChanged.emit(index, widget.status())
        self.previewRequest.emit(index, 'open')

    def _onTabCloseRequested(self, index):
        if self._saveAndContinue(index):
            widget = self.widget(index)
            self.removeTab(index)
            del widget
        if self.count() == 0:
            self.new('.rst')
        widget = self.currentWidget()
        index = self.currentIndex()
        widget.setFocus(QtCore.Qt.TabFocusReason)
        self.fileLoaded.emit(index)
        self.statusChanged.emit(index, widget.status())
        self.previewRequest.emit(index, 'open')

    def _onOpen(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, self.tr('Open a file'),
            os.getcwd(),
            ''.join(FILTER),
        )
        if filename:
            self.loadFile(os.path.abspath(filename))

    def _onSave(self, index):
        if not index:
            index = self.currentIndex()

        filepath = self.filepath(index)
        dir_name = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        basename, _ = os.path.splitext(filename)
        if not dir_name and basename == __default_basename__:
            self._onSaveAs(index)
        else:
            self.widget(index).writeFile()
            self.updateTitle(index)
            self.previewRequest.emit(index, 'save')

    def _onSaveAs(self, index):
        if not index:
            index = self.currentIndex()

        filepath = self.filepath(index)
        dir_name = os.path.dirname(filepath)
        if not dir_name:
            dir_name = os.getcwd()

        filename = os.path.basename(filepath)
        new_filepath, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
            self,
            self.tr('Save file as ...'),
            os.path.join(dir_name, filename),
            ''.join(FILTER),
        )
        if new_filepath:
            new_filepath = os.path.abspath(new_filepath)
            _, ext = os.path.splitext(new_filepath)
            if not ext:
                ext = selected_filter.split('(')[1][1:4].strip()
                new_filepath = new_filepath + ext
            self.widget(index).writeFile(new_filepath)
            self.updateTitle(index)
            self.previewRequest.emit(index, 'save')
            self.filenameChanged.emit(filepath, new_filepath)

    def _saveAndContinue(self, index):
        if self.widget(index).isModified():
            filepath = self.filepath(index)
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setIcon(QtWidgets.QMessageBox.Question)
            msgBox.setText(self.tr('The document has been modified.'))
            msgBox.setInformativeText(
                self.tr('Do you want to save your changes?\n%s' % filepath)
            )
            msgBox.setStandardButtons(
                QtWidgets.QMessageBox.Save |
                QtWidgets.QMessageBox.Discard |
                QtWidgets.QMessageBox.Cancel
            )
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == QtWidgets.QMessageBox.Cancel:
                return False
            if ret == QtWidgets.QMessageBox.Save:
                self._onSave(index)
        return True

    def _onCloseAll(self):
        self.do_close_all()
        self.new('.rst')

    def _onDefaultFont(self):
        font, ok = QtWidgets.QFontDialog.getFont(self._editor_font, self)
        if ok:
            self._editor_font = font
            self.do_set_font(self._editor_font)

    def _onOneEditor(self, value):
        self._one_editor = value

    def _newEditor(self):
        editor = Editor(self._find_dialog, self)
        editor.statusChanged.connect(self._onStatusChanged)
        editor.verticalScrollBar().valueChanged.connect(self._onVerticalScrollBarChanged)
        editor.inputPreviewRequest.connect(self._onInputPreview)
        editor.modificationChanged.connect(self._onModificationChanged)
        editor.copyAvailable.connect(self._onCopyAvailable)
        editor.filesDropped.connect(self._onFilesDropped)

        editor.enableLexer(self._enable_lexer)
        editor.setWrapMode(self._wrap_mode)
        return editor

    def action(self, action):
        return self._actions.get(action)

    def new(self, ext):
        if self._one_editor:
            self.do_close_all()
        editor = self._newEditor()
        editor.newFile(ext)
        editor.setFont(self._editor_font)
        title = ('*' if editor.isModified() else '') + os.path.basename(editor.getFileName())
        index = self.insertTab(0, editor, title)
        self.setCurrentIndex(index)
        self.fileLoaded.emit(index)
        self.statusChanged.emit(index, self.widget(index).status())
        self.previewRequest.emit(index, 'new')
        return index

    def open(self, filepath):
        if self._one_editor:
            self.do_close_all()
        editor = self._newEditor()
        editor.readFile(filepath)
        editor.setFont(self._editor_font)
        title = ('*' if editor.isModified() else '') + os.path.basename(editor.getFileName())
        index = self.insertTab(0, editor, title)
        self.setCurrentIndex(index)
        self.fileLoaded.emit(index)
        self.statusChanged.emit(index, self.widget(index).status())
        self.previewRequest.emit(index, 'open')
        return index

    def text(self, index):
        if index is None:
            editor = self.currentWidget()
        else:
            editor = self.widget(index)
        if not editor:
            return
        return editor.text()

    def filepath(self, index=None):
        if index is None:
            editor = self.currentWidget()
        else:
            editor = self.widget(index)
        if not editor:
            return
        return editor.getFileName()

    def status(self, index):
        if index is None:
            editor = self.currentWidget()
        else:
            editor = self.widget(index)
        if not editor:
            return
        return editor.status()

    def openedFiles(self):
        opened = []
        for x in range(self.count()):
            opened.append(self.filepath(x))
        return opened

    def title(self, index=None, full=False):
        if index is None:
            editor = self.currentWidget()
        else:
            editor = self.widget(index)
        if full:
            title = ('* ' if editor.isModified() else '') + editor.getFileName()
        else:
            title = ('* ' if editor.isModified() else '') + os.path.basename(editor.getFileName())
        return title

    def updateTitle(self, index):
        self.setTabText(index, self.title(index))

    def enableLexer(self, enable):
        self._enable_lexer = enable
        for x in range(self.count()):
            self.widget(x).enableLexer(enable)

    def loadFile(self, path):
        if not path:
            index = self.new('.rst')
            return index
        else:
            if not Editor.canOpened(path):
                return
            for index in range(self.count()):
                if path == self.filepath(index):
                    self.setCurrentIndex(index)
                    self.fileLoaded.emit(index)
                    self.statusChanged.emit(index, self.widget(index).status())
                    self.previewRequest.emit(index, 'open')
                    return index
            if os.path.exists(path):
                logger.debug('Loading file: %s', path)
                index = self.open(path)
            else:
                logger.debug('Creating file: %s', path)
                index = self.new(path)
            return index

    def menuAboutToShow(self):
        widget = self.currentWidget()
        widget.menuAboutToShow(self)

    def menuEdit(self, menu):
        widget = self.currentWidget()
        widget.menuEdit(menu, self)

    def menuSetting(self, menu):
        menu.addAction(self.action('wrap_line'))
        menu.addAction(self.action('one_editor'))
        menu.addSeparator()
        menu.addAction(self.action('default_font'))

    def _onAction(self, action, value):
        widget = self.currentWidget()
        if action == 'wrap_line':
            for x in range(self.count()):
                self.widget(x).do_action(action, value)
            self._wrap_mode = widget.wrapMode()
        else:
            widget.do_action(action, value)

    def do_close_all(self):
        for x in list(range(self.count()))[::-1]:
            widget = self.widget(x)
            if not self._saveAndContinue(x):
                return
            self.removeTab(x)
            del widget

    def do_set_font(self, font):
        for x in range(self.count()):
            self.widget(x).setFont(font)
