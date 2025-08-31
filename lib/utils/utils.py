import yaml
from pathlib import Path

def create_dot_spark(project_name, default_collection):
    dot_context = {
        "project_name": project_name,
        "default_collection": default_collection
    }

    with open(".spark", "w") as spark_file:
        yaml.dump(dot_context, spark_file)
    
    # ---my attempt at adding the .spark context file to the .gitignore files--------
    # if Path(".gitignore").exists():
    #     with open(".gitignore", "r") as gitignore_file:
    #         content = gitignore_file.read()
    #     if ".spark" not in content:
    #         with open(".gitignore", "a") as gitignore_file:
    #             gitignore_file.write("\n.spark")
    # else:
    #     with open(".gitignore", "w") as gitignore_file:
    #         gitignore_file.write(".spark")
