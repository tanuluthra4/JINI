import sqlite3

def get_db_connection():
    conn = sqlite3.connect("jini.db")
    cursor = conn.cursor()
    return conn, cursor

conn, cursor = get_db_connection()

# System commands table (sample/demo data)
cursor.execute("CREATE TABLE IF NOT EXISTS sys_command (name TEXT, path TEXT)")
sys_commands = [
    ('chrome', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'),  # sample path
    ('notepad', 'notepad.exe'),
    ('vs code', 'C:\\Users\\User\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'),
    ('youtube', 'https://www.youtube.com/'),
    ('chatgpt', 'https://chat.openai.com/')
]

cursor.executemany("INSERT INTO sys_command VALUES (?, ?)", sys_commands)

# Contacts table (sample/demo data)
cursor.execute("CREATE TABLE IF NOT EXISTS contacts (name TEXT, phone TEXT)")
contacts = [
    ('Alice', '9999999999'),
    ('Bob', '8888888888'),
    ('Charlie', '777777777')
]

cursor.executemany("INSERT INTO contacts VALUES (?, ?)", contacts)

conn.commit()
conn.close()
