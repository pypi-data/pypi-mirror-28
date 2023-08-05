from subprocess import Popen, PIPE, call

def shell_true(string):
    '''Function for executing subprocess with shell true

    Useful when pipes are required

    Parameters
    ----------
    string: str
        string with the command to be executed

    '''
    p = Popen(string, stdout=PIPE, stderr=PIPE, shell=True)
    p.wait()
    stdout, stderr = p.communicate()
    print(stdout, stderr)

def shell_false(list):
    '''Function for executing subprocess with shell false

    Parameters
    ----------
    list: list
        list with the commands to be executed. e.g. ["echo", "test", ">",
        "test.txt"]

    '''
    p = Popen(list, stdout=PIPE, stderr=PIPE)
    p.wait()
    stdout, stderr = p.communicate()
    print(stdout, stderr)

def shell_stdout_write(list, output):
    '''Function to execute commands with ">" without shell=True

    Parameters
    ----------
    list: list
        list with the commands to be executed. e.g. ["echo", "test", ">",
        "test.txt"]
    output: str
        a string with the full path for the file.

    '''
    with open(output, "w") as f:
        call(list, stdout=f)