###
#
#
#
###
from .base import TASModel

class User(TASModel):
    _resource_uri = 'users/'

    def __init__(self, **data):
        super(User, self).__init__()
        self.__dict__.update(data)

    def __str__(self):
        return getattr(self, 'username', '<new user>')

    def save(self):
        pass

    def request_password_reset(self, source=None):
        pass

    def confirm_password_reset(self, code, new_password, source=None):
        pass

    def verify_user(self, code):
        pass