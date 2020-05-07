###
#
#
#
###
from datetime import datetime
from pytas.models import base, users
from pytas.http import TASClient

PROJECT_TYPES = (
    (0, 'Research'),
    (2, 'Startup'),
    (4, 'Educational'),
    (1, 'Institutional'),
    (6, 'Partner'),
)

RENEWAL_START_WINDOW = 90

class Project(base.TASModel):
    _resource_uri = 'projects/'
    _fields = [
        'id',
        'title',
        'chargeCode',
        'typeId',
        'description',
        'source',
        'fieldId',
        'piId',
        'allocations',
    ]

    def __populate(self, data):
        self.__dict__.update(data)

        self.pi = users.User(initial=data['pi'])

        allocations = []
        for alloc in data['allocations']:
            allocations.append(Allocation(initial=alloc))
        self.allocations = allocations

    def __init__(self, id=None, initial={}):
        super(Project, self).__init__()
        if id is not None:
            api = TASClient()
            remote_data = api.project(id)
            self.__populate(remote_data)
        else:
            self.__populate(initial)

    def __str__(self):
        return getattr(self, 'chargeCode', '<new project>')

    def as_dict(self):
        proj_dict =  {f:getattr(self, f, None) for f in self._fields}
        proj_dict['allocations'] = [a.as_dict() for a in self.allocations]
        return proj_dict

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
        return list(cls(initial=d) for d in data)

    def save(self):
        api = TASClient()
        if self.is_new():
            created = api.create_project(self.as_dict())
            self.__populate(initial=created)

    def get_users(self):
        api = TASClient()
        user_data = api.get_project_users(self.id)
        return list(users.User(initial=u) for u in user_data)

    def add_user(self, username):
        api = TASClient()
        return api.add_project_user(self.id, username)

    def remove_user(self, username):
        api = TASClient()
        return api.del_project_user(self.id, username)

    @property
    def active_allocations(self):
        return [a for a in self.allocations if a.status == 'Active' and a.resource == 'Chameleon']

    @property
    def has_active_allocations(self):
        return len(self.active_allocations) > 0

    @property
    def inactive_allocations(self):
        return [a for a in self.allocations if a.status == 'Inactive' and a.resource == 'Chameleon']

    @property
    def has_inactive_allocations(self):
        return len(self.inactive_allocations) > 0

    @property
    def approved_allocations(self):
        return [a for a in self.allocations if a.status == 'Approved' and a.resource == 'Chameleon']

    @property
    def has_approved_allocations(self):
        return len(self.approved_allocations) > 0

    @property
    def pending_allocations(self):
        return [a for a in self.allocations if a.status == 'Pending' and a.resource == 'Chameleon']

    @property
    def has_pending_allocations(self):
        return len(self.pending_allocations) > 0

    @property
    def rejected_allocations(self):
        return [a for a in self.allocations if a.status == 'Rejected' and a.resource == 'Chameleon']

    @property
    def has_rejected_allocations(self):
        return len(self.rejected_allocations) > 0

class Allocation(base.TASModel):
    _resource_uri = 'allocations/'
    _fields = [
        'computeUsed',
        'computeAllocated',
        'computeRequested',
        'dateRequested',
        'dateReviewed',
        'decisionSummary',
        'end',
        'id',
        'justification',
        'memoryUsed',
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
        'storageUsed',
        'storageAllocated',
        'storageRequested',
    ]

    def __init__(self, initial={}):
        super(Allocation, self).__init__()
        self.__populate(initial)

    def __populate(self, data):
        self.__dict__.update(data)

    @property
    def percentComputeUsed(self):
        used = getattr(self, 'computeUsed', 0)
        alloc = getattr(self, 'computeAllocated', 0)
        if alloc > 0:
            return (used / alloc) * 100
        return 0

    @property
    def days_left(self):
        return (self.end - datetime.utcnow()).days

    @property
    def up_for_renewal(self):
        days_left = self.days_left
        return days_left >= 0 and days_left <= RENEWAL_START_WINDOW

    @property
    def renewal_days(self):
        return self.days_left

class AllocationApproval(object):
    pass
