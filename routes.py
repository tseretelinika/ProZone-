from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from ext import app, db
from models import User, Product, Review, CartItem
from forms import RegisterForm, LoginForm, ReviewForm, ProductForm

BRANDS = ["Adidas", "Nike", "Puma", "Air Jordan", "Under Armour"]

BRAND_META = {
    "Adidas":       {"icon": "bi-triangle-fill",   "tagline": "Impossible is Nothing",  "desc": "German performance and style since 1949."},
    "Nike":         {"icon": "bi-lightning-fill",   "tagline": "Just Do It",             "desc": "Innovation-driven sportswear for every athlete."},
    "Puma":         {"icon": "bi-star-fill",        "tagline": "Forever Faster",         "desc": "Sport and street culture combined since 1948."},
    "Air Jordan":   {"icon": "bi-send-fill",        "tagline": "Be Like Mike",           "desc": "Michael Jordan's legacy in every silhouette."},
    "Under Armour": {"icon": "bi-shield-fill",      "tagline": "Protect This House",     "desc": "Performance apparel engineered for athletes."},
}




def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated




@app.context_processor
def inject_globals():
    cart_count = 0
    if current_user.is_authenticated:
        cart_count = sum(i.quantity for i in CartItem.query.filter_by(user_id=current_user.id).all())
    return {"cart_count": cart_count, "BRANDS": BRANDS, "BRAND_META": BRAND_META}




@app.route("/")
def index():
    featured = {b: Product.query.filter_by(brand=b).limit(3).all() for b in BRANDS}
    return render_template("index.html", featured=featured)




@app.route("/brand/<brand_name>")
def brand(brand_name):
    if brand_name not in BRANDS:
        abort(404)
    products = Product.query.filter_by(brand=brand_name).all()
    return render_template("brand.html", brand=brand_name, products=products)




@app.route("/product/<int:pid>", methods=["GET", "POST"])
def product_detail(pid):
    product = Product.query.get_or_404(pid)
    form = ReviewForm()
    user_review = None

    if current_user.is_authenticated:
        user_review = Review.query.filter_by(user_id=current_user.id, product_id=pid).first()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Please log in to leave a review.", "warning")
            return redirect(url_for("login"))
        if user_review:
            flash("You have already reviewed this product.", "info")
        else:
            review = Review(
                content=form.content.data,
                rating=form.rating.data,
                user_id=current_user.id,
                product_id=pid,
            )
            review.create()
            flash("Review added!", "success")
        return redirect(url_for("product_detail", pid=pid))

    reviews = Review.query.filter_by(product_id=pid).order_by(Review.created_at.desc()).all()
    return render_template("product.html", product=product, form=form, reviews=reviews, user_review=user_review)




@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.create()
        flash(f"Welcome, {user.username}! Your account has been created.", "success")
        login_user(user)
        return redirect(url_for("index"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f"Welcome back, {user.username}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html", form=form)


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))




@app.route("/cart")
@login_required
def cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(i.product.price * i.quantity for i in items)
    return render_template("cart.html", items=items, total=total)


@app.route("/cart/add/<int:pid>", methods=["POST"])
@login_required
def add_to_cart(pid):
    product = Product.query.get_or_404(pid)
    item = CartItem.query.filter_by(user_id=current_user.id, product_id=pid).first()
    if item:
        item.quantity += 1
        CartItem.save()
    else:
        item = CartItem(user_id=current_user.id, product_id=pid, quantity=1)
        item.create()
    flash(f"{product.name} added to cart!", "success")
    return redirect(request.referrer or url_for("index"))


@app.route("/cart/remove/<int:item_id>", methods=["POST"])
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        abort(403)
    item.delete()
    flash("Item removed from cart.", "info")
    return redirect(url_for("cart"))




@app.route("/review/delete/<int:rid>", methods=["POST"])
@login_required
def delete_review(rid):
    review = Review.query.get_or_404(rid)
    if review.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    pid = review.product_id
    review.delete()
    flash("Review deleted.", "info")
    return redirect(url_for("product_detail", pid=pid))


@app.route("/review/edit/<int:rid>", methods=["GET", "POST"])
@login_required
def edit_review(rid):
    review = Review.query.get_or_404(rid)
    if review.user_id != current_user.id:
        abort(403)
    form = ReviewForm(obj=review)
    if form.validate_on_submit():
        review.content = form.content.data
        review.rating = form.rating.data
        Review.save()
        flash("Review updated!", "success")
        return redirect(url_for("product_detail", pid=review.product_id))
    return render_template("edit_review.html", form=form, review=review)




@app.route("/profile")
@login_required
def profile():
    reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.created_at.desc()).all()
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template("profile.html", reviews=reviews, cart_items=cart_items)




@app.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    users = User.query.order_by(User.joined_at.desc()).all()
    products = Product.query.order_by(Product.brand).all()
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    return render_template("admin.html", users=users, products=products, reviews=reviews)


@app.route("/admin/product/add", methods=["GET", "POST"])
@login_required
@admin_required
def admin_add_product():
    form = ProductForm()
    if form.validate_on_submit():
        p = Product(
            name=form.name.data,
            brand=form.brand.data,
            category=form.category.data,
            price=form.price.data,
            description=form.description.data,
            stock=form.stock.data,
        )
        p.create()
        flash(f"Product '{p.name}' added!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("product_form.html", form=form, title="Add Product")


@app.route("/admin/product/edit/<int:pid>", methods=["GET", "POST"])
@login_required
@admin_required
def admin_edit_product(pid):
    product = Product.query.get_or_404(pid)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.brand = form.brand.data
        product.category = form.category.data
        product.price = form.price.data
        product.description = form.description.data
        product.stock = form.stock.data
        Product.save()
        flash(f"Product '{product.name}' updated!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("product_form.html", form=form, title="Edit Product")


@app.route("/admin/product/delete/<int:pid>", methods=["POST"])
@login_required
@admin_required
def admin_delete_product(pid):
    product = Product.query.get_or_404(pid)
    product.delete()
    flash("Product deleted.", "info")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/user/delete/<int:uid>", methods=["POST"])
@login_required
@admin_required
def admin_delete_user(uid):
    user = User.query.get_or_404(uid)
    if user.id == current_user.id:
        flash("You cannot delete yourself.", "danger")
        return redirect(url_for("admin_dashboard"))
    user.delete()
    flash("User deleted.", "info")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/user/toggle/<int:uid>", methods=["POST"])
@login_required
@admin_required
def admin_toggle_role(uid):
    user = User.query.get_or_404(uid)
    if user.id == current_user.id:
        flash("Cannot change your own role.", "danger")
        return redirect(url_for("admin_dashboard"))
    user.role = "admin" if user.role == "user" else "user"
    User.save()
    flash(f"{user.username} is now {user.role}.", "success")
    return redirect(url_for("admin_dashboard"))
