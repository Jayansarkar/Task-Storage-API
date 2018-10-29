from flask import request
from flask_restplus import Resource

from app.main.service.task_service import (change_status, create_task,
                                           delete_task, get_all_tasks,
                                           get_d_date, get_finished,
                                           get_one_task, get_overdue, task_add,
                                           task_status)
from app.main.util.decorator import admin_token_required, token_required
from app.main.util.dto import TaskDto

api = TaskDto.api


@api.route('/')
class AllTaks(Resource):
    # @api.marshal_list_with(a_task)
    @token_required
    @api.doc("lists all tasks")
    def get(self):
        return get_all_tasks()

    @admin_token_required
    @api.expect(task_add, validate=True)
    @api.doc(security='apikey')
    def post(self):
        return create_task(api.payload)


@api.route('/<uid>')
@api.param('uid', 'unique task id')
@api.response(404, "no task found with that id")
@api.doc(security='apikey')
class SinlgeTask(Resource):
    # @api.marshal_with(a_task)
    @api.doc("Fetch that task")
    @token_required
    def get(self, uid):
        return get_one_task(uid)

    @api.doc("change status of a task. require a admin privilege")
    @api.expect(task_status)
    @admin_token_required
    def put(self, uid):
        return change_status(id=uid, payload=api.payload)

    @api.doc("delete a task, require admin privilege")
    @token_required
    def delete(self, uid):
        return delete_task(uid)


@api.route('/due')
class ShowByDue(Resource):
    @api.doc("fetch by due date")
    @token_required
    def get(self):
        try:
            d_date = request.args.get('due_date')

            return get_d_date(d_date)
        except:
            return {'message': 'due date not valid'}, 400


@api.route('/overdue')
class ShowDueTask(Resource):
    @api.doc('show overdue tasks')
    @token_required
    def get(self):
        return get_overdue()


@api.route('/finished')
class ShowFinished(Resource):
    @api.doc('show finished tasks')
    @token_required
    def get(self):
        return get_finished()
