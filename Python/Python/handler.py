# from http.server import SimpleHTTPRequestHandler
# from urllib.parse import unquote, parse_qs, urlencode
# import os
# import time
# import uuid
# from datetime import datetime
# from http.cookies import SimpleCookie
# # Assuming db.py, session.py, and html_generator.py are in the same directory
# from db import get_db_connection, get_user_by_username, get_user_by_id, is_stall_assigned, get_stall_by_name, get_stall_by_id, get_user_assigned_stall
# from session import get_current_user_from_request, create_session, delete_session
# from html_generator import get_first_page, get_choice_page, get_second_page, get_stall_page, get_cart_page, get_receipt_page, get_login_page, get_admin_dashboard, get_user_dashboard, get_error_page
# import bcrypt
# import sqlite3 # Import sqlite3 for specific error handling

# # Session expiry seconds (defined here for use in handler)
# SESSION_EXPIRY_SECONDS = 3600 # 1 hour

# class MyHandler(SimpleHTTPRequestHandler):
#     # Class-level dictionary to store carts, keyed by session_id or "guest"
#     # This cart is in-memory and will be reset when the server restarts.
#     # For persistence, a database table for carts would be needed.
#     cart = {}
#     # In-memory storage for receipt data, keyed by session_id or "guest"
#     # This is temporary and will be lost on server restart or after viewing.
#     receipt_data = {}

#     def get_session_id(self):
#         # Extracts the session ID from the request cookies.
#         # This is now handled in session.py's get_current_user_from_request,
#         # but keeping this helper for potential direct cookie access if needed.
#         cookies = SimpleCookie(self.headers.get('Cookie'))
#         if 'session_id' in cookies:
#             return cookies['session_id'].value
#         return None

#     def get_current_user(self):
#         # Gets the current user's session ID, username, and role using the session module.
#         return get_current_user_from_request(self.headers)

#     def handle_redirect(self, location='/', query_params=None):
#         # Helper to send a 303 redirect with optional query parameters.
#         if query_params:
#             # Ensure query parameters are URL-encoded
#             # Use urlencode to handle spaces and special characters in values
#             encoded_params = urlencode(query_params)
#             # Append query parameters to the location, handling existing ones
#             if '?' in location:
#                 location += '&' + encoded_params
#             else:
#                 location += '?' + encoded_params

#         self.send_response(303)
#         self.send_header('Location', location)
#         self.end_headers()

#     def do_GET(self):
#         # Handles GET requests.
#         session_id, username, role = self.get_current_user()

#         if self.path == '/' or self.path.startswith('/?'):
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             self.wfile.write(bytes(get_first_page(username), 'utf-8'))
#         elif self.path == '/choice' or self.path.startswith('/choice?'):
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             self.wfile.write(bytes(get_choice_page(username), 'utf-8'))
#         elif self.path == '/second' or self.path.startswith('/second?'):
#             # Determine the cart key for the current user/guest
#             cart_key = session_id if session_id else "guest"
#             current_cart_items = self.cart.get(cart_key, [])
#             cart_item_count = sum(item['quantity'] for item in current_cart_items)

#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             self.wfile.write(bytes(get_second_page(username, role, cart_item_count), 'utf-8'))
#         elif self.path == '/stalls':
#             # Redirecting /stalls to /second (the stalls listing page)
#             self.handle_redirect('/second')
#         elif self.path.startswith('/stall/'):
#             # Handle individual stall pages (customer view)
#             parts = self.path.split('/')
#             # Ensure there are enough parts in the path and the third part is not empty
#             if len(parts) >= 3 and parts[2]:
#                 # Extract and decode stall name directly from the path segment
#                 # Handle potential query params after name
#                 stall_name = unquote(parts[2].split('?')[0])

#                 conn = None
#                 stall_data_row = None
#                 try:
#                     conn = get_db_connection()
#                     # Retrieve stall data from the database
#                     stall_data_row = get_stall_by_name(conn, stall_name)
#                 except Exception as e:
#                     print(f"Error fetching stall data for /stall/: {e}")
#                 finally:
#                     if conn:
#                         conn.close()

#                 if stall_data_row:
#                     # Convert row to dictionary for easier access
#                     stall_data = dict(stall_data_row)
#                     self.send_response(200)
#                     self.send_header('Content-type', 'text/html')
#                     self.end_headers()
#                     # Serve the stall page with its items
#                     self.wfile.write(bytes(get_stall_page(
#                         stall_data, username, role), 'utf-8'))
#                 else:
#                     # Stall not found, serve generic 404 page
#                     self.send_response(404)
#                     self.send_header('Content-type', 'text/html')
#                     self.end_headers()
#                     self.wfile.write(bytes(get_error_page(
#                         "Stall Not Found", "The requested stall could not be found."), 'utf-8'))
#             else:
#                  # Invalid stall path format, serve generic 404 page
#                  self.send_response(404)
#                  self.send_header('Content-type', 'text/html')
#                  self.end_headers()
#                  self.wfile.write(bytes(get_error_page(
#                      "Not Found", "Invalid stall path format."), 'utf-8'))
#         elif self.path == '/cart' or self.path.startswith('/cart?'):
#             # Determine the cart key
#             cart_key = session_id if session_id else "guest"
#             user_cart = self.cart.get(cart_key, [])

#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             self.wfile.write(bytes(get_cart_page(user_cart), 'utf-8'))

#         elif self.path.startswith('/receipt/'):
#              # Handle receipt page request
#              parts = self.path.split('/')
#              if len(parts) >= 3 and parts[2]:
#                   # Get receipt ID from path
#                   receipt_id = parts[2].split('?')[0]
#                   # Retrieve receipt data from in-memory storage
#                   receipt_data = self.receipt_data.get(receipt_id)

#                   if receipt_data:
#                        self.send_response(200)
#                        self.send_header('Content-type', 'text/html')
#                        self.end_headers()
#                        self.wfile.write(
#                            bytes(get_receipt_page(receipt_data), 'utf-8'))
#                   else:
#                        # Receipt not found
#                        self.send_response(404)
#                        self.send_header('Content-type', 'text/html')
#                        self.end_headers()
#                        self.wfile.write(bytes(get_error_page(
#                            "Receipt Not Found", "The requested receipt could not be found."), 'utf-8'))
#              else:
#                   # Invalid receipt path format
#                   self.send_response(404)
#                   self.send_header('Content-type', 'text/html')
#                   self.end_headers()
#                   self.wfile.write(bytes(get_error_page(
#                       "Not Found", "Invalid receipt path format."), 'utf-8'))

#         elif self.path == '/login.html' or self.path.startswith('/login.html?'):
#             # Redirect logged-in users away from the login page
#             if username:
#                 conn = None
#                 user = None
#                 try:
#                     conn = get_db_connection()
#                     user = get_user_by_username(conn, username)
#                 except Exception as e:
#                     print(f"Error getting user in login.html redirect: {e}")
#                 finally:
#                     if conn:
#                         conn.close()

#                 if user and user['role'] == 'admin':
#                     # Redirect admin to admin dashboard
#                     self.handle_redirect('/admin')
#                 elif user and user['role'] == 'user':
#                      # Redirect user to user dashboard
#                      self.handle_redirect('/user_dashboard')
#                 else:
#                     # Default redirect if role is unexpected
#                     self.handle_redirect('/')
#                 return  # Stop processing GET request

#             # Serve the login/register page if not logged in
#             query_params = parse_qs(self.path.split('?')[-1]) if '?' in self.path else {}
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             self.wfile.write(bytes(get_login_page(query_params), 'utf-8'))

#         elif self.path == '/admin' or self.path.startswith('/admin?'):
#             # Restrict access to admin dashboard
#             # Re-check username and role after get_current_user()
#             if not username or role != 'admin':
#                 print(f"Access to /admin denied. Username: {username}, Role: {role}")
#                 self.send_response(403) # Forbidden
#                 self.send_header('Content-type', 'text/html')
#                 self.end_headers()
#                 self.wfile.write(bytes(get_error_page(
#                     "Forbidden", "You must be logged in as an admin to view this page."), 'utf-8'))
#                 return  # Stop processing GET request

#             conn = None
#             users = []
#             stalls = []
#             items_by_stall = {}

#             try:
#                 conn = get_db_connection()
#                 cursor = conn.cursor()

#                 # Fetch all users
#                 cursor.execute('SELECT id, username, role, assigned_stall, applied_stall, application_status FROM users')
#                 users = cursor.fetchall()

#                 # Fetch all stalls
#                 cursor.execute('SELECT id, name, description, image_path FROM stalls')
#                 stalls = cursor.fetchall()

#                 # Fetch all items grouped by stall for admin view
#                 # Fetch all items first
#                 cursor.execute('SELECT i.id, i.name AS item_name, i.description, i.image_path, s.name AS stall_name, s.id AS stall_id FROM items i JOIN stalls s ON i.stall_id = s.id ORDER BY s.name, i.name')
#                 all_items = cursor.fetchall()

#                 # Group items by stall name
#                 for item in all_items:
#                     stall_name = item['stall_name']
#                     if stall_name not in items_by_stall:
#                         items_by_stall[stall_name] = []
#                     items_by_stall[stall_name].append(item)

#             except Exception as e:
#                 print(f"Error fetching data for admin dashboard: {e}")
#                 self.send_response(500)
#                 self.send_header('Content-type', 'text/html')
#                 self.end_headers()
#                 self.wfile.write(bytes(get_error_page(
#                     "Internal Server Error", f"An error occurred fetching admin data: {e}"), 'utf-8'))
#                 return
#             finally:
#                 if conn:
#                     conn.close()

#             # Serve the admin dashboard
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             self.wfile.write(bytes(get_admin_dashboard(users, stalls, items_by_stall), 'utf-8'))

#         elif self.path == '/user_dashboard' or self.path.startswith('/user_dashboard?'):
#             # Restrict access to user dashboard
#             # Re-check username and role after get_current_user()
#             if not username or role != 'user':
#                 print(f"Access to /user_dashboard denied. Username: {username}, Role: {role}")
#                 self.send_response(403) # Forbidden
#                 self.send_header('Content-type', 'text/html')
#                 self.end_headers()
#                 self.wfile.write(bytes(get_error_page(
#                     "Forbidden", "You must be logged in as a user to view this page."), 'utf-8'))
#                 return  # Stop processing GET request

#             conn = None
#             user = None
#             try:
#                 conn = get_db_connection()
#                 # Get user data for the dashboard
#                 user = get_user_by_username(conn, username)
#             except Exception as e:
#                 print(f"Error getting user for user dashboard: {e}")
#                 self.send_response(500)
#                 self.send_header('Content-type', 'text/html')
#                 self.end_headers()
#                 self.wfile.write(bytes(get_error_page(
#                     "Internal Server Error", f"An error occurred fetching user data: {e}"), 'utf-8'))
#                 return
#             finally:
#                 if conn:
#                     conn.close()

#             if user:
#                 # Serve the user dashboard
#                 self.send_response(200)
#                 self.send_header('Content-type', 'text/html')
#                 self.end_headers()
#                 self.wfile.write(bytes(get_user_dashboard(user), 'utf-8'))
#             else:
#                  # User not found (shouldn't happen if get_current_user returns username, but defensive)
#                  self.send_response(404)
#                  self.send_header('Content-type', 'text/html')
#                  self.end_headers()
#                  self.wfile.write(bytes(get_error_page(
#                      "User Not Found", "Your user account could not be found."), 'utf-8'))

#         elif self.path == '/style.css':
#             # Serve the CSS file
#             self.send_response(200)
#             self.send_header('Content-type', 'text/css')
#             self.end_headers()
#             try:
#                 with open('style.css', 'rb') as f:
#                     self.wfile.write(f.read())
#             except FileNotFoundError:
#                 self.send_response(404) # CSS file not found
#                 self.send_header('Content-type', 'text/html')
#                 self.end_headers()
#                 self.wfile.write(bytes(get_error_page(
#                     "Not Found", "The requested CSS file was not found."), 'utf-8'))
#         elif self.path.startswith('/firstpageimg/') or self.path.startswith('/secondpageimg/') or self.path.startswith('/stall_images/'):
#             # Serve image files from specific directories
#             try:
#                 file_path = self.path[1:] # Remove leading slash
#                 if os.path.exists(file_path):
#                      with open(file_path, 'rb') as f:
#                         self.send_response(200)
#                         # Guess the MIME type based on file extension
#                         self.send_header('Content-type', self.guess_type(self.path))
#                         self.end_headers()
#                         self.wfile.write(f.read())
#                 else:
#                     self.send_response(404) # Image file not found
#                     self.send_header('Content-type', 'text/html')
#                     self.end_headers()
#                     self.wfile.write(bytes(get_error_page(
#                         "Image Not Found", "The requested image was not found."), 'utf-8'))
#             except Exception as e:
#                 # Log any errors during file serving
#                 print(f"Error serving file {self.path}: {e}")
#                 self.send_response(500) # Internal Server Error
#                 self.send_header('Content-type', 'text/html')
#                 self.end_headers()
#                 self.wfile.write(bytes(get_error_page(
#                     "Internal Server Error", f"An error occurred while serving the file: {e}"), 'utf-8'))
#         else:
#             # Handle any other unknown GET requests by serving the generic 404 page
#             self.send_response(404) # Not Found
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             self.wfile.write(bytes(get_error_page(
#                 "Not Found", "The requested URL was not found on this server."), 'utf-8'))

#     def do_POST(self):
#         # Handles POST requests.
#         # Get current user information
#         session_id, username, role = self.get_current_user()
#         conn = None # Initialize conn to None

#         try:
#             # Read the content of the POST request
#             content_length = int(self.headers['Content-Length'])
#             post_data = self.rfile.read(content_length).decode('utf-8')
#             # Parse the form data
#             form_data = parse_qs(post_data)

#             conn = get_db_connection() # Get database connection inside the try block
#             cursor = conn.cursor() # Get cursor here

#             # --- Handle different POST actions ---
#             if self.path == '/add_to_cart':
#                 item_variation_id = form_data.get('item_variation_id', [''])[0]
#                 # Default quantity to 1 if not provided or invalid
#                 quantity_str = form_data.get('quantity', ['1'])[0]
#                 try:
#                     quantity = int(quantity_str)
#                 except ValueError:
#                     # Handle invalid quantity input gracefully
#                     self.handle_redirect(self.headers.get('Referer', '/second'), query_params={'error': 'invalid_quantity'})
#                     return

#                 # Validate input
#                 if not item_variation_id or quantity <= 0:
#                      self.handle_redirect(self.headers.get('Referer', '/second'), query_params={'error': 'invalid_input'})
#                      return

#                 # Retrieve item variation details
#                 cursor.execute('''
#                     SELECT iv.id, iv.size, iv.price, iv.stock, i.name AS item_name, s.name AS stall_name
#                     FROM item_variations iv
#                     JOIN items i ON iv.item_id = i.id
#                     JOIN stalls s ON i.stall_id = s.id
#                     WHERE iv.id = ?
#                 ''', (item_variation_id,))
#                 variation_data = cursor.fetchone()

#                 if not variation_data:
#                      # Item variation not found
#                      self.handle_redirect(self.headers.get('Referer', '/second'), query_params={'error': 'item_not_found'})
#                      return

#                 # Convert row to dictionary
#                 variation_data = dict(variation_data)

#                 # Check if enough stock is available
#                 if variation_data['stock'] < quantity:
#                      # Redirect back to the stall page with an out-of-stock error
#                      # Correctly format the stall URL
#                      stall_url = f"/stall/{urlencode({'': variation_data['stall_name']}).replace('%3D', '')}"
#                      self.handle_redirect(stall_url, query_params={'error': 'out_of_stock', 'item': variation_data['item_name'], 'size': variation_data['size']})
#                      return

#                 # Decrease stock immediately when added to cart
#                 cursor.execute('UPDATE item_variations SET stock = stock - ? WHERE id = ?', (quantity, item_variation_id))
#                 conn.commit()

#                 # Determine the cart key (session ID for logged in, "guest" otherwise)
#                 cart_key = session_id if session_id else "guest"
#                 if cart_key not in self.cart:
#                     # Initialize cart if it doesn't exist
#                     self.cart[cart_key] = []

#                 found_item = None
#                 # Check if the item variation is already in the cart
#                 for item in self.cart[cart_key]:
#                      if item['item_variation_id'] == variation_data['id']:
#                          found_item = item
#                          break

#                 if found_item:
#                     # If found, increase the quantity
#                     found_item['quantity'] += quantity
#                 else:
#                     # If not found, add the new item variation to the cart
#                     self.cart[cart_key].append({
#                         "item_variation_id": variation_data['id'],
#                         "quantity": quantity,
#                         "name": variation_data['item_name'],
#                         "size": variation_data['size'],
#                         "price": variation_data['price'],
#                         "stall": variation_data['stall_name']
#                     })

#                 # Redirect back to the stall page with a success message
#                 # Correctly format the stall URL
#                 stall_url = f"/stall/{urlencode({'': variation_data['stall_name']}).replace('%3D', '')}"
#                 self.handle_redirect(stall_url, query_params={'success': 'added_to_cart'})

#             elif self.path == '/checkout':
#                 # Handle checkout process
#                 cart_key = session_id if session_id else "guest"
#                 user_cart = self.cart.get(cart_key, [])

#                 if not user_cart:
#                      # Cart is empty, redirect to cart page with error
#                      self.handle_redirect('/cart', query_params={'error': 'cart_empty'})
#                      return

#                 total_amount = sum(item['quantity'] * item['price'] for item in user_cart)

#                 # Record the order in the database
#                 cursor.execute('INSERT INTO orders (session_id, username, order_time, total_amount) VALUES (?, ?, ?, ?)',
#                                (session_id, username, int(time.time()), total_amount))
#                 order_id = cursor.lastrowid # Get the ID of the newly created order

#                 # Record order items
#                 for item in user_cart:
#                      cursor.execute('INSERT INTO order_items (order_id, item_name, item_size, item_price, quantity, stall_name) VALUES (?, ?, ?, ?, ?, ?)',
#                                     (order_id, item['name'], item['size'], item['price'], item['quantity'], item['stall']))

#                      # Note: Stock is now decreased when adding to cart, so no stock update here.

#                 conn.commit()

#                 # Store receipt data in memory for retrieval
#                 # Generate a unique ID for the receipt URL
#                 receipt_id = str(uuid.uuid4())
#                 self.receipt_data[receipt_id] = {
#                     'order_id': order_id,
#                     'order_time': datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'),
#                     'customer': username if username else 'Guest',
#                     'items': user_cart,
#                     'total_amount': total_amount
#                 }

#                 # Clear the user's cart after successful checkout
#                 if cart_key in self.cart:
#                     del self.cart[cart_key]

#                 # Redirect to the receipt page
#                 self.handle_redirect(f'/receipt/{receipt_id}')

#             elif self.path == '/login':
#                 username_attempt = form_data.get('username', [''])[0]
#                 password_attempt = form_data.get('password', [''])[0]

#                 try:
#                     # Retrieve user by username
#                     user = get_user_by_username(conn, username_attempt)

#                     if user:
#                         # Verify the password using bcrypt
#                         if bcrypt.checkpw(password_attempt.encode('utf-8'), user['password_hash'].encode('utf-8')):
#                             # Create a new session upon successful login
#                             new_session_id = create_session(conn, user['username'])
#                             self.send_response(303) # See Other
#                             # Redirect based on user role
#                             redirect_location = '/admin' if user['role'] == 'admin' else '/user_dashboard'
#                             self.send_header('Location', redirect_location)
#                             # Set the session cookie
#                             self.send_header('Set-Cookie', f'session_id={new_session_id}; HttpOnly; Path=/; Max-Age={SESSION_EXPIRY_SECONDS}')
#                             self.end_headers()
#                         else:
#                             # Redirect back to login with an error message
#                             self.handle_redirect('/login.html', query_params={'error': 'incorrect_password'})
#                     else:
#                         # Redirect back to login with an error message
#                         self.handle_redirect('/login.html', query_params={'error': 'account_not_found'})

#                 except Exception as e:
#                     # Log any errors during the login process
#                     print(f"Error during login process for {username_attempt}: {e}")
#                     self.send_response(500) # Internal Server Error
#                     self.send_header('Content-type', 'text/html')
#                     self.end_headers()
#                     self.wfile.write(bytes(get_error_page(
#                         "Internal Server Error", f"An internal server error occurred during login: {e}"), 'utf-8'))

#             elif self.path == '/register':
#                 reg_username = form_data.get('reg_username', [''])[0]
#                 reg_password = form_data.get('reg_password', [''])[0]
#                 # Optional stall application during registration or re-application
#                 apply_stall_name = form_data.get('apply_stall', [''])[0] or None

#                 # Basic validation
#                 if not reg_username or not reg_username.strip() or not reg_password or not reg_password.strip():
#                     self.handle_redirect('/login.html', query_params={'reg_status': 'missing_fields', 'register': 'true'})
#                     return

#                 # Check if username already exists
#                 existing_user = get_user_by_username(conn, reg_username.strip())

#                 if existing_user:
#                     # --- Handle Re-application for Declined Users ---
#                     # Check if the user is a 'user' role and their application was declined
#                     if existing_user['role'] == 'user' and existing_user['application_status'] == 'declined':
#                         if apply_stall_name:
#                             # Check if the applied stall exists
#                             stall = get_stall_by_name(conn, apply_stall_name)
#                             if stall:
#                                 # Check if the stall is already assigned to another user
#                                 if is_stall_assigned(conn, apply_stall_name):
#                                      # Redirect back to user dashboard with error
#                                      self.handle_redirect('/user_dashboard', query_params={'error': 'reapply_stall_assigned'})
#                                      return # Stop processing

#                                 # Update existing user's application status and applied stall
#                                 cursor.execute('UPDATE users SET applied_stall = ?, application_status = "pending" WHERE id = ?',
#                                                (apply_stall_name, existing_user['id']))
#                                 conn.commit()
#                                 # Redirect to user dashboard with success message
#                                 self.handle_redirect('/user_dashboard', query_params={'success': 'reapplied'})
#                                 return # Stop processing
#                             else:
#                                 # Applied stall not found
#                                 self.handle_redirect('/user_dashboard', query_params={'error': 'reapply_stall_not_found'})
#                                 return # Stop processing
#                         else:
#                              # Missing stall name for re-application
#                              self.handle_redirect('/user_dashboard', query_params={'error': 'reapply_missing_stall'})
#                              return # Stop processing
#                     else:
#                         # Username already exists and is not a declined user re-applying
#                         self.handle_redirect('/login.html', query_params={'reg_status': 'exists', 'register': 'true'})
#                         return # Stop processing

#                 # --- Handle New Registration ---
#                 # Hash the password for new registration
#                 hashed_password = bcrypt.hashpw(reg_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

#                 initial_role = 'user'
#                 initial_status = 'none'
#                 if apply_stall_name:
#                     # Check if the applied stall exists for new registration
#                     stall = get_stall_by_name(conn, apply_stall_name)
#                     if stall:
#                         # Check if the stall is already assigned to another user
#                         if is_stall_assigned(conn, apply_stall_name):
#                              # Redirect back to login with error
#                              self.handle_redirect('/login.html', query_params={'reg_status': 'stall_assigned', 'register': 'true'})
#                              return # Stop processing

#                         # Set status to pending if applying for a valid, unassigned stall
#                         initial_status = 'pending'
#                     else:
#                         apply_stall_name = None # Clear applied stall if it doesn't exist

#                 # Insert the new user into the database
#                 try:
#                     cursor.execute('INSERT INTO users (username, password_hash, role, applied_stall, application_status) VALUES (?, ?, ?, ?, ?)',
#                                    (reg_username.strip(), hashed_password, initial_role, apply_stall_name, initial_status))
#                     conn.commit()

#                     # Create a session for the newly registered user
#                     new_session_id = create_session(conn, reg_username.strip())

#                     self.send_response(303) # See Other
#                     # Redirect to user dashboard after registration
#                     self.send_header('Location', '/user_dashboard')
#                     # Set the session cookie
#                     self.send_header('Set-Cookie', f'session_id={new_session_id}; HttpOnly; Path=/; Max-Age={SESSION_EXPIRY_SECONDS}')
#                     self.end_headers()
#                 except sqlite3.IntegrityError as e:
#                     print(f"Integrity Error during registration: {e}")
#                     conn.rollback() # Rollback changes in case of error
#                     self.handle_redirect('/login.html', query_params={'reg_status': 'integrity_error', 'register': 'true'})
#                 except Exception as e:
#                     print(f"General Error during registration: {e}")
#                     conn.rollback() # Rollback changes
#                     self.handle_redirect('/login.html', query_params={'reg_status': 'general_error', 'register': 'true'})


#             elif self.path == '/logout':
#                  # Handle user logout
#                  if session_id:
#                      delete_session(conn, session_id) # Delete the session
#                      self.send_response(303) # See Other
#                      self.send_header('Location', '/') # Redirect to home page
#                      # Expire the session cookie
#                      self.send_header('Set-Cookie', 'session_id=; Max-Age=0; Path=/')
#                      self.end_headers()
#                  else:
#                      # If no session, just redirect to home
#                      self.handle_redirect('/')

#             # --- Admin User Management Actions ---
#             elif self.path == '/admin/add_user' and role == 'admin':
#                  # Restrict to admin role
#                  new_username = form_data.get('new_username', [''])[0]
#                  new_password = form_data.get('new_password', [''])[0]
#                  new_role = form_data.get('new_role', ['user'])[0]
#                  new_assigned_stall = form_data.get('new_assigned_stall', [''])[0] or None

#                  # Basic validation
#                  if not new_username or not new_username.strip() or not new_password or not new_password.strip():
#                       self.handle_redirect('/admin', query_params={'error': 'add_user_missing'})
#                       return

#                  # Check if username already exists
#                  existing_user = get_user_by_username(conn, new_username.strip())
#                  if existing_user:
#                      self.handle_redirect('/admin', query_params={'error': 'add_user_exists'})
#                      return

#                  # Check if the stall is already assigned if trying to assign one
#                  if new_assigned_stall and is_stall_assigned(conn, new_assigned_stall):
#                      self.handle_redirect('/admin', query_params={'error': 'assign_stall_assigned'})
#                      return

#                  # Hash the password
#                  hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#                  try:
#                      # Insert the new user
#                      cursor.execute('INSERT INTO users (username, password_hash, role, assigned_stall, application_status) VALUES (?, ?, ?, ?, ?)',
#                                     (new_username.strip(), hashed_password, new_role, new_assigned_stall, 'none'))
#                      conn.commit()
#                      # Redirect with success message
#                      self.handle_redirect('/admin', query_params={'success': 'add_user'})
#                  except sqlite3.IntegrityError as e:
#                       print(f"Integrity Error adding user (Admin): {e}")
#                       conn.rollback()
#                       self.handle_redirect('/admin', query_params={'error': 'add_user_integrity_error'})
#                  except Exception as e:
#                       print(f"General Error adding user (Admin): {e}")
#                       conn.rollback()
#                       self.handle_redirect('/admin', query_params={'error': 'add_user_general_error'})

#             elif self.path == '/admin/remove_user' and role == 'admin':
#                  # Restrict to admin role
#                  user_id_to_remove = form_data.get('user_id', [''])[0]
#                  if user_id_to_remove:
#                      # Prevent removing the default admin user
#                      user_to_remove = get_user_by_id(conn, user_id_to_remove)
#                      if user_to_remove and user_to_remove['username'] == 'admin':
#                          self.handle_redirect('/admin', query_params={'error': 'remove_admin_forbidden'})
#                          return

#                      try:
#                           # Delete the user by ID
#                           cursor.execute('DELETE FROM users WHERE id = ?', (user_id_to_remove,))
#                           conn.commit()
#                           # Redirect with success message
#                           self.handle_redirect('/admin', query_params={'success': 'remove_user'})
#                      except Exception as e:
#                           print(f"Error removing user (Admin): {e}")
#                           conn.rollback()
#                           self.handle_redirect('/admin', query_params={'error': 'remove_user_error'})

#                  else:
#                       # Missing user ID
#                       self.handle_redirect('/admin', query_params={'error': 'remove_user_missing_id'})

#             elif self.path == '/admin/update_user_assignment' and role == 'admin':
#                  # Restrict to admin role
#                  user_id = form_data.get('user_id', [''])[0]
#                  new_assigned_stall = form_data.get('assigned_stall', [''])[0] or None

#                  # Basic validation
#                  if not user_id:
#                       self.handle_redirect('/admin', query_params={'error': 'update_user_missing_id'})
#                       return

#                  # Get user to update
#                  user_to_update = get_user_by_id(conn, user_id)
#                  if not user_to_update:
#                      self.handle_redirect('/admin', query_params={'error': 'update_user_notfound'})
#                      return

#                  # Prevent updating the default admin user's assignment
#                  if user_to_update['username'] == 'admin':
#                      self.handle_redirect('/admin', query_params={'error': 'update_admin_forbidden'})
#                      return

#                  # Check if the new assigned stall is already assigned to another user
#                  if new_assigned_stall and is_stall_assigned(conn, new_assigned_stall, exclude_user_id=user_to_update['id']):
#                      self.handle_redirect('/admin', query_params={'error': 'assign_stall_assigned'})
#                      return

#                  try:
#                      # Update the assigned stall and reset application status if assigned
#                      if new_assigned_stall:
#                          # If assigning a stall, set status to approved and clear applied_stall
#                          cursor.execute('UPDATE users SET assigned_stall = ?, applied_stall = NULL, application_status = "approved" WHERE id = ?', (new_assigned_stall, user_id))
#                      else:
#                           # If unassigning, clear assigned_stall and set status to none
#                           cursor.execute('UPDATE users SET assigned_stall = NULL, applied_stall = NULL, application_status = "none" WHERE id = ?', (user_id,))

#                      conn.commit()
#                      # Redirect with success message
#                      self.handle_redirect('/admin', query_params={'success': 'update_user_assignment'})
#                  except Exception as e:
#                      print(f"Error updating user assignment (Admin): {e}")
#                      conn.rollback()
#                      self.handle_redirect('/admin', query_params={'error': 'update_user_assignment_error'})

#             # --- Admin Application Management Actions ---
#             elif self.path == '/admin/approve_application' and role == 'admin':
#                  # Restrict to admin role
#                  user_id = form_data.get('user_id', [''])[0]
#                  if user_id:
#                      # Get user and check application status
#                      user = get_user_by_id(conn, user_id)
#                      if user and user['application_status'] == 'pending' and user['applied_stall']:
#                          # Check if the applied stall is already assigned to another user
#                          if is_stall_assigned(conn, user['applied_stall']):
#                               self.handle_redirect('/admin', query_params={'error': 'application_stall_assigned'})
#                               return # Stop processing

#                          try:
#                              # Assign the stall and update status
#                              cursor.execute('UPDATE users SET assigned_stall = ?, applied_stall = NULL, application_status = "approved" WHERE id = ?', (user['applied_stall'], user_id))
#                              conn.commit()
#                              # Redirect with success message including stall name
#                              self.handle_redirect('/admin', query_params={'success': 'application_approved', 'stall_name': user['applied_stall']})
#                          except Exception as e:
#                               # Log and handle errors during approval
#                               print(f"Error approving application for user {user['username']}: {e}")
#                               self.handle_redirect('/admin', query_params={'error': 'application_approve_error'})
#                      else:
#                           # Application is not pending or missing applied stall
#                           self.handle_redirect('/admin', query_params={'error': 'application_not_pending'})
#                  else:
#                      # Missing user ID
#                      self.handle_redirect('/admin', query_params={'error': 'application_missing_user_id'})

#             elif self.path == '/admin/decline_application' and role == 'admin':
#                  # Restrict to admin role
#                  user_id = form_data.get('user_id', [''])[0]
#                  if user_id:
#                      # Get user and check application status
#                      user = get_user_by_id(conn, user_id)
#                      if user and user['application_status'] == 'pending':
#                          try:
#                              # Update application status to declined
#                              # Also clear applied_stall on decline
#                              cursor.execute('UPDATE users SET application_status = "declined", applied_stall = NULL WHERE id = ?', (user_id,))
#                              conn.commit()
#                              # Redirect with success message
#                              self.handle_redirect('/admin', query_params={'success': 'application_declined'})
#                          except Exception as e:
#                              # Log and handle errors during decline
#                              print(f"Error declining application for user {user['username']}: {e}")
#                              self.handle_redirect('/admin', query_params={'error': 'application_decline_error'})
#                      else:
#                          # Application is not pending
#                          self.handle_redirect('/admin', query_params={'error': 'application_not_pending'})
#                  else:
#                      # Missing user ID
#                      self.handle_redirect('/admin', query_params={'error': 'application_missing_user_id'})

#             # --- Item Management Actions (User - Assigned Stall & Admin) ---
#             # Note: Admin can also use these endpoints to manage items directly on stall pages
#             elif self.path == '/user/add_item_main' and (role == 'user' or role == 'admin'):
#                  # Restrict to user role (assigned stall) or admin
#                  stall_name = form_data.get('stall_name', [''])[0]
#                  item_name = form_data.get('item_name', [''])[0]
#                  description = form_data.get('description', [''])[0]
#                  image_path = form_data.get('image_path', [''])[0] or None # Optional image path
#                  first_variation_size = form_data.get('first_variation_size', [''])[0] or 'N/A'
#                  first_variation_price_str = form_data.get('first_variation_price', [''])[0]
#                  first_variation_stock_str = form_data.get('first_variation_stock', ['0'])[0]

#                  # Get stall data to get stall ID and verify existence
#                  stall = get_stall_by_name(conn, stall_name)
#                  if not stall:
#                       # Stall not found, redirect with error
#                       # Determine the correct redirect location based on role
#                       redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                       self.handle_redirect(redirect_url, query_params={'error': 'stall_not_found'})
#                       return # Stop processing

#                  # Check authorization for user role
#                  if role == 'user':
#                      assigned_stall = get_user_assigned_stall(conn, username)
#                      if assigned_stall != stall_name:
#                           self.send_response(403) # Forbidden
#                           self.send_header('Content-type', 'text/html')
#                           self.end_headers()
#                           self.wfile.write(bytes(get_error_page(
#                               "Forbidden", "You are not authorized to add items to this stall."), 'utf-8'))
#                           return # Stop processing

#                  # Basic validation
#                  if not item_name or not item_name.strip() or not first_variation_price_str:
#                      # Determine the correct redirect location based on role
#                      redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                      self.handle_redirect(redirect_url, query_params={'error': 'add_item_missing_fields'})
#                      return

#                  try:
#                      # Convert price and stock to appropriate types
#                      first_variation_price = float(first_variation_price_str)
#                      first_variation_stock = int(first_variation_stock_str)
#                      if first_variation_price < 0 or first_variation_stock < 0:
#                           # Determine the correct redirect location based on role
#                           redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                           self.handle_redirect(redirect_url, query_params={'error': 'add_item_invalid_price_stock'})
#                           return
#                  except ValueError:
#                       # Handle invalid number formats
#                       # Determine the correct redirect location based on role
#                       redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                       self.handle_redirect(redirect_url, query_params={'error': 'add_item_invalid_price_stock'})
#                       return

#                  try:
#                      # Check if item name already exists in this stall
#                      existing_item = cursor.execute('SELECT id FROM items WHERE name = ? AND stall_id = ?', (item_name.strip(), stall['id'])).fetchone()
#                      if existing_item:
#                           # Determine the correct redirect location based on role
#                           redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                           self.handle_redirect(redirect_url, query_params={'error': 'add_item_exists_in_stall'})
#                           return

#                      # Insert the main item
#                      cursor.execute('INSERT INTO items (name, description, image_path, stall_id) VALUES (?, ?, ?, ?)',
#                                     (item_name.strip(), description.strip() if description else None, image_path.strip() if image_path else None, stall['id']))
#                      item_id = cursor.lastrowid # Get the ID of the newly inserted item

#                      # Insert the first variation for the item
#                      # Check if the first variation size already exists for this new item (shouldn't happen, but defensive)
#                      existing_variation = cursor.execute('SELECT id FROM item_variations WHERE item_id = ? AND size = ?', (item_id, first_variation_size.strip())).fetchone()
#                      if existing_variation:
#                           print(f"Warning: Duplicate size '{first_variation_size}' found for new item ID {item_id} during initial add.")
#                           # Rollback the item insert if variation insert would fail due to duplicate size
#                           conn.rollback() # Added rollback
#                           # Determine the correct redirect location based on role
#                           redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                           self.handle_redirect(redirect_url, query_params={'error': 'add_item_initial_variation_exists'})
#                           return

#                      cursor.execute('INSERT INTO item_variations (item_id, size, price, stock) VALUES (?, ?, ?, ?)',
#                                     (item_id, first_variation_size.strip(), first_variation_price, first_variation_stock))
#                      conn.commit()
#                      # Redirect with success message
#                      # Determine the correct redirect location based on role
#                      redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                      self.handle_redirect(redirect_url, query_params={'success': 'add_item'})
#                  except sqlite3.IntegrityError as e:
#                       # Handle database integrity errors (e.g., stall_id not found)
#                       print(f"Integrity Error adding item/variation (User/Admin): {e}")
#                       conn.rollback() # Rollback changes in case of error
#                       # Determine the correct redirect location based on role
#                       redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                       self.handle_redirect(redirect_url, query_params={'error': 'add_item_integrity_error'})
#                  except Exception as e:
#                       # Handle other general errors
#                       print(f"General Error adding item/variation (User/Admin): {e}")
#                       conn.rollback() # Rollback changes
#                       # Determine the correct redirect location based on role
#                       redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                       self.handle_redirect(redirect_url, query_params={'error': 'add_item_general_error'})

#             elif self.path == '/user/add_item_variation' and (role == 'user' or role == 'admin'):
#                  # Restrict to user role (assigned stall) or admin
#                  item_id = form_data.get('item_id', [''])[0]
#                  size = form_data.get('size', [''])[0] or 'N/A'
#                  price_str = form_data.get('price', [''])[0]
#                  stock_str = form_data.get('stock', ['0'])[0]

#                  # Get the stall name and stall ID associated with the item
#                  cursor.execute('SELECT s.name, s.id FROM items i JOIN stalls s ON i.stall_id = s.id WHERE i.id = ?', (item_id,))
#                  item_stall_row = cursor.fetchone()
#                  if not item_stall_row:
#                       # Item not found, redirect with error
#                       # Determine the correct redirect location based on role
#                       redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                       self.handle_redirect(redirect_url, query_params={'error': 'item_not_found'})
#                       return
#                  item_stall_name = item_stall_row['name']
#                  item_stall_id = item_stall_row['id']

#                  # Check authorization for user role
#                  if role == 'user':
#                       assigned_stall = get_user_assigned_stall(conn, username)
#                       if assigned_stall != item_stall_name:
#                            self.send_response(403) # Forbidden
#                            self.send_header('Content-type', 'text/html')
#                            self.end_headers()
#                            self.wfile.write(bytes(get_error_page(
#                                "Forbidden", "You are not authorized to add variations to items in this stall."), 'utf-8'))
#                            return # Stop processing

#                  # Basic validation
#                  if not item_id or not price_str:
#                      # Determine the correct redirect location based on role
#                      redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                      self.handle_redirect(redirect_url, query_params={'error': 'add_variation_missing_fields'})
#                      return

#                  try:
#                      # Convert price and stock to appropriate types
#                      price = float(price_str)
#                      stock = int(stock_str)
#                      if price < 0 or stock < 0:
#                           # Determine the correct redirect location based on role
#                           redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                           self.handle_redirect(redirect_url, query_params={'error': 'add_variation_invalid_price_stock'})
#                           return
#                  except ValueError:
#                       # Handle invalid number formats
#                       # Determine the correct redirect location based on role
#                       redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                       self.handle_redirect(redirect_url, query_params={'error': 'add_variation_invalid_price_stock'})
#                       return

#                  try:
#                      # Check if variation size already exists for this item
#                      existing_variation = cursor.execute('SELECT id FROM item_variations WHERE item_id = ? AND size = ?', (item_id, size.strip())).fetchone()
#                      if existing_variation:
#                           # Determine the correct redirect location based on role
#                           redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                           self.handle_redirect(redirect_url, query_params={'error': 'add_variation_exists'})
#                           return

#                      # Insert the new variation
#                      cursor.execute('INSERT INTO item_variations (item_id, size, price, stock) VALUES (?, ?, ?, ?)',
#                                     (item_id, size.strip(), price, stock))
#                      conn.commit()
#                      # Redirect with success message
#                      # Determine the correct redirect location based on role
#                      redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                      self.handle_redirect(redirect_url, query_params={'success': 'add_variation'})
#                  except sqlite3.IntegrityError as e:
#                       # Handle database integrity errors (e.g., item_id not found)
#                       print(f"Integrity Error adding variation (User/Admin): {e}")
#                       conn.rollback() # Rollback changes
#                       # Determine the correct redirect location based on role
#                       redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                       self.handle_redirect(redirect_url, query_params={'error': 'add_variation_integrity_error'})
#                  except Exception as e:
#                       # Handle other general errors
#                       print(f"General Error adding variation (User/Admin): {e}")
#                       conn.rollback() # Rollback changes
#                       # Determine the correct redirect location based on role
#                       redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                       self.handle_redirect(redirect_url, query_params={'error': 'add_variation_general_error'})

#             elif self.path == '/user/remove_item_main' and (role == 'user' or role == 'admin'):
#                  # Restrict to user role (assigned stall) or admin
#                  item_id_to_remove = form_data.get('item_id', [''])[0]
#                  if item_id_to_remove:
#                       # Get the stall name associated with the item
#                       cursor.execute('SELECT s.name FROM items i JOIN stalls s ON i.stall_id = s.id WHERE i.id = ?', (item_id_to_remove,))
#                       item_stall_row = cursor.fetchone()
#                       if not item_stall_row:
#                            # Item not found, redirect with error
#                            # Determine the correct redirect location based on role
#                            redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                            self.handle_redirect(redirect_url, query_params={'error': 'item_not_found'})
#                            return
#                       item_stall_name = item_stall_row['name']

#                       # Check authorization for user role
#                       if role == 'user':
#                           assigned_stall = get_user_assigned_stall(conn, username)
#                           if assigned_stall != item_stall_name:
#                                self.send_response(403) # Forbidden
#                                self.send_header('Content-type', 'text/html')
#                                self.end_headers()
#                                self.wfile.write(bytes(get_error_page(
#                                    "Forbidden", "You are not authorized to remove items from this stall."), 'utf-8'))
#                                return # Stop processing

#                       try:
#                           # Delete the item (ON DELETE CASCADE handles variations)
#                           cursor.execute('DELETE FROM items WHERE id = ?', (item_id_to_remove,))
#                           conn.commit()
#                           # Redirect with success message
#                           # Determine the correct redirect location based on role
#                           redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                           self.handle_redirect(redirect_url, query_params={'success': 'remove_item'})
#                       except Exception as e:
#                            print(f"Error removing item (User/Admin): {e}")
#                            conn.rollback()
#                            redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                            self.handle_redirect(redirect_url, query_params={'error': 'remove_item_error'})

#                  else:
#                       # Missing item ID, redirect with error
#                       # Determine the correct redirect location based on role
#                       redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                       self.handle_redirect(redirect_url, query_params={'error': 'remove_item_missing_id'})


#             elif self.path == '/remove_item_main_customer':
#                  # Handle removing an item directly from the customer stall page
#                  item_id_to_remove = form_data.get('item_id', [''])[0]
#                  stall_name = form_data.get('stall_name', [''])[0]

#                  if not item_id_to_remove or not stall_name:
#                       # Missing item ID or stall name
#                       self.handle_redirect(f'/stall/{urlencode({" ": stall_name}).replace("%3D", "")}', query_params={'error': 'remove_item_missing_info'})
#                       return

#                  # Check authorization: Only assigned user or admin can remove from customer view
#                  if not username or (role == 'user' and get_user_assigned_stall(conn, username) != stall_name) or role not in ['user', 'admin']:
#                       self.send_response(403) # Forbidden
#                       self.send_header('Content-type', 'text/html')
#                       self.end_headers()
#                       self.wfile.write(bytes(get_error_page(
#                           "Forbidden", "You are not authorized to remove items from this stall."), 'utf-8'))
#                       return # Stop processing


#                  try:
#                      # Delete the item (ON DELETE CASCADE handles variations)
#                      cursor.execute('DELETE FROM items WHERE id = ?', (item_id_to_remove,))
#                      conn.commit()
#                      # Redirect back to the stall page
#                      self.handle_redirect(f'/stall/{urlencode({" ": stall_name}).replace("%3D", "")}', query_params={'success': 'remove_item'})
#                  except Exception as e:
#                      print(f"Error removing item from customer view: {e}")
#                      conn.rollback()
#                      self.handle_redirect(f'/stall/{urlencode({" ": stall_name}).replace("%3D", "")}', query_params={'error': 'remove_item_error'})


#             elif self.path == '/user/remove_item_variation' and (role == 'user' or role == 'admin'):
#                  # Restrict to user role (assigned stall) or admin
#                  variation_id_to_remove = form_data.get('variation_id', [''])[0]
#                  if variation_id_to_remove:
#                      # Get the stall name and item ID associated with the variation's item
#                      cursor.execute('SELECT s.name, iv.item_id FROM item_variations iv JOIN items i ON iv.item_id = i.id JOIN stalls s ON i.stall_id = s.id WHERE iv.id = ?', (variation_id_to_remove,))
#                      item_stall_row = cursor.fetchone()
#                      if not item_stall_row:
#                           # Variation not found, redirect with error
#                           # Determine the correct redirect location based on role
#                           redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                           self.handle_redirect(redirect_url, query_params={'error': 'variation_not_found'})
#                           return
#                      item_stall_name = item_stall_row['name']
#                      item_id = item_stall_row['item_id']

#                      # Check authorization for user role
#                      if role == 'user':
#                           assigned_stall = get_user_assigned_stall(conn, username)
#                           if assigned_stall != item_stall_name:
#                                self.send_response(403) # Forbidden
#                                self.send_header('Content-type', 'text/html')
#                                self.end_headers()
#                                self.wfile.write(bytes(get_error_page(
#                                    "Forbidden", "You are not authorized to remove variations from items in this stall."), 'utf-8'))
#                                return # Stop processing

#                      try:
#                           # Delete the item variation by ID
#                           cursor.execute('DELETE FROM item_variations WHERE id = ?', (variation_id_to_remove,))
#                           conn.commit()

#                           # After deleting the variation, check if the parent item has any variations left
#                           cursor.execute('SELECT COUNT(*) FROM item_variations WHERE item_id = ?', (item_id,))
#                           remaining_variations_count = cursor.fetchone()[0]

#                           if remaining_variations_count == 0:
#                               # If no variations left, remove the parent item
#                               print(f"Item ID {item_id} has no variations left. Removing item.")
#                               cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
#                               conn.commit()
#                               # Redirect with success message for item removal
#                               # Determine the correct redirect location based on role
#                               redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                               self.handle_redirect(redirect_url, query_params={'success': 'remove_item_no_variations'})
#                           else:
#                               # Redirect with success message for variation removal
#                               # Determine the correct redirect location based on role
#                               redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                               self.handle_redirect(redirect_url, query_params={'success': 'remove_variation'})

#                      except Exception as e:
#                           print(f"Error removing variation (User/Admin): {e}")
#                           conn.rollback()
#                           redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                           self.handle_redirect(redirect_url, query_params={'error': 'remove_variation_error'})

#                  else:
#                      # Missing variation ID, redirect with error
#                      # Determine the correct redirect location based on role
#                      redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                      self.handle_redirect(redirect_url, query_params={'error': 'remove_variation_missing_id'})


#             elif self.path == '/user/update_item_variation' and (role == 'user' or role == 'admin'):
#                  # Restrict to user role (assigned stall) or admin
#                  variation_id = form_data.get('variation_id', [''])[0]
#                  # Use None as default to distinguish missing fields from empty strings
#                  new_size = form_data.get('new_size', [None])[0]
#                  new_price_str = form_data.get('new_price', [None])[0]
#                  new_stock_str = form_data.get('new_stock', [None])[0]

#                  if not variation_id:
#                      # Missing variation ID, redirect with error
#                      # Determine the correct redirect location based on role
#                      redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                      self.handle_redirect(redirect_url, query_params={'error': 'update_variation_missing_id'})
#                      return

#                  # Get the stall name and item ID associated with the variation
#                  cursor.execute('SELECT s.name, iv.item_id FROM item_variations iv JOIN items i ON iv.item_id = i.id JOIN stalls s ON i.stall_id = s.id WHERE iv.id = ?', (variation_id,))
#                  item_stall_row = cursor.fetchone()
#                  if not item_stall_row:
#                       # Variation not found, redirect with error
#                       # Determine the correct redirect location based on role
#                       redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                       self.handle_redirect(redirect_url, query_params={'error': 'variation_not_found'})
#                       return
#                  item_stall_name = item_stall_row['name']
#                  item_id = item_stall_row['item_id']

#                  # Check authorization for user role
#                  if role == 'user':
#                       assigned_stall = get_user_assigned_stall(conn, username)
#                       if assigned_stall != item_stall_name:
#                            self.send_response(403) # Forbidden
#                            self.send_header('Content-type', 'text/html')
#                            self.end_headers()
#                            self.wfile.write(bytes(get_error_page(
#                                "Forbidden", "You are not authorized to update variations for items in this stall."), 'utf-8'))
#                            return # Stop processing

#                  update_fields = []
#                  update_values = []

#                  # Update size if provided and different
#                  if new_size is not None:
#                      updated_size = new_size.strip() if new_size else 'N/A'
#                      # Check for duplicate size for this item
#                      existing_variation_with_size = cursor.execute('SELECT id FROM item_variations WHERE item_id = ? AND size = ? AND id != ?', (item_id, updated_size, variation_id)).fetchone()
#                      if existing_variation_with_size:
#                           # Determine the correct redirect location based on role
#                           redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                           self.handle_redirect(redirect_url, query_params={'error': 'update_variation_size_exists'})
#                           return

#                      update_fields.append('size = ?')
#                      update_values.append(updated_size)

#                  # Update price if provided
#                  if new_price_str is not None:
#                       try:
#                           new_price = float(new_price_str)
#                           if new_price < 0:
#                                # Determine the correct redirect location based on role
#                                redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                                self.handle_redirect(redirect_url, query_params={'error': 'update_variation_invalid_price'})
#                                return
#                           update_fields.append('price = ?')
#                           update_values.append(new_price)
#                       except ValueError:
#                            # Handle invalid price format
#                            # Determine the correct redirect location based on role
#                            redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                            self.handle_redirect(redirect_url, query_params={'error': 'update_variation_invalid_price'})
#                            return

#                  # Update stock if provided
#                  if new_stock_str is not None:
#                      try:
#                          new_stock = int(new_stock_str)
#                          if new_stock < 0:
#                               # Determine the correct redirect location based on role
#                               redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                               self.handle_redirect(redirect_url, query_params={'error': 'update_variation_invalid_stock'})
#                               return
#                          update_fields.append('stock = ?')
#                          update_values.append(new_stock)
#                      except ValueError:
#                           # Handle invalid stock format
#                           # Determine the correct redirect location based on role
#                           redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                           self.handle_redirect(redirect_url, query_params={'error': 'update_variation_invalid_stock'})
#                           return

#                  if update_fields:
#                      update_query = f"UPDATE item_variations SET {', '.join(update_fields)} WHERE id = ?"
#                      update_values.append(variation_id)
#                      try:
#                          cursor.execute(update_query, tuple(update_values))
#                          conn.commit()
#                          # Redirect with success message
#                          # Determine the correct redirect location based on role
#                          redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                          self.handle_redirect(redirect_url, query_params={'success': 'update_variation'})
#                      except sqlite3.IntegrityError as e:
#                           print(f"Integrity Error updating variation (User/Admin): {e}")
#                           conn.rollback()
#                           redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                           self.handle_redirect(redirect_url, query_params={'error': 'update_variation_integrity_error'})
#                      except Exception as e:
#                           print(f"General Error updating variation (User/Admin): {e}")
#                           conn.rollback()
#                           redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                           self.handle_redirect(redirect_url, query_params={'error': 'update_variation_general_error'})
#                  else:
#                      # No changes made, just redirect to the dashboard
#                      redirect_url = '/user_dashboard' if role == 'user' else '/admin'
#                      self.handle_redirect(redirect_url)

#             # --- Stall Management Actions (Admin Only) ---
#             elif self.path == '/admin/add_stall' and role == 'admin':
#                 # Restrict to admin role
#                 stall_name = form_data.get('stall_name', [''])[0]
#                 description = form_data.get('description', [''])[0]
#                 image_path = form_data.get('image_path', [''])[0] or None

#                 # Basic validation
#                 if not stall_name or not stall_name.strip():
#                     self.handle_redirect('/admin', query_params={'error': 'add_stall_missing_name'})
#                     return

#                 # Check if stall name already exists
#                 existing_stall = get_stall_by_name(conn, stall_name.strip())
#                 if existing_stall:
#                     self.handle_redirect('/admin', query_params={'error': 'add_stall_exists'})
#                     return

#                 try:
#                     # Insert the new stall
#                     cursor.execute('INSERT INTO stalls (name, description, image_path) VALUES (?, ?, ?)',
#                                    (stall_name.strip(), description.strip() if description else None, image_path.strip() if image_path else None))
#                     conn.commit()
#                     # Redirect with success message
#                     self.handle_redirect('/admin', query_params={'success': 'add_stall'})
#                 except sqlite3.IntegrityError as e:
#                     print(f"Integrity Error adding stall (Admin): {e}")
#                     conn.rollback()
#                     self.handle_redirect('/admin', query_params={'error': 'add_stall_integrity_error'})
#                 except Exception as e:
#                     print(f"General Error adding stall (Admin): {e}")
#                     conn.rollback()
#                     self.handle_redirect('/admin', query_params={'error': 'add_stall_general_error'})


#             elif self.path == '/admin/remove_stall' and role == 'admin':
#                 # Restrict to admin role
#                 stall_id_to_remove = form_data.get('stall_id', [''])[0]
#                 if stall_id_to_remove:
#                     try:
#                         # Check if any user is assigned to this stall before removing
#                         cursor.execute('SELECT username FROM users WHERE assigned_stall = (SELECT name FROM stalls WHERE id = ?)', (stall_id_to_remove,))
#                         assigned_user = cursor.fetchone()
#                         if assigned_user:
#                             # Cannot remove stall if a user is assigned
#                             self.handle_redirect('/admin', query_params={'error': 'remove_stall_assigned', 'user': assigned_user['username']})
#                             return

#                         # Delete the stall by ID (ON DELETE CASCADE handles items and variations)
#                         cursor.execute('DELETE FROM stalls WHERE id = ?', (stall_id_to_remove,))
#                         conn.commit()
#                         # Redirect with success message
#                         self.handle_redirect('/admin', query_params={'success': 'remove_stall'})
#                     except Exception as e:
#                         print(f"Error removing stall (Admin): {e}")
#                         conn.rollback()
#                         self.handle_redirect('/admin', query_params={'error': 'remove_stall_error'})
#                 else:
#                     # Missing stall ID
#                     self.handle_redirect('/admin', query_params={'error': 'remove_stall_missing_id'})


#             elif self.path == '/admin/update_stall' and role == 'admin':
#                 # Restrict to admin role
#                 stall_id = form_data.get('stall_id', [''])[0]
#                 # Use None as default to distinguish missing fields from empty strings
#                 new_name = form_data.get('new_name', [None])[0]
#                 new_description = form_data.get('new_description', [None])[0]
#                 new_image_path = form_data.get('new_image_path', [None])[0]

#                 if not stall_id:
#                     self.handle_redirect('/admin', query_params={'error': 'update_stall_missing_id'})
#                     return

#                 # Get the current stall data
#                 current_stall = get_stall_by_id(conn, stall_id)
#                 if not current_stall:
#                     self.handle_redirect('/admin', query_params={'error': 'update_stall_notfound'})
#                     return

#                 update_fields = []
#                 update_values = []

#                 # Update name if provided and different
#                 if new_name is not None and new_name.strip() and new_name.strip() != current_stall['name']:
#                     updated_name = new_name.strip()
#                     # Check for duplicate stall name
#                     existing_stall_with_name = get_stall_by_name(conn, updated_name)
#                     if existing_stall_with_name and existing_stall_with_name['id'] != current_stall['id']:
#                         self.handle_redirect('/admin', query_params={'error': 'update_stall_name_exists'})
#                         return

#                     update_fields.append('name = ?')
#                     update_values.append(updated_name)

#                 # Update description if provided
#                 if new_description is not None:
#                     update_fields.append('description = ?')
#                     update_values.append(new_description.strip() if new_description.strip() else None)

#                 # Update image path if provided
#                 if new_image_path is not None:
#                     update_fields.append('image_path = ?')
#                     update_values.append(new_image_path.strip() if new_image_path.strip() else None)


#                 if update_fields:
#                     update_query = f"UPDATE stalls SET {', '.join(update_fields)} WHERE id = ?"
#                     update_values.append(stall_id)
#                     cursor.execute(update_query, tuple(update_values))
#                     conn.commit()

#                     # If the stall name was updated, also update assigned_stall for any user assigned to it
#                     if 'name = ?' in update_fields:
#                         cursor.execute('UPDATE users SET assigned_stall = ? WHERE assigned_stall = ?', (updated_name, current_stall['name']))
#                         conn.commit()

#                     # Redirect with success message
#                     self.handle_redirect('/admin', query_params={'success': 'update_stall'})
#                 else:
#                     # No changes made, just redirect back to admin dashboard
#                     self.handle_redirect('/admin')


#             else:
#                 # Handle any other unknown POST requests by serving generic 404 page
#                 self.send_response(404) # Not Found
#                 self.send_header('Content-type', 'text/html')
#                 self.end_headers()
#                 self.wfile.write(bytes(get_error_page("Not Found", "The requested URL was not found on this server."), 'utf-8'))
#         except Exception as e:
#             # Catch any unexpected errors during POST processing
#             print(f"Error processing POST request for {self.path}: {e}")
#             self.send_header('Content-type', 'text/html')
#             self.send_response(500) # Internal Server Error
#             self.end_headers()
#             self.wfile.write(bytes(get_error_page("Internal Server Error", f"An internal server error occurred: {e}"), 'utf-8'))
#         finally:
#             # Ensure database connection is closed if it was opened
#             if conn:
#                 conn.close()

# # Helper function to get assigned stall for a user (can be added to db.py as well)
# def get_user_assigned_stall(conn, username):
#     cursor = conn.cursor()
#     cursor.execute('SELECT assigned_stall FROM users WHERE username = ?', (username,))
#     result = cursor.fetchone()
#     return result['assigned_stall'] if result else None
from http.server import SimpleHTTPRequestHandler
from urllib.parse import unquote, parse_qs, urlencode, quote # Import quote
import os
import time
import uuid
from datetime import datetime
from http.cookies import SimpleCookie
# Assuming db.py, session.py, and html_generator.py are in the same directory
from db import get_db_connection, get_user_by_username, get_user_by_id, is_stall_assigned, get_stall_by_name, get_stall_by_id, get_user_assigned_stall
from session import get_current_user_from_request, create_session, delete_session
from html_generator import get_first_page, get_choice_page, get_second_page, get_stall_page, get_cart_page, get_receipt_page, get_login_page, get_admin_dashboard, get_user_dashboard, get_error_page
import bcrypt
import sqlite3 # Import sqlite3 for specific error handling

# Session expiry seconds (defined here for use in handler)
SESSION_EXPIRY_SECONDS = 3600 # 1 hour

class MyHandler(SimpleHTTPRequestHandler):
    # Class-level dictionary to store carts, keyed by session_id or "guest"
    # This cart is in-memory and will be reset when the server restarts.
    # For persistence, a database table for carts would be needed.
    cart = {}
    # In-memory storage for receipt data, keyed by session_id or "guest"
    # This is temporary and will be lost on server restart or after viewing.
    receipt_data = {}

    def get_session_id(self):
        # Extracts the session ID from the request cookies.
        # This is now handled in session.py's get_current_user_from_request,
        # but keeping this helper for potential direct cookie access if needed.
        cookies = SimpleCookie(self.headers.get('Cookie'))
        if 'session_id' in cookies:
            return cookies['session_id'].value
        return None

    def get_current_user(self):
        # Gets the current user's session ID, username, and role using the session module.
        return get_current_user_from_request(self.headers)

    def handle_redirect(self, location='/', query_params=None):
        # Helper to send a 303 redirect with optional query parameters.
        if query_params:
            # Ensure query parameters are URL-encoded
            # Use urlencode to handle spaces and special characters in values
            encoded_params = urlencode(query_params)
            # Append query parameters to the location, handling existing ones
            if '?' in location:
                location += '&' + encoded_params
            else:
                location += '?' + encoded_params

        self.send_response(303)
        self.send_header('Location', location)
        self.end_headers()

    def do_GET(self):
        # Handles GET requests.
        session_id, username, role = self.get_current_user()

        if self.path == '/' or self.path.startswith('/?'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(get_first_page(username), 'utf-8'))
        elif self.path == '/choice' or self.path.startswith('/choice?'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(get_choice_page(username), 'utf-8'))
        elif self.path == '/second' or self.path.startswith('/second?'):
            # Determine the cart key for the current user/guest
            cart_key = session_id if session_id else "guest"
            current_cart_items = self.cart.get(cart_key, [])
            cart_item_count = sum(item['quantity'] for item in current_cart_items)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(get_second_page(username, role, cart_item_count), 'utf-8'))
        elif self.path == '/stalls':
            # Redirecting /stalls to /second (the stalls listing page)
            self.handle_redirect('/second')
        elif self.path.startswith('/stall/'):
            # Handle individual stall pages (customer view)
            parts = self.path.split('/')
            # Ensure there are enough parts in the path and the third part is not empty
            if len(parts) >= 3 and parts[2]:
                # Extract and decode stall name directly from the path segment
                # Handle potential query params after name
                stall_name = unquote(parts[2].split('?')[0])
                query_params = parse_qs(self.path.split('?')[-1]) if '?' in self.path else {} # Get query params

                conn = None
                stall_data_row = None
                try:
                    conn = get_db_connection()
                    # Retrieve stall data from the database
                    stall_data_row = get_stall_by_name(conn, stall_name)
                except Exception as e:
                    print(f"Error fetching stall data for /stall/: {e}")
                finally:
                    if conn:
                        conn.close()

                if stall_data_row:
                    # Convert row to dictionary for easier access
                    stall_data = dict(stall_data_row)
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    # Serve the stall page with its items, passing query params for messages
                    self.wfile.write(bytes(get_stall_page(
                        stall_data, username, role, query_params), 'utf-8')) # Pass query_params
                else:
                    # Stall not found, serve generic 404 page
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(bytes(get_error_page(
                        "Stall Not Found", "The requested stall could not be found."), 'utf-8'))
            else:
                 # Invalid stall path format, serve generic 404 page
                 self.send_response(404)
                 self.send_header('Content-type', 'text/html')
                 self.end_headers()
                 self.wfile.write(bytes(get_error_page(
                     "Not Found", "Invalid stall path format."), 'utf-8'))
        elif self.path == '/cart' or self.path.startswith('/cart?'):
            # Determine the cart key
            cart_key = session_id if session_id else "guest"
            user_cart = self.cart.get(cart_key, [])

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(get_cart_page(user_cart), 'utf-8'))

        elif self.path.startswith('/receipt/'):
             # Handle receipt page request
             parts = self.path.split('/')
             if len(parts) >= 3 and parts[2]:
                  # Get receipt ID from path
                  receipt_id = parts[2].split('?')[0]
                  # Retrieve receipt data from in-memory storage
                  receipt_data = self.receipt_data.get(receipt_id)

                  if receipt_data:
                       self.send_response(200)
                       self.send_header('Content-type', 'text/html')
                       self.end_headers()
                       self.wfile.write(
                           bytes(get_receipt_page(receipt_data), 'utf-8'))
                  else:
                       # Receipt not found
                       self.send_response(404)
                       self.send_header('Content-type', 'text/html')
                       self.end_headers()
                       self.wfile.write(bytes(get_error_page(
                           "Receipt Not Found", "The requested receipt could not be found."), 'utf-8'))
             else:
                  # Invalid receipt path format
                  self.send_response(404)
                  self.send_header('Content-type', 'text/html')
                  self.end_headers()
                  self.wfile.write(bytes(get_error_page(
                      "Not Found", "Invalid receipt path format."), 'utf-8'))

        elif self.path == '/login.html' or self.path.startswith('/login.html?'):
            # Redirect logged-in users away from the login page
            if username:
                conn = None
                user = None
                try:
                    conn = get_db_connection()
                    user = get_user_by_username(conn, username)
                except Exception as e:
                    print(f"Error getting user in login.html redirect: {e}")
                finally:
                    if conn:
                        conn.close()

                if user and user['role'] == 'admin':
                    # Redirect admin to admin dashboard
                    self.handle_redirect('/admin')
                elif user and user['role'] == 'user':
                     # Redirect user to user dashboard
                     self.handle_redirect('/user_dashboard')
                else:
                    # Default redirect if role is unexpected
                    self.handle_redirect('/')
                return  # Stop processing GET request

            # Serve the login/register page if not logged in
            query_params = parse_qs(self.path.split('?')[-1]) if '?' in self.path else {}
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(get_login_page(query_params), 'utf-8'))

        elif self.path == '/admin' or self.path.startswith('/admin?'):
            # Restrict access to admin dashboard
            # Re-check username and role after get_current_user()
            if not username or role != 'admin':
                print(f"Access to /admin denied. Username: {username}, Role: {role}")
                self.send_response(403) # Forbidden
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(get_error_page(
                    "Forbidden", "You must be logged in as an admin to view this page."), 'utf-8'))
                return  # Stop processing GET request

            conn = None
            users = []
            stalls = []
            items_by_stall = {}

            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                # Fetch all users
                cursor.execute('SELECT id, username, role, assigned_stall, applied_stall, application_status FROM users')
                users = cursor.fetchall()

                # Fetch all stalls
                cursor.execute('SELECT id, name, description, image_path FROM stalls')
                stalls = cursor.fetchall()

                # Fetch all items grouped by stall for admin view
                # Fetch all items first
                cursor.execute('SELECT i.id, i.name AS item_name, i.description, i.image_path, s.name AS stall_name, s.id AS stall_id FROM items i JOIN stalls s ON i.stall_id = s.id ORDER BY s.name, i.name')
                all_items = cursor.fetchall()

                # Group items by stall name
                for item in all_items:
                    stall_name = item['stall_name']
                    if stall_name not in items_by_stall:
                        items_by_stall[stall_name] = []
                    items_by_stall[stall_name].append(item)

            except Exception as e:
                print(f"Error fetching data for admin dashboard: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(get_error_page(
                    "Internal Server Error", f"An error occurred fetching admin data: {e}"), 'utf-8'))
                return
            finally:
                if conn:
                    conn.close()

            # Serve the admin dashboard
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(get_admin_dashboard(users, stalls, items_by_stall), 'utf-8'))

        elif self.path == '/user_dashboard' or self.path.startswith('/user_dashboard?'):
            # Restrict access to user dashboard
            # Re-check username and role after get_current_user()
            if not username or role != 'user':
                print(f"Access to /user_dashboard denied. Username: {username}, Role: {role}")
                self.send_response(403) # Forbidden
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(get_error_page(
                    "Forbidden", "You must be logged in as a user to view this page."), 'utf-8'))
                return  # Stop processing GET request

            conn = None
            user = None
            try:
                conn = get_db_connection()
                # Get user data for the dashboard
                user = get_user_by_username(conn, username)
            except Exception as e:
                print(f"Error getting user for user dashboard: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(get_error_page(
                    "Internal Server Error", f"An error occurred fetching user data: {e}"), 'utf-8'))
                return
            finally:
                if conn:
                    conn.close()

            if user:
                # Serve the user dashboard
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(get_user_dashboard(user), 'utf-8'))
            else:
                 # User not found (shouldn't happen if get_current_user returns username, but defensive)
                 self.send_response(404)
                 self.send_header('Content-type', 'text/html')
                 self.end_headers()
                 self.wfile.write(bytes(get_error_page(
                     "User Not Found", "Your user account could not be found."), 'utf-8'))

        elif self.path == '/style.css':
            # Serve the CSS file
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            try:
                with open('style.css', 'rb') as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_response(404) # CSS file not found
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(get_error_page(
                    "Not Found", "The requested CSS file was not found."), 'utf-8'))
        elif self.path.startswith('/firstpageimg/') or self.path.startswith('/secondpageimg/') or self.path.startswith('/stall_images/'):
            # Serve image files from specific directories
            try:
                file_path = self.path[1:] # Remove leading slash
                if os.path.exists(file_path):
                     with open(file_path, 'rb') as f:
                        self.send_response(200)
                        # Guess the MIME type based on file extension
                        self.send_header('Content-type', self.guess_type(self.path))
                        self.end_headers()
                        self.wfile.write(f.read())
                else:
                    self.send_response(404) # Image file not found
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(bytes(get_error_page(
                        "Image Not Found", "The requested image was not found."), 'utf-8'))
            except Exception as e:
                # Log any errors during file serving
                print(f"Error serving file {self.path}: {e}")
                self.send_response(500) # Internal Server Error
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(get_error_page(
                    "Internal Server Error", f"An error occurred while serving the file: {e}"), 'utf-8'))
        else:
            # Handle any other unknown GET requests by serving the generic 404 page
            self.send_response(404) # Not Found
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(get_error_page(
                "Not Found", "The requested URL was not found on this server."), 'utf-8'))

    def do_POST(self):
        # Handles POST requests.
        # Get current user information
        session_id, username, role = self.get_current_user()
        conn = None # Initialize conn to None

        try:
            # Read the content of the POST request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            # Parse the form data
            form_data = parse_qs(post_data)

            conn = get_db_connection() # Get database connection inside the try block
            cursor = conn.cursor() # Get cursor here

            # --- Handle different POST actions ---
            if self.path == '/add_to_cart':
                item_variation_id = form_data.get('item_variation_id', [''])[0]
                # Default quantity to 1 if not provided or invalid
                quantity_str = form_data.get('quantity', ['1'])[0]
                try:
                    quantity = int(quantity_str)
                except ValueError:
                    # Handle invalid quantity input gracefully
                    self.handle_redirect(self.headers.get('Referer', '/second'), query_params={'error': 'invalid_quantity'})
                    return

                # Validate input
                if not item_variation_id or quantity <= 0:
                     self.handle_redirect(self.headers.get('Referer', '/second'), query_params={'error': 'invalid_input'})
                     return

                # Retrieve item variation details
                cursor.execute('''
                    SELECT iv.id, iv.size, iv.price, iv.stock, i.name AS item_name, s.name AS stall_name
                    FROM item_variations iv
                    JOIN items i ON iv.item_id = i.id
                    JOIN stalls s ON i.stall_id = s.id
                    WHERE iv.id = ?
                ''', (item_variation_id,))
                variation_data = cursor.fetchone()

                if not variation_data:
                     # Item variation not found
                     self.handle_redirect(self.headers.get('Referer', '/second'), query_params={'error': 'item_not_found'})
                     return

                # Convert row to dictionary
                variation_data = dict(variation_data)

                # Check if enough stock is available
                if variation_data['stock'] < quantity:
                     # Redirect back to the stall page with an out-of-stock error
                     # Correctly format the stall URL
                     stall_url = f"/stall/{quote(variation_data['stall_name'])}"
                     self.handle_redirect(stall_url, query_params={'error': 'out_of_stock', 'item': variation_data['item_name'], 'size': variation_data['size']})
                     return

                # Decrease stock immediately when added to cart
                cursor.execute('UPDATE item_variations SET stock = stock - ? WHERE id = ?', (quantity, item_variation_id))
                conn.commit()

                # Determine the cart key (session ID for logged in, "guest" otherwise)
                cart_key = session_id if session_id else "guest"
                if cart_key not in self.cart:
                    # Initialize cart if it doesn't exist
                    self.cart[cart_key] = []

                found_item = None
                # Check if the item variation is already in the cart
                for item in self.cart[cart_key]:
                     if item['item_variation_id'] == variation_data['id']:
                         found_item = item
                         break

                if found_item:
                    # If found, increase the quantity
                    found_item['quantity'] += quantity
                else:
                    # If not found, add the new item variation to the cart
                    self.cart[cart_key].append({
                        "item_variation_id": variation_data['id'],
                        "quantity": quantity,
                        "name": variation_data['item_name'],
                        "size": variation_data['size'],
                        "price": variation_data['price'],
                        "stall": variation_data['stall_name']
                    })

                # Redirect back to the stall page with a success message
                # Correctly format the stall URL and add success query param
                stall_url = f"/stall/{quote(variation_data['stall_name'])}"
                self.handle_redirect(stall_url, query_params={'success': 'added_to_cart', 'item': variation_data['item_name'], 'size': variation_data['size']})

            elif self.path == '/checkout':
                # Handle checkout process
                cart_key = session_id if session_id else "guest"
                user_cart = self.cart.get(cart_key, [])

                if not user_cart:
                     # Cart is empty, redirect to cart page with error
                     self.handle_redirect('/cart', query_params={'error': 'cart_empty'})
                     return

                total_amount = sum(item['quantity'] * item['price'] for item in user_cart)

                # Record the order in the database
                # Use username if available, otherwise 'Guest'
                customer_name = username if username else 'Guest'
                cursor.execute('INSERT INTO orders (session_id, username, order_time, total_amount) VALUES (?, ?, ?, ?)',
                               (session_id, customer_name, int(time.time()), total_amount))
                order_id = cursor.lastrowid # Get the ID of the newly created order

                # Record order items
                for item in user_cart:
                     cursor.execute('INSERT INTO order_items (order_id, item_name, item_size, item_price, quantity, stall_name) VALUES (?, ?, ?, ?, ?, ?)',
                                    (order_id, item['name'], item['size'], item['price'], item['quantity'], item['stall']))

                     # Note: Stock is now decreased when adding to cart, so no stock update here.

                conn.commit()

                # Store receipt data in memory for retrieval
                # Generate a unique ID for the receipt URL
                receipt_id = str(uuid.uuid4())
                self.receipt_data[receipt_id] = {
                    'order_id': order_id,
                    'order_time': datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'),
                    'customer': customer_name,
                    'items': user_cart,
                    'total_amount': total_amount
                }

                # Clear the user's cart after successful checkout
                if cart_key in self.cart:
                    del self.cart[cart_key]

                # Redirect to the receipt page
                self.handle_redirect(f'/receipt/{receipt_id}')

            elif self.path == '/login':
                username_attempt = form_data.get('username', [''])[0]
                password_attempt = form_data.get('password', [''])[0]

                try:
                    # Retrieve user by username
                    user = get_user_by_username(conn, username_attempt)

                    if user:
                        # Verify the password using bcrypt
                        if bcrypt.checkpw(password_attempt.encode('utf-8'), user['password_hash'].encode('utf-8')):
                            # Create a new session upon successful login
                            new_session_id = create_session(conn, user['username'])
                            self.send_response(303) # See Other
                            # Redirect based on user role
                            redirect_location = '/admin' if user['role'] == 'admin' else '/user_dashboard'
                            self.send_header('Location', redirect_location)
                            # Set the session cookie
                            self.send_header('Set-Cookie', f'session_id={new_session_id}; HttpOnly; Path=/; Max-Age={SESSION_EXPIRY_SECONDS}')
                            self.end_headers()
                        else:
                            # Redirect back to login with an error message
                            self.handle_redirect('/login.html', query_params={'error': 'incorrect_password'})
                    else:
                        # Redirect back to login with an error message
                        self.handle_redirect('/login.html', query_params={'error': 'account_not_found'})

                except Exception as e:
                    # Log any errors during the login process
                    print(f"Error during login process for {username_attempt}: {e}")
                    self.send_response(500) # Internal Server Error
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(bytes(get_error_page(
                        "Internal Server Error", f"An internal server error occurred during login: {e}"), 'utf-8'))

            elif self.path == '/register':
                reg_username = form_data.get('reg_username', [''])[0]
                reg_password = form_data.get('reg_password', [''])[0]
                # Optional stall application during registration or re-application
                apply_stall_name = form_data.get('apply_stall', [''])[0] or None

                # Basic validation
                if not reg_username or not reg_username.strip() or not reg_password or not reg_password.strip():
                    self.handle_redirect('/login.html', query_params={'reg_status': 'missing_fields', 'register': 'true'})
                    return

                # Check if username already exists
                existing_user = get_user_by_username(conn, reg_username.strip())

                if existing_user:
                    # --- Handle Re-application for Declined Users ---
                    # Check if the user is a 'user' role and their application was declined
                    if existing_user['role'] == 'user' and existing_user['application_status'] == 'declined':
                        if apply_stall_name:
                            # Check if the applied stall exists
                            stall = get_stall_by_name(conn, apply_stall_name)
                            if stall:
                                # Check if the stall is already assigned to another user
                                if is_stall_assigned(conn, apply_stall_name):
                                     # Redirect back to user dashboard with error
                                     self.handle_redirect('/user_dashboard', query_params={'error': 'reapply_stall_assigned'})
                                     return # Stop processing

                                # Update existing user's application status and applied stall
                                cursor.execute('UPDATE users SET applied_stall = ?, application_status = "pending" WHERE id = ?',
                                               (apply_stall_name, existing_user['id']))
                                conn.commit()
                                self.handle_redirect('/user_dashboard', query_params={'success': 'reapplied'})
                                return # Stop processing
                            else:
                                # Applied stall not found
                                self.handle_redirect('/user_dashboard', query_params={'error': 'reapply_stall_not_found'})
                                return # Stop processing
                        else:
                             # Missing stall name for re-application
                             self.handle_redirect('/user_dashboard', query_params={'error': 'reapply_missing_stall'})
                             return # Stop processing
                    else:
                        # Username already exists and is not a declined user re-applying
                        self.handle_redirect('/login.html', query_params={'reg_status': 'exists', 'register': 'true'})
                        return # Stop processing

                # --- Handle New Registration ---
                # Hash the password for new registration
                hashed_password = bcrypt.hashpw(reg_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                initial_role = 'user'
                initial_status = 'none'
                if apply_stall_name:
                    # Check if the applied stall exists for new registration
                    stall = get_stall_by_name(conn, apply_stall_name)
                    if stall:
                        # Check if the stall is already assigned to another user
                        if is_stall_assigned(conn, apply_stall_name):
                             # Redirect back to login with error
                             self.handle_redirect('/login.html', query_params={'reg_status': 'stall_assigned', 'register': 'true'})
                             return # Stop processing

                        # Set status to pending if applying for a valid, unassigned stall
                        initial_status = 'pending'
                    else:
                        apply_stall_name = None # Clear applied stall if it doesn't exist

                # Insert the new user into the database
                try:
                    cursor.execute('INSERT INTO users (username, password_hash, role, applied_stall, application_status) VALUES (?, ?, ?, ?, ?)',
                                   (reg_username.strip(), hashed_password, initial_role, apply_stall_name, initial_status))
                    conn.commit()

                    # Create a session for the newly registered user
                    new_session_id = create_session(conn, reg_username.strip())

                    self.send_response(303) # See Other
                    # Redirect to user dashboard after registration
                    self.send_header('Location', '/user_dashboard')
                    # Set the session cookie
                    self.send_header('Set-Cookie', f'session_id={new_session_id}; HttpOnly; Path=/; Max-Age={SESSION_EXPIRY_SECONDS}')
                    self.end_headers()
                except sqlite3.IntegrityError as e:
                    print(f"Integrity Error during registration: {e}")
                    conn.rollback() # Rollback changes in case of error
                    self.handle_redirect('/login.html', query_params={'reg_status': 'integrity_error', 'register': 'true'})
                except Exception as e:
                    print(f"General Error during registration: {e}")
                    conn.rollback() # Rollback changes
                    self.handle_redirect('/login.html', query_params={'reg_status': 'general_error', 'register': 'true'})


            elif self.path == '/logout':
                 # Handle user logout
                 if session_id:
                     delete_session(conn, session_id) # Delete the session
                     self.send_response(303) # See Other
                     self.send_header('Location', '/') # Redirect to home page
                     # Expire the session cookie
                     self.send_header('Set-Cookie', 'session_id=; Max-Age=0; Path=/')
                     self.end_headers()
                 else:
                     # If no session, just redirect to home
                     self.handle_redirect('/')

            # --- Admin User Management Actions ---
            elif self.path == '/admin/add_user' and role == 'admin':
                 # Restrict to admin role
                 new_username = form_data.get('new_username', [''])[0]
                 new_password = form_data.get('new_password', [''])[0]
                 new_role = form_data.get('new_role', ['user'])[0]
                 new_assigned_stall = form_data.get('new_assigned_stall', [''])[0] or None

                 # Basic validation
                 if not new_username or not new_username.strip() or not new_password or not new_password.strip():
                      self.handle_redirect('/admin', query_params={'error': 'add_user_missing'})
                      return

                 # Check if username already exists
                 existing_user = get_user_by_username(conn, new_username.strip())
                 if existing_user:
                     self.handle_redirect('/admin', query_params={'error': 'add_user_exists'})
                     return

                 # Check if the stall is already assigned if trying to assign one
                 if new_assigned_stall and is_stall_assigned(conn, new_assigned_stall):
                     self.handle_redirect('/admin', query_params={'error': 'assign_stall_assigned'})
                     return

                 # Hash the password
                 hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                 try:
                     # Insert the new user
                     cursor.execute('INSERT INTO users (username, password_hash, role, assigned_stall, application_status) VALUES (?, ?, ?, ?, ?)',
                                    (new_username.strip(), hashed_password, new_role, new_assigned_stall, 'none'))
                     conn.commit()
                     # Redirect with success message
                     self.handle_redirect('/admin', query_params={'success': 'add_user'})
                 except sqlite3.IntegrityError as e:
                      print(f"Integrity Error adding user (Admin): {e}")
                      conn.rollback()
                      self.handle_redirect('/admin', query_params={'error': 'add_user_integrity_error'})
                 except Exception as e:
                      print(f"General Error adding user (Admin): {e}")
                      conn.rollback()
                      self.handle_redirect('/admin', query_params={'error': 'add_user_general_error'})

            elif self.path == '/admin/remove_user' and role == 'admin':
                 # Restrict to admin role
                 user_id_to_remove = form_data.get('user_id', [''])[0]
                 if user_id_to_remove:
                     # Prevent removing the default admin user
                     user_to_remove = get_user_by_id(conn, user_id_to_remove)
                     if user_to_remove and user_to_remove['username'] == 'admin':
                         self.handle_redirect('/admin', query_params={'error': 'remove_admin_forbidden'})
                         return

                     try:
                          # Delete the user by ID
                          cursor.execute('DELETE FROM users WHERE id = ?', (user_id_to_remove,))
                          conn.commit()
                          # Redirect with success message
                          self.handle_redirect('/admin', query_params={'success': 'remove_user'})
                     except Exception as e:
                          print(f"Error removing user (Admin): {e}")
                          conn.rollback()
                          self.handle_redirect('/admin', query_params={'error': 'remove_user_error'})

                 else:
                      # Missing user ID
                      self.handle_redirect('/admin', query_params={'error': 'remove_user_missing_id'})

            elif self.path == '/admin/update_user_assignment' and role == 'admin':
                 # Restrict to admin role
                 user_id = form_data.get('user_id', [''])[0]
                 new_assigned_stall = form_data.get('assigned_stall', [''])[0] or None

                 # Basic validation
                 if not user_id:
                      self.handle_redirect('/admin', query_params={'error': 'update_user_missing_id'})
                      return

                 # Get user to update
                 user_to_update = get_user_by_id(conn, user_id)
                 if not user_to_update:
                     self.handle_redirect('/admin', query_params={'error': 'update_user_notfound'})
                     return

                 # Prevent updating the default admin user's assignment
                 if user_to_update['username'] == 'admin':
                     self.handle_redirect('/admin', query_params={'error': 'update_admin_forbidden'})
                     return

                 # Check if the new assigned stall is already assigned to another user
                 if new_assigned_stall and is_stall_assigned(conn, new_assigned_stall, exclude_user_id=user_to_update['id']):
                     self.handle_redirect('/admin', query_params={'error': 'assign_stall_assigned'})
                     return

                 try:
                     # Update the assigned stall and reset application status if assigned
                     if new_assigned_stall:
                         # If assigning a stall, set status to approved and clear applied_stall
                         cursor.execute('UPDATE users SET assigned_stall = ?, applied_stall = NULL, application_status = "approved" WHERE id = ?', (new_assigned_stall, user_id))
                     else:
                          # If unassigning, clear assigned_stall and set status to none
                          cursor.execute('UPDATE users SET assigned_stall = NULL, applied_stall = NULL, application_status = "none" WHERE id = ?', (user_id,))

                     conn.commit()
                     # Redirect with success message
                     self.handle_redirect('/admin', query_params={'success': 'update_user_assignment'})
                 except Exception as e:
                     print(f"Error updating user assignment (Admin): {e}")
                     conn.rollback()
                     self.handle_redirect('/admin', query_params={'error': 'update_user_assignment_error'})

            # --- Admin Application Management Actions ---
            elif self.path == '/admin/approve_application' and role == 'admin':
                 # Restrict to admin role
                 user_id = form_data.get('user_id', [''])[0]
                 if user_id:
                     # Get user and check application status
                     user = get_user_by_id(conn, user_id)
                     if user and user['application_status'] == 'pending' and user['applied_stall']:
                         # Check if the applied stall is already assigned to another user
                         if is_stall_assigned(conn, user['applied_stall']):
                              self.handle_redirect('/admin', query_params={'error': 'application_stall_assigned'})
                              return # Stop processing

                         try:
                             # Assign the stall and update status
                             cursor.execute('UPDATE users SET assigned_stall = ?, applied_stall = NULL, application_status = "approved" WHERE id = ?', (user['applied_stall'], user_id))
                             conn.commit()
                             # Redirect with success message including stall name
                             self.handle_redirect('/admin', query_params={'success': 'application_approved', 'stall_name': user['applied_stall']})
                         except Exception as e:
                              # Log and handle errors during approval
                              print(f"Error approving application for user {user['username']}: {e}")
                              self.handle_redirect('/admin', query_params={'error': 'application_approve_error'})
                     else:
                          # Application is not pending or missing applied stall
                          self.handle_redirect('/admin', query_params={'error': 'application_not_pending'})
                 else:
                     # Missing user ID
                     self.handle_redirect('/admin', query_params={'error': 'application_missing_user_id'})

            elif self.path == '/admin/decline_application' and role == 'admin':
                 # Restrict to admin role
                 user_id = form_data.get('user_id', [''])[0]
                 if user_id:
                     # Get user and check application status
                     user = get_user_by_id(conn, user_id)
                     if user and user['application_status'] == 'pending':
                         try:
                             # Update application status to declined
                             # Also clear applied_stall on decline
                             cursor.execute('UPDATE users SET application_status = "declined", applied_stall = NULL WHERE id = ?', (user_id,))
                             conn.commit()
                             # Redirect with success message
                             self.handle_redirect('/admin', query_params={'success': 'application_declined'})
                         except Exception as e:
                             # Log and handle errors during decline
                             print(f"Error declining application for user {user['username']}: {e}")
                             self.handle_redirect('/admin', query_params={'error': 'application_decline_error'})
                     else:
                         # Application is not pending
                         self.handle_redirect('/admin', query_params={'error': 'application_not_pending'})
                 else:
                     # Missing user ID
                     self.handle_redirect('/admin', query_params={'error': 'application_missing_user_id'})

            # --- Item Management Actions (User - Assigned Stall & Admin) ---
            # Note: Admin can also use these endpoints to manage items directly on stall pages
            elif self.path == '/user/add_item_main' and (role == 'user' or role == 'admin'):
                 # Restrict to user role (assigned stall) or admin
                 stall_name = form_data.get('stall_name', [''])[0]
                 item_name = form_data.get('item_name', [''])[0]
                 description = form_data.get('description', [''])[0]
                 image_path = form_data.get('image_path', [''])[0] or None # Optional image path
                 first_variation_size = form_data.get('first_variation_size', [''])[0] or 'N/A'
                 first_variation_price_str = form_data.get('first_variation_price', [''])[0]
                 first_variation_stock_str = form_data.get('first_variation_stock', ['0'])[0]

                 # Get stall data to get stall ID and verify existence
                 stall = get_stall_by_name(conn, stall_name)
                 if not stall:
                      # Stall not found, redirect with error
                      # Determine the correct redirect location based on role
                      redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                      self.handle_redirect(redirect_url, query_params={'error': 'stall_not_found'})
                      return # Stop processing

                 # Check authorization for user role
                 if role == 'user':
                     assigned_stall = get_user_assigned_stall(conn, username)
                     if assigned_stall != stall_name:
                          self.send_response(403) # Forbidden
                          self.send_header('Content-type', 'text/html')
                          self.end_headers()
                          self.wfile.write(bytes(get_error_page(
                              "Forbidden", "You are not authorized to add items to this stall."), 'utf-8'))
                          return # Stop processing

                 # Basic validation
                 if not item_name or not item_name.strip() or not first_variation_price_str:
                     # Determine the correct redirect location based on role
                     redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                     self.handle_redirect(redirect_url, query_params={'error': 'add_item_missing_fields'})
                     return

                 try:
                     # Convert price and stock to appropriate types
                     first_variation_price = float(first_variation_price_str)
                     first_variation_stock = int(first_variation_stock_str)
                     if first_variation_price < 0 or first_variation_stock < 0:
                          # Determine the correct redirect location based on role
                          redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                          self.handle_redirect(redirect_url, query_params={'error': 'add_item_invalid_price_stock'})
                          return
                 except ValueError:
                      # Handle invalid number formats
                      # Determine the correct redirect location based on role
                      redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                      self.handle_redirect(redirect_url, query_params={'error': 'add_item_invalid_price_stock'})
                      return

                 try:
                     # Check if item name already exists in this stall
                     existing_item = cursor.execute('SELECT id FROM items WHERE name = ? AND stall_id = ?', (item_name.strip(), stall['id'])).fetchone()
                     if existing_item:
                          # Determine the correct redirect location based on role
                          redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                          self.handle_redirect(redirect_url, query_params={'error': 'add_item_exists_in_stall'})
                          return

                     # Insert the main item
                     cursor.execute('INSERT INTO items (name, description, image_path, stall_id) VALUES (?, ?, ?, ?)',
                                    (item_name.strip(), description.strip() if description else None, image_path.strip() if image_path else None, stall['id']))
                     item_id = cursor.lastrowid # Get the ID of the newly inserted item

                     # Insert the first variation for the item
                     # Check if the first variation size already exists for this new item (shouldn't happen, but defensive)
                     existing_variation = cursor.execute('SELECT id FROM item_variations WHERE item_id = ? AND size = ?', (item_id, first_variation_size.strip())).fetchone()
                     if existing_variation:
                          print(f"Warning: Duplicate size '{first_variation_size}' found for new item ID {item_id} during initial add.")
                          # Rollback the item insert if variation insert would fail due to duplicate size
                          conn.rollback() # Added rollback
                          # Determine the correct redirect location based on role
                          redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                          self.handle_redirect(redirect_url, query_params={'error': 'add_item_initial_variation_exists'})
                          return

                     cursor.execute('INSERT INTO item_variations (item_id, size, price, stock) VALUES (?, ?, ?, ?)',
                                    (item_id, first_variation_size.strip(), first_variation_price, first_variation_stock))
                     conn.commit()
                     # Redirect with success message
                     # Determine the correct redirect location based on role
                     redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                     self.handle_redirect(redirect_url, query_params={'success': 'add_item'})
                 except sqlite3.IntegrityError as e:
                      # Handle database integrity errors (e.g., stall_id not found)
                      print(f"Integrity Error adding item/variation (User/Admin): {e}")
                      conn.rollback() # Rollback changes in case of error
                      # Determine the correct redirect location based on role
                      redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                      self.handle_redirect(redirect_url, query_params={'error': 'add_item_integrity_error'})
                 except Exception as e:
                      # Handle other general errors
                      print(f"General Error adding item/variation (User/Admin): {e}")
                      conn.rollback() # Rollback changes
                      # Determine the correct redirect location based on role
                      redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                      self.handle_redirect(redirect_url, query_params={'error': 'add_item_general_error'})

            elif self.path == '/user/add_item_variation' and (role == 'user' or role == 'admin'):
                 # Restrict to user role (assigned stall) or admin
                 item_id = form_data.get('item_id', [''])[0]
                 size = form_data.get('size', [''])[0] or 'N/A'
                 price_str = form_data.get('price', [''])[0]
                 stock_str = form_data.get('stock', ['0'])[0]

                 # Get the stall name and stall ID associated with the item
                 cursor.execute('SELECT s.name, s.id FROM items i JOIN stalls s ON i.stall_id = s.id WHERE i.id = ?', (item_id,))
                 item_stall_row = cursor.fetchone()
                 if not item_stall_row:
                      # Item not found, redirect with error
                      # Determine the correct redirect location based on role
                      redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                      self.handle_redirect(redirect_url, query_params={'error': 'item_not_found'})
                      return
                 item_stall_name = item_stall_row['name']
                 item_stall_id = item_stall_row['id']

                 # Check authorization for user role
                 if role == 'user':
                      assigned_stall = get_user_assigned_stall(conn, username)
                      if assigned_stall != item_stall_name:
                           self.send_response(403) # Forbidden
                           self.send_header('Content-type', 'text/html')
                           self.end_headers()
                           self.wfile.write(bytes(get_error_page(
                               "Forbidden", "You are not authorized to add variations to items in this stall."), 'utf-8'))
                           return # Stop processing

                 # Basic validation
                 if not item_id or not price_str:
                     # Determine the correct redirect location based on role
                     redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                     self.handle_redirect(redirect_url, query_params={'error': 'add_variation_missing_fields'})
                     return

                 try:
                     # Convert price and stock to appropriate types
                     price = float(price_str)
                     stock = int(stock_str)
                     if price < 0 or stock < 0:
                          # Determine the correct redirect location based on role
                          redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                          self.handle_redirect(redirect_url, query_params={'error': 'add_variation_invalid_price_stock'})
                          return
                 except ValueError:
                      # Handle invalid number formats
                      # Determine the correct redirect location based on role
                      redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                      self.handle_redirect(redirect_url, query_params={'error': 'add_variation_invalid_price_stock'})
                      return

                 try:
                     # Check if variation size already exists for this item
                     existing_variation = cursor.execute('SELECT id FROM item_variations WHERE item_id = ? AND size = ?', (item_id, size.strip())).fetchone()
                     if existing_variation:
                          # Determine the correct redirect location based on role
                          redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                          self.handle_redirect(redirect_url, query_params={'error': 'add_variation_exists'})
                          return

                     # Insert the new variation
                     cursor.execute('INSERT INTO item_variations (item_id, size, price, stock) VALUES (?, ?, ?, ?)',
                                    (item_id, size.strip(), price, stock))
                     conn.commit()
                     # Redirect with success message
                     # Determine the correct redirect location based on role
                     redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                     self.handle_redirect(redirect_url, query_params={'success': 'add_variation'})
                 except sqlite3.IntegrityError as e:
                      # Handle database integrity errors (e.g., item_id not found)
                      print(f"Integrity Error adding variation (User/Admin): {e}")
                      conn.rollback() # Rollback changes
                      # Determine the correct redirect location based on role
                      redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                      self.handle_redirect(redirect_url, query_params={'error': 'add_variation_integrity_error'})
                 except Exception as e:
                      # Handle other general errors
                      print(f"General Error adding variation (User/Admin): {e}")
                      conn.rollback() # Rollback changes
                      # Determine the correct redirect location based on role
                      redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                      self.handle_redirect(redirect_url, query_params={'error': 'add_variation_general_error'})

            elif self.path == '/user/remove_item_main' and (role == 'user' or role == 'admin'):
                 # Restrict to user role (assigned stall) or admin
                 item_id_to_remove = form_data.get('item_id', [''])[0]
                 if item_id_to_remove:
                      # Get the stall name associated with the item
                      cursor.execute('SELECT s.name FROM items i JOIN stalls s ON i.stall_id = s.id WHERE i.id = ?', (item_id_to_remove,))
                      item_stall_row = cursor.fetchone()
                      if not item_stall_row:
                           # Item not found, redirect with error
                           # Determine the correct redirect location based on role
                           redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                           self.handle_redirect(redirect_url, query_params={'error': 'item_not_found'})
                           return
                      item_stall_name = item_stall_row['name']

                      # Check authorization for user role
                      if role == 'user':
                          assigned_stall = get_user_assigned_stall(conn, username)
                          if assigned_stall != item_stall_name:
                               self.send_response(403) # Forbidden
                               self.send_header('Content-type', 'text/html')
                               self.end_headers()
                               self.wfile.write(bytes(get_error_page(
                                   "Forbidden", "You are not authorized to remove items from this stall."), 'utf-8'))
                               return # Stop processing

                      try:
                          # Delete the item (ON DELETE CASCADE handles variations)
                          cursor.execute('DELETE FROM items WHERE id = ?', (item_id_to_remove,))
                          conn.commit()
                          # Redirect with success message
                          # Determine the correct redirect location based on role
                          redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                          self.handle_redirect(redirect_url, query_params={'success': 'remove_item'})
                      except Exception as e:
                           print(f"Error removing item (User/Admin): {e}")
                           conn.rollback()
                           redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                           self.handle_redirect(redirect_url, query_params={'error': 'remove_item_error'})

                 else:
                      # Missing item ID, redirect with error
                      # Determine the correct redirect location based on role
                      redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                      self.handle_redirect(redirect_url, query_params={'error': 'remove_item_missing_id'})


            elif self.path == '/remove_item_main_customer':
                 # Handle removing an item directly from the customer stall page
                 item_id_to_remove = form_data.get('item_id', [''])[0]
                 stall_name = form_data.get('stall_name', [''])[0]

                 if not item_id_to_remove or not stall_name:
                      # Missing item ID or stall name
                      self.handle_redirect(f'/stall/{quote(stall_name)}', query_params={'error': 'remove_item_missing_info'})
                      return

                 # Check authorization: Only assigned user or admin can remove from customer view
                 if not username or (role == 'user' and get_user_assigned_stall(conn, username) != stall_name) or role not in ['user', 'admin']:
                      self.send_response(403) # Forbidden
                      self.send_header('Content-type', 'text/html')
                      self.end_headers()
                      self.wfile.write(bytes(get_error_page(
                          "Forbidden", "You are not authorized to remove items from this stall."), 'utf-8'))
                      return # Stop processing


                 try:
                     # Delete the item (ON DELETE CASCADE handles variations)
                     cursor.execute('DELETE FROM items WHERE id = ?', (item_id_to_remove,))
                     conn.commit()
                     # Redirect back to the stall page
                     self.handle_redirect(f'/stall/{quote(stall_name)}', query_params={'success': 'remove_item'})
                 except Exception as e:
                     print(f"Error removing item from customer view: {e}")
                     conn.rollback()
                     self.handle_redirect(f'/stall/{quote(stall_name)}', query_params={'error': 'remove_item_error'})


            elif self.path == '/user/remove_item_variation' and (role == 'user' or role == 'admin'):
                 # Restrict to user role (assigned stall) or admin
                 variation_id_to_remove = form_data.get('variation_id', [''])[0]
                 if variation_id_to_remove:
                     # Get the stall name and item ID associated with the variation's item
                     cursor.execute('SELECT s.name, iv.item_id FROM item_variations iv JOIN items i ON iv.item_id = i.id JOIN stalls s ON i.stall_id = s.id WHERE iv.id = ?', (variation_id_to_remove,))
                     item_stall_row = cursor.fetchone()
                     if not item_stall_row:
                          # Variation not found, redirect with error
                          # Determine the correct redirect location based on role
                          redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                          self.handle_redirect(redirect_url, query_params={'error': 'variation_not_found'})
                          return
                     item_stall_name = item_stall_row['name']
                     item_id = item_stall_row['item_id']

                     # Check authorization for user role
                     if role == 'user':
                          assigned_stall = get_user_assigned_stall(conn, username)
                          if assigned_stall != item_stall_name:
                               self.send_response(403) # Forbidden
                               self.send_header('Content-type', 'text/html')
                               self.end_headers()
                               self.wfile.write(bytes(get_error_page(
                                   "Forbidden", "You are not authorized to remove variations from items in this stall."), 'utf-8'))
                               return # Stop processing

                     try:
                          # Delete the item variation by ID
                          cursor.execute('DELETE FROM item_variations WHERE id = ?', (variation_id_to_remove,))
                          conn.commit()

                          # After deleting the variation, check if the parent item has any variations left
                          cursor.execute('SELECT COUNT(*) FROM item_variations WHERE item_id = ?', (item_id,))
                          remaining_variations_count = cursor.fetchone()[0]

                          if remaining_variations_count == 0:
                              # If no variations left, remove the parent item
                              print(f"Item ID {item_id} has no variations left. Removing item.")
                              cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
                              conn.commit()
                              # Redirect with success message for item removal
                              # Determine the correct redirect location based on role
                              redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                              self.handle_redirect(redirect_url, query_params={'success': 'remove_item_no_variations'})
                          else:
                              # Redirect with success message for variation removal
                              # Determine the correct redirect location based on role
                              redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                              self.handle_redirect(redirect_url, query_params={'success': 'remove_variation'})

                     except Exception as e:
                          print(f"Error removing variation (User/Admin): {e}")
                          conn.rollback()
                          redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                          self.handle_redirect(redirect_url, query_params={'error': 'remove_variation_error'})

                 else:
                     # Missing variation ID, redirect with error
                     # Determine the correct redirect location based on role
                     redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                     self.handle_redirect(redirect_url, query_params={'error': 'remove_variation_missing_id'})


            elif self.path == '/user/update_item_variation' and (role == 'user' or role == 'admin'):
                 # Restrict to user role (assigned stall) or admin
                 variation_id = form_data.get('variation_id', [''])[0]
                 # Use None as default to distinguish missing fields from empty strings
                 new_size = form_data.get('new_size', [None])[0]
                 new_price_str = form_data.get('new_price', [None])[0]
                 new_stock_str = form_data.get('new_stock', [None])[0]

                 if not variation_id:
                     # Missing variation ID, redirect with error
                     # Determine the correct redirect location based on role
                     redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                     self.handle_redirect(redirect_url, query_params={'error': 'update_variation_missing_id'})
                     return

                 # Get the stall name and item ID associated with the variation
                 cursor.execute('SELECT s.name, iv.item_id FROM item_variations iv JOIN items i ON iv.item_id = i.id JOIN stalls s ON i.stall_id = s.id WHERE iv.id = ?', (variation_id,))
                 item_stall_row = cursor.fetchone()
                 if not item_stall_row:
                      # Variation not found, redirect with error
                      # Determine the correct redirect location based on role
                      redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                      self.handle_redirect(redirect_url, query_params={'error': 'variation_not_found'})
                      return
                 item_stall_name = item_stall_row['name']
                 item_id = item_stall_row['item_id']

                 # Check authorization for user role
                 if role == 'user':
                      assigned_stall = get_user_assigned_stall(conn, username)
                      if assigned_stall != item_stall_name:
                           self.send_response(403) # Forbidden
                           self.send_header('Content-type', 'text/html')
                           self.end_headers()
                           self.wfile.write(bytes(get_error_page(
                               "Forbidden", "You are not authorized to update variations for items in this stall."), 'utf-8'))
                           return # Stop processing

                 update_fields = []
                 update_values = []

                 # Update size if provided and different
                 if new_size is not None:
                     updated_size = new_size.strip() if new_size else 'N/A'
                     # Check for duplicate size for this item
                     existing_variation_with_size = cursor.execute('SELECT id FROM item_variations WHERE item_id = ? AND size = ? AND id != ?', (item_id, updated_size, variation_id)).fetchone()
                     if existing_variation_with_size:
                          # Determine the correct redirect location based on role
                          redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                          self.handle_redirect(redirect_url, query_params={'error': 'update_variation_size_exists'})
                          return

                     update_fields.append('size = ?')
                     update_values.append(updated_size)

                 # Update price if provided
                 if new_price_str is not None:
                      try:
                          new_price = float(new_price_str)
                          if new_price < 0:
                               # Determine the correct redirect location based on role
                               redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                               self.handle_redirect(redirect_url, query_params={'error': 'update_variation_invalid_price'})
                               return
                          update_fields.append('price = ?')
                          update_values.append(new_price)
                      except ValueError:
                           # Handle invalid price format
                           # Determine the correct redirect location based on role
                           redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                           self.handle_redirect(redirect_url, query_params={'error': 'update_variation_invalid_price'})
                           return

                 # Update stock if provided
                 if new_stock_str is not None:
                     try:
                         new_stock = int(new_stock_str)
                         if new_stock < 0:
                              # Determine the correct redirect location based on role
                              redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                              self.handle_redirect(redirect_url, query_params={'error': 'update_variation_invalid_stock'})
                              return
                         update_fields.append('stock = ?')
                         update_values.append(new_stock)
                     except ValueError:
                          # Handle invalid stock format
                          # Determine the correct redirect location based on role
                          redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                          self.handle_redirect(redirect_url, query_params={'error': 'update_variation_invalid_stock'})
                          return

                 if update_fields:
                     update_query = f"UPDATE item_variations SET {', '.join(update_fields)} WHERE id = ?"
                     update_values.append(variation_id)
                     try:
                         cursor.execute(update_query, tuple(update_values))
                         conn.commit()
                         # Redirect with success message
                         # Determine the correct redirect location based on role
                         redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                         self.handle_redirect(redirect_url, query_params={'success': 'update_variation'})
                     except sqlite3.IntegrityError as e:
                          print(f"Integrity Error updating variation (User/Admin): {e}")
                          conn.rollback()
                          redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                          self.handle_redirect(redirect_url, query_params={'error': 'update_variation_integrity_error'})
                     except Exception as e:
                          print(f"General Error updating variation (User/Admin): {e}")
                          conn.rollback()
                          redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                          self.handle_redirect(redirect_url, query_params={'error': 'update_variation_general_error'})
                 else:
                     # No changes made, just redirect to the dashboard
                     redirect_url = '/user_dashboard' if role == 'user' else '/admin'
                     self.handle_redirect(redirect_url)

            # --- Stall Management Actions (Admin Only) ---
            elif self.path == '/admin/add_stall' and role == 'admin':
                # Restrict to admin role
                stall_name = form_data.get('stall_name', [''])[0]
                description = form_data.get('description', [''])[0]
                image_path = form_data.get('image_path', [''])[0] or None

                # Basic validation
                if not stall_name or not stall_name.strip():
                    self.handle_redirect('/admin', query_params={'error': 'add_stall_missing_name'})
                    return

                # Check if stall name already exists
                existing_stall = get_stall_by_name(conn, stall_name.strip())
                if existing_stall:
                    self.handle_redirect('/admin', query_params={'error': 'add_stall_exists'})
                    return

                try:
                    # Insert the new stall
                    cursor.execute('INSERT INTO stalls (name, description, image_path) VALUES (?, ?, ?)',
                                   (stall_name.strip(), description.strip() if description else None, image_path.strip() if image_path else None))
                    conn.commit()
                    # Redirect with success message
                    self.handle_redirect('/admin', query_params={'success': 'add_stall'})
                except sqlite3.IntegrityError as e:
                    print(f"Integrity Error adding stall (Admin): {e}")
                    conn.rollback()
                    self.handle_redirect('/admin', query_params={'error': 'add_stall_integrity_error'})
                except Exception as e:
                    print(f"General Error adding stall (Admin): {e}")
                    conn.rollback()
                    self.handle_redirect('/admin', query_params={'error': 'add_stall_general_error'})


            elif self.path == '/admin/remove_stall' and role == 'admin':
                # Restrict to admin role
                stall_id_to_remove = form_data.get('stall_id', [''])[0]
                if stall_id_to_remove:
                    try:
                        # Check if any user is assigned to this stall before removing
                        cursor.execute('SELECT username FROM users WHERE assigned_stall = (SELECT name FROM stalls WHERE id = ?)', (stall_id_to_remove,))
                        assigned_user = cursor.fetchone()
                        if assigned_user:
                            # Cannot remove stall if a user is assigned
                            self.handle_redirect('/admin', query_params={'error': 'remove_stall_assigned', 'user': assigned_user['username']})
                            return

                        # Delete the stall by ID (ON DELETE CASCADE handles items and variations)
                        cursor.execute('DELETE FROM stalls WHERE id = ?', (stall_id_to_remove,))
                        conn.commit()
                        # Redirect with success message
                        self.handle_redirect('/admin', query_params={'success': 'remove_stall'})
                    except Exception as e:
                        print(f"Error removing stall (Admin): {e}")
                        conn.rollback()
                        self.handle_redirect('/admin', query_params={'error': 'remove_stall_error'})
                else:
                    # Missing stall ID
                    self.handle_redirect('/admin', query_params={'error': 'remove_stall_missing_id'})


            elif self.path == '/admin/update_stall' and role == 'admin':
                # Restrict to admin role
                stall_id = form_data.get('stall_id', [''])[0]
                # Use None as default to distinguish missing fields from empty strings
                new_name = form_data.get('new_name', [None])[0]
                new_description = form_data.get('new_description', [None])[0]
                new_image_path = form_data.get('new_image_path', [None])[0]

                if not stall_id:
                    self.handle_redirect('/admin', query_params={'error': 'update_stall_missing_id'})
                    return

                # Get the current stall data
                current_stall = get_stall_by_id(conn, stall_id)
                if not current_stall:
                    self.handle_redirect('/admin', query_params={'error': 'update_stall_notfound'})
                    return

                update_fields = []
                update_values = []

                # Update name if provided and different
                if new_name is not None and new_name.strip() and new_name.strip() != current_stall['name']:
                    updated_name = new_name.strip()
                    # Check for duplicate stall name
                    existing_stall_with_name = get_stall_by_name(conn, updated_name)
                    if existing_stall_with_name and existing_stall_with_name['id'] != current_stall['id']:
                        self.handle_redirect('/admin', query_params={'error': 'update_stall_name_exists'})
                        return

                    update_fields.append('name = ?')
                    update_values.append(updated_name)

                # Update description if provided
                if new_description is not None:
                    update_fields.append('description = ?')
                    update_values.append(new_description.strip() if new_description.strip() else None)

                # Update image path if provided
                if new_image_path is not None:
                    update_fields.append('image_path = ?')
                    update_values.append(new_image_path.strip() if new_image_path.strip() else None)


                if update_fields:
                    update_query = f"UPDATE stalls SET {', '.join(update_fields)} WHERE id = ?"
                    update_values.append(stall_id)
                    cursor.execute(update_query, tuple(update_values))
                    conn.commit()

                    # If the stall name was updated, also update assigned_stall for any user assigned to it
                    if 'name = ?' in update_fields:
                        cursor.execute('UPDATE users SET assigned_stall = ? WHERE assigned_stall = ?', (updated_name, current_stall['name']))
                        conn.commit()

                    # Redirect with success message
                    self.handle_redirect('/admin', query_params={'success': 'update_stall'})
                else:
                    # No changes made, just redirect back to admin dashboard
                    self.handle_redirect('/admin')


            else:
                # Handle any other unknown POST requests by serving generic 404 page
                self.send_response(404) # Not Found
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(get_error_page("Not Found", "The requested URL was not found on this server."), 'utf-8'))
        except Exception as e:
            # Catch any unexpected errors during POST processing
            print(f"Error processing POST request for {self.path}: {e}")
            self.send_header('Content-type', 'text/html')
            self.send_response(500) # Internal Server Error
            self.end_headers()
            self.wfile.write(bytes(get_error_page("Internal Server Error", f"An internal server error occurred: {e}"), 'utf-8'))
        finally:
            # Ensure database connection is closed if it was opened
            if conn:
                conn.close()

# Helper function to get assigned stall for a user (can be added to db.py as well)
def get_user_assigned_stall(conn, username):
    cursor = conn.cursor()
    cursor.execute('SELECT assigned_stall FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    return result['assigned_stall'] if result else None
