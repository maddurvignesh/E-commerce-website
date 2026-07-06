# ShopEase - E-Commerce Store

A modern e-commerce web application built with **Django** featuring a responsive UI, shopping cart, order processing, and user authentication.

🔗 **Live Demo:** [e-commerce-website-1-51gk.onrender.com](https://e-commerce-website-1-51gk.onrender.com/)

## Features

- **Product Catalog** — Browse products with images, descriptions, and pricing
- **Product Details** — View full product info with quantity selector
- **Shopping Cart** — Add, update, and remove items with stock validation
- **Order Processing** — Checkout with shipping address, stock deduction, and order history
- **User Authentication** — Register, login, and logout with password validation
- **Responsive Design** — Optimized for desktop, tablet, and mobile
- **Admin Panel** — Manage products, orders, and users via Django admin

## Tech Stack

| Layer      | Technology          |
|------------|---------------------|
| Backend    | Python / Django     |
| Frontend   | HTML, CSS, JavaScript |
| Database   | SQLite              |
| Images     | Pillow / LoremFlickr |

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repo
git clone https://github.com/maddurvignesh/E-commerce-website.git
cd E-commerce-website

# Install dependencies
pip install django pillow

# Run migrations
python manage.py migrate

# Seed sample products
python manage.py seed_data

# (Optional) Download product images
python manage.py add_images

# Start the server
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

### Admin Access

```
URL:    http://127.0.0.1:8000/admin/
User:   admin
Pass:   admin123
```

## Project Structure

```
E-commerce-website/
├── ecommerce/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                  # Main app
│   ├── models.py           # Product, CartItem, Order, OrderItem
│   ├── views.py            # All view logic
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin registration
│   └── management/         # Custom commands
│       └── commands/
│           ├── seed_data.py    # Populate sample products
│           └── add_images.py   # Download product images
├── templates/              # HTML templates
├── static/                 # CSS and JavaScript
├── media/                  # Product images
└── manage.py
```

## Developer

**Maddur Vignesh**  
[github.com/maddurvignesh](https://github.com/maddurvignesh)

## License

MIT
