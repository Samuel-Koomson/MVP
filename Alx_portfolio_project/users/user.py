from user_access import data_read, data_write


class User:
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)


    @classmethod
    def create_user(cls, *args, **kwargs):
        user = cls(*args, **kwargs)
        user.save()
        return user

    def save(self):
        users_data = data_read('./user.json')
        self.id = len(users_data) + 1
        users_data.append(self.__dict__)
        data_write(users_data, './user.json')

    @classmethod
    def initial_users(cls):

        pass

    @classmethod
    def find_user(cls, field_name, field_value):
        users_data = data_read ('./user.json')
        found_user =[]
        for user in users_data:
            if user[field_name] == field_value:
                found_user.append(cls(**user))
        return found_user if found_user else None

    

    
