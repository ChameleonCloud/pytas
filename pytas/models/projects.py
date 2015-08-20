###
#
#
#
###
from .base import TASModel
from .users import User
from pytas.http import TASClient

PROJECT_TYPES = (
    (0, 'Research'),
    (2, 'Startup'),
    (4, 'Educational'),
    (1, 'Institutional'),
    (6, 'Partner'),
)

class Project(TASModel):
    _resource_uri = 'projects/'
    _fields = [
        'id',
        'title',
        'typeId',
        'description',
        'source',
        'fieldId',
        'piId',
        'allocations',
    ]

    def __init__(self, **data):
        super(Project, self).__init__()
        self.__dict__.update(data)

        self.pi = User(**data['pi'])

        allocations = []
        for alloc in data['allocations']:
            allocations.append(Allocation(**alloc))
        self.allocations = allocations

    def __str__(self):
        return getattr(self, 'chargeCode', '<new project>')

    @classmethod
    def list(cls, username=None, group=None):
        """
        Returns a list for projects for the given username or group.
        An argument for username or group is required and only one
        may be provided.
        """
        if username is None and group is None:
            raise TypeError('Argument username or group is required')
        if username is not None and group is not None:
            raise TypeError('One one of username or group can be passed')

        api = TASClient()
        if username:
            data = api.projects_for_user(username)
        elif group:
            data = api.projects_for_group(group)
        return list(cls(**d) for d in data)

    @classmethod
    def get(cls, project_id):
        """
        Returns a project by ID.
        """
        api = TASClient()
        data = api.project(project_id)
        return cls(**data)

    def save(self):
        api = TASClient()
        if self.is_new():
            api.create_project(self.as_dict())

    def get_users(self):
        api = TASClient()
        user_data = api.get_project_users(self.id)
        return list(User(**u) for u in user_data)

    def add_user(self, username):
        api = TASClient()
        return api.add_project_user(self.id, username)

    def remove_user(self, username):
        api = TASClient()
        return api.del_project_user(self.id, username)



class Allocation(TASModel):
    _resource_uri = 'allocations/'
    _fields = [
        'computeAllocated',
        'computeRequested',
        'dateRequested',
        'dateReviewed',
        'decisionSummary',
        'end',
        'id',
        'justification',
        'memoryAllocated',
        'memoryRequested',
        'project',
        'projectId',
        'requestor',
        'requestorId',
        'resource',
        'resourceId',
        'reviewer',
        'reviewerId',
        'start',
        'status',
        'storageAllocated',
        'storageRequested',
    ]

    def __init__(self, **data):
        super(Allocation, self).__init__()
        self.__dict__.update(data)


class AllocationApproval(object):
    pass