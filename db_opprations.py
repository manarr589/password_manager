import sqlite3

class DbOperations:
    def __init__(self):
        self.conn = sqlite3.connect("password_manager.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    ## Password manger table
    def create_table(self):
        """Creates the password table if it doesn't exist."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                website TEXT,
                                username TEXT,
                                password TEXT)''')
        self.conn.commit()
    
    ## Add Code
    def create_record(self, data):
        """Inserts a new record into the passwords table."""
        self.cursor.execute('''INSERT INTO passwords (website, username, password)
                               VALUES (?, ?, ?)''', (data['website'], data['username'], data['password']))
        self.conn.commit()
    
    ## Show Records Code
    def show_records(self):
        """Fetches all records from the passwords table."""
        self.cursor.execute('SELECT * FROM passwords')
        return self.cursor.fetchall()

    ## Update Code
    def update_record(self, data):
        """Updates an existing record in the passwords table."""
        self.cursor.execute('''UPDATE passwords SET website = ?, username = ?, password = ? 
                               WHERE id = ?''', (data['website'], data['username'], data['password'], data['id']))
        self.conn.commit()

    ## Delete Code
    def delete_record(self, record_id):
        """Deletes a record from the passwords table."""
        self.cursor.execute('DELETE FROM passwords WHERE id = ?', (record_id,))
        self.conn.commit()

    ## Search Code
    def search_records(self, website):
     """Searches for records by website name."""
     self.cursor.execute('SELECT * FROM passwords WHERE website LIKE ?', ('%' + website + '%',))
     return self.cursor.fetchall()
