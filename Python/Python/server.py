from http.server import HTTPServer
import os
from db import init_db
from handler import MyHandler
from PIL import Image, ImageDraw, ImageFont 


def run(server_class=HTTPServer, handler_class=MyHandler, port=8000):
    
    init_db() 
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nStopping httpd...')

if __name__ == '__main__':
    os.makedirs('firstpageimg', exist_ok=True)
    os.makedirs('secondpageimg', exist_ok=True)
    os.makedirs('stall_images', exist_ok=True)

    
    if not os.path.exists('style.css'):
        print("Creating dummy style.css")
        try:
            with open('style.css', 'w') as f:
                f.write("""
/* Basic styles for the kiosk application */
body {
    font-family: 'Nunito', sans-serif;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Default background image for all pages */
.default-background {
    background-image: url('/secondpageimg/background.jpg'); /* Replace with your image path */
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed; /* Keeps the background fixed when scrolling */
}


.kiosk-container,
.choice-container,
.auth-container,
.cart-container,
.receipt-container,
.admin-container,
.user-dashboard {
    /* Add common container styles here if needed */
}

/* Add specific styles for pastel green theme */
.bg-green-50 { background-color: #f0fdf4; }
.bg-green-100 { background-color: #dcfce7; }
.bg-green-200 { background-color: #bbf7d0; }
.bg-green-300 { background-color: #86efac; }
.bg-green-600 { background-color: #16a34a; }
.bg-green-700 { background-color: #15803d; }
.text-green-800 { color: #14532d; } /* Changed to color for text */
.text-green-900 { color: #052e16; }

.text-green-600 { color: #16a34a; }
.text-green-700 { color: #15803d; }
.text-green-800 { color: #14532d; }


/* Pastel Blue */
.bg-blue-100 { background-color: #e0f2fe; }
.border-blue-200 { border-color: #bfdbfe; }
.text-blue-800 { color: #1e40af; }
.focus\:border-blue-300:focus { border-color: #93c5fd; }
.bg-blue-600 { background-color: #2563eb; }
.hover\:bg-blue-700:hover { background-color: #1d4ed8; }
.text-blue-600 { color: #2563eb; }


/* Pastel Yellow */
.bg-yellow-100 { background-color: #fef9c3; }
.border-yellow-200 { border-color: #fde68a; }
.text-yellow-800 { color: #92400e; }
.text-yellow-600 { color: #ca8a04; }
.focus\:border-yellow-300:focus { border-color: #fcd34d; }
.bg-yellow-600 { background-color: #ca8a04; }
.hover\:bg-yellow-700:hover { background-color: #a16207; }


/* Pastel Purple */
.bg-purple-600 { background-color: #9333ea; }
.hover\:bg-purple-700:hover { background-color: #7e22ce; }


/* Red for errors/removal */
.bg-red-500 { background-color: #ef4444; }
.hover\:bg-red-600:hover { background-color: #dc2626; }
.text-red-500 { color: #ef4444; }
.text-red-600 { color: #dc2626; }


/* Gray for back buttons etc. */
.bg-gray-500 { background-color: #6b7280; }
.hover\:bg-gray-700:hover { background-color: #374151; }
.text-gray-600 { color: #4b5563; }
.border-gray-200 { border-color: #e5e7eb; }
.text-gray-700 { color: #374151; }
.text-gray-800 { color: #1f2937; }


/* Animations */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
.animate-fade-in { animation: fadeIn 0.5s ease-out; }

@keyframes slideIn {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}
.animate-slide-in { animation: slideIn 0.5s ease-out; }
.animation-delay-100 { animation-delay: 0.1s; }

@keyframes fadeDown {
    from { transform: translateY(-20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}
.animate-fade-down { animation: fadeDown 0.5s ease-out; }

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
.animate-pulse { animation: pulse 2s infinite; }

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    60% { transform: translateY(-5px); }
}
.animate-bounce { animation: bounce 1s infinite; }


/* Ensure images don't exceed container width */
img {
    max-width: 100%;
    height: auto;
}

/* Basic styling for details/summary for collapsible sections */
details {
    cursor: pointer;
}

summary {
    outline: none; /* Remove default outline */
}

/* Optional: Style for open details */
details[open] summary {
    /* Add styles when details is open */
}

.stall-items-content, .item-content {
    /* Add styles for content within collapsible sections */
}

/* Specific style for Admin Dashboard header to align logo and logout */
.admin-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #fff; /* White background for header */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    padding: 1rem;
    border-bottom: 2px solid #bbf7d0; /* Border matching pastel theme */
}

.admin-header img {
    height: 4rem; /* Adjust logo size */
}

.admin-header form {
    margin: 0; /* Remove default form margin */
}

/* Specific style for User Dashboard header to align logo and logout */
.user-dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #fff; /* White background for header */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    padding: 1rem;
    border-bottom: 2px solid #bbf7d0; /* Border matching pastel theme */
}

.user-dashboard-header img {
    height: 4rem; /* Adjust logo size */
}

.user-dashboard-header form {
    margin: 0; /* Remove default form margin */
}

/* Flexbox for side-by-side layout in Admin Dashboard */
.admin-management-sections {
    display: flex;
    flex-wrap: wrap; /* Allow wrapping on smaller screens */
    margin: 0 -0.75rem; /* Counteract padding from child columns */
}

.admin-management-sections > div {
    padding: 0 0.75rem; /* Add padding to create gutters */
}

/* Adjust item card layout for better organization */
.item-card .flex-grow {
    flex-basis: 0; /* Allow flex-grow to work correctly */
    min-width: 0; /* Prevent content from overflowing */
}

.item-card .flex-wrap > * {
    flex-shrink: 0; /* Prevent form elements from shrinking too much */
}

/* Adjust spacing for variation forms */
.item-content form.flex {
    display: flex;
    align-items: center;
    flex-wrap: wrap; /* Allow wrapping for small screens */
    gap: 0.5rem; /* Add gap between form elements */
}

.item-content form.flex input,
.item-content form.flex button {
    /* Adjust padding and margin for form elements */
    padding: 0.25rem 0.5rem; /* py-1 px-2 */
    font-size: 0.75rem; /* text-xs */
}

.item-content form.flex input[type="text"],
.item-content form.flex input[type="number"] {
    width: auto; /* Allow inputs to size based on content or min-width */
    min-width: 4rem; /* Ensure a minimum width */
}

/* Ensure buttons in variation forms have consistent size */
.item-content form.flex button {
    flex-shrink: 0; /* Prevent buttons from shrinking */
}

/* Style for the "Add New Variation" form within item details */
.item-content .mt-4.p-3.bg-green-200 {
    /* Ensure consistent spacing and alignment */
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.item-content .mt-4.p-3.bg-green-200 form {
     display: flex;
     flex-wrap: wrap;
     align-items: center;
     gap: 0.5rem;
}

.item-content .mt-4.p-3.bg-green-200 form input,
.item-content .mt-4.p-3.bg-green-200 form button {
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
}

.item-content .mt-4.p-3.bg-green-200 form input[type="text"],
.item-content .mt-4.p-3.bg-green-200 form input[type="number"] {
    width: auto;
    min-width: 4rem;
}

""")
        except Exception as e:
            print(f"Error creating style.css: {e}")


    # Create a dummy background image file if it doesn't exist
    background_image_path = 'secondpageimg/background.jpg'
    if not os.path.exists(background_image_path):
        print(f"Creating dummy background image file at {background_image_path}")
        try:
            # Create a simple placeholder image
            img = Image.new('RGB', (800, 600), color = (220, 252, 231)) # Pastel green background
            d = ImageDraw.Draw(img)
            try:
                # Try to use a common font
                fnt = ImageFont.truetype("arial.ttf", 40)
            except IOError:
                # Fallback to default font if arial.ttf is not found
                fnt = ImageFont.load_default()
                print("Warning: arial.ttf not found, using default font for placeholder image.")

            text = "Background Image"
            text_width, text_height = d.textsize(text, font=fnt)
            text_x = (800 - text_width) // 2
            text_y = (600 - text_height) // 2
            d.text((text_x, text_y), text, fill=(14, 83, 45), font=fnt) # Dark green text
            img.save(background_image_path)
            print("Dummy background image created.")
        except ImportError:
            print("Warning: Pillow library not found. Cannot create dummy background image.")
            print("Please install Pillow (`pip install Pillow`) or provide your own background.jpg in secondpageimg/.")
        except Exception as e:
            print(f"Error creating dummy background image: {e}")


    run() # Start the server
