# ProZone 

<img width="1901" height="969" alt="image" src="https://github.com/user-attachments/assets/7e35615d-f9d7-4af3-a83c-f575fa2074eb" />


ProZone is a small e-commerce site for sports gear and sneakers, built with Flask. Think of it as a mini online store featuring big brands like Adidas, Nike, Puma, Air Jordan, and Under Armour — complete with user accounts, a shopping cart, product reviews, and an admin panel behind the scenes.

I built this mainly to practice full-stack Flask development: auth, databases, forms, and role-based access control all in one project.

## What it can do

- Browse products by brand, each with its own page and vibe (logo, tagline, description)
- View product details, pricing, stock, and category
- Create an account and log in securely (passwords are hashed, never stored in plain text)
- Leave star ratings and written reviews on products — and edit or delete your own later
- Add items to a cart and see your running total
- Check your profile for a quick view of your reviews and cart
- Admins get a dashboard to add/edit/delete products and manage users (promote, demote, or remove them)

## Built with

- **Flask** – the web framework
- **Flask-SQLAlchemy** – database models and queries
- **Flask-Login** – user sessions and authentication
- **Flask-WTF** – forms and validation
- **SQLite** – simple file-based database
- **Bootstrap Icons + custom CSS** – for the frontend look

## Project layout
<img width="1881" height="966" alt="image" src="https://github.com/user-attachments/assets/07591839-4695-4bb9-a341-95628cce2146" />

```
prozone/
├── app.py            # Starts the app
├── ext.py            # Flask app, database, and login manager setup
├── models.py         # Database models (User, Product, Review, CartItem)
├── forms.py          # All the forms (register, login, review, product)
├── routes.py         # Every page/route in the app
├── init_db.py        # Sets up the database and fills it with sample products
├── static/
│   └── css/style.css
├── templates/        # All the HTML pages
└── instance/
    └── prozone.db    # The SQLite database (created automatically)
```
<img width="1892" height="958" alt="image" src="https://github.com/user-attachments/assets/1583842a-4c2a-4986-ba67-172e8660c797" />

## Getting it running

1. **Clone this repo**
   ```bash
   git clone <your-repo-url>
   cd prozone
   ```

2. **Set up a virtual environment and install the dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   pip install flask flask-sqlalchemy flask-login flask-wtf
   ```

3. **Set up the database** (this also adds some sample products so the store isn't empty)
   ```bash
   python init_db.py
   ```

4. **Run it**
   ```bash
   python app.py
   ```

5. Head to `http://127.0.0.1:5000` in your browser and you're good to go.

## A few honest notes

- This was built as a learning project, so it's not hardened for production. Things like the secret key in `ext.py` should be moved to environment variables before deploying anywhere real.
- An admin account is created automatically the first time you run `init_db.py` — check `init_db.py` for the credentials if you need them, and definitely change them before going live with anything.
- Product images come from Unsplash, picked based on category.

## License

Free to use for learning, tinkering, or building on top of.
