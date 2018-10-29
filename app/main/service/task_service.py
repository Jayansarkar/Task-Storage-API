from app.main.model.task import Task, mk_date
from app.main.db import get_db
from app.main.util.dto import TaskDto

api = TaskDto.api
task_add = TaskDto.a_add_task
task_status = TaskDto.task_status


def create_task(payload):
    task = Task.from_payload(payload)
    return task.add()


def change_status(id, payload):
    task = Task(id)
    return task.update(payload['status'])


def delete_task(id):
    task = Task(id)
    return task.delete()


def get_all_tasks():
    db = get_db()
    tasks = db.execute(
        'SELECT * FROM task'
    ).fetchall()

    if not tasks:
        return {'message': "no task found"}
    ans = []
    for t in tasks:
        task = Task.from_sql_row(t)
        ans.append(task.to_json())

    return {'data': ans}


def get_one_task(uid):
    task = Task(uid)
    if not task.fetch_info():
        api.abort(404)
    return {'data': task.to_json()}


def get_overdue():
    db = get_db()
    tasks = db.execute(
        'SELECT * FROM task WHERE due_date < date(?) and status !=?', ('now',
                                                                       'Finished')
    ).fetchall()
    if not tasks:
        return "no task found"
    ans = []
    for t in tasks:
        task = Task.from_sql_row(t)
        ans.append(task.to_json())

    return {'data':ans}


def get_d_date(d_date):
    db = get_db()
    d_date = mk_date(d_date)
    tasks = db.execute(
        'SELECT * FROM task WHERE due_date = ?', (d_date,)
    ).fetchall()
    if not tasks:
        return "no task found"
    ans = []
    for t in tasks:
        task = Task.from_sql_row(t)
        ans.append(task.to_json())

    return {'data':ans}


def get_finished():
    db = get_db()
    tasks = db.execute(
        'SELECT * FROM task WHERE status = "Finished"'
    ).fetchall()
    if not tasks:
        return "no task found"
    ans = []
    for t in tasks:
        task = Task.from_sql_row(t)
        ans.append(task.to_json())
    return {'data':ans}
