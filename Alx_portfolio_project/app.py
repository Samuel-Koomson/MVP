from flask import Flask, render_template, request, redirect, url_for
from vegg_list import vegetables
from alx_portfolio_project import calculate_cost, check_quantity_in_stock, sufficient_money
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///shop_database.db"
db = SQLAlchemy(app)


class ShoppingCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vegetable = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()


class PaymentInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.Integer, nullable=False)
    confirm_card = db.Column(db.Integer, nullable=False)
    card_expiry = db.Column(db.Integer, nullable=False)
    card_holder = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


# Define a global variable to store the shopping cart
shopping_cart = []


# Define a route for the home page
@app.route('/')
def home():
    return render_template('home_page.html')


# Define a route for the vegetable selection page
@app.route('/select_items', methods=['GET', 'POST'])
def select_items():
    global shopping_cart  # Allow access to the global shopping_cart variable

    if request.method == 'POST':
        # Get the selected vegetables and quantities from the form
        selected_vegetables = request.form.getlist('vegetable')
        quantities = request.form.getlist('quantity')

        # Add the selected items and quantities to the shopping cart
        for veggie, quantity in zip(selected_vegetables, quantities):
            cart_item = ShoppingCart(
                vegetable=veggie,
                quantity=int(quantity)
            )
            db.session.add(cart_item)
            shopping_cart.append((veggie, int(quantity)))

        db.session.commit()
        # Redirect back to the vegetable selection page
        return redirect(url_for('view_shopping_cart'))

    # Render the vegetable selection page with the available vegetables
    return render_template('vegetable_selection.html', vegetables=vegetables)


# Define a route for the shopping cart page
@app.route('/shopping_cart')
def view_shopping_cart():
    shopping_cart_items = ShoppingCart.query.all()
    return render_template('shopping_cart.html', shopping_cart_items=shopping_cart_items)


# Define a route for checking the quantity in stock
@app.route('/check_quantity')
def check_quantity():
    shelf_stock, out_of_stock_veggies = check_quantity_in_stock(shopping_cart)

    if shelf_stock:
        return render_template('full_shelf.html', message="All items are in stock.")
    else:
        return render_template('empty_shelf.html', message=f"Sorry, {out_of_stock_veggies} is out of stock, check back later.")


# Define a route for calculating the total cost
@app.route('/calculate_cost')
def calculate_cart_cost():
    shopping_cart_items = ShoppingCart.query.all()

    total_cost = calculate_cost([(item.vegetable, item.quantity) for item in shopping_cart_items])
    return render_template('calculate_cost.html', total_cost=f"{total_cost:.2f}")
    # return f"Total cost: ${total_cost:.2f}"


# Define a route for the payment page
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        credit_card_num = request.form['card-number']
        expiry_date = request.form['expiry-date']
        cardholder_name = request.form['card-holder-name']
        confirm_credit_card_num = int(request.form['card-confirmation'])

        if credit_card_num == confirm_credit_card_num:
            new_card = PaymentInformation(
                card_number=credit_card_num,
                card_expiry=expiry_date,
                card_holder=cardholder_name
            )
            db.session.add(new_card)
            db.session.commit()

        return redirect(url_for('purchase'))

    return render_template('payment_information.html')


# Define a route for making the purchase
@app.route('/purchase')
def purchase():
    total_cost = calculate_cost(shopping_cart)
    wallet_amount = 100  # Assuming a wallet balance of $100

    if sufficient_money(total_cost, wallet_amount):
        return render_template('purchase_status.html', purchase_message="Purchase Successful")
    else:
        return render_template('purchase_status.html', purchase_message="Insufficient funds in your wallet")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

