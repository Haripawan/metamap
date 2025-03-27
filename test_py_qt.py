Let’s create a Python desktop application using PyQt (assuming “python flat” was meant to be “PyQt”) for your database table column mapping specification. Here’s a comprehensive solution:
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTableWidget, QPushButton, QComboBox, 
                            QLineEdit, QTableWidgetItem, QInputDialog, QMessageBox)
from PyQt5.QtCore import Qt

class ColumnMapper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Column Mapping Tool")
        self.setGeometry(100, 100, 1000, 600)
        
        # Sample data structure to store mappings
        self.mappings = {}
        self.source_tables = {
            "schema1.table1": ["col1", "col2", "col3"],
            "schema1.table2": ["col_a", "col_b", "col_c"],
            "schema2.table1": ["field1", "field2", "field3"]
        }
        self.target_columns = ["target_col1", "target_col2", "target_col3"]
        
        self.init_ui()

    def init_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Target columns table
        self.target_table = QTableWidget()
        self.target_table.setColumnCount(3)
        self.target_table.setHorizontalHeaderLabels(["Target Column", "Source Mapping", "Derivation"])
        self.update_target_table()
        layout.addWidget(self.target_table)

        # Control panel
        control_panel = QHBoxLayout()
        
        # Add mapping button
        self.add_btn = QPushButton("Add Mapping")
        self.add_btn.clicked.connect(self.add_mapping)
        control_panel.addWidget(self.add_btn)

        # Edit mapping button
        self.edit_btn = QPushButton("Edit Mapping")
        self.edit_btn.clicked.connect(self.edit_mapping)
        control_panel.addWidget(self.edit_btn)

        # Delete mapping button
        self.delete_btn = QPushButton("Delete Mapping")
        self.delete_btn.clicked.connect(self.delete_mapping)
        control_panel.addWidget(self.delete_btn)

        layout.addLayout(control_panel)

    def update_target_table(self):
        self.target_table.setRowCount(len(self.target_columns))
        for row, target_col in enumerate(self.target_columns):
            # Target column
            self.target_table.setItem(row, 0, QTableWidgetItem(target_col))
            
            # Source mapping
            mapping = self.mappings.get(target_col, {}).get("sources", [])
            mapping_str = ", ".join([f"{src}" for src in mapping])
            self.target_table.setItem(row, 1, QTableWidgetItem(mapping_str))
            
            # Derivation
            derivation = self.mappings.get(target_col, {}).get("derivation", "")
            self.target_table.setItem(row, 2, QTableWidgetItem(derivation))

    def add_mapping_dialog(self, target_col=None, edit_mode=False):
        dialog = QWidget()
        layout = QVBoxLayout(dialog)

        # Target column selection
        target_label = QLineEdit()
        target_combo = QComboBox()
        target_combo.addItems(self.target_columns)
        if target_col:
            target_combo.setCurrentText(target_col)
            target_combo.setEnabled(False) if edit_mode else target_combo.setEnabled(True)
        layout.addWidget(target_combo)

        # Source table.column selection
        source_combo = QComboBox()
        all_columns = []
        for table, columns in self.source_tables.items():
            for col in columns:
                all_columns.append(f"{table}.{col}")
        source_combo.addItems(all_columns)
        layout.addWidget(source_combo)

        # Derivation input
        derivation_input = QLineEdit()
        derivation_input.setPlaceholderText("Enter derivation logic (e.g., CONCAT, SUM, etc.)")
        if edit_mode and target_col in self.mappings:
            derivation_input.setText(self.mappings[target_col]["derivation"])
        layout.addWidget(derivation_input)

        # Buttons
        btn_layout = QHBoxLayout()
        add_source_btn = QPushButton("Add Another Source")
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        
        btn_layout.addWidget(add_source_btn)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        # Store selected sources
        selected_sources = [] if not edit_mode else self.mappings.get(target_col, {}).get("sources", [])
        
        def add_source():
            selected_sources.append(source_combo.currentText())
            source_combo.removeItem(source_combo.currentIndex())

        def save_mapping():
            target = target_combo.currentText()
            derivation = derivation_input.text()
            
            self.mappings[target] = {
                "sources": selected_sources if selected_sources else [source_combo.currentText()],
                "derivation": derivation
            }
            self.update_target_table()
            dialog.close()

        add_source_btn.clicked.connect(add_source)
        ok_btn.clicked.connect(save_mapping)
        cancel_btn.clicked.connect(dialog.close)

        dialog.setLayout(layout)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def add_mapping(self):
        self.add_mapping_dialog()

    def edit_mapping(self):
        selected_row = self.target_table.currentRow()
        if selected_row >= 0:
            target_col = self.target_table.item(selected_row, 0).text()
            self.add_mapping_dialog(target_col, edit_mode=True)
        else:
            QMessageBox.warning(self, "Warning", "Please select a target column to edit")

    def delete_mapping(self):
        selected_row = self.target_table.currentRow()
        if selected_row >= 0:
            target_col = self.target_table.item(selected_row, 0).text()
            if target_col in self.mappings:
                del self.mappings[target_col]
                self.update_target_table()
        else:
            QMessageBox.warning(self, "Warning", "Please select a mapping to delete")

def main():
    app = QApplication(sys.argv)
    window = ColumnMapper()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
This application provides:
	1	Main Interface:
	◦	A table displaying target columns, their source mappings, and derivations
	◦	Buttons for adding, editing, and deleting mappings
	2	Features:
	◦	View all target columns and their current mappings
	◦	Add new mappings with multiple source columns and derivation logic
	◦	Edit existing mappings
	◦	Delete mappings
	◦	Interactive dialog for mapping configuration
	3	Functionality:
	◦	Target columns are pre-defined (can be modified in target_columns)
	◦	Source columns come from multiple schema.tables (defined in source_tables)
	◦	Mappings are stored in a dictionary with source columns and derivation logic
	◦	Real-time table updates after any modification
To use this application:
	1	Install PyQt5:
pip install PyQt5
	2	Customize the data:
	•	Modify target_columns with your actual target table columns
	•	Update source_tables with your actual schema.table.column structure
	3	Run the application:
	•	The main window shows all target columns
	•	Click “Add Mapping” to create new mappings
	•	Select a row and click “Edit Mapping” to modify
	•	Select a row and click “Delete Mapping” to remove
The mapping data is stored in the mappings dictionary in this format:
{
    "target_col1": {
        "sources": ["schema1.table1.col1", "schema1.table2.col_a"],
        "derivation": "CONCAT"
    }
}
You can extend this by:
	•	Adding database connectivity to load actual schema
	•	Saving mappings to a file/database
	•	Adding validation rules
	•	Enhancing the UI with more styling
	•	Adding export functionality for the mapping specification
