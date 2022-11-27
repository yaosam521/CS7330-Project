# CS7330-Project

## Getting Started:
### Running the Virtual Environment
1. Type 'pip install virtualenv' to install virtualenvironment
2. Navigate to the directory in which you want to place your environment
3. DO NOT PUSH the venv into the github. Put it in a .gitignore.
4. To create a venv, type 'python -m venv name_of_venv'
5. To activate the venv, type 'name_of_venv\Scripts\activate.bat' for windows, and 'source name_of_venv/bin/activate' for MacOS
6. While the venv is running, type 'pip install -r requirements.txt'

### Running the Web App
1. Make sure the virtual environment is running
2. Navigate into the folder containing the project (in this case, 'sports_gui')
3. Type into the command line 'python manage.py runserver'
4. If the compilation is successful, follow this link: http://127.0.0.1:8000