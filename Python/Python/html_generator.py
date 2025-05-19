
# import os
# from urllib.parse import urlencode, quote, parse_qs
# from datetime import datetime
# # Assuming db.py and session.py are in the same directory
# from db import get_db_connection, get_stall_by_name, is_stall_assigned, get_stall_by_id, get_user_by_id, get_user_assigned_stall
# from session import get_current_user_from_request

# # --- HTML Generation Functions ---

# def get_error_page(title, message):
#     # Generates a generic HTML error page with pastel theme and background.
#     return f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Error: {title}</title>
#         <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
#         <link rel="preconnect" href="https://fonts.googleapis.com">
#         <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
#         <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap" rel="stylesheet">
#         <link rel="stylesheet" href="/style.css">
#     </head>
#     <body class="bg-green-50 flex justify-center items-center min-h-screen m-0 relative font-nunito default-background">
#         <div class="error-container bg-white rounded-xl shadow-lg p-8 text-center w-4/5 max-w-md border border-green-200 animate-fade-in">
#             <h1 class="text-3xl font-bold text-red-600 mb-4">{title}</h1>
#             <p class="text-gray-700 mb-6">{message}</p>
#             <a href="/" class="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline inline-block transition duration-300 ease-in-out transform hover:scale-105">
#                 Go to Home Page
#             </a>
#              <a href="/second" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline inline-block ml-4 transition duration-300 ease-in-out transform hover:scale-105">
#                 View Stalls
#              </a>
#         </div>
#     </body>
#     </html>
#     """

# def get_first_page(username):
#     # Generates the HTML for the first page with pastel theme and background.
#     logged_in_message = f"<p class='text-center text-gray-600 mt-4'>Logged in as: {username}</p>" if username else ""
#     logout_button = "<div class='text-center mt-4'><form action='/logout' method='post'><button type='submit' class='bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300 ease-in-out'>Logout</button></form></div>" if username else ""

#     return f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Welcome to the Kiosk</title>
#         <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
#         <link rel="preconnect" href="https://fonts.googleapis.com">
#         <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
#         <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap" rel="stylesheet">
#         <link rel="stylesheet" href="/style.css">
#     </head>
#     <body class="bg-green-50 flex justify-center items-center min-h-screen m-0 relative font-nunito default-background">
#         <div class="kiosk-container bg-white rounded-xl shadow-lg p-8 text-center w-4/5 max-w-lg animate-fade-in border border-green-200">
#             <div class="logo mb-6">
#                 <img src="/secondpageimg/craveeatsnobg.png" alt="CraveEats Logo" class="mx-auto h-24 animate-pulse">
#             </div>
#             <h1 class="text-4xl font-bold text-green-800 mb-4 animate-fade-down">Welcome to CraveEats Kiosk!</h1>
#             <p class="text-gray-700 mb-6 animate-fade-down animation-delay-100">Your one-stop shop for delicious treats.</p>
#             <a href="/choice" class="bg-green-600 hover:bg-green-700 text-white font-bold py-4 px-8 text-lg rounded-lg shadow-md transition duration-300 ease-in-out transform hover:scale-105 animate-bounce">
#                 Start Ordering
#             </a>
#             {logged_in_message}
#             {logout_button}
#         </div>
#          <div class="admin-button absolute top-4 right-4">
#              <a href="/login.html" class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300 ease-in-out">
#                  Login/Register
#              </a>
#          </div>
#          <div class="umak-logo absolute bottom-4 left-4">
#              <img src="/secondpageimg/umaklogo.png" alt="UMAK Logo" class="h-10">
#          </div>
#     </body>
#     </html>
#     """

# def get_choice_page(username):
#     # Generates the HTML for the choice page (Customer or Stall Owner) with pastel theme and background.
#     logged_in_message = f"<p class='text-center text-gray-600 mt-4'>Logged in as: {username}</p>" if username else ""
#     logout_button = "<div class='text-center mt-4'><form action='/logout' method='post'><button type='submit' class='bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300 ease-in-out'>Logout</button></form></div>" if username else ""

#     return f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Choose Your Role</title>
#         <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
#         <link rel="preconnect" href="https://fonts.googleapis.com">
#         <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
#         <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap" rel="stylesheet">
#         <link rel="stylesheet" href="/style.css">
#     </head>
#     <body class="bg-green-50 flex justify-center items-center min-h-screen m-0 relative font-nunito default-background">
#         <div class="choice-container bg-white rounded-xl shadow-lg p-8 text-center w-4/5 max-w-md animate-fade-in border border-green-200">
#             <h1 class="text-3xl font-bold text-green-800 mb-6 animate-fade-down">Are you a Customer or a Stall Owner?</h1>
#             <a href="/second" class="block bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg shadow-md transition duration-300 ease-in-out transform hover:scale-105 mb-4 animate-slide-in">
#                 Customer
#             </a>
#             <a href="/login.html" class="block bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-lg shadow-md transition duration-300 ease-in-out transform hover:scale-105 animate-slide-in animation-delay-100">
#                 Stall Owner
#             </a>
#             <a href="/" class="block bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-6 transition duration-300 ease-in-out">
#                 Back to Home
#             </a>
#             {logged_in_message}
#             {logout_button}
#         </div>
#          <div class="admin-button absolute top-4 right-4">
#              <a href="/login.html" class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300 ease-in-out">
#                  Login/Register
#              </a>
#          </div>
#     </body>
#     </html>
#     """

# def get_second_page(username, role, cart_item_count):
#     # Generates the HTML for the second page, listing stalls, with pastel theme and background.
#     conn = None
#     stalls = []
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute('SELECT id, name, description, image_path FROM stalls')
#         stalls = cursor.fetchall()
#     except Exception as e:
#         print(f"Error fetching stalls for second page: {e}")
#     finally:
#         if conn:
#             conn.close()

#     stalls_html = ""
#     if stalls:
#         for stall in stalls:
#             # Correctly encode stall name for the URL path using quote
#             stall_url_name = quote(stall['name'])
#             stalls_html += f"""
#             <a href="/stall/{stall_url_name}" class="option-card bg-white rounded-lg shadow-md p-4 text-center transition duration-300 ease-in-out transform hover:scale-105 hover:shadow-xl border border-green-100">
#                 <img src="{stall['image_path'] if stall['image_path'] and os.path.exists(stall['image_path'][1:]) else '/stall_images/placeholder.jpg'}" alt="{stall['name']}" class="mx-auto h-24 w-auto object-cover rounded-md mb-2 border border-gray-200">
#                 <h3 class="text-lg font-semibold text-green-800">{stall['name']}</h3>
#                 <p class="text-sm text-gray-600">{stall['description'] if stall['description'] else 'No description available.'}</p>
#             </a>
#             """
#     else:
#         stalls_html = "<p class='text-center text-gray-600'>No stalls available yet.</p>"

#     logged_in_message = f"<p class='text-center text-gray-600 mt-4'>Logged in as: {username}</p>" if username else ""
#     logout_button = "<div class='text-center mt-4'><form action='/logout' method='post'><button type='submit' class='bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300 ease-in-out'>Logout</button></form></div>" if username else ""


#     return f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Available Stalls</title>
#         <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
#         <link rel="preconnect" href="https://fonts.googleapis.com">
#         <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
#         <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap" rel="stylesheet">
#         <link rel="stylesheet" href="/style.css">
#     </head>
#     <body class="bg-green-50 min-h-screen m-0 relative font-nunito default-background">
#         <div class="kiosk-header bg-white shadow-md p-4 text-center border-b border-green-200">
#              <img src="/secondpageimg/craveeatsnobg.png" alt="CraveEats Logo" class="mx-auto h-16">
#         </div>
#         <div class="container mx-auto p-4 mt-4 animate-fade-in">
#             <h1 class="text-3xl font-bold text-green-800 text-center mb-6">Choose a Stall</h1>
#             <div class="options-container grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
#                 {stalls_html}
#             </div>
#             <div class="text-center mt-8 flex justify-center space-x-4">
#                 <a href="/choice" class="back-button bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline inline-block transition duration-300 ease-in-out">
#                     Back to Choices
#                 </a>
#                 <a href="/cart" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline inline-block transition duration-300 ease-in-out">
#                      View Cart ({cart_item_count})
#                 </a>
#             </div>
#              <div class="admin-button absolute top-4 right-4">
#                  <a href="/login.html" class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300 ease-in-out">
#                      Login/Register
#                  </a>
#              </div>
#         </body>
#     </html>
#     """

# def get_stall_page(stall_data, username, role, query_params):
#     # Generates the HTML for an individual stall's page with background. This is primarily for customer view.
#     conn = None
#     items = []
#     message_html = ""

#     # Check for messages in query parameters
#     if 'success' in query_params:
#         if query_params['success'][0] == 'added_to_cart':
#             item_name = query_params.get('item', [''])[0]
#             item_size = query_params.get('size', [''])[0]
#             message_html = f"<div id='notification' class='notification-message success bg-green-500 text-white p-3 rounded-md text-center'>Added {item_name} ({item_size}) to cart!</div>"
#         elif query_params['success'][0] == 'remove_item':
#              message_html = "<div id='notification' class='notification-message success bg-green-500 text-white p-3 rounded-md text-center'>Item removed successfully!</div>"

#     if 'error' in query_params:
#         if query_params['error'][0] == 'out_of_stock':
#             item_name = query_params.get('item', [''])[0]
#             item_size = query_params.get('size', [''])[0]
#             message_html = f"<div id='notification' class='notification-message error bg-red-500 text-white p-3 rounded-md text-center'>Sorry, {item_name} ({item_size}) is out of stock or requested quantity exceeds available stock.</div>"
#         elif query_params['error'][0] == 'remove_item_missing_info':
#              message_html = "<div id='notification' class='notification-message error bg-red-500 text-white p-3 rounded-md text-center'>Error: Missing item information for removal.</div>"
#         elif query_params['error'][0] == 'remove_item_error':
#              message_html = "<div id='notification' class='notification-message error bg-red-500 text-white p-3 rounded-md text-center'>Error removing item.</div>"


#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         # Fetch items for this specific stall
#         cursor.execute('SELECT id, name, description, image_path FROM items WHERE stall_id = (SELECT id FROM stalls WHERE name = ?) ORDER BY name', (stall_data['name'],))
#         items = cursor.fetchall()

#     except Exception as e:
#         print(f"Error fetching stall data for stall page {stall_data['name']}: {e}")
#     finally:
#         if conn:
#             conn.close()

#     item_cards_html = ""
#     if items:
#         for item in items:
#             item_cards_html += f"""
#             <div class="item-card bg-white rounded-lg shadow-lg p-4 border border-green-100 flex flex-col justify-between transition transform hover:scale-105 duration-300 ease-in-out">
#                 <div>
#                     <img src="{item['image_path'] if item['image_path'] and os.path.exists(item['image_path'][1:]) else '/stall_images/placeholder.jpg'}" alt="{item['name']}" class="mx-auto h-40 w-full object-cover rounded-md mb-3 border border-gray-200 shadow-sm">
#                     <h3 class="text-xl font-semibold text-green-800 mb-2">{item['name']}</h3>
#                     <p class="text-gray-700 text-sm mb-3">{item['description'] if item['description'] else 'No description available.'}</p>

#                     <h4 class="text-md font-medium text-green-700 mb-2">Variations:</h4>
#                     <ul class="list-none p-0 space-y-2">
#             """
#             conn_variations = None
#             variations = []
#             try:
#                 conn_variations = get_db_connection()
#                 cursor_variations = conn_variations.cursor()
#                 # Fetch variations for the current item
#                 cursor_variations.execute('SELECT id, size, price, stock FROM item_variations WHERE item_id = ? ORDER BY size', (item['id'],))
#                 variations = cursor_variations.fetchall()
#             except Exception as e:
#                 print(f"Error fetching variations for item {item['name']}: {e}")
#             finally:
#                 if conn_variations:
#                     conn_variations.close()

#             if variations:
#                 for variation in variations:
#                     # Add 'out-of-stock' class if stock is 0
#                     stock_class = 'text-red-600 font-bold' if variation['stock'] <= 0 else ''
#                     stock_text = f"Stock: {variation['stock']}" if variation['stock'] > 0 else "Out of Stock"
#                     item_cards_html += f"""
#                         <li class="flex justify-between items-center bg-green-50 rounded-md p-2 border border-green-100 flex-wrap">
#                             <span class="text-gray-800 text-sm mr-4 flex-grow">{variation['size']} - ₱{variation['price']:.2f}</span>
#                             <span class="text-gray-600 text-sm {stock_class}">{stock_text}</span>
#                             <div class="flex items-center space-x-2 mt-2 md:mt-0">
#                     """
#                     # Add to Cart form (visible to all customers) - disabled if stock is 0
#                     item_cards_html += f"""
#                                  <form action="/add_to_cart" method="post" class="inline-block flex items-center">
#                                      <input type="hidden" name="item_variation_id" value="{variation['id']}">
#                                       <input type="number" name="quantity" value="1" min="1" max="{variation['stock']}" class="border rounded px-2 py-1 w-16 text-xs focus:outline-none focus:ring focus:border-blue-300 mr-1" {"disabled" if variation['stock'] <= 0 else ""}>
#                                      <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-1 px-3 rounded focus:outline-none focus:shadow-outline text-xs transition duration-300 ease-in-out" {"disabled" if variation['stock'] <= 0 else ""}>
#                                          Add to Cart
#                                      </button>
#                                  </form>
#                     """
#                     item_cards_html += "</div></li>"

#                 # Add "Remove Item" button for the main item here, below variations
#                 # Only show remove button if user is logged in (not guest)
#                 if username:
#                     item_cards_html += f"""
#                     <li class="text-center mt-4">
#                         <form action="/remove_item_main_customer" method="post" onsubmit="return confirm('WARNING: This will remove {item['name']} and ALL its variations from this stall. Are you sure?');" class="inline-block">
#                             <input type="hidden" name="item_id" value="{item['id']}">
#                             <input type="hidden" name="stall_name" value="{stall_data['name']}">
#                             <button type="submit" class="bg-red-500 hover:bg-red-600 text-white font-bold py-1 px-3 rounded focus:outline-none focus:shadow-outline text-xs transition duration-300 ease-in-out">
#                                 Remove Item
#                             </button>
#                         </form>
#                     </li>
#                     """
#             else:
#                 item_cards_html += "<p class='text-gray-600 text-sm ml-4'>No variations available for this item.</p>"
#                 # Add "Remove Item" button even if no variations exist, but only if logged in
#                 if username:
#                     item_cards_html += f"""
#                     <li class="text-center mt-4">
#                         <form action="/remove_item_main_customer" method="post" onsubmit="return confirm('WARNING: This will remove {item['name']} from this stall. Are you sure?');" class="inline-block">
#                             <input type="hidden" name="item_id" value="{item['id']}">
#                             <input type="hidden" name="stall_name" value="{stall_data['name']}">
#                             <button type="submit" class="bg-red-500 hover:bg-red-600 text-white font-bold py-1 px-3 rounded focus:outline-none focus:shadow-outline text-xs transition duration-300 ease-in-out">
#                                 Remove Item
#                             </button>
#                         </form>
#                     </li>
#                     """


#             item_cards_html += "</ul>" # Close variations list

#             item_cards_html += "</div>" # Close item card content div
#             item_cards_html += "</div>" # Close item card

#     else:
#         item_cards_html = "<p class='text-center text-gray-600'>No items available at this stall.</p>"

#     return f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>{stall_data['name']} Menu</title>
#         <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
#         <link rel="preconnect" href="https://fonts.googleapis.com">
#         <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
#         <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap" rel="stylesheet">
#         <link rel="stylesheet" href="/style.css">
#     </head>
#     <body class="bg-green-50 min-h-screen m-0 relative font-nunito default-background">
#         <div class="kiosk-header bg-white shadow-md p-4 text-center border-b border-green-200">
#              <img src="/secondpageimg/craveeatsnobg.png" alt="CraveEats Logo" class="mx-auto h-16">
#         </div>
#         <div class="container mx-auto p-4 mt-4 animate-fade-in">
#             <div class="stall-page bg-white rounded-xl shadow-lg p-6 border border-green-200 relative"> <h1 class="text-3xl font-bold text-green-800 text-center mb-4">{stall_data['name']}</h1>
#                 <p class="text-center text-gray-600 mb-6">{stall_data['description'] if stall_data['description'] else 'No description available.'}</p>

#                 <div id="notification-container">
#                     {message_html}
#                 </div>


#                 <div class="items-slider-container">
#                     <div class="items-list-slider">
#                         {item_cards_html}
#                     </div>
#                 </div>

#                 <div class="text-center mt-8 flex justify-center space-x-4">
#                     <a href="/second" class="back-button bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline inline-block transition duration-300 ease-in-out">
#                         Back to Stalls
#                     </a>
#                      <a href="/cart" class="cart-button bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline inline-block ml-4 transition duration-300 ease-in-out">
#                          View Cart
#                      </a>
#                 </div>
#             </div>
#         </div>
#          <script>
#              // Script to fade out and hide notification messages
#              const notification = document.getElementById('notification');
#              if (notification) {{
#                  // Use setTimeout to allow the initial display before starting fade out
#                  setTimeout(() => {{
#                      notification.style.transition = 'opacity 1s ease-out';
#                      notification.style.opacity = '0';
#                  }}, 3000); // Start fade out after 3 seconds

#                  // Use transitionend to set display: none after the fade out is complete
#                  notification.addEventListener('transitionend', () => {{
#                      if (notification.style.opacity === '0') {{
#                          notification.style.display = 'none';
#                      }}
#                  }});
#              }}
#          </script>
#     </body>
#     </html>
#     """

# def get_cart_page(user_cart):
#     # Generates the HTML for the cart page with pastel theme and background.

#     cart_items_html = ""
#     total_price = 0

#     if user_cart:
#         for item in user_cart:
#             cart_items_html += f"""
#             <div class="flex justify-between items-center bg-green-100 rounded-md p-3 mb-3 border border-green-200">
#                 <span class="text-gray-800 font-medium">{item['name']} ({item['size']})</span>
#                 <span class="text-gray-700">{item['quantity']} x ₱{item['price']:.2f}</span>
#                 <span class="font-semibold text-green-700">₱{(item['quantity'] * item['price']):.2f}</span>
#             </div>
#             """
#             total_price += item['quantity'] * item['price']

#         # Add checkout button if the cart is not empty
#         cart_items_html += f"""
#         <div class="mt-6 pt-4 border-t-2 border-green-200 flex justify-between items-center">
#             <span class="text-xl font-bold text-green-800">Total:</span>
#             <span class="text-xl font-bold text-green-600">₱{total_price:.2f}</span>
#         </div>
#         <div class="text-center mt-8">
#             <form action="/checkout" method="post">
#                  <button type="submit" class="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded-lg focus:outline-none focus:shadow-outline inline-block transition duration-300 ease-in-out transform hover:scale-105">
#                      Proceed to Checkout
#                  </button>
#             </form>
#         </div>
#         """
#     else:
#         cart_items_html = "<p class='text-center text-gray-600'>Your cart is empty.</p>"
#         total_price = 0 # Ensure total is 0 if cart is empty

#     return f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Your Cart</title>
#         <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
#         <link rel="preconnect" href="https://fonts.googleapis.com">
#         <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
#         <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap" rel="stylesheet">
#         <link rel="stylesheet" href="/style.css">
#     </head>
#     <body class="bg-green-50 min-h-screen m-0 relative font-nunito default-background">
#         <div class="kiosk-header bg-white shadow-md p-4 text-center border-b border-green-200">
#              <img src="/secondpageimg/craveeatsnobg.png" alt="CraveEats Logo" class="mx-auto h-16">
#         </div>
#         <div class="container mx-auto p-4 mt-4 animate-fade-in">
#             <div class="cart-container bg-white rounded-xl shadow-lg p-6 border border-green-200">
#                 <h1 class="text-3xl font-bold text-green-800 text-center mb-6">Your Shopping Cart</h1>
#                 {cart_items_html}
#                 <div class="text-center mt-8">
#                     <a href="/second" class="back-button bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline inline-block transition duration-300 ease-in-out">
#                         Continue Shopping
#                     </a>
#                 </div>
#             </div>
#         </div>
#          <div class="admin-button absolute top-4 right-4">
#              <a href="/login.html" class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300 ease-in-out">
#                  Login/Register
#              </a>
#          </div>
#     </body>
#     </html>
#     """

# def get_receipt_page(receipt_data):
#     # Generates the HTML for the e-receipt page with pastel theme and background.
#     if not receipt_data:
#         return get_error_page("Receipt Not Found", "Could not retrieve receipt details.")

#     order_items_html = ""
#     for item in receipt_data['items']:
#         order_items_html += f"""
#         <div class="flex justify-between items-center border-b border-gray-200 py-2">
#             <span class="text-gray-700">{item['name']} ({item['size']}) - {item['quantity']} x ₱{item['price']:.2f} ({item['stall']})</span>
#             <span class="font-semibold text-green-700">₱{(item['quantity'] * item['price']):.2f}</span>
#         </div>
#         """

#     return f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Order Receipt</title>
#         <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
#         <link rel="preconnect" href="https://fonts.googleapis.com">
#         <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
#         <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap" rel="stylesheet">
#         <link rel="stylesheet" href="/style.css">
#     </head>
#     <body class="bg-green-50 flex justify-center items-center min-h-screen m-0 relative font-nunito default-background">
#         <div class="receipt-container bg-white rounded-xl shadow-lg p-8 w-4/5 max-w-md border border-green-200 animate-fade-in">
#             <h1 class="text-3xl font-bold text-green-800 text-center mb-6">Order Receipt</h1>

#             <div class="mb-6 text-gray-700">
#                 <p><strong>Order ID:</strong> {receipt_data['order_id']}</p>
#                 <p><strong>Date & Time:</strong> {receipt_data['order_time']}</p>
#                 <p><strong>Customer:</strong> {receipt_data['customer']}</p>
#             </div>

#             <h2 class="text-xl font-semibold text-green-700 mb-4">Items:</h2>
#             {order_items_html}

#             <div class="mt-6 pt-4 border-t-2 border-green-200 flex justify-between items-center">
#                 <span class="text-xl font-bold text-green-800">Total:</span>
#                 <span class="text-xl font-bold text-green-600">₱{receipt_data['total_amount']:.2f}</span>
#             </div>

#             <div class="text-center mt-8 flex justify-center space-x-4">
#                 <a href="/" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline inline-block transition duration-300 ease-in-out">
#                     Back to Home
#                 </a>
#                  <a href="/second" class="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline inline-block transition duration-300 ease-in-out">
#                      Order Again (View Stalls)
#                  </a>
#             </div>
#         </div>
#     </body>
#     </html>
#     """

# def get_login_page(query_params):
#     # Generates the HTML for the login and registration page with pastel theme and background.
#     error_message = ""
#     reg_message = "" # Use a single message variable for registration feedback
#     # Show register form if 'register=true' is in query params
#     show_register_form = 'register' in query_params

#     if 'error' in query_params:
#         error_type = query_params['error'][0]
#         if error_type == 'incorrect_password':
#             error_message = "<p class='text-red-500 text-center mb-4'>Incorrect username or password.</p>"
#         elif error_type == 'account_not_found':
#             error_message = "<p class='text-red-500 text-center mb-4'>Account not found.</p>"
#         # Add other login errors here if needed

#     if 'reg_status' in query_params: # Use reg_status for clearer feedback
#         reg_status_code = query_params['reg_status'][0]
#         if reg_status_code == 'success':
#             reg_message = "<p class='text-green-500 text-center mb-4'>Registration successful! Please log in.</p>"
#         elif reg_status_code == 'exists':
#             reg_message = "<p class='text-red-500 text-center mb-4'>Username already exists.</p>"
#         elif reg_status_code == 'missing_fields':
#             reg_message = "<p class='text-red-500 text-center mb-4'>Username and password are required.</p>"
#         elif reg_status_code == 'stall_assigned':
#              reg_message = "<p class='text-red-500 text-center mb-4'>The selected stall is already assigned to another user.</p>"
#         elif reg_status_code == 'integrity_error':
#              reg_message = "<p class='text-red-500 text-center mb-4'>A database error occurred during registration. Please try again.</p>"
#         elif reg_status_code == 'general_error':
#              reg_message = "<p class='text-red-500 text-center mb-4'>An unexpected error occurred during registration.</p>"
#         elif reg_status_code == 'reapplied': # Feedback for successful re-application
#              reg_message = "<p class='text-green-500 text-center mb-4'>Re-application submitted! Your status is now pending review.</p>"


#     conn = None
#     stalls = []
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         # Fetch only stalls that are NOT currently assigned
#         cursor.execute('SELECT name FROM stalls WHERE name NOT IN (SELECT assigned_stall FROM users WHERE assigned_stall IS NOT NULL)')
#         stalls = cursor.fetchall()
#     except Exception as e:
#         print(f"Error fetching stalls for login page: {e}")
#     finally:
#         if conn:
#             conn.close()

#     stall_options = "<option value=''>Select a Stall (Optional)</option>"
#     for stall in stalls:
#         stall_options += f"<option value='{stall['name']}'>{stall['name']}</option>"

#     return f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Login or Register</title>
#         <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
#         <link rel="preconnect" href="https://fonts.googleapis.com">
#         <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
#         <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap" rel="stylesheet">
#         <link rel="stylesheet" href="/style.css">
#     </head>
#     <body class="bg-green-50 flex justify-center items-center min-h-screen m-0 relative font-nunito default-background">
#         <div class="auth-container bg-white rounded-xl shadow-lg p-8 w-4/5 max-w-md animate-fade-in border border-green-200">
#             <h1 class="text-3xl font-bold text-green-800 text-center mb-6">Account Access</h1>

#             {error_message}
#             {reg_message}

#             <div id="login-form" class="{'block' if not show_register_form else 'hidden'}">
#                 <h2 class="text-2xl font-semibold text-green-700 text-center mb-4">Login</h2>
#                 <form action="/login" method="post" class="space-y-4">
#                     <div>
#                         <label for="username" class="block text-gray-700 font-semibold mb-1">Username:</label>
#                         <input type="text" id="username" name="username" required class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-blue-300">
#                     </div>
#                     <div>
#                         <label for="password" class="block text-gray-700 font-semibold mb-1">Password:</label>
#                         <input type="password" id="password" name="password" required class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-blue-300">
#                     </div>
#                     <div class="text-center">
#                         <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded focus:outline-none focus:shadow-outline transition duration-300 ease-in-out">
#                             Login
#                         </button>
#                     </div>
#                 </form>
#                 <p class="text-center text-gray-600 mt-4">Don't have an account? <a href="/login.html?register=true" class="text-blue-600 hover:underline">Register here</a>.</p>
#             </div>

#             <div id="register-form" class="{'block' if show_register_form else 'hidden'}">
#                 <h2 class="text-2xl font-semibold text-green-700 text-center mb-4">Register</h2>
#                 <form action="/register" method="post" class="space-y-4">
#                     <div>
#                         <label for="reg_username" class="block text-gray-700 font-semibold mb-1">Username:</label>
#                         <input type="text" id="reg_username" name="reg_username" required class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-300">
#                     </div>
#                     <div>
#                         <label for="reg_password" class="block text-gray-700 font-semibold mb-1">Password:</label>
#                         <input type="password" id="reg_password" name="reg_password" required class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-300">
#                     </div>
#                      <div>
#                          <label for="apply_stall" class="block text-gray-700 font-semibold mb-1">Apply to Manage a Stall (Optional):</label>
#                          <select id="apply_stall" name="apply_stall" class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-300">
#                              {stall_options}
#                          </select>
#                      </div>
#                     <div class="text-center">
#                         <button type="submit" class="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded focus:outline-none focus:shadow-outline transition duration-300 ease-in-out">
#                             Register
#                         </button>
#                     </div>
#                 </form>
#                 <p class="text-center text-gray-600 mt-4">Already have an account? <a href="/login.html" class="text-blue-600 hover:underline">Login here</a>.</p>
#             </div>

#             <div class="text-center mt-6">
#                  <a href="/choice" class="back-button bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline inline-block transition duration-300 ease-in-out">
#                      Back to Choices
#                  </a>
#             </div>
#         </div>
#     </body>
#     </html>
#     """


# def get_admin_dashboard(users, stalls, items_by_stall):
#     # Generates the HTML for the admin dashboard with pastel theme and enhanced item management.

#     # --- Add Stall Form ---
#     add_stall_form = f"""
#     <div class="p-6 bg-green-200 rounded-xl shadow-md border border-green-300 flex-1 min-w-[300px]">
#          <h2 class="text-2xl font-bold text-green-900 mb-4">Add New Stall</h2>
#          <form action="/admin/add_stall" method="post" class="flex flex-col space-y-4">
#              <div>
#                  <label for="stall_name" class="block text-gray-700 font-semibold mb-1">Stall Name:</label>
#                  <input type="text" id="stall_name" name="stall_name" required class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400">
#              </div>
#              <div>
#                  <label for="stall_description" class="block text-gray-700 font-semibold mb-1">Description (Optional):</label>
#                  <textarea id="stall_description" name="description" rows="2" class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400"></textarea>
#              </div>
#               <div>
#                   <label for="stall_image_path" class="block text-gray-700 font-semibold mb-1">Image Path (Optional, e.g., /stall_images/stall.jpg):</label>
#                   <input type="text" id="stall_image_path" name="image_path" class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400">
#               </div>
#              <div class="text-center">
#                  <button type="submit" class="bg-green-700 hover:bg-green-800 text-white font-bold py-2 px-6 rounded-lg focus:outline-none focus:shadow-outline transition duration-300 ease-in-out">
#                      Add Stall
#                  </button>
#              </div>
#          </form>
#     </div>
#     """

#     # --- Add User Form ---
#     # Need a connection to check assigned stalls for the dropdown
#     conn_for_user_form = None
#     stall_options_for_user_form = "<option value=''>None</option>"
#     try:
#         conn_for_user_form = get_db_connection()
#         cursor_for_user_form = conn_for_user_form.cursor()
#         # Fetch only stalls that are NOT currently assigned
#         cursor_for_user_form.execute('SELECT name FROM stalls WHERE name NOT IN (SELECT assigned_stall FROM users WHERE assigned_stall IS NOT NULL)')
#         stalls_for_user_form = cursor_for_user_form.fetchall()
#         for stall in stalls_for_user_form:
#              stall_options_for_user_form += f"<option value='{stall['name']}'>{stall['name']}</option>"
#     except Exception as e:
#         print(f"Error fetching stalls for add user form: {e}")
#     finally:
#         if conn_for_user_form:
#             conn_for_user_form.close()


#     add_user_form = f"""
#      <div class="p-6 bg-blue-100 rounded-xl shadow-md border border-blue-200 flex-1 min-w-[300px]">
#           <h2 class="text-2xl font-bold text-blue-800 mb-4">Add New User</h2>
#           <form action="/admin/add_user" method="post" class="flex flex-col space-y-4">
#               <div>
#                   <label for="new_username" class="block text-gray-700 font-semibold mb-1">Username:</label>
#                   <input type="text" id="new_username" name="new_username" required class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-blue-300">
#               </div>
#               <div>
#                   <label for="new_password" class="block text-gray-700 font-semibold mb-1">Password:</label>
#                   <input type="password" id="new_password" name="new_password" required class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-blue-300">
#               </div>
#                <div>
#                    <label for="new_role" class="block text-gray-700 font-semibold mb-1">Role:</label>
#                    <select id="new_role" name="new_role" class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-blue-300">
#                        <option value="user">User</option>
#                        <option value="admin">Admin</option>
#                    </select>
#                </div>
#                <div>
#                    <label for="new_assigned_stall" class="block text-gray-700 font-semibold mb-1">Assign Stall (Optional, for users):</label>
#                    <select id="new_assigned_stall" name="new_assigned_stall" class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-blue-300">
#                        {stall_options_for_user_form}
#                    </select>
#                </div>
#           <div class="text-center">
#               <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg focus:outline-none focus:shadow-outline transition duration-300 ease-in-out">
#                   Add User
#               </button>
#           </div>
#       </form>
#  </div>
#  """

#     # --- User Management Section ---
#     user_list_html = ""
#     if users:
#         # Need a connection to check assigned stalls for the dropdown in update form
#         conn_for_user_list = None
#         try:
#             conn_for_user_list = get_db_connection()
#             # Fetch all stalls for the update assignment dropdown
#             all_stalls_for_user_list = conn_for_user_list.cursor().execute('SELECT name FROM stalls').fetchall()

#             for user in users:
#                 user_list_html += f"""
#                 <li class="bg-green-100 rounded-md p-4 mb-3 flex justify-between items-center flex-wrap border border-green-200 shadow-sm">
#                     <div class="flex-grow mr-4">
#                         <span class="font-semibold text-green-800">{user['username']}</span> <span class="text-gray-600 text-sm">({user['role']})</span><br>
#                         <span class="text-gray-700 text-sm">Assigned: <span class="font-medium">{user['assigned_stall'] if user['assigned_stall'] else 'None'}</span></span><br>
#                         <span class="text-gray-700 text-sm">Applied: <span class="font-medium">{user['applied_stall'] if user['applied_stall'] else 'None'}</span> (<span class="font-medium text-yellow-600">{user['application_status']}</span>)</span>
#                     </div>
#                     <div class="flex items-center space-x-2 mt-2 md:mt-0">
#                 """
#                 # Add remove button for non-admin users
#                 if user['role'] != 'admin':
#                     user_list_html += f"""
#                         <form action="/admin/remove_user" method="post" onsubmit="return confirm('Are you sure you want to remove user {user['username']}?');" class="inline-block">
#                             <input type="hidden" name="user_id" value="{user['id']}">
#                             <button type="submit" class="bg-red-500 hover:bg-red-600 text-white font-bold py-1 px-3 rounded focus:outline-none focus:shadow-outline text-xs transition duration-300 ease-in-out">
#                                 Remove
#                             </button>
#                         </form>
#                     """
#                 # Add update assignment form for non-admin users
#                 if user['role'] != 'admin':
#                      stall_options_update_user = "<option value=''>Unassign</option>"
#                      for stall in all_stalls_for_user_list:
#                           # Check if the stall is assigned to someone else, excluding the current user
#                           is_assigned_to_other = is_stall_assigned(conn_for_user_list, stall['name'], exclude_user_id=user['id'])
#                           stall_options_update_user += f"<option value='{stall['name']}' {'selected' if stall['name'] == user['assigned_stall'] else ''} {'disabled' if is_assigned_to_other else ''}>{stall['name']}</option>"

#                      user_list_html += f"""
#                           <form action="/admin/update_user_assignment" method="post" class="inline-block flex items-center">
#                                <input type="hidden" name="user_id" value="{user['id']}">
#                                <select name="assigned_stall" class="border rounded px-2 py-1 text-xs mr-1 focus:outline-none focus:ring focus:border-yellow-300">
#                                     {stall_options_update_user}
#                                </select>
#                                <button type="submit" class="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-1 px-3 rounded focus:outline-none focus:shadow-outline text-xs transition duration-300 ease-in-out">
#                                    Update Assignment
#                                </button>
#                           </form>
#                      """
#                 # Add application management buttons for pending applications
#                 if user['application_status'] == 'pending':
#                      user_list_html += f"""
#                           <form action="/admin/approve_application" method="post" class="inline-block ml-2">
#                                <input type="hidden" name="user_id" value="{user['id']}">
#                                <button type="submit" class="bg-green-600 hover:bg-green-700 text-white font-bold py-1 px-3 rounded focus:outline-none focus:shadow-outline text-xs transition duration-300 ease-in-out">
#                                    Approve
#                                </button>
#                           </form>
#                            <form action="/admin/decline_application" method="post" class="inline-block ml-2">
#                                 <input type="hidden" name="user_id" value="{user['id']}">
#                                 <button type="submit" class="bg-red-600 hover:bg-red-700 text-white font-bold py-1 px-3 rounded focus:outline-none focus:shadow-outline text-xs transition duration-300 ease-in-out">
#                                     Decline
#                                 </button>
#                            </form>
#                      """
#                 user_list_html += "</div></li>"
#         except Exception as e:
#             print(f"Error generating user list HTML: {e}")
#         finally:
#             if conn_for_user_list:
#                 conn_for_user_list.close()

#     else:
#         user_list_html = "<p class='text-center text-gray-600'>No users found.</p>"

#     # --- Stall Management Section ---
#     stall_list_html = ""
#     if stalls:
#         for stall in stalls:
#             stall_list_html += f"""
#             <li class="bg-green-100 rounded-md p-4 mb-3 flex justify-between items-center flex-wrap border border-green-200 shadow-sm">
#                 <div class="flex-grow mr-4">
#                      <span class="font-semibold text-green-800">{stall['name']}</span><br>
#                      <span class="text-gray-700 text-sm">{stall['description'] if stall['description'] else 'No description'}</span>
#                 </div>
#                 <div class="flex items-center space-x-2 mt-2 md:mt-0">
#                     <form action="/admin/remove_stall" method="post" onsubmit="return confirm('WARNING: This will remove stall {stall['name']} and ALL its items. Are you sure?');" class="inline-block">
#                         <input type="hidden" name="stall_id" value="{stall['id']}">
#                         <button type="submit" class="bg-red-500 hover:bg-red-600 text-white font-bold py-1 px-3 rounded focus:outline-none focus:shadow-outline text-xs transition duration-300 ease-in-out">
#                             Remove
#                         </button>
#                     </form>
#                      <form action="/admin/update_stall" method="post" class="inline-block flex items-center">
#                          <input type="hidden" name="stall_id" value="{stall['id']}">
#                          <input type="text" name="new_name" placeholder="New Name" class="border rounded px-2 py-1 w-20 text-xs mr-1 focus:outline-none focus:ring focus:border-yellow-300">
#                          <input type="text" name="new_description" placeholder="New Description" class="border rounded px-2 py-1 w-20 text-xs mr-1 focus:outline-none focus:ring focus:border-yellow-300">
#                          <input type="text" name="new_image_path" placeholder="New Image Path" class="border rounded px-2 py-1 w-20 text-xs mr-1 focus:outline-none focus:ring focus:border-yellow-300">
#                          <button type="submit" class="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-1 px-3 rounded focus:outline-none focus:shadow-outline text-xs transition duration-300 ease-in-out">
#                              Update
#                          </button>
#                      </form>
#                 </div>
#             </li>
#             """
#     else:
#         stall_list_html = "<p class='text-center text-gray-600'>No stalls found.</p>"

#     # --- Item Management Section (Admin Dashboard) ---
#     item_management_html = ""

#     # Add New Item Form (for Admin Dashboard) - Stays at the top
#     stall_options_add_item = "<option value=''>Select a Stall</option>"
#     for stall in stalls: # Use the already fetched stalls list
#          stall_options_add_item += f"<option value='{stall['name']}'>{stall['name']}</option>"

#     add_item_form_admin = f"""
#     <div class="mt-6 mb-8 p-6 bg-green-200 rounded-xl shadow-md border border-green-300">
#          <h2 class="text-2xl font-bold text-green-900 mb-4">Add New Item (Admin)</h2>
#          <form action="/user/add_item_main" method="post" class="flex flex-col space-y-4">
#              <div>
#                  <label for="admin_add_item_stall" class="block text-gray-700 font-semibold mb-1">Select Stall:</label>
#                  <select id="admin_add_item_stall" name="stall_name" required class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400">
#                      {stall_options_add_item}
#                  </select>
#              </div>
#              <div>
#                  <label for="admin_add_item_name" class="block text-gray-700 font-semibold mb-1">Item Name:</label>
#                  <input type="text" id="admin_add_item_name" name="item_name" required class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400">
#              </div>
#              <div>
#                  <label for="admin_add_item_description" class="block text-gray-700 font-semibold mb-1">Description (Optional):</label>
#                  <textarea id="admin_add_item_description" name="description" rows="2" class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400"></textarea>
#              </div>
#               <div>
#                   <label for="admin_add_item_image_path" class="block text-gray-700 font-semibold mb-1">Image Path (Optional, e.g., /stall_images/item.jpg):</label>
#                   <input type="text" id="admin_add_item_image_path" name="image_path" class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400">
#               </div>
#              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
#                   <div>
#                        <label for="admin_first_variation_size" class="block text-gray-700 font-semibold mb-1">First Variation Size (e.g., Regular):</label>
#                        <input type="text" id="admin_first_variation_size" name="first_variation_size" value="N/A" class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400">
#                   </div>
#                   <div>
#                        <label for="admin_first_variation_price" class="block text-gray-700 font-semibold mb-1">First Variation Price:</label>
#                        <input type="number" id="admin_first_variation_price" name="first_variation_price" step="0.01" required class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400">
#                   </div>
#                   <div>
#                        <label for="admin_first_variation_stock" class="block text-gray-700 font-semibold mb-1">First Variation Stock:</label>
#                        <input type="number" id="admin_first_variation_stock" name="first_variation_stock" value="0" min="0" class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400">
#                   </div>
#              </div>
#              <div class="text-center">
#                  <button type="submit" class="bg-green-700 hover:bg-green-800 text-white font-bold py-2 px-6 rounded-lg focus:outline-none focus:shadow-outline transition duration-300 ease-in-out">
#                      Add Item
#                  </button>
#              </div>
#          </form>
#     </div>
#     """

#     # List items organized by stall using collapsible details
#     if items_by_stall:
#         for stall_name, items_list in items_by_stall.items():
#             item_management_html += f"""
#             <details class="stall-items-details bg-green-100 rounded-lg shadow-md p-4 mb-4 border border-green-200">
#                 <summary class="cursor-pointer text-xl font-semibold text-green-800">
#                     {stall_name}'s Items ({len(items_list)})
#                 </summary>
#                 <div class="stall-items-content mt-4 pt-4 border-t border-green-200">
#             """
#             conn_for_variations = None
#             try:
#                 conn_for_variations = get_db_connection()
#                 cursor_for_variations = conn_for_variations.cursor()

#                 for item in items_list:
#                      item_management_html += f"""
#                      <details class="item-details bg-white rounded-lg shadow-md p-4 mb-3 border border-green-200">
#                          <summary class="cursor-pointer flex items-center justify-between text-lg font-semibold text-green-800">
#                              <div class="flex items-center">
#                                   <img src="{item['image_path'] if item['image_path'] and os.path.exists(item['image_path'][1:]) else '/stall_images/placeholder.jpg'}" alt="{item['item_name']}" class="w-12 h-12 object-cover rounded-md mr-4 border border-gray-200">
#                                   <span>{item['item_name']}</span>
#                              </div>
#                              <span class="text-sm text-gray-500 ml-4">Click to see details</span>
#                          </summary>
#                          <div class="item-content mt-4 pt-4 border-t border-gray-200">
#                              <p class="text-gray-700 text-sm mb-3">{item['description'] if item['description'] else 'No description available.'}</p>

#                              <h4 class="text-md font-medium text-green-700 mb-2">Variations:</h4>
#                              <ul class="list-none p-0">
#                      """
#                      # Fetch variations for the current item
#                      cursor_for_variations.execute('SELECT id, size, price, stock FROM item_variations WHERE item_id = ? ORDER BY size', (item['id'],))
#                      variations = cursor_for_variations.fetchall()

#                      if variations:
#                          for variation in variations:
#                              # Add 'out-of-stock' class if stock is 0
#                              stock_class = 'text-red-600 font-bold' if variation['stock'] <= 0 else ''
#                              stock_text = f"Stock: {variation['stock']}" if variation['stock'] > 0 else "Out of Stock"
#                              item_management_html += f"""
#                                  <li class="flex justify-between items-center bg-green-50 rounded-md p-2 mb-1 border border-green-100 flex-wrap">
#                                      <span class="text-gray-800 text-sm mr-4 flex-grow">{variation['size']} - ₱{variation['price']:.2f}</span>
#                                      <span class="text-gray-600 text-sm {stock_class}">{stock_text}</span>
#                                      <div class="flex items-center space-x-2 mt-2 md:mt-0">
#                                          <form action="/user/remove_item_variation" method="post" onsubmit="return confirm('Are you sure you want to remove this variation?');" class="inline-block">
#                                              <input type="hidden" name="variation_id" value="{variation['id']}">
#                                              <button type="submit" class="bg-red-500 hover:bg-red-600 text-white font-bold py-0.5 px-2 rounded focus:outline-none focus:shadow-outline text-xs transition duration-300 ease-in-out">
#                                                  Remove
#                                              </button>
#                                          </form>
#                                          <form action="/user/update_item_variation" method="post" class="inline-block flex items-center">
#                                               <input type="hidden" name="variation_id" value="{variation['id']}">
#                                               <input type="text" name="new_size" placeholder="Size" class="border rounded px-1 py-0.5 w-16 text-xs mr-1 focus:outline-none focus:ring focus:border-yellow-300">
#                                               <input type="number" name="new_price" placeholder="Price" step="0.01" class="border rounded px-1 py-0.5 w-14 text-xs mr-1 focus:outline-none focus:ring focus:border-yellow-300">
#                                               <input type="number" name="new_stock" placeholder="Stock" class="border rounded px-1 py-0.5 w-12 text-xs mr-1 focus:outline-none focus:ring focus:border-yellow-300">
#                                               <button type="submit" class="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-0.5 px-2 rounded focus:outline-none focus:shadow-outline text-xs transition duration-300 ease-in-out">
#                                                   Update
#                                               </button>
#                                              </form>
#                                          </div>
#                                      </li>
#                                  """
#                          item_management_html += "</ul>" # Close variations list

#                      else:
#                          item_management_html += "<p class='text-gray-600 text-sm ml-4'>No variations available for this item.</p>"

#                      # Add Variation form for this item (MOVED OUTSIDE VARIATION LOOP)
#                      item_management_html += f"""
#                      <div class="mt-4 p-3 bg-green-200 rounded-md border border-green-300">
#                           <h5 class="text-sm font-medium text-green-900 mb-2">Add New Variation for {item['item_name']}:</h5>
#                           <form action="/user/add_item_variation" method="post" class="flex flex-wrap items-center space-x-2">
#                               <input type="hidden" name="item_id" value="{item['id']}">
#                               <input type="text" name="size" placeholder="Size" class="border rounded px-2 py-1 w-20 text-xs focus:outline-none focus:ring focus:border-green-400">
#                               <input type="number" name="price" placeholder="Price" step="0.01" required class="border rounded px-2 py-1 w-16 text-xs focus:outline-none focus:ring focus:border-green-400">
#                               <input type="number" name="stock" placeholder="Stock" value="0" min="0" class="border rounded px-2 py-1 w-14 text-xs focus:outline-none focus:ring focus:border-green-400">
#                               <button type="submit" class="bg-green-700 hover:bg-green-800 text-white font-bold py-1 px-3 rounded focus:outline-none focus:shadow-outline text-xs transition duration-300 ease-in-out">
#                                   Add Variation
#                               </button>
#                           </form>
#                      </div>
#                      """

#                      item_management_html += "</div>" # Close item-content div
#                      item_management_html += "</details>" # Close item-details (collapsible)

#                 # Add a form to remove the main item
#                 item_management_html += f"""
#                      <div class="mt-4 text-center">
#                          <form action="/user/remove_item_main" method="post" onsubmit="return confirm('WARNING: This will remove this item and ALL its variations. Are you sure?');" class="inline-block">
#                              <input type="hidden" name="item_id" value="{item['id']}">
#                              <button type="submit" class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300 ease-in-out">
#                                  Remove Item
#                              </button>
#                          </form>
#                      </div>
#                 """


#             except Exception as e:
#                  print(f"Error generating item management HTML for stall {stall_name}: {e}")
#             finally:
#                  if conn_for_variations:
#                       conn_for_variations.close()


#             item_management_html += "</div>" # Close stall-items-content div
#             item_management_html += "</details>" # Close stall-items-details (collapsible)

#     else:
#         item_management_html = "<p class='text-center text-gray-600'>No items found.</p>"


#     return f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Admin Dashboard</title>
#         <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
#         <link rel="preconnect" href="https://fonts.googleapis.com">
#         <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
#         <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap" rel="stylesheet">
#         <link rel="stylesheet" href="/style.css">
#     </head>
#     <body class="bg-green-50 min-h-screen m-0 relative font-nunito default-background">
#         <div class="kiosk-header bg-white shadow-md p-4 text-center border-b border-green-200 flex justify-between items-center">
#              <img src="/secondpageimg/craveeatsnobg.png" alt="CraveEats Logo" class="h-16">
#              <form action="/logout" method="post" class="inline-block">
#                  <button type="submit" class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300 ease-in-out">
#                      Logout
#                  </button>
#              </form>
#         </div>
#         <div class="container mx-auto p-4 mt-4 animate-fade-in">
#             <div class="admin-container bg-white rounded-xl shadow-lg p-6 border border-green-200">
#                 <h1 class="text-3xl font-bold text-green-800 text-center mb-6">Admin Dashboard</h1>

#                 <div class="flex flex-wrap -mx-3 mb-6">
#                      <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
#                          <div class="p-6 bg-green-100 rounded-xl border border-green-200 h-full">
#                              <h2 class="text-2xl font-semibold text-green-800 mb-4">User Management</h2>
#                              <ul class="list-none p-0 space-y-3 max-h-96 overflow-y-auto">
#                                  {user_list_html}
#                              </ul>
#                              {add_user_form}
#                          </div>
#                      </div>
#                      <div class="w-full md:w-1/2 px-3">
#                          <div class="p-6 bg-green-100 rounded-xl border border-green-200 h-full">
#                              <h2 class="text-2xl font-semibold text-green-800 mb-4">Stall Management</h2>
#                              <ul class="list-none p-0 space-y-3 max-h-96 overflow-y-auto">
#                                  {stall_list_html}
#                              </ul>
#                              {add_stall_form}
#                          </div>
#                      </div>
#                 </div>


#                  <div class="p-6 bg-green-100 rounded-xl border border-green-200">
#                      <h2 class="text-2xl font-semibold text-green-800 mb-4">Item Management</h2>
#                      {add_item_form_admin}
#                      <div class="mt-6">
#                          {item_management_html}
#                      </div>
#                  </div>


#             </div>
#         </div>
#     </body>
#     </html>
#     """

# def get_user_dashboard(user):
#     # Generates the HTML for the user dashboard with pastel theme and background.
#     conn = None
#     assigned_stall_name = user['assigned_stall']
#     assigned_stall_html = ""
#     item_management_html = ""
#     application_status_html = ""
#     items = []
#     stalls = [] # Needed for the re-apply dropdown

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         if assigned_stall_name:
#             assigned_stall_html = f"""
#             <p class='text-gray-700 mb-4 text-center'>You are assigned to manage the stall: <span class='font-semibold text-green-800'>{assigned_stall_name}</span></p>
#             <div class="mt-6 p-6 bg-green-100 rounded-xl shadow-md border border-green-200">
#                  <h2 class="text-2xl font-bold text-green-800 mb-4 text-center">Your Stall's Menu</h2>
#             """
#             # Fetch items for the assigned stall
#             cursor.execute('SELECT id, name, description, image_path FROM items WHERE stall_id = (SELECT id FROM stalls WHERE name = ?) ORDER BY name', (assigned_stall_name,))
#             items = cursor.fetchall()

#             item_list_html = ""
#             # Add New Item form for the assigned stall at the top of the item list (MOVED OUTSIDE ITEM LOOP)
#             assigned_stall_data = get_stall_by_name(conn, assigned_stall_name)
#             if assigned_stall_data:
#                 item_list_html += f"""
#                 <div class="mb-8 p-6 bg-green-200 rounded-xl shadow-md border border-green-300">
#                      <h3 class="text-xl font-bold text-green-900 mb-4 text-center">Add New Item to Your Stall</h3>
#                      <form action="/user/add_item_main" method="post" class="flex flex-col space-y-4">
#                          <input type="hidden" name="stall_name" value="{assigned_stall_name}">
#                          <div>
#                              <label for="user_item_name" class="block text-gray-700 font-semibold mb-1">Item Name:</label>
#                              <input type="text" id="user_item_name" name="item_name" required class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400">
#                          </div>
#                          <div>
#                              <label for="user_description" class="block text-gray-700 font-semibold mb-1">Description (Optional):</label>
#                              <textarea id="user_description" name="description" rows="2" class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400"></textarea>
#                          </div>
#                           <div>
#                               <label for="user_image_path" class="block text-gray-700 font-semibold mb-1">Image Path (Optional, e.g., /stall_images/item.jpg):</label>
#                               <input type="text" id="user_image_path" name="image_path" class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400">
#                           </div>
#                          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
#                               <div>
#                                    <label for="user_first_variation_size" class="block text-gray-700 font-semibold mb-1">First Variation Size (e.g., Regular):</label>
#                                    <input type="text" id="user_first_variation_size" name="first_variation_size" value="N/A" class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400">
#                               </div>
#                               <div>
#                                    <label for="user_first_variation_price" class="block text-gray-700 font-semibold mb-1">First Variation Price:</label>
#                                    <input type="number" id="user_first_variation_price" name="first_variation_price" step="0.01" required class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400">
#                               </div>
#                               <div>
#                                    <label for="user_first_variation_stock" class="block text-gray-700 font-semibold mb-1">First Variation Stock:</label>
#                                    <input type="number" id="user_first_variation_stock" name="first_variation_stock" value="0" min="0" class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400">
#                                   </div>
#                              </div>
#                          <div class="text-center">
#                              <button type="submit" class="bg-green-700 hover:bg-green-800 text-white font-bold py-2 px-6 rounded-lg focus:outline-none focus:shadow-outline transition duration-300 ease-in-out">
#                                  Add Item
#                              </button>
#                          </div>
#                      </form>
#                 </div>
#                 """

#             if items:
#                 for item in items:
#                     item_list_html += f"""
#                      <details class="item-details bg-white rounded-lg shadow-md p-4 mb-3 border border-green-200">
#                          <summary class="cursor-pointer flex items-center justify-between text-lg font-semibold text-green-800">
#                              <div class="flex items-center">
#                                   <img src="{item['image_path'] if item['image_path'] and os.path.exists(item['image_path'][1:]) else '/stall_images/placeholder.jpg'}" alt="{item['name']}" class="w-12 h-12 object-cover rounded-md mr-4 border border-gray-200">
#                                   <span>{item['name']}</span>
#                              </div>
#                              <span class="text-sm text-gray-500 ml-4">Click to see details</span>
#                          </summary>
#                          <div class="item-content mt-4 pt-4 border-t border-gray-200">
#                              <p class="text-gray-700 text-sm mb-3">{item['description'] if item['description'] else 'No description available.'}</p>

#                              <h4 class="text-md font-medium text-green-700 mb-2">Variations:</h4>
#                              <ul class="list-none p-0 space-y-2">
#                      """
#                     # Fetch variations for the current item
#                     cursor.execute('SELECT id, size, price, stock FROM item_variations WHERE item_id = ? ORDER BY size', (item['id'],))
#                     variations = cursor.fetchall()

#                     if variations:
#                         for variation in variations:
#                             # Add 'out-of-stock' class if stock is 0
#                             stock_class = 'text-red-600 font-bold' if variation['stock'] <= 0 else ''
#                             stock_text = f"Stock: {variation['stock']}" if variation['stock'] > 0 else "Out of Stock"
#                             item_list_html += f"""
#                                 <li class="flex justify-between items-center bg-green-50 rounded-md p-2 border border-green-100 flex-wrap">
#                                     <span class="text-gray-800 text-sm mr-4 flex-grow">{variation['size']} - ₱{variation['price']:.2f}</span>
#                                     <span class="text-gray-600 text-sm {stock_class}">{stock_text}</span>
#                                     <div class="flex items-center space-x-2 mt-2 md:mt-0">
#                                         <form action="/user/remove_item_variation" method="post" onsubmit="return confirm('Are you sure you want to remove this variation?');" class="inline-block">
#                                             <input type="hidden" name="variation_id" value="{variation['id']}">
#                                             <button type="submit" class="bg-red-500 hover:bg-red-600 text-white font-bold py-1 px-3 rounded focus:outline-none focus:shadow-outline text-xs transition duration-300 ease-in-out">
#                                                 Remove
#                                             </button>
#                                         </form>
#                                         <form action="/user/update_item_variation" method="post" class="inline-block flex items-center space-x-1">
#                                              <input type="hidden" name="variation_id" value="{variation['id']}">
#                                              <input type="text" name="new_size" placeholder="Size" class="border rounded px-1 py-0.5 w-16 text-xs focus:outline-none focus:ring focus:border-yellow-300">
#                                              <input type="number" name="new_price" placeholder="Price" step="0.01" class="border rounded px-1 py-0.5 w-14 text-xs focus:outline-none focus:ring focus:border-yellow-300">
#                                              <input type="number" name="new_stock" placeholder="Stock" class="border rounded px-1 py-0.5 w-12 text-xs focus:outline-none focus:ring focus:border-yellow-300">
#                                              <button type="submit" class="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-0.5 px-2 rounded focus:outline-none focus:shadow-outline text-xs transition duration-300 ease-in-out">
#                                                  Update
#                                              </button>
#                                         </form>
#                                     </div>
#                                 </li>
#                             """
#                         item_list_html += "</ul>" # Close variations list

#                     else:
#                         item_list_html += "<p class='text-gray-600 text-sm ml-4'>No variations available for this item.</p>"

#                     # Add Variation form for this item (MOVED OUTSIDE VARIATION LOOP)
#                     item_list_html += f"""
#                     <div class="mt-4 p-3 bg-green-200 rounded-md border border-green-300">
#                          <h5 class="text-sm font-medium text-green-900 mb-2">Add New Variation for {item['name']}:</h5>
#                          <form action="/user/add_item_variation" method="post" class="flex flex-wrap items-center space-x-2">
#                              <input type="hidden" name="item_id" value="{item['id']}">
#                              <input type="text" name="size" placeholder="Size" class="border rounded px-2 py-1 w-20 text-xs focus:outline-none focus:ring focus:border-green-400">
#                              <input type="number" name="price" placeholder="Price" step="0.01" required class="border rounded px-2 py-1 w-16 text-xs focus:outline-none focus:ring focus:border-green-400">
#                              <input type="number" name="stock" placeholder="Stock" value="0" min="0" class="border rounded px-2 py-1 w-14 text-xs focus:outline-none focus:ring focus:border-green-400">
#                              <button type="submit" class="bg-green-700 hover:bg-green-800 text-white font-bold py-1 px-3 rounded focus:outline-none focus:shadow-outline text-xs transition duration-300 ease-in-out">
#                                  Add Variation
#                              </button>
#                          </form>
#                     </div>
#                     """


#                     item_list_html += "</div>" # Close item-content div
#                     item_list_html += "</details>" # Close item-details (collapsible)

#                 # Add a form to remove the main item
#                 item_list_html += f"""
#                      <div class="mt-4 text-center">
#                          <form action="/user/remove_item_main" method="post" onsubmit="return confirm('WARNING: This will remove this item and ALL its variations. Are you sure?');" class="inline-block">
#                              <input type="hidden" name="item_id" value="{item['id']}">
#                              <button type="submit" class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300 ease-in-out">
#                                  Remove Item
#                              </button>
#                          </form>
#                      </div>
#                 """


#             else:
#                 # If no items exist, still show the "Add New Item" form
#                 assigned_stall_data = get_stall_by_name(conn, assigned_stall_name)
#                 if assigned_stall_data:
#                     item_list_html += f"""
#                     <div class="mb-8 p-6 bg-green-200 rounded-xl shadow-md border border-green-300">
#                          <h3 class="text-xl font-bold text-green-900 mb-4 text-center">Add New Item to Your Stall</h3>
#                          <form action="/user/add_item_main" method="post" class="flex flex-col space-y-4">
#                              <input type="hidden" name="stall_name" value="{assigned_stall_name}">
#                              <div>
#                                  <label for="user_item_name" class="block text-gray-700 font-semibold mb-1">Item Name:</label>
#                                  <input type="text" id="user_item_name" name="item_name" required class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400">
#                              </div>
#                              <div>
#                                  <label for="user_description" class="block text-gray-700 font-semibold mb-1">Description (Optional):</label>
#                                  <textarea id="user_description" name="description" rows="2" class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400"></textarea>
#                              </div>
#                               <div>
#                                   <label for="user_image_path" class="block text-gray-700 font-semibold mb-1">Image Path (Optional, e.g., /stall_images/item.jpg):</label>
#                                   <input type="text" id="user_image_path" name="image_path" class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400">
#                               </div>
#                              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
#                                   <div>
#                                        <label for="user_first_variation_size" class="block text-gray-700 font-semibold mb-1">First Variation Size (e.g., Regular):</label>
#                                        <input type="text" id="user_first_variation_size" name="first_variation_size" value="N/A" class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400">
#                                   </div>
#                                   <div>
#                                        <label for="user_first_variation_price" class="block text-gray-700 font-semibold mb-1">First Variation Price:</label>
#                                        <input type="number" id="user_first_variation_price" name="first_variation_price" step="0.01" required class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400">
#                                   </div>
#                                   <div>
#                                        <label for="user_first_variation_stock" class="block text-gray-700 font-semibold mb-1">First Variation Stock:</label>
#                                        <input type="number" id="user_first_variation_stock" name="first_variation_stock" value="0" min="0" class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-green-400">
#                                   </div>
#                              </div>
#                              <div class="text-center">
#                                  <button type="submit" class="bg-green-700 hover:bg-green-800 text-white font-bold py-2 px-6 rounded-lg focus:outline-none focus:shadow-outline transition duration-300 ease-in-out">
#                                      Add Item
#                                  </button>
#                              </div>
#                          </form>
#                     </div>
#                     """
#                 else:
#                      item_list_html = "<p class='text-center text-gray-600'>Could not retrieve stall data.</p>"


#             item_management_html += item_list_html # Add the list of items
#             item_management_html += "</div>" # Close the assigned stall items div

#         else:
#             # If no stall is assigned, show application status and form
#             application_status = user['application_status']
#             applied_stall = user['applied_stall']

#             if application_status == 'none':
#                 application_status_html = "<p class='text-gray-700 mb-4 text-center'>You are not currently assigned to a stall.</p>"
#                 # Form to apply for a stall
#                 cursor.execute('SELECT name FROM stalls')
#                 stalls = cursor.fetchall()
#                 # Use the existing connection for is_stall_assigned inside the loop
#                 stall_options = "<option value=''>Select a Stall to Apply For</option>"
#                 for stall in stalls:
#                      # Only show stalls that are not currently assigned
#                      if not is_stall_assigned(conn, stall['name']):
#                          stall_options += f"<option value='{stall['name']}'>{stall['name']}</option>"


#                 application_status_html += f"""
#                      <div class="user-dashboard-apply-form mt-6 p-6 bg-yellow-100 rounded-xl shadow-md border border-yellow-200">
#                           <h3 class="text-xl font-bold text-yellow-800 mb-4 text-center">Apply to Manage a Stall</h3>
#                           <form action="/register" method="post" class="flex flex-col space-y-4">
#                               <input type="hidden" name="reg_username" value="{user['username']}">
#                               <input type="hidden" name="reg_password" value="">
#                               <div>
#                                   <label for="apply_stall" class="block text-gray-700 font-semibold mb-1 text-left">Choose a Stall:</label>
#                                   <select id="apply_stall" name="apply_stall" required class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-yellow-300">
#                                       {stall_options}
#                                   </select>
#                               </div>
#                               <div class="text-center">
#                                   <button type="submit" class="bg-yellow-600 hover:bg-yellow-700 text-white font-bold py-2 px-6 rounded-lg focus:outline-none focus:shadow-outline transition duration-300 ease-in-out">
#                                       Submit Application
#                                   </button>
#                               </div>
#                           </form>
#                      </div>
#                 """
#             elif application_status == 'pending':
#                 application_status_html = f"<p class='text-gray-700 mb-4 text-center'>Your application to manage stall <span class='font-semibold text-green-800'>{applied_stall if applied_stall else 'N/A'}</span> is currently <span class='font-semibold text-yellow-600'>pending</span> review.</p>"
#             elif application_status == 'declined':
#                 application_status_html = "<p class='text-gray-700 mb-4 text-center'>Your previous application was <span class='font-semibold text-red-600'>declined</span>.</p>"
#                 # Option to re-apply
#                 cursor.execute('SELECT name FROM stalls')
#                 stalls = cursor.fetchall()
#                 # Use the existing connection for is_stall_assigned inside the loop
#                 stall_options = "<option value=''>Select a Stall to Re-apply For</option>"
#                 for stall in stalls:
#                      # Only show stalls that are not currently assigned
#                      if not is_stall_assigned(conn, stall['name']):
#                          stall_options += f"<option value='{stall['name']}'>{stall['name']}</option>"


#                 application_status_html += f"""
#                      <div class="user-dashboard-apply-form mt-6 p-6 bg-yellow-100 rounded-xl shadow-md border border-yellow-200">
#                           <h3 class="text-xl font-bold text-yellow-800 mb-4 text-center">Re-apply to Manage a Stall</h3>
#                           <form action="/register" method="post" class="flex flex-col space-y-4">
#                               <input type="hidden" name="reg_username" value="{user['username']}">
#                               <input type="hidden" name="reg_password" value="">
#                               <div>
#                                   <label for="apply_stall" class="block text-gray-700 font-semibold mb-1 text-left">Choose a Stall:</label>
#                                   <select id="apply_stall" name="apply_stall" required class="border rounded px-3 py-2 w-full focus:outline-none focus:ring focus:border-yellow-300">
#                                       {stall_options}
#                                   </select>
#                               </div>
#                               <div class="text-center">
#                                   <button type="submit" class="bg-yellow-600 hover:bg-yellow-700 text-white font-bold py-2 px-6 rounded-lg focus:outline-none focus:shadow-outline transition duration-300 ease-in-out">
#                                       Submit Re-application
#                                   </button>
#                               </div>
#                           </form>
#                      </div>
#                 """
#     except Exception as e:
#          print(f"Error generating user dashboard HTML: {e}")
#     finally:
#          if conn:
#               conn.close()


#     return f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>User Dashboard</title>
#         <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
#         <link rel="preconnect" href="https://fonts.googleapis.com">
#         <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
#         <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap" rel="stylesheet">
#         <link rel="stylesheet" href="/style.css">
#     </head>
#     <body class="bg-green-50 min-h-screen m-0 relative font-nunito default-background">
#         <div class="kiosk-header bg-white shadow-md p-4 text-center border-b border-green-200 flex justify-between items-center">
#              <img src="/secondpageimg/craveeatsnobg.png" alt="CraveEats Logo" class="mx-auto h-16">
#              <form action="/logout" method="post" class="inline-block">
#                  <button type="submit" class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300 ease-in-out">
#                      Logout
#                  </button>
#              </form>
#         </div>
#         <div class="container mx-auto p-4 mt-4 animate-fade-in">
#             <div class="user-dashboard bg-white rounded-xl shadow-lg p-6 border border-green-200">
#                 <h1 class="text-3xl font-bold text-green-800 mb-6 text-center">Welcome, {user['username']}!</h1>

#                 {assigned_stall_html}
#                 {application_status_html}
#                 {item_management_html}


#                 <div class="text-center mt-8">
#                     <a href="/second" class="back-button bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline inline-block transition duration-300 ease-in-out">
#                         View Stalls (Customer View)
#                     </a>
#                 </div>
#             </div>
#         </div>
#     </body>
#     </html>
#     """
import os
from urllib.parse import urlencode, quote, parse_qs
from datetime import datetime
# Assuming db.py and session.py are in the same directory
from db import get_db_connection, get_stall_by_name, is_stall_assigned, get_stall_by_id, get_user_by_id, get_user_assigned_stall
from session import get_current_user_from_request

# --- HTML Generation Functions ---

def get_error_page(title, message):
    # Generates a generic HTML error page with pastel theme and background.
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Error: {title}</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/style.css">
    </head>
    <body class="bg-green-50 flex justify-center items-center min-h-screen m-0 relative font-poppins default-background">
        <div class="error-container bg-white rounded-xl shadow-lg p-8 text-center w-4/5 max-w-md border border-green-200 animate-fade-in">
            <h1 class="text-3xl font-bold text-red-600 mb-4">{title}</h1>
            <p class="text-gray-700 mb-6">{message}</p>
            <a href="/" class="btn btn-primary">
                Go to Home Page
            </a>
             <a href="/second" class="btn btn-secondary ml-4">
                View Stalls
             </a>
        </div>
    </body>
    </html>
    """

def get_first_page(username):
    # Generates the HTML for the first page with pastel theme and background.
    logged_in_message = f"<p class='text-center text-gray-600 mt-4'>Logged in as: {username}</p>" if username else ""
    logout_button = "<div class='text-center mt-4'><form action='/logout' method='post'><button type='submit' class='btn btn-danger'>Logout</button></form></div>" if username else ""

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to CraveEats Kiosk</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/style.css">
    </head>
    <body class="bg-green-50 flex justify-center items-center min-h-screen m-0 relative font-poppins default-background">
        <div class="kiosk-container bg-white rounded-xl shadow-lg p-8 text-center w-4/5 max-w-lg animate-fade-in border border-green-200">
            <div class="logo mb-6">
                <img src="/secondpageimg/craveeatsnobg.png" alt="CraveEats Logo" class="mx-auto h-24 animate-pulse">
            </div>
            <h1 class="text-4xl font-bold text-green-800 mb-4 animate-fade-down">Welcome to CraveEats Kiosk!</h1>
            <p class="text-gray-700 mb-6 animate-fade-down animation-delay-100">Your one-stop shop for delicious treats.</p>
            <a href="/choice" class="btn btn-primary btn-lg animate-bounce">
                Start Ordering
            </a>
            {logged_in_message}
            {logout_button}
        </div>
         <div class="admin-button absolute top-4 right-4">
             <a href="/login.html" class="btn btn-secondary">
                 Login/Register
             </a>
         </div>
         <div class="umak-logo absolute bottom-4 left-4">
             <img src="/secondpageimg/umaklogo.png" alt="UMAK Logo" class="h-10">
         </div>
    </body>
    </html>
    """

def get_choice_page(username):
    # Generates the HTML for the choice page (Customer or Stall Owner) with pastel theme and background.
    logged_in_message = f"<p class='text-center text-gray-600 mt-4'>Logged in as: {username}</p>" if username else ""
    logout_button = "<div class='text-center mt-4'><form action='/logout' method='post'><button type='submit' class='btn btn-danger'>Logout</button></form></div>" if username else ""

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Choose Your Role</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/style.css">
    </head>
    <body class="bg-green-50 flex justify-center items-center min-h-screen m-0 relative font-poppins default-background">
        <div class="choice-container bg-white rounded-xl shadow-lg p-8 text-center w-4/5 max-w-md animate-fade-in border border-green-200">
            <h1 class="text-3xl font-bold text-green-800 mb-6 animate-fade-down">Are you a Customer or a Stall Owner?</h1>
            <div class="choice-buttons flex flex-col space-y-4"> 
                <a href="/second" class="btn btn-primary block animate-slide-in">
                    Customer
                </a>
                <a href="/login.html" class="btn btn-secondary block animate-slide-in animation-delay-100">
                    Stall Owner
                </a>
                <a href="/" class="btn btn-outline mt-2"> 
                    Back to Home
                </a>
            </div>
            {logged_in_message}
            {logout_button}
        </div>
         <div class="admin-button absolute top-4 right-4">
             <a href="/login.html" class="btn btn-secondary">
                 Login/Register
             </a>
         </div>
    </body>
    </html>
    """

def get_second_page(username, role, cart_item_count):
    # Generates the HTML for the second page, listing stalls, with pastel theme and background.
    conn = None
    stalls = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, description, image_path FROM stalls')
        stalls = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching stalls for second page: {e}")
    finally:
        if conn:
            conn.close()

    stalls_html = ""
    if stalls:
        for stall in stalls:
            # Correctly encode stall name for the URL path using quote
            stall_url_name = quote(stall['name'])
            stalls_html += f"""
            <a href="/stall/{stall_url_name}" class="option-card bg-white rounded-lg shadow-md p-4 text-center transition duration-300 ease-in-out transform hover:scale-105 hover:shadow-xl border border-green-100">
                <img src="{stall['image_path'] if stall['image_path'] and os.path.exists(stall['image_path'][1:]) else '/stall_images/placeholder.jpg'}" alt="{stall['name']}" class="mx-auto h-24 w-auto object-cover rounded-md mb-2 border border-gray-200">
                <h3 class="text-lg font-semibold text-green-800">{stall['name']}</h3>
                <p class="text-sm text-gray-600">{stall['description'] if stall['description'] else 'No description available.'}</p>
            </a>
            """
    else:
        stalls_html = "<p class='text-center text-gray-600'>No stalls available yet.</p>"

    logged_in_message = f"<p class='text-center text-gray-600 mt-4'>Logged in as: {username}</p>" if username else ""
    logout_button = "<div class='text-center mt-4'><form action='/logout' method='post'><button type='submit' class='btn btn-danger'>Logout</button></form></div>" if username else ""


    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Available Stalls</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/style.css">
    </head>
    <body class="bg-green-50 min-h-screen m-0 relative font-poppins default-background">
        <div class="kiosk-header bg-white shadow-md p-4 text-center border-b border-green-200">
             <img src="/secondpageimg/craveeatsnobg.png" alt="CraveEats Logo" class="mx-auto h-16">
        </div>
        <div class="container mx-auto p-4 mt-4 animate-fade-in">
            <h1 class="text-3xl font-bold text-green-800 text-center mb-6">Choose a Stall</h1>
            <div class="options-container grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {stalls_html}
            </div>
            <div class="text-center mt-8 flex justify-center space-x-4">
                <a href="/choice" class="btn btn-outline">
                    Back to Choices
                </a>
                <a href="/cart" class="btn btn-secondary ml-4">
                     View Cart ({cart_item_count})
                </a>
            </div>
             <div class="admin-button absolute top-4 right-4">
                 <a href="/login.html" class="btn btn-secondary">
                     Login/Register
                 </a>
             </div>
        </body>
    </html>
    """

def get_stall_page(stall_data, username, role, query_params):
    # Generates the HTML for an individual stall's page with background. This is primarily for customer view.
    conn = None
    items = []
    message_html = ""

    # Check for messages in query parameters
    if 'success' in query_params:
        if query_params['success'][0] == 'added_to_cart':
            item_name = query_params.get('item', [''])[0]
            item_size = query_params.get('size', [''])[0]
            message_html = f"<div id='notification' class='notification-message success bg-green-500 text-white p-3 rounded-md text-center'>Added {item_name} ({item_size}) to cart!</div>"
        elif query_params['success'][0] == 'remove_item':
             message_html = "<div id='notification' class='notification-message success bg-green-500 text-white p-3 rounded-md text-center'>Item removed successfully!</div>"

    if 'error' in query_params:
        if query_params['error'][0] == 'out_of_stock':
            item_name = query_params.get('item', [''])[0]
            item_size = query_params.get('size', [''])[0]
            message_html = f"<div id='notification' class='notification-message error bg-red-500 text-white p-3 rounded-md text-center'>Sorry, {item_name} ({item_size}) is out of stock or requested quantity exceeds available stock.</div>"
        elif query_params['error'][0] == 'remove_item_missing_info':
             message_html = "<div id='notification' class='notification-message error bg-red-500 text-white p-3 rounded-md text-center'>Error: Missing item information for removal.</div>"
        elif query_params['error'][0] == 'remove_item_error':
             message_html = "<div id='notification' class='notification-message error bg-red-500 text-white p-3 rounded-md text-center'>Error removing item.</div>"


    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch items for this specific stall
        cursor.execute('SELECT id, name, description, image_path FROM items WHERE stall_id = (SELECT id FROM stalls WHERE name = ?) ORDER BY name', (stall_data['name'],))
        items = cursor.fetchall()

    except Exception as e:
        print(f"Error fetching stall data for stall page {stall_data['name']}: {e}")
    finally:
        if conn:
            conn.close()

    item_cards_html = ""
    if items:
        for item in items:
            item_cards_html += f"""
            <div class="item-card bg-white rounded-lg shadow-lg p-4 border border-green-100">
                <div>
                    <img src="{item['image_path'] if item['image_path'] and os.path.exists(item['image_path'][1:]) else '/stall_images/placeholder.jpg'}" alt="{item['name']}" class="mx-auto h-40 w-full object-cover rounded-md mb-3 border border-gray-200 shadow-sm">
                    <h3 class="text-xl font-semibold text-green-800 mb-2">{item['name']}</h3>
                    <p class="text-gray-700 text-sm mb-3">{item['description'] if item['description'] else 'No description available.'}</p>

                    <h4 class="text-md font-medium text-green-700 mb-2">Variations:</h4>
                    <ul class="list-none p-0 space-y-2">
            """
            conn_variations = None
            variations = []
            try:
                conn_variations = get_db_connection()
                cursor_variations = conn_variations.cursor()
                # Fetch variations for the current item
                cursor_variations.execute('SELECT id, size, price, stock FROM item_variations WHERE item_id = ? ORDER BY size', (item['id'],))
                variations = cursor_variations.fetchall()
            except Exception as e:
                print(f"Error fetching variations for item {item['name']}: {e}")
            finally:
                if conn_variations:
                    conn_variations.close()

            if variations:
                for variation in variations:
                    # Add 'out-of-stock' class if stock is 0
                    stock_class = 'text-red-600 font-bold' if variation['stock'] <= 0 else ''
                    stock_text = f"Stock: {variation['stock']}" if variation['stock'] > 0 else "Out of Stock"
                    item_cards_html += f"""
                        <li class="flex justify-between items-center bg-green-50 rounded-md p-2 border border-green-100 flex-wrap">
                            <span class="text-gray-800 text-sm mr-4 flex-grow">{variation['size']} - ₱{variation['price']:.2f}</span>
                            <span class="text-gray-600 text-sm {stock_class}">{stock_text}</span>
                            <div class="flex items-center space-x-2 mt-2 md:mt-0">
                    """
                    # Add to Cart form (visible to all customers) - disabled if stock is 0
                    item_cards_html += f"""
                                 <form action="/add_to_cart" method="post" class="inline-block flex items-center">
                                     <input type="hidden" name="item_variation_id" value="{variation['id']}">
                                      <input type="number" name="quantity" value="1" min="1" max="{variation['stock']}" class="border rounded px-2 py-1 w-16 text-xs focus:outline-none focus:ring focus:border-blue-300 mr-1" {"disabled" if variation['stock'] <= 0 else ""}>
                                     <button type="submit" class="btn btn-sm btn-primary" {"disabled" if variation['stock'] <= 0 else ""}>
                                         Add to Cart
                                     </button>
                                 </form>
                    """
                    item_cards_html += "</div></li>"

                # Add "Remove Item" button for the main item here, below variations
                # Only show remove button if user is logged in (not guest)
                if username:
                    item_cards_html += f"""
                    <li class="text-center mt-4">
                        <form action="/remove_item_main_customer" method="post" onsubmit="return confirm('WARNING: This will remove {item['name']} and ALL its variations from this stall. Are you sure?');" class="inline-block">
                            <input type="hidden" name="item_id" value="{item['id']}">
                            <input type="hidden" name="stall_name" value="{stall_data['name']}">
                            <button type="submit" class="btn btn-sm btn-danger">
                                Remove Item
                            </button>
                        </form>
                    </li>
                    """
            else:
                item_cards_html += "<p class='text-gray-600 text-sm ml-4'>No variations available for this item.</p>"
                # Add "Remove Item" button even if no variations exist, but only if logged in
                if username:
                    item_cards_html += f"""
                    <li class="text-center mt-4">
                        <form action="/remove_item_main_customer" method="post" onsubmit="return confirm('WARNING: This will remove {item['name']} from this stall. Are you sure?');" class="inline-block">
                            <input type="hidden" name="item_id" value="{item['id']}">
                            <input type="hidden" name="stall_name" value="{stall_data['name']}">
                            <button type="submit" class="btn btn-sm btn-danger">
                                Remove Item
                            </button>
                        </form>
                    </li>
                    """


            item_cards_html += "</ul>" # Close variations list

            item_cards_html += "</div>" # Close item card content div
            item_cards_html += "</div>" # Close item card

    else:
        item_cards_html = "<p class='text-center text-gray-600'>No items available at this stall.</p>"

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{stall_data['name']} Menu</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/style.css">
    </head>
    <body class="bg-green-50 min-h-screen m-0 relative font-poppins default-background">
        <div class="kiosk-header bg-white shadow-md p-4 text-center border-b border-green-200">
             <img src="/secondpageimg/craveeatsnobg.png" alt="CraveEats Logo" class="mx-auto h-16">
        </div>
        <div class="container mx-auto p-4 mt-4 animate-fade-in">
            <div class="stall-page bg-white rounded-xl shadow-lg p-6 border border-green-200 relative">
                <h1 class="text-3xl font-bold text-green-800 text-center mb-4">{stall_data['name']}</h1>
                <p class="text-center text-gray-600 mb-6">{stall_data['description'] if stall_data['description'] else 'No description available.'}</p>

                <div id="notification-container">
                    {message_html}
                </div>

                <div class="carousel-container"> 
                    <div class="items-list-carousel"> 
                        {item_cards_html}
                    </div>
                     <button id="prevButton" class="carousel-button left">
                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                             <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
                         </svg>
                     </button>
                     <button id="nextButton" class="carousel-button right">
                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                             <path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z"/>
                         </svg>
                     </button>
                </div>


                <div class="text-center mt-8 flex justify-center space-x-4">
                    <a href="/second" class="btn btn-outline">
                        Back to Stalls
                    </a>
                     <a href="/cart" class="btn btn-secondary ml-4">
                         View Cart
                     </a>
                </div>
            </div>
        </div>
         <script>
             // Script to fade out and hide notification messages
             const notification = document.getElementById('notification');
             if (notification) {{
                 // Use setTimeout to allow the initial display before starting fade out
                 setTimeout(() => {{
                     notification.style.transition = 'opacity 1s ease-out';
                     notification.style.opacity = '0';
                 }}, 3000); // Start fade out after 3 seconds

                 // Use transitionend to set display: none after the fade out is complete
                 notification.addEventListener('transitionend', () => {{
                     if (notification.style.opacity === '0') {{
                         notification.style.display = 'none';
                     }}
                 }});
             }}

             // Carousel Script
             const carousel = document.querySelector('.items-list-carousel');
             const items = document.querySelectorAll('.items-list-carousel .item-card');
             const prevButton = document.getElementById('prevButton');
             const nextButton = document.getElementById('nextButton');

             let currentIndex = 0;

             function updateCarousel() {{
                 // Calculate the scroll position to center the current item
                 const itemWidth = items[0].offsetWidth + parseInt(getComputedStyle(items[0]).marginRight) * 2; // Item width + horizontal margins
                 const scrollLeft = currentIndex * itemWidth;
                 carousel.scrollTo({{
                     left: scrollLeft,
                     behavior: 'smooth'
                 }});

                 // Update button states (optional: disable buttons at ends)
                 prevButton.disabled = currentIndex === 0;
                 nextButton.disabled = currentIndex === items.length - 1;
             }}

             // Event listeners for buttons
             prevButton.addEventListener('click', () => {{
                 if (currentIndex > 0) {{
                     currentIndex--;
                     updateCarousel();
                 }}
             }});

             nextButton.addEventListener('click', () => {{
                 if (currentIndex < items.length - 1) {{
                     currentIndex++;
                     updateCarousel();
                 }}
             }});

             // Initial carousel display
             if (items.length > 0) {{
                  // Center the first item initially
                  const initialScrollLeft = (carousel.offsetWidth - items[0].offsetWidth) / 2 - parseInt(getComputedStyle(items[0]).marginLeft);
                  carousel.scrollTo({{
                       left: initialScrollLeft,
                       behavior: 'auto' // No smooth scroll on initial load
                  }});
                 updateCarousel(); // Update button states
             }} else {{
                 // Hide buttons if no items
                 prevButton.style.display = 'none';
                 nextButton.style.display = 'none';
             }}

             // Optional: Update carousel on window resize
             window.addEventListener('resize', updateCarousel);

         </script>
    </body>
    </html>
    """

def get_cart_page(user_cart):
    # Generates the HTML for the cart page with pastel theme and background.

    cart_items_html = ""
    total_price = 0

    if user_cart:
        for item in user_cart:
            cart_items_html += f"""
            <div class="flex justify-between items-center bg-green-100 rounded-md p-3 mb-3 border border-green-200">
                <span class="text-gray-800 font-medium">{item['name']} ({item['size']})</span>
                <span class="text-gray-700">{item['quantity']} x ₱{item['price']:.2f}</span>
                <span class="font-semibold text-green-700">₱{(item['quantity'] * item['price']):.2f}</span>
            </div>
            """
            total_price += item['quantity'] * item['price']

        # Add checkout button if the cart is not empty
        cart_items_html += f"""
        <div class="mt-6 pt-4 border-t-2 border-green-200 flex justify-between items-center">
            <span class="text-xl font-bold text-green-800">Total:</span>
            <span class="text-xl font-bold text-green-600">₱{total_price:.2f}</span>
        </div>
        <div class="text-center mt-8">
            <form action="/checkout" method="post">
                 <button type="submit" class="btn btn-primary btn-lg">
                     Proceed to Checkout
                 </button>
            </form>
        </div>
        """
    else:
        cart_items_html = "<p class='text-center text-gray-600'>Your cart is empty.</p>"
        total_price = 0 # Ensure total is 0 if cart is empty

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Your Cart</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/style.css">
    </head>
    <body class="bg-green-50 min-h-screen m-0 relative font-poppins default-background">
        <div class="kiosk-header bg-white shadow-md p-4 text-center border-b border-green-200">
             <img src="/secondpageimg/craveeatsnobg.png" alt="CraveEats Logo" class="mx-auto h-16">
        </div>
        <div class="container mx-auto p-4 mt-4 animate-fade-in">
            <div class="cart-container bg-white rounded-xl shadow-lg p-6 border border-green-200">
                <h1 class="text-3xl font-bold text-green-800 text-center mb-6">Your Shopping Cart</h1>
                {cart_items_html}
                <div class="text-center mt-8">
                    <a href="/second" class="btn btn-outline">
                        Continue Shopping
                    </a>
                </div>
            </div>
        </div>
         <div class="admin-button absolute top-4 right-4">
             <a href="/login.html" class="btn btn-secondary">
                 Login/Register
             </a>
         </div>
    </body>
    </html>
    """

def get_receipt_page(receipt_data):
    # Generates the HTML for the e-receipt page with pastel theme and background.
    if not receipt_data:
        return get_error_page("Receipt Not Found", "Could not retrieve receipt details.")

    order_items_html = ""
    for item in receipt_data['items']:
        order_items_html += f"""
        <div class="flex justify-between items-center border-b border-gray-200 py-2">
            <span class="text-gray-700">{item['name']} ({item['size']}) - {item['quantity']} x ₱{item['price']:.2f} ({item['stall']})</span>
            <span class="font-semibold text-green-700">₱{(item['quantity'] * item['price']):.2f}</span>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Order Receipt</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/style.css">
    </head>
    <body class="bg-green-50 flex justify-center items-center min-h-screen m-0 relative font-poppins default-background">
        <div class="receipt-container bg-white rounded-xl shadow-lg p-8 w-4/5 max-w-md border border-green-200 animate-fade-in">
            <h1 class="text-3xl font-bold text-green-800 text-center mb-6">Order Receipt</h1>

            <div class="receipt-details mb-6 text-gray-700"> 
                <p><strong>Order ID:</strong> {receipt_data['order_id']}</p>
                <p><strong>Date & Time:</strong> {receipt_data['order_time']}</p>
                <p><strong>Customer:</strong> {receipt_data['customer']}</p>
            </div>

            <div class="receipt-items-list mb-6"> 
                <h2 class="text-xl font-semibold text-green-700 mb-4">Items:</h2>
                {order_items_html}
            </div>

            <div class="receipt-total mt-6 pt-4 border-t-2 border-green-200 flex justify-between items-center"> 
                <span class="text-xl font-bold text-green-800">Total:</span>
                <span class="text-xl font-bold text-green-600">₱{receipt_data['total_amount']:.2f}</span>
            </div>

            <div class="receipt-footer-buttons text-center mt-8 flex justify-center space-x-4"> 
                <a href="/" class="btn btn-secondary">
                    Back to Home
                </a>
                 <a href="/second" class="btn btn-primary ml-4">
                     Order Again (View Stalls)
                 </a>
            </div>
        </div>
    </body>
    </html>
    """

def get_login_page(query_params):
    # Generates the HTML for the login and registration page with pastel theme and background.
    error_message = ""
    reg_message = "" # Use a single message variable for registration feedback
    # Show register form if 'register=true' is in query params
    show_register_form = 'register' in query_params

    if 'error' in query_params:
        error_type = query_params['error'][0]
        if error_type == 'incorrect_password':
            error_message = "<p class='text-red-500 text-center mb-4'>Incorrect username or password.</p>"
        elif error_type == 'account_not_found':
            error_message = "<p class='text-red-500 text-center mb-4'>Account not found.</p>"
        # Add other login errors here if needed

    if 'reg_status' in query_params: # Use reg_status for clearer feedback
        reg_status_code = query_params['reg_status'][0]
        if reg_status_code == 'success':
            reg_message = "<p class='text-green-500 text-center mb-4'>Registration successful! Please log in.</p>"
        elif reg_status_code == 'exists':
            reg_message = "<p class='text-red-500 text-center mb-4'>Username already exists.</p>"
        elif reg_status_code == 'missing_fields':
            reg_message = "<p class='text-red-500 text-center mb-4'>Username and password are required.</p>"
        elif reg_status_code == 'stall_assigned':
             reg_message = "<p class='text-red-500 text-center mb-4'>The selected stall is already assigned to another user.</p>"
        elif reg_status_code == 'integrity_error':
             reg_message = "<p class='text-red-500 text-center mb-4'>A database error occurred during registration. Please try again.</p>"
        elif reg_status_code == 'general_error':
             reg_message = "<p class='text-red-500 text-center mb-4'>An unexpected error occurred during registration.</p>"
        elif reg_status_code == 'reapplied': # Feedback for successful re-application
             reg_message = "<p class='text-green-500 text-center mb-4'>Re-application submitted! Your status is now pending review.</p>"


    conn = None
    stalls = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Fetch only stalls that are NOT currently assigned
        cursor.execute('SELECT name FROM stalls WHERE name NOT IN (SELECT assigned_stall FROM users WHERE assigned_stall IS NOT NULL)')
        stalls = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching stalls for login page: {e}")
    finally:
        if conn:
            conn.close()

    stall_options = "<option value=''>Select a Stall (Optional)</option>"
    for stall in stalls:
        stall_options += f"<option value='{stall['name']}'>{stall['name']}</option>"

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login or Register</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/style.css">
    </head>
    <body class="bg-green-50 flex justify-center items-center min-h-screen m-0 relative font-poppins default-background">
        <div class="auth-container bg-white rounded-xl shadow-lg p-8 w-4/5 max-w-md animate-fade-in border border-green-200">
            <h1 class="text-3xl font-bold text-green-800 text-center mb-6">Account Access</h1>

            {error_message}
            {reg_message}

            <div id="login-form" class="{'block' if not show_register_form else 'hidden'}">
                <h2 class="text-2xl font-semibold text-green-700 text-center mb-4">Login</h2>
                <form action="/login" method="post" class="space-y-4">
                    <div>
                        <label for="username" class="block text-gray-700 font-semibold mb-1">Username:</label>
                        <input type="text" id="username" name="username" required class="form-input">
                    </div>
                    <div>
                        <label for="password" class="block text-gray-700 font-semibold mb-1">Password:</label>
                        <input type="password" id="password" name="password" required class="form-input">
                    </div>
                    <div class="text-center">
                        <button type="submit" class="btn btn-primary">
                            Login
                        </button>
                    </div>
                </form>
                <p class="text-center text-gray-600 mt-4">Don't have an account? <a href="/login.html?register=true" class="text-blue-600 hover:underline">Register here</a>.</p>
            </div>

            <div id="register-form" class="{'block' if show_register_form else 'hidden'}">
                <h2 class="text-2xl font-semibold text-green-700 text-center mb-4">Register</h2>
                <form action="/register" method="post" class="space-y-4">
                    <div>
                        <label for="reg_username" class="block text-gray-700 font-semibold mb-1">Username:</label>
                        <input type="text" id="reg_username" name="reg_username" required class="form-input">
                    </div>
                    <div>
                        <label for="reg_password" class="block text-gray-700 font-semibold mb-1">Password:</label>
                        <input type="password" id="reg_password" name="reg_password" required class="form-input">
                    </div>
                     <div>
                         <label for="apply_stall" class="block text-gray-700 font-semibold mb-1">Apply to Manage a Stall (Optional):</label>
                         <select id="apply_stall" name="apply_stall" class="form-select">
                             {stall_options}
                         </select>
                     </div>
                    <div class="text-center">
                        <button type="submit" class="btn btn-primary">
                            Register
                        </button>
                    </div>
                </form>
                <p class="text-center text-gray-600 mt-4">Already have an account? <a href="/login.html" class="text-blue-600 hover:underline">Login here</a>.</p>
            </div>

            <div class="text-center mt-6">
                 <a href="/choice" class="btn btn-outline">
                     Back to Choices
                 </a>
            </div>
        </div>
    </body>
    </html>
    """


def get_admin_dashboard(users, stalls, items_by_stall):
    # Generates the HTML for the admin dashboard with pastel theme and enhanced item management.

    # --- Add Stall Form ---
    add_stall_form = f"""
    <div class="p-6 bg-green-200 rounded-xl shadow-md border border-green-300 flex-1 min-w-[300px]">
         <h2 class="text-2xl font-bold text-green-900 mb-4">Add New Stall</h2>
         <form action="/admin/add_stall" method="post" class="flex flex-col space-y-4">
             <div>
                 <label for="stall_name" class="block text-gray-700 font-semibold mb-1">Stall Name:</label>
                 <input type="text" id="stall_name" name="stall_name" required class="form-input">
             </div>
             <div>
                 <label for="stall_description" class="block text-gray-700 font-semibold mb-1">Description (Optional):</label>
                 <textarea id="stall_description" name="description" rows="2" class="form-textarea"></textarea>
             </div>
              <div>
                  <label for="stall_image_path" class="block text-gray-700 font-semibold mb-1">Image Path (Optional, e.g., /stall_images/stall.jpg):</label>
                  <input type="text" id="stall_image_path" name="image_path" class="form-input">
              </div>
             <div class="text-center">
                 <button type="submit" class="btn btn-primary">
                     Add Stall
                 </button>
             </div>
         </form>
    </div>
    """

    # --- Add User Form ---
    # Need a connection to check assigned stalls for the dropdown
    conn_for_user_form = None
    stall_options_for_user_form = "<option value=''>None</option>"
    try:
        conn_for_user_form = get_db_connection()
        cursor_for_user_form = conn_for_user_form.cursor()
        # Fetch only stalls that are NOT currently assigned
        cursor_for_user_form.execute('SELECT name FROM stalls WHERE name NOT IN (SELECT assigned_stall FROM users WHERE assigned_stall IS NOT NULL)')
        stalls_for_user_form = cursor_for_user_form.fetchall()
        for stall in stalls_for_user_form:
             stall_options_for_user_form += f"<option value='{stall['name']}'>{stall['name']}</option>"
    except Exception as e:
        print(f"Error fetching stalls for add user form: {e}")
    finally:
        if conn_for_user_form:
            conn_for_user_form.close()


    add_user_form = f"""
     <div class="p-6 bg-blue-100 rounded-xl shadow-md border border-blue-200 flex-1 min-w-[300px]">
          <h2 class="text-2xl font-bold text-blue-800 mb-4">Add New User</h2>
          <form action="/admin/add_user" method="post" class="flex flex-col space-y-4">
              <div>
                  <label for="new_username" class="block text-gray-700 font-semibold mb-1">Username:</label>
                  <input type="text" id="new_username" name="new_username" required class="form-input">
              </div>
              <div>
                  <label for="new_password" class="block text-gray-700 font-semibold mb-1">Password:</label>
                  <input type="password" id="new_password" name="new_password" required class="form-input">
              </div>
               <div>
                   <label for="new_role" class="block text-gray-700 font-semibold mb-1">Role:</label>
                   <select id="new_role" name="new_role" class="form-select">
                       <option value="user">User</option>
                       <option value="admin">Admin</option>
                   </select>
               </div>
               <div>
                   <label for="new_assigned_stall" class="block text-gray-700 font-semibold mb-1">Assign Stall (Optional, for users):</label>
                   <select id="new_assigned_stall" name="new_assigned_stall" class="form-select">
                       {stall_options_for_user_form}
                   </select>
               </div>
          <div class="text-center">
              <button type="submit" class="btn btn-primary">
                  Add User
              </button>
          </div>
      </form>
 </div>
 """

    # --- User Management Section ---
    user_list_html = ""
    if users:
        # Need a connection to check assigned stalls for the dropdown in update form
        conn_for_user_list = None
        try:
            conn_for_user_list = get_db_connection()
            # Fetch all stalls for the update assignment dropdown
            all_stalls_for_user_list = conn_for_user_list.cursor().execute('SELECT name FROM stalls').fetchall()

            for user in users:
                user_list_html += f"""
                <li class="bg-green-100 rounded-md p-4 mb-3 flex justify-between items-center flex-wrap border border-green-200 shadow-sm">
                    <div class="flex-grow mr-4">
                        <span class="font-semibold text-green-800">{user['username']}</span> <span class="text-gray-600 text-sm">({user['role']})</span><br>
                        <span class="text-gray-700 text-sm">Assigned: <span class="font-medium">{user['assigned_stall'] if user['assigned_stall'] else 'None'}</span></span><br>
                        <span class="text-gray-700 text-sm">Applied: <span class="font-medium">{user['applied_stall'] if user['applied_stall'] else 'None'}</span> (<span class="font-medium text-yellow-600">{user['application_status']}</span>)</span>
                    </div>
                    <div class="flex items-center space-x-2 mt-2 md:mt-0">
                """
                # Add remove button for non-admin users
                if user['role'] != 'admin':
                    user_list_html += f"""
                        <form action="/admin/remove_user" method="post" onsubmit="return confirm('Are you sure you want to remove user {user['username']}?');" class="inline-block">
                            <input type="hidden" name="user_id" value="{user['id']}">
                            <button type="submit" class="btn btn-sm btn-danger">
                                Remove
                            </button>
                        </form>
                    """
                # Add update assignment form for non-admin users
                if user['role'] != 'admin':
                     stall_options_update_user = "<option value=''>Unassign</option>"
                     for stall in all_stalls_for_user_list:
                          # Check if the stall is assigned to someone else, excluding the current user
                          is_assigned_to_other = is_stall_assigned(conn_for_user_list, stall['name'], exclude_user_id=user['id'])
                          stall_options_update_user += f"<option value='{stall['name']}' {'selected' if stall['name'] == user['assigned_stall'] else ''} {'disabled' if is_assigned_to_other else ''}>{stall['name']}</option>"

                     user_list_html += f"""
                          <form action="/admin/update_user_assignment" method="post" class="inline-block flex items-center">
                               <input type="hidden" name="user_id" value="{user['id']}">
                               <select name="assigned_stall" class="form-select form-select-sm mr-1">
                                    {stall_options_update_user}
                               </select>
                               <button type="submit" class="btn btn-sm btn-secondary">
                                   Update Assignment
                               </button>
                          </form>
                     """
                # Add application management buttons for pending applications
                if user['application_status'] == 'pending':
                     user_list_html += f"""
                          <form action="/admin/approve_application" method="post" class="inline-block ml-2">
                               <input type="hidden" name="user_id" value="{user['id']}">
                               <button type="submit" class="btn btn-sm btn-primary">
                                   Approve
                               </button>
                          </form>
                           <form action="/admin/decline_application" method="post" class="inline-block ml-2">
                                <input type="hidden" name="user_id" value="{user['id']}">
                                <button type="submit" class="btn btn-sm btn-danger">
                                    Decline
                                </button>
                           </form>
                     """
                user_list_html += "</div></li>"
        except Exception as e:
            print(f"Error generating user list HTML: {e}")
        finally:
            if conn_for_user_list:
                conn_for_user_list.close()

    else:
        user_list_html = "<p class='text-center text-gray-600'>No users found.</p>"

    # --- Stall Management Section ---
    stall_list_html = ""
    if stalls:
        for stall in stalls:
            stall_list_html += f"""
            <li class="bg-green-100 rounded-md p-4 mb-3 flex justify-between items-center flex-wrap border border-green-200 shadow-sm">
                <div class="flex-grow mr-4">
                     <span class="font-semibold text-green-800">{stall['name']}</span><br>
                     <span class="text-gray-700 text-sm">{stall['description'] if stall['description'] else 'No description'}</span>
                </div>
                <div class="flex items-center space-x-2 mt-2 md:mt-0">
                    <form action="/admin/remove_stall" method="post" onsubmit="return confirm('WARNING: This will remove stall {stall['name']} and ALL its items. Are you sure?');" class="inline-block">
                        <input type="hidden" name="stall_id" value="{stall['id']}">
                        <button type="submit" class="btn btn-sm btn-danger">
                            Remove
                        </button>
                    </form>
                     <form action="/admin/update_stall" method="post" class="inline-block flex items-center">
                         <input type="hidden" name="stall_id" value="{stall['id']}">
                         <input type="text" name="new_name" placeholder="New Name" class="form-input form-input-sm mr-1">
                         <input type="text" name="new_description" placeholder="New Description" class="form-input form-input-sm mr-1">
                         <input type="text" name="new_image_path" placeholder="New Image Path" class="form-input form-input-sm mr-1">
                         <button type="submit" class="btn btn-sm btn-secondary">
                             Update
                         </button>
                     </form>
                </div>
            </li>
            """
    else:
        stall_list_html = "<p class='text-center text-gray-600'>No stalls found.</p>"

    # --- Item Management Section (Admin Dashboard) ---
    item_management_html = ""

    # Add New Item Form (for Admin Dashboard) - Stays at the top
    stall_options_add_item = "<option value=''>Select a Stall</option>"
    for stall in stalls: # Use the already fetched stalls list
         stall_options_add_item += f"<option value='{stall['name']}'>{stall['name']}</option>"

    add_item_form_admin = f"""
    <div class="mt-6 mb-8 p-6 bg-green-200 rounded-xl shadow-md border border-green-300">
         <h2 class="text-2xl font-bold text-green-900 mb-4">Add New Item (Admin)</h2>
         <form action="/user/add_item_main" method="post" class="flex flex-col space-y-4">
             <div>
                 <label for="admin_add_item_stall" class="block text-gray-700 font-semibold mb-1">Select Stall:</label>
                 <select id="admin_add_item_stall" name="stall_name" required class="form-select">
                     {stall_options_add_item}
                 </select>
             </div>
             <div>
                 <label for="admin_add_item_name" class="block text-gray-700 font-semibold mb-1">Item Name:</label>
                 <input type="text" id="admin_add_item_name" name="item_name" required class="form-input">
             </div>
             <div>
                 <label for="admin_add_item_description" class="block text-gray-700 font-semibold mb-1">Description (Optional):</label>
                 <textarea id="admin_add_item_description" name="description" rows="2" class="form-textarea"></textarea>
             </div>
              <div>
                  <label for="admin_add_item_image_path" class="block text-gray-700 font-semibold mb-1">Image Path (Optional, e.g., /stall_images/item.jpg):</label>
                  <input type="text" id="admin_add_item_image_path" name="image_path" class="form-input">
              </div>
             <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                       <label for="admin_first_variation_size" class="block text-gray-700 font-semibold mb-1">First Variation Size:</label>
                       <input type="text" id="admin_first_variation_size" name="first_variation_size" value="N/A" class="form-input">
                  </div>
                  <div>
                       <label for="admin_first_variation_price" class="block text-gray-700 font-semibold mb-1">First Variation Price:</label>
                       <input type="number" id="admin_first_variation_price" name="first_variation_price" step="0.01" required class="form-input">
                  </div>
                  <div>
                       <label for="admin_first_variation_stock" class="block text-gray-700 font-semibold mb-1">First Variation Stock:</label>
                       <input type="number" id="admin_first_variation_stock" name="first_variation_stock" value="0" min="0" class="form-input">
                  </div>
             </div>
             <div class="text-center">
                 <button type="submit" class="btn btn-primary">
                     Add Item
                 </button>
             </div>
         </form>
    </div>
    """

    # List items organized by stall using collapsible details
    if items_by_stall:
        for stall_name, items_list in items_by_stall.items():
            item_management_html += f"""
            <details class="stall-items-details bg-green-100 rounded-lg shadow-md p-4 mb-4 border border-green-200">
                <summary class="cursor-pointer text-xl font-semibold text-green-800">
                    {stall_name}'s Items ({len(items_list)})
                </summary>
                <div class="stall-items-content mt-4 pt-4 border-t border-green-200">
            """
            conn_for_variations = None
            try:
                conn_for_variations = get_db_connection()
                cursor_for_variations = conn_for_variations.cursor()

                for item in items_list:
                     item_management_html += f"""
                     <details class="item-details bg-white rounded-lg shadow-md p-4 mb-3 border border-green-200">
                         <summary class="cursor-pointer flex items-center justify-between text-lg font-semibold text-green-800">
                             <div class="flex items-center">
                                  <img src="{item['image_path'] if item['image_path'] and os.path.exists(item['image_path'][1:]) else '/stall_images/placeholder.jpg'}" alt="{item['item_name']}" class="w-12 h-12 object-cover rounded-md mr-4 border border-gray-200">
                                  <span>{item['item_name']}</span>
                             </div>
                             <span class="text-sm text-gray-500 ml-4">Click to see details</span>
                         </summary>
                         <div class="item-content mt-4 pt-4 border-t border-gray-200">
                             <p class="text-gray-700 text-sm mb-3">{item['description'] if item['description'] else 'No description available.'}</p>

                             <h4 class="text-md font-medium text-green-700 mb-2">Variations:</h4>
                             <ul class="list-none p-0">
                     """
                     # Fetch variations for the current item
                     cursor_for_variations.execute('SELECT id, size, price, stock FROM item_variations WHERE item_id = ? ORDER BY size', (item['id'],))
                     variations = cursor_for_variations.fetchall()

                     if variations:
                         for variation in variations:
                             # Add 'out-of-stock' class if stock is 0
                             stock_class = 'text-red-600 font-bold' if variation['stock'] <= 0 else ''
                             stock_text = f"Stock: {variation['stock']}" if variation['stock'] > 0 else "Out of Stock"
                             item_management_html += f"""
                                 <li class="flex justify-between items-center bg-green-50 rounded-md p-2 mb-1 border border-green-100 flex-wrap">
                                     <span class="text-gray-800 text-sm mr-4 flex-grow">{variation['size']} - ₱{variation['price']:.2f}</span>
                                     <span class="text-gray-600 text-sm {stock_class}">{stock_text}</span>
                                     <div class="flex items-center space-x-2 mt-2 md:mt-0">
                                         <form action="/user/remove_item_variation" method="post" onsubmit="return confirm('Are you sure you want to remove this variation?');" class="inline-block">
                                             <input type="hidden" name="variation_id" value="{variation['id']}">
                                             <button type="submit" class="btn btn-sm btn-danger">
                                                 Remove
                                             </button>
                                         </form>
                                         <form action="/user/update_item_variation" method="post" class="inline-block flex items-center">
                                              <input type="hidden" name="variation_id" value="{variation['id']}">
                                              <input type="text" name="new_size" placeholder="Size" class="form-input form-input-sm mr-1">
                                              <input type="number" name="new_price" placeholder="Price" step="0.01" class="form-input form-input-sm mr-1">
                                              <input type="number" name="new_stock" placeholder="Stock" class="form-input form-input-sm mr-1">
                                              <button type="submit" class="btn btn-sm btn-secondary">
                                                  Update
                                              </button>
                                             </form>
                                         </div>
                                     </li>
                                 """
                         item_management_html += "</ul>" # Close variations list

                     else:
                         item_management_html += "<p class='text-gray-600 text-sm ml-4'>No variations available for this item.</p>"

                     # Add Variation form for this item (MOVED OUTSIDE VARIATION LOOP)
                     item_management_html += f"""
                     <div class="mt-4 p-3 bg-green-200 rounded-md border border-green-300">
                          <h5 class="text-sm font-medium text-green-900 mb-2">Add New Variation for {item['item_name']}:</h5>
                          <form action="/user/add_item_variation" method="post" class="flex flex-wrap items-center space-x-2">
                              <input type="hidden" name="item_id" value="{item['id']}">
                              <input type="text" name="size" placeholder="Size" class="form-input form-input-sm">
                              <input type="number" name="price" placeholder="Price" step="0.01" required class="form-input form-input-sm">
                              <input type="number" name="stock" placeholder="Stock" value="0" min="0" class="form-input form-input-sm">
                              <button type="submit" class="btn btn-sm btn-primary">
                                  Add Variation
                              </button>
                          </form>
                     </div>
                     """

                     item_management_html += "</div>" # Close item-content div
                     item_management_html += "</details>" # Close item-details (collapsible)

                # Add a form to remove the main item
                item_management_html += f"""
                     <div class="mt-4 text-center">
                         <form action="/user/remove_item_main" method="post" onsubmit="return confirm('WARNING: This will remove this item and ALL its variations. Are you sure?');" class="inline-block">
                             <input type="hidden" name="item_id" value="{item['id']}">
                             <button type="submit" class="btn btn-sm btn-danger">
                                 Remove Item
                             </button>
                         </form>
                     </div>
                """


            except Exception as e:
                 print(f"Error generating item management HTML for stall {stall_name}: {e}")
            finally:
                 if conn_for_variations:
                      conn_for_variations.close()


            item_management_html += "</div>" # Close stall-items-content div
            item_management_html += "</details>" # Close stall-items-details (collapsible)

    else:
        item_management_html = "<p class='text-center text-gray-600'>No items found.</p>"


    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/style.css">
    </head>
    <body class="bg-green-50 min-h-screen m-0 relative font-poppins default-background">
        <div class="admin-header bg-white shadow-md p-4 border-b border-green-200 flex justify-between items-center"> 
             <img src="/secondpageimg/craveeatsnobg.png" alt="CraveEats Logo" class="h-16"> 
             <form action="/logout" method="post" class="inline-block">
                 <button type="submit" class="btn btn-sm btn-danger"> 
                     Logout
                 </button>
             </form>
        </div>
        <div class="container mx-auto p-4 mt-4 animate-fade-in">
            <div class="admin-container bg-white rounded-xl shadow-lg p-6 border border-green-200">
                <h1 class="text-3xl font-bold text-green-800 text-center mb-6">Admin Dashboard</h1>

                <div class="flex flex-wrap -mx-3 mb-6">
                     <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
                         <div class="p-6 bg-green-100 rounded-xl border border-green-200 h-full">
                             <h2 class="text-2xl font-semibold text-green-800 mb-4">User Management</h2>
                             <ul class="list-none p-0 space-y-3 max-h-96 overflow-y-auto">
                                 {user_list_html}
                             </ul>
                             {add_user_form}
                         </div>
                     </div>
                     <div class="w-full md:w-1/2 px-3">
                         <div class="p-6 bg-green-100 rounded-xl border border-green-200 h-full">
                             <h2 class="text-2xl font-semibold text-green-800 mb-4">Stall Management</h2>
                             <ul class="list-none p-0 space-y-3 max-h-96 overflow-y-auto">
                                 {stall_list_html}
                             </ul>
                             {add_stall_form}
                         </div>
                     </div>
                </div>


                 <div class="p-6 bg-green-100 rounded-xl border border-green-200">
                     <h2 class="text-2xl font-semibold text-green-800 mb-4">Item Management</h2>
                     {add_item_form_admin}
                     <div class="mt-6">
                         {item_management_html}
                     </div>
                 </div>


            </div>
        </div>
    </body>
    </html>
    """

def get_user_dashboard(user):
    # Generates the HTML for the user dashboard with pastel theme and background.
    conn = None
    assigned_stall_name = user['assigned_stall']
    assigned_stall_html = ""
    item_management_html = ""
    application_status_html = ""
    items = []
    stalls = [] # Needed for the re-apply dropdown

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if assigned_stall_name:
            assigned_stall_html = f"""
            <p class='text-gray-700 mb-4 text-center'>You are assigned to manage the stall: <span class='font-semibold text-green-800'>{assigned_stall_name}</span></p>
            <div class="mt-6 p-6 bg-green-100 rounded-xl shadow-md border border-green-200">
                 <h2 class="text-2xl font-bold text-green-800 mb-4 text-center">Your Stall's Menu</h2>
            """
            # Fetch items for the assigned stall
            cursor.execute('SELECT id, name, description, image_path FROM items WHERE stall_id = (SELECT id FROM stalls WHERE name = ?) ORDER BY name', (assigned_stall_name,))
            items = cursor.fetchall()

            item_list_html = ""
            # Add New Item form for the assigned stall at the top of the item list (MOVED OUTSIDE ITEM LOOP)
            assigned_stall_data = get_stall_by_name(conn, assigned_stall_name)
            if assigned_stall_data:
                item_list_html += f"""
                <div class="mb-8 p-6 bg-green-200 rounded-xl shadow-md border border-green-300">
                     <h3 class="text-xl font-bold text-green-900 mb-4 text-center">Add New Item to Your Stall</h3>
                     <form action="/user/add_item_main" method="post" class="flex flex-col space-y-4">
                         <input type="hidden" name="stall_name" value="{assigned_stall_name}">
                         <div>
                             <label for="user_item_name" class="block text-gray-700 font-semibold mb-1">Item Name:</label>
                             <input type="text" id="user_item_name" name="item_name" required class="form-input">
                         </div>
                         <div>
                             <label for="user_description" class="block text-gray-700 font-semibold mb-1">Description (Optional):</label>
                             <textarea id="user_description" name="description" rows="2" class="form-textarea"></textarea>
                         </div>
                          <div>
                              <label for="user_image_path" class="block text-gray-700 font-semibold mb-1">Image Path (Optional, e.g., /stall_images/item.jpg):</label>
                              <input type="text" id="user_image_path" name="image_path" class="form-input">
                          </div>
                         <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                              <div>
                                   <label for="user_first_variation_size" class="block text-gray-700 font-semibold mb-1">First Variation Size:</label>
                                   <input type="text" id="user_first_variation_size" name="first_variation_size" value="N/A" class="form-input">
                              </div>
                              <div>
                                   <label for="user_first_variation_price" class="block text-gray-700 font-semibold mb-1">First Variation Price:</label>
                                   <input type="number" id="user_first_variation_price" name="first_variation_price" step="0.01" required class="form-input">
                              </div>
                              <div>
                                   <label for="user_first_variation_stock" class="block text-gray-700 font-semibold mb-1">First Variation Stock:</label>
                                   <input type="number" id="user_first_variation_stock" name="first_variation_stock" value="0" min="0" class="form-input">
                                  </div>
                             </div>
                         <div class="text-center">
                             <button type="submit" class="btn btn-primary">
                                 Add Item
                             </button>
                         </div>
                     </form>
                </div>
                """

            if items:
                for item in items:
                    item_list_html += f"""
                     <details class="item-details bg-white rounded-lg shadow-md p-4 mb-3 border border-green-200">
                         <summary class="cursor-pointer flex items-center justify-between text-lg font-semibold text-green-800">
                             <div class="flex items-center">
                                  <img src="{item['image_path'] if item['image_path'] and os.path.exists(item['image_path'][1:]) else '/stall_images/placeholder.jpg'}" alt="{item['name']}" class="w-12 h-12 object-cover rounded-md mr-4 border border-gray-200">
                                  <span>{item['name']}</span>
                             </div>
                             <span class="text-sm text-gray-500 ml-4">Click to see details</span>
                         </summary>
                         <div class="item-content mt-4 pt-4 border-t border-gray-200">
                             <p class="text-gray-700 text-sm mb-3">{item['description'] if item['description'] else 'No description available.'}</p>

                             <h4 class="text-md font-medium text-green-700 mb-2">Variations:</h4>
                             <ul class="list-none p-0 space-y-2">
                     """
                    # Fetch variations for the current item
                    cursor.execute('SELECT id, size, price, stock FROM item_variations WHERE item_id = ? ORDER BY size', (item['id'],))
                    variations = cursor.fetchall()

                    if variations:
                        for variation in variations:
                            # Add 'out-of-stock' class if stock is 0
                            stock_class = 'text-red-600 font-bold' if variation['stock'] <= 0 else ''
                            stock_text = f"Stock: {variation['stock']}" if variation['stock'] > 0 else "Out of Stock"
                            item_list_html += f"""
                                <li class="flex justify-between items-center bg-green-50 rounded-md p-2 mb-1 border border-green-100 flex-wrap">
                                    <span class="text-gray-800 text-sm mr-4 flex-grow">{variation['size']} - ₱{variation['price']:.2f}</span>
                                    <span class="text-gray-600 text-sm {stock_class}">{stock_text}</span>
                                    <div class="flex items-center space-x-2 mt-2 md:mt-0">
                                        <form action="/user/remove_item_variation" method="post" onsubmit="return confirm('Are you sure you want to remove this variation?');" class="inline-block">
                                            <input type="hidden" name="variation_id" value="{variation['id']}">
                                            <button type="submit" class="btn btn-sm btn-danger">
                                                Remove
                                            </button>
                                        </form>
                                        <form action="/user/update_item_variation" method="post" class="inline-block flex items-center space-x-1">
                                             <input type="hidden" name="variation_id" value="{variation['id']}">
                                             <input type="text" name="new_size" placeholder="Size" class="form-input form-input-sm">
                                             <input type="number" name="new_price" placeholder="Price" step="0.01" class="form-input form-input-sm">
                                             <input type="number" name="new_stock" placeholder="Stock" class="form-input form-input-sm">
                                             <button type="submit" class="btn btn-sm btn-secondary">
                                                 Update
                                             </button>
                                        </form>
                                    </div>
                                </li>
                            """
                        item_list_html += "</ul>" # Close variations list

                    else:
                        item_list_html += "<p class='text-gray-600 text-sm ml-4'>No variations available for this item.</p>"

                    # Add Variation form for this item (MOVED OUTSIDE VARIATION LOOP)
                    item_list_html += f"""
                    <div class="mt-4 p-3 bg-green-200 rounded-md border border-green-300">
                         <h5 class="text-sm font-medium text-green-900 mb-2">Add New Variation for {item['name']}:</h5>
                         <form action="/user/add_item_variation" method="post" class="flex flex-wrap items-center space-x-2">
                             <input type="hidden" name="item_id" value="{item['id']}">
                             <input type="text" name="size" placeholder="Size" class="form-input form-input-sm">
                             <input type="number" name="price" placeholder="Price" step="0.01" required class="form-input form-input-sm">
                             <input type="number" name="stock" placeholder="Stock" value="0" min="0" class="form-input form-input-sm">
                             <button type="submit" class="btn btn-sm btn-primary">
                                 Add Variation
                             </button>
                         </form>
                    </div>
                    """


                    item_list_html += "</div>" # Close item-content div
                    item_list_html += "</details>" # Close item-details (collapsible)

                # Add a form to remove the main item
                item_list_html += f"""
                     <div class="mt-4 text-center">
                         <form action="/user/remove_item_main" method="post" onsubmit="return confirm('WARNING: This will remove this item and ALL its variations. Are you sure?');" class="inline-block">
                             <input type="hidden" name="item_id" value="{item['id']}">
                             <button type="submit" class="btn btn-sm btn-danger">
                                 Remove Item
                             </button>
                         </form>
                     </div>
                """


            else:
                # If no items exist, still show the "Add New Item" form
                assigned_stall_data = get_stall_by_name(conn, assigned_stall_name)
                if assigned_stall_data:
                    item_list_html += f"""
                    <div class="mb-8 p-6 bg-green-200 rounded-xl shadow-md border border-green-300">
                         <h3 class="text-xl font-bold text-green-900 mb-4 text-center">Add New Item to Your Stall</h3>
                         <form action="/user/add_item_main" method="post" class="flex flex-col space-y-4">
                             <input type="hidden" name="stall_name" value="{assigned_stall_name}">
                             <div>
                                 <label for="user_item_name" class="block text-gray-700 font-semibold mb-1">Item Name:</label>
                                 <input type="text" id="user_item_name" name="item_name" required class="form-input">
                             </div>
                             <div>
                                 <label for="user_description" class="block text-gray-700 font-semibold mb-1">Description (Optional):</label>
                                 <textarea id="user_description" name="description" rows="2" class="form-textarea"></textarea>
                             </div>
                              <div>
                                  <label for="user_image_path" class="block text-gray-700 font-semibold mb-1">Image Path (Optional, e.g., /stall_images/item.jpg):</label>
                                  <input type="text" id="user_image_path" name="image_path" class="form-input">
                              </div>
                             <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                  <div>
                                       <label for="user_first_variation_size" class="block text-gray-700 font-semibold mb-1">First Variation Size:</label>
                                       <input type="text" id="user_first_variation_size" name="first_variation_size" value="N/A" class="form-input">
                                  </div>
                                  <div>
                                       <label for="user_first_variation_price" class="block text-gray-700 font-semibold mb-1">First Variation Price:</label>
                                       <input type="number" id="user_first_variation_price" name="first_variation_price" step="0.01" required class="form-input">
                                  </div>
                                  <div>
                                       <label for="user_first_variation_stock" class="block text-gray-700 font-semibold mb-1">First Variation Stock:</label>
                                       <input type="number" id="user_first_variation_stock" name="first_variation_stock" value="0" min="0" class="form-input">
                                  </div>
                             </div>
                             <div class="text-center">
                                 <button type="submit" class="btn btn-primary">
                                     Add Item
                                 </button>
                             </div>
                         </form>
                    </div>
                    """
                else:
                     item_list_html = "<p class='text-center text-gray-600'>Could not retrieve stall data.</p>"


            item_management_html += item_list_html # Add the list of items
            item_management_html += "</div>" # Close the assigned stall items div

        else:
            # If no stall is assigned, show application status and form
            application_status = user['application_status']
            applied_stall = user['applied_stall']

            if application_status == 'none':
                application_status_html = "<p class='text-gray-700 mb-4 text-center'>You are not currently assigned to a stall.</p>"
                # Form to apply for a stall
                cursor.execute('SELECT name FROM stalls')
                stalls = cursor.fetchall()
                # Use the existing connection for is_stall_assigned inside the loop
                stall_options = "<option value=''>Select a Stall to Apply For</option>"
                for stall in stalls:
                     # Only show stalls that are not currently assigned
                     if not is_stall_assigned(conn, stall['name']):
                         stall_options += f"<option value='{stall['name']}'>{stall['name']}</option>"


                application_status_html += f"""
                     <div class="user-dashboard-apply-form mt-6 p-6 bg-yellow-100 rounded-xl shadow-md border border-yellow-200">
                          <h3 class="text-xl font-bold text-yellow-800 mb-4 text-center">Apply to Manage a Stall</h3>
                          <form action="/register" method="post" class="flex flex-col space-y-4">
                              <input type="hidden" name="reg_username" value="{user['username']}">
                              <input type="hidden" name="reg_password" value="">
                              <div>
                                  <label for="apply_stall" class="block text-gray-700 font-semibold mb-1 text-left">Choose a Stall:</label>
                                  <select id="apply_stall" name="apply_stall" required class="form-select">
                                      {stall_options}
                                  </select>
                              </div>
                              <div class="text-center">
                                  <button type="submit" class="btn btn-secondary">
                                      Submit Application
                                  </button>
                              </div>
                          </form>
                     </div>
                """
            elif application_status == 'pending':
                application_status_html = f"<p class='text-gray-700 mb-4 text-center'>Your application to manage stall <span class='font-semibold text-green-800'>{applied_stall if applied_stall else 'N/A'}</span> is currently <span class='font-semibold text-yellow-600'>pending</span> review.</p>"
            elif application_status == 'declined':
                application_status_html = "<p class='text-gray-700 mb-4 text-center'>Your previous application was <span class='font-semibold text-red-600'>declined</span>.</p>"
                # Option to re-apply
                cursor.execute('SELECT name FROM stalls')
                stalls = cursor.fetchall()
                # Use the existing connection for is_stall_assigned inside the loop
                stall_options = "<option value=''>Select a Stall to Re-apply For</option>"
                for stall in stalls:
                     # Only show stalls that are not currently assigned
                     if not is_stall_assigned(conn, stall['name']):
                         stall_options += f"<option value='{stall['name']}'>{stall['name']}</option>"


                application_status_html += f"""
                     <div class="user-dashboard-apply-form mt-6 p-6 bg-yellow-100 rounded-xl shadow-md border border-yellow-200">
                          <h3 class="text-xl font-bold text-yellow-800 mb-4 text-center">Re-apply to Manage a Stall</h3>
                          <form action="/register" method="post" class="flex flex-col space-y-4">
                              <input type="hidden" name="reg_username" value="{user['username']}">
                              <input type="hidden" name="reg_password" value="">
                              <div>
                                  <label for="apply_stall" class="block text-gray-700 font-semibold mb-1 text-left">Choose a Stall:</label>
                                  <select id="apply_stall" name="apply_stall" required class="form-select">
                                      {stall_options}
                                  </select>
                              </div>
                              <div class="text-center">
                                  <button type="submit" class="btn btn-secondary">
                                      Submit Re-application
                                  </button>
                              </div>
                          </form>
                     </div>
                """
    except Exception as e:
         print(f"Error generating user dashboard HTML: {e}")
    finally:
         if conn:
              conn.close()


    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>User Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/style.css">
    </head>
    <body class="bg-green-50 min-h-screen m-0 relative font-poppins default-background">
        <div class="kiosk-header bg-white shadow-md p-4 text-center border-b border-green-200 flex justify-between items-center">
             <img src="/secondpageimg/craveeatsnobg.png" alt="CraveEats Logo" class="mx-auto h-16">
             <form action="/logout" method="post" class="inline-block">
                 <button type="submit" class="btn btn-danger">
                     Logout
                 </button>
             </form>
        </div>
        <div class="container mx-auto p-4 mt-4 animate-fade-in">
            <div class="user-dashboard bg-white rounded-xl shadow-lg p-6 border border-green-200">
                <h1 class="text-3xl font-bold text-green-800 mb-6 text-center">Welcome, {user['username']}!</h1>

                {assigned_stall_html}
                {application_status_html}
                {item_management_html}


                <div class="text-center mt-8">
                    <a href="/second" class="btn btn-outline">
                        View Stalls (Customer View)
                    </a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
