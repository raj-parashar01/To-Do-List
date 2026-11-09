import os

filename = "tasks.txt"

def load_tasks():
    if os.path.exists(filename):
        with open(filename, "r") as file:
            tasks = file.readlines()
            tasks = [task.strip() for task in tasks]
    else:
        tasks = []
    return tasks


def save_tasks(tasks):
    with open(filename, "w") as file:
        for task in tasks:
            file.write(task + "\n")


def show_tasks(tasks):
    if not tasks:
        print("No tasks found!")
    else:
        print("\nYour Tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"[{i}]. {task}")


def add_task(tasks):
    task = input("Enter a new task: ")
    tasks.append(task)
    print("Task added!")


def delete_task(tasks):
    show_tasks(tasks)
    if not tasks:
        return
    try:
        num = int(input("Enter task number to delete: "))
        if 1 <= num <= len(tasks):
            removed = tasks.pop(num - 1)
            print(f"Deleted: {removed}")
        else:
            print("Invalid task number!")
    except ValueError:
        print("Please enter a valid number!")


def main():
    tasks = load_tasks()
    while True:
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Delete Task")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")
        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
            save_tasks(tasks)
        elif choice == "3":
            delete_task(tasks)
            save_tasks(tasks)
        elif choice == "4":
            save_tasks(tasks)
            print("Good Bye!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()