# ShopHub E-Commerce Store

A complete, production-quality e-commerce web application built with Django, SQLite, and vanilla HTML/CSS/JS.

## Features
* **Amazon-style UI**: Dense product grids, dark navy header, orange/yellow accents.
* **Product Catalog**: Categories, search, filtering by category, price sorting.
* **Shopping Cart**: AJAX-based add to cart, quantity updates, without page reloads.
* **Checkout Flow**: Simple checkout form for shipping and mock payment (COD / Card).
* **Order History**: View past orders and details.
* **Authentication**: User registration, login, and profile management.
* **Responsive Design**: Mobile-friendly layout using CSS Flexbox and Grid.

## Setup Instructions

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\Activate.ps1
   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   * Copy `.env.example` to `.env`
   * Get a free Unsplash Access Key from `https://unsplash.com/developers` and add it to `.env`:
     ```env
     UNSPLASH_ACCESS_KEY=your_actual_key_here
     ```

4. **Apply Database Migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Seed the Database** (Creates categories, products, and a superuser):
   ```bash
   python manage.py seed_data
   ```
   *Superuser credentials: Username: `admin`, Password: `admin123`*

5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

6. Open your browser and navigate to `http://127.0.0.1:8000/`.
