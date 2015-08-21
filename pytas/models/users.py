###
#
#
#
###
import base
import projects
from pytas.http import TASClient

class User(base.TASModel):
    _resource_uri = 'users/'

    def __init__(self, username=None, id=None, initial={}):
        super(User, self).__init__()
        if username is not None or id is not None:
            api = TASClient()
            remote_data = api.get_user(id=id, username=username)
            self.__populate(remote_data)
        else:
            self.__populate(initial)

    def __str__(self):
        return getattr(self, 'username', '<new user>')

    def __populate(self, data):
        self.__dict__.update(data)

    @property
    def projects(self):
        _projects = []
        if self.username:
            api = TASClient()
            project_data = api.projects_for_user(username=self.username)
            for d in project_data:
                _projects.append(projects.Project(initial=d))
        return _projects

    def save(self):
        pass

    def request_password_reset(self, source=None):
        pass

    def confirm_password_reset(self, code, new_password, source=None):
        pass

    def verify_user(self, code):
        pass