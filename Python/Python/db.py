import sqlite3
import bcrypt

# --- Database Setup ---
DB_FILE = 'kiosk.db'

def get_db_connection():
    # Establishes and returns a connection to the database.
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row # Access columns by name
    return conn

def init_db():
    # Initializes the SQLite database and creates necessary tables.
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                assigned_stall TEXT NULL UNIQUE,
                applied_stall TEXT NULL,
                application_status TEXT NOT NULL DEFAULT 'none' -- none, pending, approved, declined
            )
        ''')

        # Add columns if they don't exist (for backward compatibility)
        try:
            cursor.execute("SELECT applied_stall FROM users LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE users ADD COLUMN applied_stall TEXT NULL")
            conn.commit()

        try:
            cursor.execute("SELECT application_status FROM users LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE users ADD COLUMN application_status TEXT NOT NULL DEFAULT 'none'")
            conn.commit()

        # Create stalls table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stalls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                image_path TEXT
            )
        ''')

        # Create items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NULL,
                image_path TEXT NULL,
                stall_id INTEGER NOT NULL,
                FOREIGN KEY (stall_id) REFERENCES stalls(id) ON DELETE CASCADE,
                UNIQUE(name, stall_id) -- Ensure item names are unique within a stall
            )
        ''')

        # Add columns if they don't exist (for backward compatibility)
        try:
            cursor.execute("SELECT description FROM items LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE items ADD COLUMN description TEXT NULL")
            conn.commit()

        try:
            cursor.execute("SELECT image_path FROM items LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE items ADD COLUMN image_path TEXT NULL")
            conn.commit()

        # Create item_variations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS item_variations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                size TEXT NOT NULL DEFAULT 'N/A',
                price REAL NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                UNIQUE(item_id, size), -- Ensure variation sizes are unique for an item
                FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
            )
        ''')

        # Create sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                expiry_time INTEGER NOT NULL,
                FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
            )
        ''')

        # Create orders table (for checkout history)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NULL, -- Allow NULL for guest orders
                username TEXT NULL, -- Allow NULL for guest orders
                order_time INTEGER NOT NULL,
                total_amount REAL NOT NULL
            )
        ''')

        # Create order_items table (for details of each order)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                item_name TEXT NOT NULL,
                item_size TEXT NOT NULL,
                item_price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                stall_name TEXT NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
            )
        ''')

        # Create default admin user if none exists
        cursor.execute('SELECT COUNT(*) FROM users WHERE role = ?', ('admin',))
        if cursor.fetchone()[0] == 0:
            admin_username = 'admin'
            admin_password = 'adminpass'
            hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                           (admin_username, hashed_password, 'admin'))
            conn.commit()

        conn.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def get_user_by_username(conn, username):
    # Retrieves a user's data by username.
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id, username, password_hash, role, assigned_stall, applied_stall, application_status FROM users WHERE username = ?', (username,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error getting user by username {username}: {e}")
        return None

def get_user_by_id(conn, user_id):
    # Retrieves a user's data by user ID.
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id, username, password_hash, role, assigned_stall, applied_stall, application_status FROM users WHERE id = ?', (user_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error getting user by id {user_id}: {e}")
        return None

def get_user_role(conn, username):
    # Retrieves a user's role by username.
    user = get_user_by_username(conn, username)
    return user['role'] if user else None

def get_user_assigned_stall(conn, username):
    # Retrieves the name of the stall assigned to a user.
    user = get_user_by_username(conn, username)
    # Only return assigned stall if the user is a 'user' role
    return user['assigned_stall'] if user and user['role'] == 'user' else None

def get_stall_by_name(conn, stall_name):
    # Retrieves a stall's data by name.
    if not stall_name:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id, name, description, image_path FROM stalls WHERE name = ?', (stall_name,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error getting stall by name {stall_name}: {e}")
        return None

def get_stall_by_id(conn, stall_id):
    # Retrieves a stall's data by ID.
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id, name, description, image_path FROM stalls WHERE id = ?', (stall_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error getting stall by id {stall_id}: {e}")
        return None

def is_stall_assigned(conn, stall_name, exclude_user_id=None):
    # Checks if a stall is currently assigned to any user, optionally excluding a specific user.
    if not stall_name:
        return False
    cursor = conn.cursor()
    try:
        query = 'SELECT COUNT(*) FROM users WHERE assigned_stall = ?'
        params = (stall_name,)
        if exclude_user_id is not None:
            query += ' AND id != ?'
            params += (exclude_user_id,)
        cursor.execute(query, params)
        count = cursor.fetchone()[0]
        return count > 0
    except Exception as e:
        print(f"Error checking if stall {stall_name} is assigned: {e}")
        return False
