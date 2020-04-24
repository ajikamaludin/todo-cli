from db import Todo as Tomod
from datetime import datetime
import sys
from prettytable import PrettyTable

class Todo:
    
    todo = ""
    priority = 0
    deadline = datetime.now()

    def __init__(self):
        self.table = PrettyTable()
        self.table.field_names = ['ID', 'TODO', 'Priority', 'Deadline', 'Status']

    def add(self, params):
        for i in range(len(params)):
            if params[i] == '--todo' :
                if self.validate(params, i) :
                    self.todo = params[i + 1]
            if params[i] == '--priority' :
                if self.validate(params, i) :
                    self.priority = params[i + 1]
            if params[i] == '--deadline' :
                if self.validate(params, i) :
                    self.deadline = params[i + 1]
        new_todo = Tomod.create(todo=self.todo, priority=self.priority, deadline=self.deadline)
        self.handle_row(new_todo)
        print(self.table)

    def today(self, params):
        query = Tomod.select().where(Tomod.deadline == datetime.today()).where(Tomod.status == 0).order_by(Tomod.created_at.desc())
        for todo in query:
            self.handle_row(todo)
            print("Nothing todo today")
        if len(self.table._rows) <= 0:
            print('Nothing Todo')
        else:
            print(self.table)

    def show(self, params):
        query = Tomod.select().order_by(Tomod.created_at.desc())
        
        for i in range(len(params)):
            if params[i] == '--undone':
                query = query.where(Tomod.status == 0)
            if params[i] == '--done':
                query = query.where(Tomod.status == 1)
            if params[i] == '--priority':
                query = query.order_by(Tomod.priority.desc())

        for todo in query:
            self.handle_row(todo)
        print(self.table)

    def mark_done(self, params):
        for i in range(len(params)):
            if params[i] == '--all':
                query = Tomod.update(status=1)
                query.execute()
                print('marked done all')
                return
            if params[i] == '--undone':
                if(self.validate(params, i)):
                    tomod = Tomod.get_by_id(params[i + 1])
                    tomod.status = 0
                    tomod.save()
                    self.handle_row(tomod)
                    print(self.table)
                    return
            if params[i] == '--done':
                if(self.validate(params, i)):
                    tomod = Tomod.get_by_id(params[i + 1])
                    tomod.status = 1
                    tomod.save()
                    self.handle_row(tomod)
                    print(self.table)
                    return
        print('noting to delete please define --id {id}')

    def delete(self, params):
        for i in range(len(params)):
            if params[i] == '--all':
                query = Tomod.delete()
                query.execute()
                print('deleted all')
                return
            if params[i] == '--id':
                if(self.validate(params, i)):
                    Tomod.delete_by_id(params[i + 1])
                    print(str(params[i + 1]) + ' deleted')
                    return
        print('noting to delete please define --id {id}')

    def help(self):
        print("type `todo help` to show this help message")
        print("""
    `today` - show todo today
    `show` - show all todos
        --done - show only done
        --undone - show only undone
        --priority - sort biggest priority
    `add` - add a todo
        --todo - text todo
        --priority - priotity number eg (0 - 10), default 0
        --deadline - deadline date 
    `mark` - mark done or undone todo
        --done - id to mark done 
        --undone - id to mark undone
        --all - mark all done
    `delete` - delete todo
        --all - delete all todos
        --id - id todo to delete
        """)
        return
    
    def validate(self, params, i):
        try:
            if params[i + 1] is None:
                print("if not use dont define it")
                sys.exit()
        except Exception:
            print("if not use dont define it")
            sys.exit()
        
        if params[i + 1].startswith('-'):
            print("if not use dont define it")
            sys.exit()
        return True
    
    def handle_row(self, todo):
        status = 'done' if todo.status == 1 else '-'
        self.table.add_row([todo.id, todo.todo, todo.priority, todo.deadline, status])