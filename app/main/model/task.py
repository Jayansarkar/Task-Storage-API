from app.main.db import get_db
from app.main.util.dto import TaskDto

from datetime import datetime, timedelta

api = TaskDto.api

def mk_date(date_str):
    return datetime.date(datetime.strptime(date_str, '%Y-%m-%d'))

class Task:
    def __init__(self, uid):
        self.uid = uid
        self.title = None
        self.description = None
        self.due_date = None
        self.status = None

    @classmethod
    def from_payload(cls, payload):
        task = cls(None)
        task.title = payload['title']
        task.description = payload['description']
        task.due_date = mk_date(payload['due_date'])
        task.status = payload['status']

        return task

    @classmethod
    def from_sql_row(cls, row):
        task = cls(row['id'])
        task.title = row['title']
        task.status = row['status']
        task.due_date = row['due_date']
        task.description = row['description']

        return task

    def fetch_info(self):
        db = get_db()
        task = db.execute(
            'SELECT * FROM task WHERE id = ?', (self.uid,)
        ).fetchone()
        if not task:
            return False
        self.title = task['title']
        self.description = task['description']
        self.due_date = task['due_date']
        self.status = task['status']

        return True

    def update(self, stat):
        if not self.fetch_info():
            api.abort(404)
        db = get_db()
        self.status = stat
        db.execute(
            'UPDATE task SET status = ? WHERE id = ?', (self.status, self.uid)
        )
        db.commit()
        return {
            'message': 'successfully updated',
            'task_details': self.to_json()
        }

    def add(self):
        db = get_db()
        db.execute(
            'INSERT INTO task (title, description, status, due_date) VALUES (?,?,?,?)',
            (self.title, self.description, self.status, self.due_date)
        )
        db.commit()
        return {'message':"task added successfully"}

    def delete(self):
        db = get_db()
        task = db.execute(
            'SELECT id FROM task WHERE id = ?', (self.uid,)
        ).fetchone()
        if not task:
            api.abort(404)
        db.execute(
            'DELETE FROM task WHERE id = ?', (self.uid,)
        )
        db.commit()
        return {'message':'task removed successfully'}

    def to_json(self):
        return {
            'id': self.uid,
            'title': self.title,
            'due date': self.due_date.strftime('%Y-%m-%d'),
            'description': self.description,
            'status': self.status
        }
