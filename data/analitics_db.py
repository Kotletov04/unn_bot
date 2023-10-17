import sqlite3




class Bot_DB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()



    def add_name(self, user_id, name, time, button):
        self.cursor.execute("""create table if not exists users(user_id INT, name VARCHAR(30), button VARCHAR(30), time INT);""")
        self.cursor.execute("INSERT INTO users (user_id, name, time, button) VALUES (?, ?, ?, ?) ;", (user_id, name, time, button))
        return self.conn.commit()
    
    def close(self):
        
        self.connection.close()
