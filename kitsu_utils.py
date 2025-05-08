import gazu
import pprint


def get_user_projects():
    project_names = []
    user_active_projects = gazu.user.all_open_projects()
    print("User active projects: ")
    #pprint.pprint(user_active_projects)
    for project in user_active_projects:
        print(f"Project Name: {project["name"]}")
        project_names.append(project["name"])
    return project_names

def get_user_tasks_for_project(user_email, project_name):
    person = gazu.person.get_person_by_email(user_email)
    #project = gazu.project.get_project_by_name(project_name)
    tasks = gazu.task.all_tasks_for_person(person)
    entity_names = []
    task_names = []

    for task in tasks:
        if task["project_name"] == project_name:
            pprint.pprint(task)
            if task["entity_name"] not in entity_names:
                entity_names.append(task["entity_name"])
                if task["task_type_name"] not in task_names:
                    task_names.append(task["task_type_name"])

    return entity_names, task_names

"""
entity_name - Group by this second
entity_type_name - Group by this first
project_name - Filter by this first

"""
