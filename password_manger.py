import sqlite3
from cryptography.fernet import Fernet
import pyperclip
from tkinter import CENTER, END, Tk, Label, Entry, Button, Frame, ttk
from db_opprations import DbOperations  # Ensure this is correctly imported

class root_window:
    
    def __init__(self, root, db):
        self.db = db
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("900x550+40+40")
        # Secret key for encryption (you should store this securely)
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

        head_title = Label(self.root, text="Password Manager", width=40, bg="white",fg="#57a1f8", font=("Calibri(Body)",20,"bold"), padx=10, pady=10, justify=CENTER, anchor="center").grid(columnspan=4, padx=140, pady=20)

        self.crud_frame = Frame(self.root, bg="white", highlightthickness=1, padx=10, pady=30)
        self.crud_frame.grid()
        self.create_entry_labels()
        self.create_entry_boxes()
        self.create_crud_buttons()

        # Entry for search input
        self.search_entry = Entry(self.crud_frame, width=30)
        self.search_entry.grid(row=self.row_no + 1, column=self.col_no, padx=5, pady=5)

        # Search button
        Button(self.crud_frame, text="Search", bg='#57a1f8', fg='white', font=("Calibri(Body)", 12), padx=2, pady=1, width=15, command=self.search_record).grid(row=self.row_no + 1, column=self.col_no + 1, padx=5, pady=10)

        # Create Treeview to show records
        self.create_records_tree()
        self.records_tree.bind('<<TreeviewSelect>>', self.on_record_select)
        # Adjust grid placement to replace Listbox
        self.records_tree.grid(row=self.row_no + 2, columnspan=4, padx=10, pady=10)

        # Store the actual password when needed
        self.actual_password = ""

    def create_entry_labels(self):
        self.col_no, self.row_no = 0, 0
        Labels_info = ('ID', 'Website', 'Username', 'Password')
        for label_info in Labels_info:
            Label(self.crud_frame, text=label_info, bg='white', fg='black', font=("Calibri(Body)", 15), padx=5, pady=2).grid(row=self.row_no, column=self.col_no, padx=5, pady=2)
            self.col_no += 1

    def create_crud_buttons(self):
        self.col_no = 0
        self.row_no += 1
        buttons_info = (('Save', '#57a1f8', self.save_record),
                        ('Delete', '#57a1f8', self.delete_record),
                        ('Copy Password', '#57a1f8', self.copy_password),
                        ('Show All Records', '#57a1f8', self.show_records),
                        ('Update', '#57a1f8', self.update_record) ,
                        ('Clear All', '#57a1f8', self.clear))
        for btn_info in buttons_info:
            if btn_info[0] == 'Show All Records':
                self.row_no += 1
                self.col_no = 0
            Button(self.crud_frame, text=btn_info[0], bg=btn_info[1], fg='white', font=("Calibri(Body)", 12), padx=2, pady=1, width=15, command=btn_info[2]).grid(row=self.row_no, column=self.col_no, padx=5, pady=10)
            self.col_no += 1

    def create_entry_boxes(self):
        self.row_no += 1
        self.entry_boxes = []
        self.col_no = 0
        for i in range(4):
            show = ""
            if i == 3:
                show = "*"  
            entry_boxes = Entry(self.crud_frame, width=20, background="lightgray", font=("Arial", 12), show=show)
            entry_boxes.grid(row=self.row_no, column=self.col_no, padx=5, pady=2)
            self.col_no += 1
            self.entry_boxes.append(entry_boxes)

    def create_records_tree(self):
        columns = ['ID', 'Website', 'Username','password']
        self.records_tree = ttk.Treeview(self.root, columns=columns, show='headings')

        for col in columns:
            self.records_tree.heading(col, text=col)
            self.records_tree.column(col, width=200 if col != 'ID' else 50)

    def save_record(self):
        website = self.entry_boxes[1].get()
        username = self.entry_boxes[2].get()
        password = self.entry_boxes[3].get()

        # Store the actual password in a variable (for copying)
        self.actual_password = password

        if website and username and password:
            self.db.create_record({'website': website, 'username': username, 'password': password})
            print("Record saved.")
            self.show_records()
        else:
            print("Please fill in all fields.")

    def delete_record(self):
        selected_item = self.records_tree.selection()
        if selected_item:
            record_id = self.records_tree.item(selected_item)['values'][0]
            self.db.delete_record(record_id)
            print(f"Record {record_id} deleted.")
            self.show_records()
        else:
            print("Please select a record to delete.")

    def update_record(self):
        record_id = self.entry_boxes[0].get()
        website = self.entry_boxes[1].get()
        username = self.entry_boxes[2].get()
        password = self.entry_boxes[3].get()

        # Update the actual password in the variable
        self.actual_password = password

        if record_id and website and username and password:
            self.db.update_record({'id': record_id, 'website': website, 'username': username, 'password': password})
            print(f"Record {record_id} updated.")
            self.show_records()
        else:
            print("Please fill in all fields.")
    def encrypt_password(self, password):
        """Encrypt the password using the provided key."""
        encrypted_password = self.cipher_suite.encrypt(password.encode())
        return encrypted_password

    def copy_password(self):
     '''Copy the plain password from the entry field to the clipboard.'''
     password = self.entry_boxes[3].get()  # Get the password from the Entry field
     if password:
        pyperclip.copy(password)  # Copy the plain password to clipboard
        print("Password copied to clipboard.")
     else:
        print("No password to copy.")

    def show_records(self):
        records = self.db.show_records()
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        for record in records:
            # Show actual password in the Treeview (unmasked)
            self.records_tree.insert('', 'end', values=(record[0], record[1], record[2], record[3]))  # Actual password (unmasked)

    def search_record(self):
        website = self.search_entry.get()
        records = self.db.search_records(website)
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        for record in records:
            self.records_tree.insert('', 'end', values=record)
    def clear(self):
    # Clear all the entry boxes
       for entry in self.entry_boxes:
        entry.delete(0, 'end')

      

    def on_record_select(self, event):
        selected_item = self.records_tree.selection()  # Get selected item
        if selected_item:
            # Retrieve the record's data
            record = self.records_tree.item(selected_item)['values']
            record_id, website, username, password = record  # Unpack the data
            
            # Populate the fields with the selected record's data
            self.entry_boxes[0].delete(0, END)  # Clear ID field
            self.entry_boxes[0].insert(0, record_id)  # Set ID

            self.entry_boxes[1].delete(0, END)  # Clear website field
            self.entry_boxes[1].insert(0, website)  # Set website

            self.entry_boxes[2].delete(0, END)  # Clear username field
            self.entry_boxes[2].insert(0, username)  # Set username

            self.entry_boxes[3].delete(0, END)  # Clear password field
            self.entry_boxes[3].insert(0, password)  # Set password (masked)
            self.actual_password = password  # Save the actual password

# Main Program
if __name__ == "__main__":
    db = DbOperations()  # Create the DbOperations object
    root = Tk()
    app = root_window(root, db)  # Pass the DbOperations object to the GUI class
    root.mainloop()
