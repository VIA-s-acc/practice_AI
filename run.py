import subprocess
import os
def run():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    subprocess.call([f'.venv/Scripts/flet', 'run', 'gui'])

    
if __name__ == '__main__':
    run()