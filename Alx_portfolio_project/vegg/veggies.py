from vegg_access import data_read, data_write

class Veggie:
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)


    @classmethod
    def create(cls, *args, **kwargs):
        veggie = cls(*args, **kwargs)
        veggie.save()
        return veggie

    def save():
        veggie_data = data_read('./veggies.json')
        self.id = len(veggie_data) + 1
        veggie_data.append(self.__dict__)
        data_write(veggie_data, './veggies.json')
