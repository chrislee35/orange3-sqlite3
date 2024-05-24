#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from AnyQt.QtCore import Qt
from AnyQt.QtWidgets import QStyle, QSizePolicy, QFileDialog
from Orange.data import Table
from Orange.data import Domain
from Orange.data import StringVariable, ContinuousVariable
#from Orange.data import  DiscreteVariable
from Orange.widgets import gui, settings
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Msg, Output
import numpy as np
import sqlite3
from os import path

class OWSqlite3(OWWidget):
    name = "Sqlite3 Loader"
    description = "Opens an SQLite3 database and performs a query"
    icon = "icons/sqlite3.svg"
    priority = 55
    keywords = "sqlite3"
    
    class Outputs:
        data = Output("Table", Table)
        
    class Error(OWWidget.Error):
        sql_exception = Msg('Exception with sql: {} => {}')
        
    settingsHandler = settings.DomainContextHandler()
    dbfile = settings.ContextSetting(None)
    recentFiles = settings.ContextSetting([])
    sqlquery = settings.ContextSetting("SELECT * FROM TAB1")
    sqlhist = settings.ContextSetting([])
    
    want_control_area = False
    
    def __init__(self):
        super().__init__()
        self.file_index = 0
        self.result_set = None
        
        self.populate_controlArea()
        self.populate_mainArea()
        
        self.populate_comboboxes()
        self.reload()
    
    def populate_controlArea(self):
        hb2 = gui.widgetBox(self.mainArea, orientation=Qt.Horizontal)
        self.sqltext = gui.lineEdit(hb2, self, "sqlquery", 
            callback=self.reload)
        gui.button(
            hb2, self, 'Query', callback=self.reload,
            icon=self.style().standardIcon(QStyle.SP_BrowserReload),
            sizePolicy=(QSizePolicy.Maximum, QSizePolicy.Fixed))

        hb = gui.widgetBox(self.mainArea, orientation=Qt.Horizontal)
        self.filecombo = gui.comboBox(
            hb, self, "file_index", callback=self.select_db_file, 
            minimumWidth=200)
        gui.button(hb, self, '...', callback=self.browse_db_file,
            disabled=0, icon=self.style().standardIcon(QStyle.SP_DirOpenIcon),
            sizePolicy=(QSizePolicy.Maximum, QSizePolicy.Fixed)
        )
        
    def populate_mainArea(self):
        self.fieldTable = gui.table(self.mainArea, rows=0, columns=3)
        self.fieldTable.setHorizontalHeaderLabels(['idx', 'Name', 'Type'])
        self.fieldTable.setColumnWidth(0, 50)
        self.fieldTable.setColumnWidth(1, 255)
        self.fieldTable.setColumnWidth(2, 150)
        
    def load_result_set(self):
        conn = sqlite3.connect(self.dbfile)
        c = conn.cursor()
        try:
            c.execute(self.sqlquery)
        except Exception as e:
            self.Error.sql_exception(self.sqlquery, e)
            return
        self.Error.clear()
        self.column_names = [desc[0] for desc in c.description]
        self.result_set = c.fetchall()
        
    def update_field_table(self):
        rows = self.result_set
        column_names = self.column_names
        self.fieldTable.clear()
        self.fieldTable.setRowCount(len(column_names))
        for idx, col in enumerate(column_names):
            gui.tableItem(self.fieldTable, idx, 0, str(idx))
            gui.tableItem(self.fieldTable, idx, 1, col)
            if isinstance(rows[0][idx], (int, float)):
                gui.tableItem(self.fieldTable, idx, 2, 'Continuous')
            elif isinstance(rows[0][idx], (str)):
                gui.tableItem(self.fieldTable, idx, 2, 'String')
                        
    def create_table_from_resultset(self):
        if not self.result_set: return
        column_names = self.column_names
        rows = self.result_set
        attr_vars = []
        class_var = []
        meta_vars = []
        column_map = { 'a': [], 'c': [], 'm': [] }
        for idx, col in enumerate(column_names):
            if isinstance(rows[0][idx], (int, float)):
                attr_vars.append(ContinuousVariable(name=col))
                column_map['a'].append(idx)
            elif isinstance(rows[0][idx], (str)):
                meta_vars.append(StringVariable(name=col))
                column_map['m'].append(idx)
            
        domain = Domain(attr_vars, class_var, meta_vars)
        indicies = column_map['a']+column_map['c']+column_map['m']
        rows = np.array(rows)[:, indicies].tolist()
        table = Table.from_list(domain, rows)
        return table

    def reload(self):
        if not self.sqlquery: return
        if not self.dbfile: return
        
        self.load_result_set()
        if self.result_set:
            self.update_field_table()
            table = self.create_table_from_resultset()
            self.Outputs.data.send(table)
        
    def browse_db_file(self, browse_demos=False):
        """user pressed the '...' button to manually select a file to load"""
        startfile = self.recentFiles[0] if self.recentFiles else '.'

        filename, _ = QFileDialog.getOpenFileName(
            self, 'Open a SQLite3 File', startfile,
            ';;'.join((".sqlite3 files (*.sqlite3)",".db files (*.db)", "*.* (*)")))
        if not filename:
            return False

        if filename in self.recentFiles:
            self.recentFiles.remove(filename)
        self.recentFiles.insert(0, filename)

        self.populate_comboboxes()
        self.file_index = 0
        self.select_db_file()
        return True
    
    def select_db_file(self):
        """user selected a db file from the combo box"""
        if self.file_index > len(self.recentFiles) - 1:
            if not self.browse_db_file(True):
                return  # Cancelled
        elif self.file_index:
            self.recentFiles.insert(0, self.recentFiles.pop(self.file_index))
            self.file_index = 0
            self.populate_comboboxes()
        if self.recentFiles:
            self.dbfile = self.recentFiles[0]
            self.reload()

    def populate_comboboxes(self):
        self.filecombo.clear()
        for file in self.recentFiles or ("(None)",):
            self.filecombo.addItem(path.basename(file))
        self.filecombo.addItem("Browse SQLite3 Files...")
        self.filecombo.updateGeometry()
        
        
if __name__ == "__main__":
    WidgetPreview(OWSqlite3).run()
        