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
    tasks = gazu.task.all_tasks_for_person(person)
    entity_names = []
    task_details = []

    for task in tasks:
        if task["project_name"] == project_name:
            #pprint.pprint(task)
            if task["entity_name"] not in entity_names:
                entity_names.append(task["entity_name"])
            task_details.append({
                "entity_name": task["entity_name"],
                "task_type_name": task["task_type_name"],
                "due_date": task["due_date"],
                "status": task["task_status_short_name"],
                "entity_type_name": task["entity_type_name"]
            })


    return entity_names, task_details
# FIXME: This should get the thumbnail from the task or asset and download it so it can be used in the GUI
def get_preview_thumbnail():
    entity_names, entity_list = get_user_tasks_for_project(user_email, project_name)



"""
entity_name - Group by this second
entity_type_name - Group by this first
project_name - Filter by this first

"""
