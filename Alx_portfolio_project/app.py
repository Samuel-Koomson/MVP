# from flask import Flask, render_template, request
# from vegg_list import *
# from alx_portfolio_project import *
#
# app = Flask(__name__)
# app.static_folder = 'static'
#
#
# @app.route('/')
# def home():
#     return render_template('home_page.html')
#
# @app.route('/select_items', methods=['GET', 'POST'])
# def select_vegetables():
#     if request.method == 'POST':
#         items_needed = request.form.getlist('vegetables')
#         quantity = int(request.form['quantity'])
#         shopping_cart = select_items(items_needed, quantity)
#
#         shelf_stock, out_of_stock_veggies = check_quantity_in_stock(shopping_cart)
#         if shelf_stock:
#             total_cost = calculate_cost(shopping_cart)
#             return render_template('payment_information.html', shopping_cart=shopping_cart, total_cost=total_cost)
#         else:
#             return render_template('out_of_stock.html', out_of_stock_veggies=out_of_stock_veggies)
#     return render_template('veg_selection', vegetables=vegetables)
#
# @app.route('/purchase')
# def purchase():
#     if process_payment():
#         if sufficient_money(50, 100):
#             purchase_message = "Purchase successful"
#         else:
#             purchase_message = "Insufficient funds in your wallet"
#     else:
#         purchase_message = "Payment information does not match"
#     return render_template('purchase_status.html', purchase_message=purchase_message)
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True, port=8000)

# from flask import Flask, render_template, request, redirect, url_for
# from vegg_list import *
# from alx_portfolio_project import *
#
# app = Flask(__name__)
# app.static_folder = 'static'
# @app.route('/')
# def home():
#     return render_template('home_page.html')
# @app.route('/select_items', methods=['GET', 'POST'])
# def select_items():
#     if request.method == 'POST':
#         items_needed = request.form.getlist('vegetable')
#         quantities = request.form.getlist('quantity')
#
#         total_cost = calculate_cost(items_needed, quantities)
#         return redirect(url_for('payment-information.html', total_cost=total_cost))
#
#     return render_template('vegetable_selection.html', vegetables=vegetables)
#
# @app.route('/payment-information', methods=['GET', 'POST'])
# def payment_information():
#     if request.method == 'POST':
#         card_number = request.form.get('card-number')
#         if process_payment(card_number):
#             if sufficient_money(50, 100):
#                 purchase_message = "Purchase successful"
#             else:
#                 purchase_message = "Insufficient funds in your wallet"
#         else:
#             purchase_message = "Payment information does not match"
#         return render_template('purchase_status.html', purchase_message=purchase_message)
#     total_cost=request.args.get('total_cost')
#     return render_template('payment-information.html', total_cost=total_cost)
# # @app.route('/purchase', methods=['GET', 'POST'])
# # def purchase():
# #     if process_payment():
# #         if sufficient_money(50, 100):
# #             purchase_message = "Purchase successful"
# #         else:
# #             purchase_message = "Insufficient funds in your wallet"
# #     else:
# #         purchase_message = "Payment information does not match"
# #     return render_template('purchase_status.html', purchase_message=purchase_message)
#
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000)


from flask import Flask, render_template, request, redirect, url_for
from vegg_list import vegetables
from alx_portfolio_project import calculate_cost, check_quantity_in_stock, sufficient_money
app = Flask(__name__)

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
            shopping_cart.append((veggie, int(quantity)))

        # Redirect back to the vegetable selection page
        return redirect(url_for('view_shopping_cart'))

    # Render the vegetable selection page with the available vegetables
    return render_template('vegetable_selection.html', vegetables=vegetables)


# Define a route for the shopping cart page
@app.route('/shopping_cart')
def view_shopping_cart():
    return render_template('shopping_cart.html', shopping_cart=shopping_cart)


# Define a route for checking the quantity in stock
@app.route('/check_quantity')
def check_quantity():
    shelf_stock, out_of_stock_veggies = check_quantity_in_stock(shopping_cart)

    if shelf_stock:
        return "All items are in stock."
    else:
        return f"Sorry, {out_of_stock_veggies} is out of stock, check back later."


# Define a route for calculating the total cost
@app.route('/calculate_cost')
def calculate_cart_cost():
    total_cost = calculate_cost(shopping_cart)
    return render_template('calculate_cost.html', total_cost=total_cost)
    # return f"Total cost: ${total_cost:.2f}"


# Define a route for the payment page
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        credit_card_num = int(request.form['card-number'])
        confirm_credit_card_num = int(request.form['card-confirmation'])

        if credit_card_num == confirm_credit_card_num:
            return redirect(url_for('purchase'))

    return render_template('payment_information.html')


# Define a route for making the purchase
@app.route('/purchase')
def purchase():
    total_cost = calculate_cost(shopping_cart)
    wallet_amount = 100  # Assuming a wallet balance of $100

    if sufficient_money(total_cost, wallet_amount):
        return "Purchase Successful"
    else:
        return "Insufficient funds in your wallet"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
