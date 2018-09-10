from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate


class SavePlowing:
    def __init__(self, parent):
        """
        A class for storing plowing data
        :param parent: GeoDataFarm "self"
        """
        self.dw = parent.dock_widget
        self.tr = parent.tr
        self.parent = parent

    def set_widget_connections(self):
        """A simple function that sets the buttons on the plowing tab"""
        self.parent.dock_widget.PBPloSaveManual.clicked.connect(self.save_manual_data)

    def save_manual_data(self):
        if self.check_input():
            field = self.dw.CBPloField.currentText()
            date_ = self.dw.DEPlowing.text()
            depth = self.dw.LEPloDepth.text()
            other = self.dw.LEPloOther.toPlainText()
            if depth == '':
                depth = 'Null'
            if other == '':
                other = 'Null'
            sql = f"""Insert into other.plowing_manual(field, date_, depth, other) 
            VALUES ('{field}', '{date_}','{depth}','{other}')"""
            try:
                self.parent.db.execute_sql(sql)
                QMessageBox.information(None, self.tr('Success'), self.tr('The data was stored correctly'))
            except Exception as e:
                QMessageBox.information(None, self.tr('Error'),
                                        self.tr('Following error occurred: {m}'.format(m=e)))
        self.reset_widget()

    def reset_widget(self):
        """Resets the widget to the default values"""
        self.dw.CBHwField.setCurrentIndex(0)
        self.dw.DEPlowing.setDate(QDate.fromString('2000-01-01', 'yyyy-MM-dd'))
        self.dw.LEPloDepth.setText('')
        self.dw.LEPloOther.setPlainText('')

    def check_input(self):
        """Some simple checks that ensure that the basic data is filled in.
        :return bool"""
        if self.dw.CBHvField.currentText() == self.tr('--- Select field ---'):
            QMessageBox.information(None, self.tr('Error:'), self.tr('In order to save the data you must select a field'))
            return False
        if self.dw.DEPlowing.text() == '2000-01-01':
            QMessageBox.information(None, self.tr('Error:'), self.tr('In order to save the data you must select a date'))
            return False
        return True