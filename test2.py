from cx_Freeze import setup, Executable

# Replace 'app.py' with the name of your Streamlit application script
executables = [Executable('test.py')]

# Replace 'AppName' with the desired name of your executable file
setup(name='AppName',
      version='1.0',
      description='Description of your application',
      executables=executables)
