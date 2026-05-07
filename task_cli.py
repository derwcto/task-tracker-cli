import sys
import json
import os
from datetime import datetime

JSON_FILE = 'tasks.json'

# --- Funciones de Persistencia ---

def load_tasks():
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(JSON_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# --- Funciones de Lógica de Negocio ---

def add_task(description):
    tasks = load_tasks()
    # Calculamos el ID basado en el máximo actual para evitar duplicados al borrar
    new_id = max([t['id'] for t in tasks], default=0) + 1
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_id})")

def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully.")
            return
    print(f"Error: Task with ID {task_id} not found.")

def delete_task(task_id):
    tasks = load_tasks()
    original_count = len(tasks)
    tasks = [t for t in tasks if t['id'] != task_id]
    
    if len(tasks) < original_count:
        save_tasks(tasks)
        print(f"Task {task_id} deleted successfully.")
    else:
        print(f"Error: Task with ID {task_id} not found.")

def mark_task(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}.")
            return
    print(f"Error: Task with ID {task_id} not found.")

def list_tasks(status_filter=None):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    filtered_tasks = tasks if not status_filter else [t for t in tasks if t['status'] == status_filter]
    
    if not filtered_tasks:
        print(f"No tasks found with status: {status_filter}")
        return

    print(f"\n{'ID':<5} {'Description':<30} {'Status':<15} {'Updated At'}")
    print("-" * 70)
    for t in filtered_tasks:
        print(f"{t['id']:<5} {t['description']:<30} {t['status']:<15} {t['updatedAt']}")

# --- Controlador Principal (CLI) ---

def main():
    if len(sys.argv) < 2:
        print("\nUsage: python task_cli.py [command] [args]")
        print("Commands: add, update, delete, mark-in-progress, mark-done, list [status]")
        return

    command = sys.argv[1]

    try:
        if command == "add":
            add_task(sys.argv[2])
        
        elif command == "update":
            update_task(int(sys.argv[2]), sys.argv[3])
        
        elif command == "delete":
            delete_task(int(sys.argv[2]))
        
        elif command == "mark-in-progress":
            mark_task(int(sys.argv[2]), "in-progress")
        
        elif command == "mark-done":
            mark_task(int(sys.argv[2]), "done")
        
        elif command == "list":
            status = sys.argv[2] if len(sys.argv) > 2 else None
            list_tasks(status)
        
        else:
            print(f"Unknown command: {command}")
    except IndexError:
        print("Error: Missing arguments for the command.")
    except ValueError:
        print("Error: ID must be a number.")

if __name__ == "__main__":
    main()