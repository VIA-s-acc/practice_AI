import subprocess
import os
def run():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    subprocess.call([f'{this_dir}\\.venv\\Scripts\\activate.bat'])
    subprocess.call([f'{this_dir}\\.venv\\Scripts\\flet.exe', 'run', f'{this_dir}\\gui'])

    
if __name__ == '__main__':
    run()