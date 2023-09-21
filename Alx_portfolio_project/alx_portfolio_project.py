"""
Things to be done for this project
1. item selection function
2. checking sufficient items on shelf
3. checking wallet amount to buy
4. process payment
5. Make purchase
6. sending emails and sms of transactions
7. Data storage and manipulation
"""
from vegg_list import vegetables
def select_items():
    shopping_cart = []
    while True:
        veggies_needed = input("Select your list of vegetables: ").title()
        if veggies_needed == 'Done'.title():
            break
        if veggies_needed in vegetables:
            quantity = int(input(f"What quantity of {veggies_needed} do you need: "))
            shopping_cart.append((veggies_needed, quantity))
        else:
            print(f"Sorry, {veggies_needed} is not available, please check later")
    return shopping_cart
# print(select_items())

def check_quantity_in_stock(shopping_cart):
    for veg_name, requested_quantity in shopping_cart:
        available_quantity = vegetables[veg_name]['quantity']
        if requested_quantity > available_quantity:
            return False, veg_name
    return True, None
# print(quantity_in_stock(5))

def calculate_cost(shopping_cart):
    total_cost = 0
    for veg_name, requested_quantity in shopping_cart:
        if veg_name in vegetables:
            total_cost += vegetables[veg_name]['price'] * requested_quantity
    return total_cost
# print(calculate_cost('cabbage'))
shopping_cart = select_items()
shelf_stock, out_of_stock_veggies = check_quantity_in_stock(shopping_cart)
if shelf_stock:
    total_cost = calculate_cost(shopping_cart)
    print(f"Total cost: ${total_cost:.2f}")
else:
    print(f"Sorry, {out_of_stock_veggies} is out of stock, check back later.")
def process_payment():
    credit_card_num = int(input("What is your credit card number: "))
    confirm_credit_card_num = int(input("Re-enter your credit card number: "))
    # card_amount = int(input("What is your card amount"))
    if credit_card_num == confirm_credit_card_num:
        return True
    else:
        return False
# print(process_payment())


def sufficient_money(total_cost, wallet_amount):
    return total_cost <= wallet_amount
wallet_amount = 100
total_cost = calculate_cost(shopping_cart)


def make_purchase(total_cost, wallet_amount):
    if process_payment():
        if sufficient_money(total_cost, wallet_amount):
            return "Purchase Successful"
        else:
            return "Insufficient funds in your wallet"
    else:
        return "Payment information does not match"
print(sufficient_money(total_cost, wallet_amount))
print(make_purchase(total_cost, wallet_amount))


# def make_purchase():
#     is_sufficient = False
#     if sufficient_money(['kale', 'chilly'], 50, 100) == True:
#         is_sufficient = True
#     return is_sufficient
# print(make_purchase())
