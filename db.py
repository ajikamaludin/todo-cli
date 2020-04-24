from peewee import SqliteDatabase, Model, UUIDField, TextField, IntegerField, DateTimeField, DateField, AutoField
import uuid
from datetime import datetime

sqlite_db = SqliteDatabase('/media/aji/datautama.NeTv3SD/Development/python/project/todo-cli/db/todo.db3', pragmas={'journal_mode': 'wal'})

class Todo(Model):
    class Meta:
        database = sqlite_db
    
    id = IntegerField(primary_key=True)#UUIDField(primary_key=True, default=uuid.uuid4())
    todo = TextField()
    priority = IntegerField(default=0)
    deadline = DateField()
    status  = IntegerField(default=0)
    created_at = DateTimeField(default=datetime.now())

    def __str__(self):
        return "| " + str(self.id) + " | " + self.todo + " | " + str(self.priority) + " | " + str(self.deadline)[0:10] + " | " + ('done' if self.status == 1 else 'undone') + " | "
