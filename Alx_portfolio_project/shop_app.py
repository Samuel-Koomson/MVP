from flask import Flask, render_template, request
from vegg_list import *
from alx_portfolio_project import *

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def home():
    return render_template('home_page.html')

@app.route('/select_items', methods=['GET', 'POST'])
def select_vegetables():
    if request.method == 'POST':
        items_needed = request.form.getlist('vegetables')
        quantity = int(request.form['quantity'])
        shopping_cart = select_items(items_needed, quantity)

        shelf_stock, out_of_stock_veggies = check_quantity_in_stock(shopping_cart)
        if shelf_stock:
            total_cost = calculate_cost(shopping_cart)
            return render_template('Payment-information.html', shopping_cart=shopping_cart, total_cost=total_cost)
        else:
            return render_template('out_of_stock.html', out_of_stock_veggies=out_of_stock_veggies)
    return render_template('veg_selection', vegetables=vegetables)

@app.route('/purchase')
def purchase():
    if process_payment():
        if sufficient_money(50, 100):
            purchase_message = "Purchase successful"
        else:
            purchase_message = "Insufficient funds in your wallet"
    else:
        purchase_message = "Payment information does not match"
    return render_template('purchase_status.html', purchase_message=purchase_message)

if __name__ == '__main__':
    app.run(debug=True)