import subprocess
import traceback
import os
import string
import sys
EXIT_CODES = {
    'SUCCESS': 0,
    'VENV_ERROR': 1,
    'VERSION_ERROR': 2,
    'PIP_ERROR': 3
}
colors = {
    'HEADER': '\033[95m',
    'BLUE': '\033[94m',
    'GREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
}

def install(req_path = 'requirements.txt'):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"{colors['HEADER']}Start Checker... {colors['ENDC']}")
    print(f"{colors['BLUE']}Checking python version...{colors['ENDC']}")
    python_version = sys.version.split()[0]
    print(f"{colors['GREEN']}Python version is {python_version} {colors['ENDC']}")
    if not '3.10' in python_version:
        print(f"{colors['FAIL']}Python version is not 3.10.* ❌{colors['ENDC']}")
        print(f"{colors['FAIL']}Fix the error and try again{colors['ENDC']}")
        exit(EXIT_CODES['VERSION_ERROR'])
        
    
    if not os.path.exists('.venv'):
        print(f"{colors['FAIL']}Virtual environment does not exist, creating...{colors['ENDC']}")
        try:
            subprocess.check_call([sys.executable, '-m', 'venv', '.venv'])
            print(f"{colors['GREEN']}Virtual environment ('.venv') created ✅{colors['ENDC']}")
        except subprocess.CalledProcessError:
            print(f"{colors['FAIL']}Failed to create virtual environment ❌{colors['ENDC']}")
            print(f"{colors['FAIL']}Fix the error and try again{colors['ENDC']}")
            print(f"{colors['FAIL']}Need python version 3.10{colors['ENDC']}")
            exit(EXIT_CODES['VENV_ERROR'])
    else:
        print(f"{colors['GREEN']}Virtual environment already exists ✅{colors['ENDC']}")
        print(f"{colors['BLUE']}Checking virtual environment python version...{colors['ENDC']}")
        if sys.platform == 'win32':
            venv_python = os.path.join(f'{this_dir}/.venv', 'Scripts', 'python.exe')
        else:
            venv_python = os.path.join(f'{this_dir}/.venv', 'bin', 'python')
        python_version = subprocess.check_output([venv_python, '--version'], shell=True, stderr=subprocess.DEVNULL).decode().strip()
        print(f"Virtual environment Python version: {python_version}")
        if not '3.10' in python_version:
            print(f"{colors['FAIL']}Virtual environment Python version is not 3.10 ❌{colors['ENDC']}")
            print(f"{colors['FAIL']}Fix the error and try again{colors['ENDC']}")
            exit(EXIT_CODES['VERSION_ERROR'])
    if sys.platform == 'win32':
        libs = subprocess.check_output([f"{this_dir}/.venv/Scripts/pip", "list"]).decode().split('\n')
    else: 
        libs = subprocess.check_output([f"{this_dir}/.venv/bin/pip", "list"]).decode().split('\n')
        
    libs = libs[2:]
    for i in range(len(libs)):
        libs[i] = ' '.join(libs[i].split()).replace(' ', '==')
    
    try:
        print(f"{colors['BLUE']}Updating pip...{colors['ENDC']}")
        subprocess.check_call([venv_python, "-m", "pip", "install", "--upgrade", "pip"])
        print(f"{colors['GREEN']}pip updated ✅{colors['ENDC']}")
    except subprocess.CalledProcessError:
        print(f"{colors['FAIL']}Failed to update pip ❌{colors['ENDC']}")
        print(f"{colors['FAIL']}Fix the error and try again{colors['ENDC']}")
        
    with open(req_path, 'r') as f:
        for line in f.readlines():
            lib = line.strip()
            lib = ''.join(filter(lambda x: x in string.printable, lib))
            lib = lib.replace('\x00', '')
            if lib:
                if lib in libs:
                    print(f"{colors['GREEN']}Check Pass | {lib} is already installed ✅{colors['ENDC']}")
                elif lib == "torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118":
                    print(f"{lib} not installed, installing...")
                    pcgs  = [
                        'torch',
                        'torchvision',
                        'torchaudio'
                    ]
                    command = [venv_python, '-m', 'pip', 'install'] + pcgs + ['--index-url', 'https://download.pytorch.org/whl/cu118']
                    subprocess.run(command, check=True)
                else:
                    print(f"{lib} not installed, installing...")
                    try:
                        print(f"{colors['BLUE']}Check : {lib} not installed, installing...{colors['ENDC']}")
                        subprocess.run([venv_python, '-m', 'pip', 'install', lib], check=True)
                        print(f"{colors['GREEN']}Successfully installed {lib} ✅{colors['ENDC']}")
                    except Exception as e:
                        print(f"{colors['FAIL']}Failed to install {lib} ❌{colors['ENDC']}")
                        print(f"{colors['FAIL']}Error: \n", e)
                        print(f"{colors['FAIL']}Traceback: \n", traceback.format_exc())
                        print(f"{colors['FAIL']}Fix the error and try again{colors['ENDC']}")
                        exit(EXIT_CODES['PIP_ERROR'])
                    
    print(f"{colors['GREEN']}Successfully checked all requirements ✅{colors['ENDC']}")
    print(f"{colors['GREEN']}Starting program...{colors['ENDC']}")
    exit(EXIT_CODES['SUCCESS'])
                        
if __name__ == '__main__':
    install()
