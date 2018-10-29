from flask_restplus import Namespace, fields

class UserDto:
    api = Namespace('users', description="User related operations")

    user = api.model(name='a user', model={
        'name': fields.String(required=True, description='Name'),
        'username': fields.String(required=True, description='Username'),
        'pub_id': fields.String(required=True, description='Public id'),
        'admin': fields.Boolean(required=True, description="is admin"),
        'password': fields.String(required=True, description='password hash')
    })

class AuthDto:
    api = Namespace('auth', description="Authentication related operations")

    login = api.model(name="user login", model={
        'username': fields.String(required=True, description="Username"),
        'password': fields.String(required=True, description="Password")
    })
    register = api.model(name="rser reg", model={
        'name': fields.String(required=True, description="Name"),
        'username': fields.String(required=True, description="Username"),
        'password': fields.String(required=True, description="Password")
    })

class TaskDto:
    api = Namespace('tasks', description="Task related operations")

    a_add_task = api.model(name='a_add task', model={
        'title': fields.String(required=True, description="Task title"),
        'due_date': fields.Date(required=True, description="YYYY-MM-DD"),
        'status': fields.String(required=True, description="current status"),
        'description': fields.String(required=True, description="Description")
    })

    task_status = api.model(name='task_stat', model={'status': fields.String(reqiured=True, description="status of task")})

