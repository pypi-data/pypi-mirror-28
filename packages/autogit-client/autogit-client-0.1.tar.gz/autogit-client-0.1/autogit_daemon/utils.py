
def get_list_of_branch(in_list):
    branches = clean_the_list_of_branches(in_list)
    return [branch for branch in branches if '*' not in branch]

def clean_the_list_of_branches(in_list):
    return filter(len, filter(None, in_list.replace(" ", '').split('\n')))