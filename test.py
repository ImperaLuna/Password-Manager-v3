class Login():
    def __init__(self) -> None:
        self.user_id = 200

class Storage():
    def __init__(self, user_id) -> None:
        self.user_id = user_id


login_instance = Login()
user_id_from_login = login_instance.user_id


storage_instance = Storage(user_id_from_login)
print(f'the value inside Storage is: {storage_instance.user_id}')