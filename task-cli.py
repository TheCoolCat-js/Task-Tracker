#                                                .--.
#                                                `.  \
#                                                  \  \
#                                                   .  \
#                                                   :   .
#                                                   |    .
#                                                   |    :
#                                                   |    |
#   ..._  ___                                       |    |
#  `."".`''''""--..___                              |    |
#  ,-\  \             ""-...__         _____________/    |
#  / ` " '                    `""""""""                  .
#  \                                                      L
#  (>                        pisica trb sa                 \
# /                       fie aici normal                   \
# \_    ___..---.                                            L
#   `--'         '.                                           \
#                  .                                           \_
#                 _/`.                                           `.._
#              .'     -.                                             `.
#             /     __.-Y     /''''''-...___,...--------.._            |
#            /   _."    |    /                ' .      \   '---..._    |
#           /   /      /    /                _,. '    ,/           |   |
#           \_,'     _.'   /              /''     _,-'            _|   |
#                   '     /               `-----''               /     |
#                   `...-'                                       `...-'

import json
import os
import sys
from datetime import datetime

class TaskTracker:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        if not os.path.exists(self.filename):
            return []
        
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save_tasks(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except IOError as e:
            print(f"Error saving tasks: {e}")
            sys.exit(1)

    def add_task(self, description):
        next_id = max([task['id'] for task in self.tasks], default=0) + 1
        
        new_task = {
            'id': next_id,
            'description': description,
            'status': 'todo',
            'createdAt': datetime.now().isoformat(),
            'updatedAt': datetime.now().isoformat()
        }
        
        self.tasks.append(new_task)
        self._save_tasks()
        print(f"Task added successfully (ID: {next_id})")

    def update_task(self, task_id, new_description):
        for task in self.tasks:
            if task['id'] == task_id:
                task['description'] = new_description
                task['updatedAt'] = datetime.now().isoformat()
                self._save_tasks()
                print(f"Task {task_id} updated successfully")
                return
        
        print(f"Task with ID {task_id} not found")

    def delete_task(self, task_id):
        original_length = len(self.tasks)
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        
        if len(self.tasks) < original_length:
            self._save_tasks()
            print(f"Task {task_id} deleted successfully")
        else:
            print(f"Task with ID {task_id} not found")

    def mark_task_status(self, task_id, status):
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = status
                task['updatedAt'] = datetime.now().isoformat()
                self._save_tasks()
                print(f"Task {task_id} marked as {status}")
                return
        
        print(f"Task with ID {task_id} not found")

    def list_tasks(self, filter_status=None):
        filtered_tasks = self.tasks
        
        if filter_status:
            filtered_tasks = [
                task for task in self.tasks 
                if task['status'] == filter_status
            ]
        
        if not filtered_tasks:
            print("No tasks found.")
            return
        
        for task in filtered_tasks:
            print(f"ID: {task['id']}, "
                  f"Description: {task['description']}, "
                  f"Status: {task['status']}, "
                  f"Created: {task['createdAt']}")

def main():
    tracker = TaskTracker()
    
    if len(sys.argv) < 2:
        print("Usage: task-cli [command] [arguments]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    try:
        if command == 'add' and len(sys.argv) > 2:
            tracker.add_task(sys.argv[2])
        
        elif command == 'update' and len(sys.argv) > 3:
            task_id = int(sys.argv[2])
            tracker.update_task(task_id, sys.argv[3])
        
        elif command == 'delete' and len(sys.argv) > 2:
            task_id = int(sys.argv[2])
            tracker.delete_task(task_id)
        
        elif command == 'mark-in-progress' and len(sys.argv) > 2:
            task_id = int(sys.argv[2])
            tracker.mark_task_status(task_id, 'in-progress')
        
        elif command == 'mark-done' and len(sys.argv) > 2:
            task_id = int(sys.argv[2])
            tracker.mark_task_status(task_id, 'done')
        
        elif command == 'list':
            if len(sys.argv) > 2:
                status = sys.argv[2]
                tracker.list_tasks(status)
            else:
                tracker.list_tasks()
        
        else:
            print("Invalid command. Available commands:")
            print("add 'task description'")
            print("update <id> 'new description'")
            print("delete <id>")
            print("mark-in-progress <id>")
            print("mark-done <id>")
            print("list [status]")
    
    except ValueError:
        print("Invalid task ID. Please provide a valid integer.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()