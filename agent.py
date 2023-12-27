from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
import networkx as nx


# Initialize the LLM (Language Large Model)
llm = OpenAI(ai_key='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')

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def ask_agent(question):
    response = llm.invoke(question)
    return response


def get_user_input():
    task = input("Enter your task or feature: ")

# Construct prompts for category and priority
    category_prompt = f"What category should the task '{task}' belong to? Return a single word. Good category examples include: 'bug', 'feature', 'documentation', 'testing', 'research', 'maintenance', 'meeting', 'discussion', 'planning', 'design', 'deployment', 'release', 'other'."
    priority_prompt = f"What should be the priority of the task '{task}'? Priorities can be High, Medium, or Low. Response should be a single word. Example 1: 'High' Example 2: 'Low'"
    status_prompt = f"What is the status of the task '{task}'? Status can be Not Started, In Progress, or Complete. Response should be a single word. Example 1: 'In Progress', Example 2: 'Complete'"
    # Use the modified ask_agent function with custom prompts
    category_suggestion = ask_agent(category_prompt)
    priority_suggestion = ask_agent(priority_prompt)
    status_suggestion = ask_agent(status_prompt)

    # LLM suggests category and priority
    #category_suggestion = ask_agent(f"What category should the task '{task}' belong to?")
    #priority_suggestion = ask_agent(f"What should be the priority of the task '{task}'?")
    #status_suggestion = ask_agent(f"What is the status of the task '{task}'?")

    print(f"Suggested Category: {category_suggestion}")
    print(f"Suggested Priority: {priority_suggestion}")
    print(f"Suggested Status: {status_suggestion}")

    # User confirmation or modification
    category = input("Edit category (or press Enter to accept the suggestion): ")
    priority = input("Edit priority (or press Enter to accept the suggestion): ")
    status = input("Edit status (or press Enter to accept the suggestion): ")
    # If user does not provide input, use the suggestion
    category = category if category else category_suggestion
    priority = priority if priority else priority_suggestion
    status = status if status else status_suggestion

    return task, category, priority, status



# Initialize a directed graph
task_graph = nx.DiGraph()

def add_task_to_graph(task, category, priority, status="Not Started"):
    task_graph.add_node(task, category=category, priority=priority, status=status)

def edit_task(task_number):
    tasks = list(task_graph.nodes(data=True))
    if task_number < 1 or task_number > len(tasks):
        print("Invalid task number.")
        return

    task_name = tasks[task_number - 1][0]
    
    if task_name not in task_graph:
        print(f"Task '{task_name}' not found.")
        return

    print("Enter new details for the task (leave blank to keep current value):")
    new_category = input(f"New Category (Current: {task_graph.nodes[task_name]['category']}): ")
    new_priority = input(f"New Priority (Current: {task_graph.nodes[task_name]['priority']}): ")
    new_status = input(f"New Status (Current: {task_graph.nodes[task_name]['status']}): ")

    if new_category:
        task_graph.nodes[task_name]['category'] = new_category
    if new_priority:
        task_graph.nodes[task_name]['priority'] = new_priority
    if new_status:
        task_graph.nodes[task_name]['status'] = new_status

def delete_task(task_number):
    tasks = list(task_graph.nodes(data=True))
    if task_number < 1 or task_number > len(tasks):
        print("Invalid task number.")
        return

    task_name = tasks[task_number - 1][0]

    if task_name in task_graph:
        confirmation = input(f"Are you sure you want to delete '{task_name}'? (yes/no): ")
        if confirmation.lower() == 'yes':
            task_graph.remove_node(task_name)
            print(f"Task '{task_name}' deleted.")
    else:
        print(f"Task '{task_name}' not found.")

def display_tasks():
    if not task_graph.nodes:
        print("No tasks added yet.")
        return

    for index, task in enumerate(task_graph.nodes(data=True), start=1):
        task_description = task[0]
        task_data = task[1]
        category = task_data.get('category', 'No category')
        priority = task_data.get('priority', 'No priority')
        status = task_data.get('status', 'Not Started')

        print(f"{index}. Task: {task_description}\n\tCategory: {category}\n\tPriority: {priority}\n\tStatus: {status}\n")


    for task in task_graph.nodes(data=True):
        task_description = task[0]
        task_data = task[1]
        category = task_data.get('category', 'No category')
        priority = task_data.get('priority', 'No priority')
        status = task_data.get('status', 'Not Started')

        # Removing 'content=' from the output
        if isinstance(category, str):
            category = category
        else:
            category = category.content if hasattr(category, 'content') else category

        if isinstance(priority, str):
            priority = priority
        else:
            priority = priority.content if hasattr(priority, 'content') else priority

        if isinstance(status, str):
            status = status
        else:
            status = status.content if hasattr(status, 'content') else status

        print(f"Task: {task_description}\n\tCategory: {category}\n\tPriority: {priority}\n\tStatus: {status}\n")


        

def main():
    while True:
        print("\n1. Add Task\n2. Show Tasks\n3. Edit Task\n4. Delete Task\n5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            task, category, priority, status = get_user_input()
            add_task_to_graph(task, category, priority, status)
        elif choice == '2':
            display_tasks()
        elif choice == '3':
            display_tasks()
            task_number = int(input("Enter the number of the task to edit: "))
            edit_task(task_number)
        elif choice == '4':
            display_tasks()
            task_number = int(input("Enter the number of the task to delete: "))
            delete_task(task_number)
        elif choice == '5':
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()

