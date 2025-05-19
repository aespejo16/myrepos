import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import sqlite3
import sys

# --- Define the Color Palette ---
COLOR_BG_DARK = '#1a1a1a'         # Dark background
COLOR_BG_MEDIUM = '#2a2a2a'       # Slightly lighter background for frames/sections
COLOR_FG_GREEN_LIGHT = '#00ff00'  # Bright green for main text/accents
COLOR_FG_GREEN_DARK = '#00cc00'   # Slightly darker green
COLOR_FG_GREY = '#aaaaaa'         # Grey for secondary text (like file path)
COLOR_BORDER = '#006600'          # Darker green for borders/separators
COLOR_SELECT_BG = '#004400'       # Background for selected items
COLOR_SELECT_FG = COLOR_FG_GREEN_LIGHT # Text color for selected items

# --- Define Fonts ---
FONT_MONOSPACE = ('Consolas', 10) if sys.platform == 'win32' else ('Monospace', 10)
FONT_DEFAULT = ('Segoe UI', 10) if sys.platform == 'win32' else ('', 10)
FONT_STATUS = ('Segoe UI', 9) if sys.platform == 'win32' else ('', 9)


class ThemedSQLiteViewer:
    def __init__(self, root):
        self.root = root
        root.title("SQLite Database Viewer")
        root.configure(bg=COLOR_BG_DARK) # Set root window background

        # --- Configure ttk Styles ---
        style = ttk.Style()
        try:
            style.theme_use('alt') # Use a basic clean theme as a base
        except tk.TclError:
            print("Warning: 'alt' theme not available, using default.")

        # Configure general TFrame style
        style.configure('TFrame', background=COLOR_BG_MEDIUM)
        style.configure('TLabelFrame', background=COLOR_BG_MEDIUM, foreground=COLOR_FG_GREEN_LIGHT, font=FONT_DEFAULT)
        style.configure('TLabelframe.Label', background=COLOR_BG_MEDIUM, foreground=COLOR_FG_GREEN_LIGHT, font=FONT_DEFAULT)

        # Configure Labels
        style.configure('TLabel', background=COLOR_BG_MEDIUM, foreground=COLOR_FG_GREEN_LIGHT, font=FONT_DEFAULT)
        style.configure('Path.TLabel', background=COLOR_BG_MEDIUM, foreground=COLOR_FG_GREY, font=FONT_DEFAULT)

        # Configure Buttons
        style.configure('TButton',
                        background=COLOR_BORDER,
                        foreground=COLOR_FG_GREEN_LIGHT,
                        font=FONT_DEFAULT,
                        padding=(10, 5))
        style.map('TButton',
                  background=[('active', COLOR_FG_GREEN_DARK), ('pressed', COLOR_FG_GREEN_DARK)],
                  foreground=[('active', COLOR_BG_DARK)])

        # Configure Treeview (for both data and table list)
        style.configure('Treeview',
                        background=COLOR_BG_DARK,
                        foreground=COLOR_FG_GREEN_LIGHT,
                        fieldbackground=COLOR_BG_DARK,
                        bordercolor=COLOR_BORDER,
                        borderwidth=1,
                        rowheight=25)
        style.configure('Treeview.Heading',
                        background=COLOR_BORDER,
                        foreground=COLOR_FG_GREEN_LIGHT,
                        font=(FONT_DEFAULT[0], FONT_DEFAULT[1], 'bold'))
        style.map('Treeview',
                  background=[('selected', COLOR_SELECT_BG)],
                  foreground=[('selected', COLOR_SELECT_FG)])

        # Configure Scrollbars
        style.configure('Vertical.TScrollbar',
                        background=COLOR_BG_MEDIUM,
                        troughcolor=COLOR_BG_DARK,
                        bordercolor=COLOR_BORDER,
                        arrowcolor=COLOR_FG_GREEN_LIGHT)
        style.map('Vertical.TScrollbar',
                  background=[('active', COLOR_BORDER)],
                  arrowcolor=[('active', COLOR_FG_GREEN_DARK)])
        style.configure('Horizontal.TScrollbar',
                        background=COLOR_BG_MEDIUM,
                        troughcolor=COLOR_BG_DARK,
                        bordercolor=COLOR_BORDER,
                        arrowcolor=COLOR_FG_GREEN_LIGHT)
        style.map('Horizontal.TScrollbar',
                  background=[('active', COLOR_BORDER)],
                  arrowcolor=[('active', COLOR_FG_GREEN_DARK)])

        # Configure PanedWindow
        style.configure('TPanedwindow', background=COLOR_BG_DARK)
        style.configure('TPanedwindow.separator', background=COLOR_BORDER)


        # Configure root window grid weights for responsiveness
        root.grid_columnconfigure(0, weight=1) # Left pane (tables)
        root.grid_columnconfigure(1, weight=3) # Right pane (schema and data)
        root.grid_rowconfigure(0, weight=1)    # Main content area
        root.option_add('*tearOff', False)


        self.db_path = None
        self.conn = None
        self.cursor = None
        self.current_table = None


        # --- PanedWindow for Left/Right Split ---
        self.paned_window = ttk.PanedWindow(root, orient=tk.HORIZONTAL, style='TPanedwindow')
        self.paned_window.grid(row=0, column=0, columnspan=2, sticky=(tk.N, tk.S, tk.W, tk.E), padx=10, pady=10)

        # --- Left Pane: Table List (using Treeview) ---
        left_pane = ttk.Frame(self.paned_window, padding="10")
        self.paned_window.add(left_pane, weight=1)
        left_pane.grid_columnconfigure(0, weight=1)
        left_pane.grid_rowconfigure(1, weight=1)

        ttk.Label(left_pane, text="Tables:", style='TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        # Using Treeview configured as a Listbox
        self.table_treeview = ttk.Treeview(left_pane, show='tree', selectmode='browse', style='Treeview') # show='tree' hides headings, selectmode='browse' for single selection
        self.table_treeview.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W, tk.E), pady=5)
        self.table_treeview.bind('<<TreeviewSelect>>', self.on_table_select) # Bind to TreeviewSelect event

        # Scrollbars for the table Treeview
        table_list_vscroll = ttk.Scrollbar(left_pane, orient=tk.VERTICAL, command=self.table_treeview.yview, style='Vertical.TScrollbar')
        table_list_vscroll.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.table_treeview.configure(yscrollcommand=table_list_vscroll.set)


        # --- Right Pane: File Selection, Schema, and Data Views ---
        right_pane = ttk.Frame(self.paned_window, padding="10")
        self.paned_window.add(right_pane, weight=3)
        right_pane.grid_columnconfigure(0, weight=1)
        right_pane.grid_rowconfigure(1, weight=1)
        right_pane.grid_rowconfigure(2, weight=2)


        # --- File Selection and Path Display ---
        file_select_frame = ttk.Frame(right_pane)
        file_select_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        file_select_frame.grid_columnconfigure(0, weight=1)

        self.path_label = ttk.Label(file_select_frame, text="No database selected.", anchor=tk.W, style='Path.TLabel')
        self.path_label.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))

        self.select_button = ttk.Button(file_select_frame, text="Select Database", command=self.select_db_file, style='TButton')
        self.select_button.grid(row=0, column=1, sticky=tk.E)


        # --- Schema Details Frame ---
        schema_frame = ttk.LabelFrame(right_pane, text="Schema Details", padding="10")
        schema_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W, tk.E), pady=10)
        schema_frame.grid_columnconfigure(0, weight=1)
        schema_frame.grid_rowconfigure(0, weight=1)

        # Configure ScrolledText colors directly
        self.schema_text = scrolledtext.ScrolledText(schema_frame, wrap=tk.WORD, height=10, font=FONT_MONOSPACE,
                                                     bg=COLOR_BG_DARK, fg=COLOR_FG_GREEN_LIGHT,
                                                     insertbackground=COLOR_FG_GREEN_LIGHT, # Cursor color
                                                     bd=0, highlightthickness=0, relief=tk.FLAT)
        self.schema_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.schema_text.config(state=tk.DISABLED, padx=5, pady=5)


        # --- Data View Frame ---
        data_frame = ttk.LabelFrame(right_pane, text="Table Data", padding="10")
        data_frame.grid(row=2, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        data_frame.grid_columnconfigure(0, weight=1)
        data_frame.grid_rowconfigure(0, weight=1)

        # Treeview for data - using the styled Treeview
        self.data_treeview = ttk.Treeview(data_frame, show='headings', style='Treeview')
        self.data_treeview.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))

        # Use themed scrollbars for Treeview
        data_vscroll = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=self.data_treeview.yview, style='Vertical.TScrollbar')
        data_vscroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.data_treeview.configure(yscrollcommand=data_vscroll.set)

        data_hscroll = ttk.Scrollbar(data_frame, orient=tk.HORIZONTAL, command=self.data_treeview.xview, style='Horizontal.TScrollbar')
        data_hscroll.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.data_treeview.configure(xscrollcommand=data_hscroll.set)


        # --- Status Bar ---
        status_frame = ttk.Frame(root, relief=tk.FLAT, padding="5", style='TFrame')
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        # Configure status label color directly
        self.status_label = tk.Label(status_frame, text="Ready.", anchor=tk.W, font=FONT_STATUS,
                                      bg=COLOR_BG_MEDIUM, fg=COLOR_FG_GREEN_DARK)
        self.status_label.pack(fill=tk.X)

        # --- Initial state ---
        self.disable_widgets()
        root.geometry("1200x800")
        root.minsize(700, 500)


    def select_db_file(self):
        """Opens a file dialog for the user to select an SQLite database file."""
        file_path = filedialog.askopenfilename(
            initialdir=".",
            title="Select SQLite Database File",
            filetypes=(("SQLite Database Files", "*.db *.sqlite *.sqlite3"), ("All files", "*.*"))
        )

        if file_path:
            self.db_path = file_path
            self.path_label.config(text=f"Database: {self.db_path}")
            self.current_table = None
            if self.connect_db():
                self.populate_table_list()
                self.enable_widgets()
                self.update_schema_text("Database loaded successfully.\n\nSelect a table from the list on the left to view its schema and data.")
                self.clear_data_treeview()
                self.update_status("Database loaded. Select a table.")
            else:
                 self.update_status("Failed to load database.")


    def connect_db(self):
        """Connects to the selected SQLite database."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not connect to database:\n{e}")
            self.db_path = None
            self.path_label.config(text="No database selected.")
            self.disable_widgets()
            self.clear_table_list() # Clear table list Treeview
            self.update_schema_text("Error connecting to database.")
            self.clear_data_treeview()
            return False

    def populate_table_list(self):
        """Fetches table names from the database and populates the table Treeview."""
        self.clear_table_list() # Clear existing list
        if self.cursor:
            try:
                self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
                tables = self.cursor.fetchall()
                if tables:
                    for table in tables:
                        # Insert into Treeview, the item ID will be the table name
                        self.table_treeview.insert('', tk.END, text=table[0], iid=table[0])
                    self.update_status(f"Found {len(tables)} tables.")
                else:
                     self.update_schema_text("No tables found in this database.")
                     self.update_status("No tables found.")

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Could not fetch table names:\n{e}")
                self.update_schema_text("Error fetching table names.")
                self.update_status("Error fetching tables.")

    def clear_table_list(self):
         """Clears all items from the table list Treeview."""
         for item in self.table_treeview.get_children():
             self.table_treeview.delete(item)


    def on_table_select(self, event):
        """Event handler when a table is selected in the table Treeview."""
        selected_item_id = self.table_treeview.focus() # Get the ID of the focused (selected) item

        if not selected_item_id:
            # If selection is cleared
            if self.current_table is not None:
                 self.update_schema_text("Select a table to view its schema and data.")
                 self.clear_data_treeview()
                 self.current_table = None
                 self.update_status("Table selection cleared.")
            return

        # The item ID is the table name
        table_name = selected_item_id

        # Prevent reloading if the same table is clicked again
        if table_name == self.current_table:
            return

        self.current_table = table_name
        self.update_status(f"Loading data for table: '{table_name}'...")
        self.display_table_schema(table_name)
        self.display_table_data(table_name)
        # Status updated within display_table_data based on row count


    def display_table_schema(self, table_name):
        """Fetches and displays the schema for the selected table."""
        self.update_schema_text("") # Clear current schema

        if self.cursor:
            try:
                self.cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
                create_sql_row = self.cursor.fetchone()
                create_sql = create_sql_row[0] if create_sql_row else "N/A"

                schema_output = f"Table: {table_name}\n\n"
                schema_output += f"CREATE Statement:\n{create_sql}\n\n"

                self.cursor.execute(f"PRAGMA table_info('{table_name}');")
                columns = self.cursor.fetchall()
                if columns:
                    schema_output += "Column Details:\n"
                    schema_output += "{:<5} {:<25} {:<15} {:<8} {:<15} {:<5}\n".format(
                        "CID", "Name", "Type", "NotNull", "DefaultValue", "PK")
                    schema_output += "{:<5} {:<25} {:<15} {:<8} {:<15} {:<5}\n".format(
                        "---", "----", "----", "-------", "------------", "---")
                    for cid, name, type, notnull, dflt_value, pk in columns:
                         schema_output += "{:<5} {:<25} {:<15} {:<8} {:<15} {:<5}\n".format(
                             cid, name, type, bool(notnull), str(dflt_value) if dflt_value is not None else "NULL", bool(pk))
                else:
                    schema_output += "No column information available for this table.\n"

                self.update_schema_text(schema_output)


            except sqlite3.Error as e:
                self.update_schema_text(f"Error fetching schema for '{table_name}':\n{e}\n")
            except Exception as e:
                 self.update_schema_text(f"An unexpected error occurred while fetching schema for '{table_name}':\n{e}\n")


    def display_table_data(self, table_name):
        """Fetches and displays data for the selected table in the data Treeview."""
        self.clear_data_treeview()

        if self.cursor:
            try:
                self.cursor.execute(f"PRAGMA table_info('{table_name}');")
                columns_info = self.cursor.fetchall()
                column_names = [col[1] for col in columns_info]

                if not column_names:
                    self.update_schema_text(self.schema_text.get(1.0, tk.END).strip() + "\n\nTable has no columns, cannot display data.")
                    self.update_status(f"Table '{table_name}' has no columns.")
                    return

                self.data_treeview['columns'] = column_names
                self.data_treeview.column("#0", width=0, stretch=tk.NO)

                for col_name in column_names:
                    self.data_treeview.heading(col_name, text=col_name, anchor=tk.W)
                    self.data_treeview.column(col_name, width=150, minwidth=50, anchor=tk.W, stretch=tk.YES)

                limit = 5000
                self.cursor.execute(f"SELECT * FROM '{table_name}' LIMIT ?;", (limit,))
                rows = self.cursor.fetchall()

                if rows:
                    for row in rows:
                        formatted_row = tuple(str(cell) if cell is not None else "NULL" for cell in row)
                        self.data_treeview.insert("", tk.END, values=formatted_row)

                    total_rows = self.get_row_count(table_name)
                    if total_rows != "Unknown" and len(rows) < total_rows:
                         self.update_status(f"Displayed {len(rows)} of {total_rows} rows for table: '{table_name}'. (Display limit: {limit})")
                    else:
                         self.update_status(f"Displayed {len(rows)} rows for table: '{table_name}'.")

                else:
                    self.update_schema_text(self.schema_text.get(1.0, tk.END).strip() + "\n\nTable is empty. No data to display.")
                    self.update_status(f"Table '{table_name}' is empty.")

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Could not fetch data for table '{table_name}':\n{e}")
                self.update_schema_text(self.schema_text.get(1.0, tk.END).strip() + f"\n\nError fetching data: {e}")
                self.update_status(f"Error fetching data for '{table_name}'.")

            except Exception as e:
                 messagebox.showerror("Error", f"An unexpected error occurred while displaying data for '{table_name}':\n{e}")
                 self.update_schema_text(self.schema_text.get(1.0, tk.END).strip() + f"\n\nAn unexpected error occurred: {e}")
                 self.update_status(f"An unexpected error occurred for '{table_name}'.")

    def get_row_count(self, table_name):
         """Attempts to get the total row count for a table."""
         if self.cursor:
             try:
                 self.cursor.execute(f"SELECT COUNT(*) FROM '{table_name}';")
                 count = self.cursor.fetchone()[0]
                 return count
             except Exception:
                 return "Unknown"

    def clear_data_treeview(self):
        """Clears all data and columns from the data Treeview."""
        self.data_treeview["columns"] = ()
        for item in self.data_treeview.get_children():
            self.data_treeview.delete(item)

    def update_schema_text(self, text):
        """Updates the schema text area."""
        self.schema_text.config(state=tk.NORMAL)
        self.schema_text.delete(1.0, tk.END)
        self.schema_text.insert(tk.END, text)
        self.schema_text.config(state=tk.DISABLED)

    def update_status(self, message):
        """Updates the status bar message."""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def enable_widgets(self):
        """Enables UI widgets after a database is loaded."""
        # Enable the table list Treeview
        self.table_treeview.state(['!disabled']) # ttk widgets use state lists

    def disable_widgets(self):
        """Disables UI widgets when no database is loaded."""
        # Disable the table list Treeview
        self.table_treeview.state(['disabled'])
        self.clear_table_list()
        self.clear_data_treeview()
        self.update_schema_text("Select a database file to begin.")
        self.path_label.config(text="No database selected.")
        self.update_status("Ready.")
        self.current_table = None


    def on_closing(self):
        """Handles closing the window, ensuring the database connection is closed."""
        if self.conn:
            self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ThemedSQLiteViewer(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()