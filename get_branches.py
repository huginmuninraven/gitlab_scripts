import gitlab
import os
from texttable import Texttable

# Given a Gitlab Group ID, this script returns all branches that are not main, for targeted cleanup


##############
#  Variables #
##############
destination_url = ''
destination_group_name = 1
destination_token = ''

##############
#  Functions #
##############

# Creates connection to Gitlab
def create_connection(url,token):
    gl = gitlab.Gitlab(url,token)
    return gl
    
# Gets list of all projects
def get_projects(connection, group_name):
    group = connection.groups.get(group_name)
    projects = group.projects.list(all=True, include_subgroups=True)
    return projects

    
### Main ### 

if __name__ == '__main__':
    
    t = Texttable()

    # Create connections to each gitlab
    gl = create_connection(destination_url, destination_token)
    
    # get all projects under one group
    branch_projects = get_projects(gl,destination_group_name)

    for project in branch_projects:
        project = gl.projects.get(project.id,statistics=True)

        # Excludes projects that don't have a parent_id
        if project.namespace["parent_id"]:
            branches = project.branches.list()

            # Use this to delete all merged branches
            # project.delete_merged_branches()
    
            # Add all non-main projects to a table
            for branch in branches: 
                if branch.name not in [ 'develop', 'master','main','default']:
                    t.add_rows([['Project', 'Branch', 'Merged','Author'], [project.name, branch.name, branch.merged, branch.commit['author_name']]])

    # Prints out table of branches 
    print(t.draw())

    
    print("Program Complete")
        
