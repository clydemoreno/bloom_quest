import os

def sync_file_io_task(task_id):
    with open('test_file.txt', 'r') as file:
        content = file.read()
        print(f"Sync Task {task_id}: Read content: {content.strip()}")

def main():
    for i in range(10):
        sync_file_io_task(i)

if __name__ == "__main__":
    main()
