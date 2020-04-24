from todo import Todo
import sys
app = Todo()
params = sys.argv

if len(params) <= 1 :
    app.help()
    sys.exit()

command = params[1]

if command == 'add':
    app.add(params)
elif command in ('today', 'day', 'to'):
    app.today(params)
elif command in ('show', 'list'):
    app.show(params)
elif command in ('delete', 'remove'):
    app.delete(params)
elif command in ('mark', 'done'):
    app.mark_done(params)
elif command == 'help':
    app.help()
else:
    app.help()