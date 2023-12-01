import subprocess
from subprocess import Popen, PIPE
import sys

#---------------------Manually Change Variables----------------------
# ClearML parameters for credentials
a_key = "<your access key>" 
s_key = "<your secret key>"

# ClearML parameters for speical task
task_name = "<your task name>" 
project_name = "<your project name>" 
args_change_list = [] # e.g. [("epochs",2),("batch_size",128)]
queue_name = "<your queue name>" 

#-------------------------Task Execution-------------------------
# install clearml and clearml-agent
subprocess.check_call([sys.executable, "-m", "pip", "install", "clearml", "clearml-agent"])

# clearml-agent initialization (skip the info except for credential keys)
p = subprocess.Popen('clearml-agent init', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
stdout, stderr = p.communicate(input = f"\n{a_key}\n{s_key}\n\n\n\n\n\n\n".encode("utf-8"))

# Pass credential
from clearml import Task
Task.set_credentials(api_host="https://api.clear.ml",
                     web_host="https://app.clear.ml",
                     files_host="https://files.clear.ml",
                     key=a_key,
                     secret=s_key)
task = Task.create(project_name=project_name,
                   task_name=task_name,
                   script='torch_script.py',
                   requirements_file="requirements.txt",
                   argparse_args=args_change_list)
Task.enqueue(task,queue_name = queue_name)
_ = subprocess.Popen(f'clearml-agent daemon --queue {queue_name}', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)




