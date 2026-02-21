# TaskNest
Task Nest is an task manager. When you execute the command you can enter the graphic interface. You have 3 differents buttons: add, to add
a new task, the delete button and the done button to change the status of a task.

# Minimum requis

Il faut avoir python d'installé.

## Lib utilisé à installer

(Il est conseillé d'utiliser un docker ou env pour pouvoir executer)

### Pour créer un env

``` bash
python3 -m venv venv
source venv/bin/activate
```

## Pour executer

### Il existe 4 commandes:
Add pour ajouter une task, list pour afficher les tasks, done pour changer le status d'une task, delete pour supprimer une task.
```bash
python3 main.py add [task_title]
python3 main.py list
python main.py done [task_id]
python main.py delete [task_id]
```