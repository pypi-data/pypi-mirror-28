from sys import version_info

YES = ['y', 'Y']
NO = ['n', 'N']

# If Python version is 3 or later, create raw_input function
if version_info.major >= 3:
    def raw_input(text):
        return input(text)


def question(text, default='y'):
    """Ask a question to the user
    Parameters:
        - text - The question to the user
        - default - Default answer ('y' or 'n')
    """

    answer = False
    if default == 'y':
        hint = '[Y/n]'
    elif default == 'n':
        hint = '[y/N]'
    else:
        hint = '[y/n]'

    while answer not in YES and answer not in NO:
        answer = raw_input(text + hint) or default
    if answer in YES:
        return(True)
    else:
        return(False)
