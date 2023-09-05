from order_access import data_read, data_write

class Order:
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)


    @classmethod
    def order_made(cls, *args, **kwargs):
        order = cls(*args, **kwargs)
        order.save()
        return order

    def save(self):
        orders_data = data_read('./order.json')
        self.id = len(orders_data) + 1
        orders_data.append(self.__dict__)
        data_write(orders_data, './order.json')


    @classmethod
    def get_orders_by_user(cls, user_id):
        orders_data = data_read('./order.json')
        user_orders = []
        for order in orders_data:
            if order['user_id'] == user_id:
                user_orders.append(cls(**order))
        return user_orders
