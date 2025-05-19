import uuid
import time
from http.cookies import SimpleCookie
from datetime import datetime
# Assuming db.py is in the same directory
from db import get_db_connection, get_user_by_username

# --- Session Management ---
SESSION_EXPIRY_SECONDS = 3600 # 1 hour

def create_session(conn, username):
    # Creates a new session for a user and returns the session ID.
    session_id = str(uuid.uuid4())
    expiry_time = int(time.time()) + SESSION_EXPIRY_SECONDS
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO sessions (session_id, username, expiry_time) VALUES (?, ?, ?)',
                       (session_id, username, expiry_time))
        conn.commit()
        return session_id
    except Exception as e:
        print(f"Error creating session for {username}: {e}")
        conn.rollback()
        return None

def get_username_from_session(conn, session_id):
    # Retrieves the username from a session ID if the session is valid and not expired.
    if not session_id:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT username, expiry_time FROM sessions WHERE session_id = ?', (session_id,))
        row = cursor.fetchone()
        if row:
            username, expiry_time = row
            if expiry_time > int(time.time()):
                return username
            else:
                # Session expired, delete it
                print(f"Session {session_id} expired. Deleting.")
                delete_session(conn, session_id)
        return None
    except Exception as e:
        print(f"Error getting username from session {session_id}: {e}")
        return None

def delete_session(conn, session_id):
    # Deletes a session from the database.
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
        conn.commit()
        print(f"Session {session_id} deleted.")
    except Exception as e:
        print(f"Error deleting session {session_id}: {e}")
        conn.rollback()

def get_current_user_from_request(request_headers):
    # Extracts session ID from headers and retrieves user info.
    cookies = SimpleCookie(request_headers.get('Cookie'))
    session_id = cookies['session_id'].value if 'session_id' in cookies else None

    if not session_id:
        return None, None, None

    conn = None
    try:
        conn = get_db_connection()
        username = get_username_from_session(conn, session_id)

        if username:
            user = get_user_by_username(conn, username)
            if user:
                return session_id, user['username'], user['role']
            else:
                # Invalid session (user not found), delete it
                print(f"get_current_user_from_request: User not found for session ID {session_id}. Deleting session.")
                delete_session(conn, session_id)
                return session_id, None, None
        else:
             # Session ID exists but is invalid or expired
             return session_id, None, None
    except Exception as e:
         print(f"Error in get_current_user_from_request: {e}")
         return session_id, None, None
    finally:
        if conn:
            conn.close()

