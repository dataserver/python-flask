:: wt new-tab --profile "Command Prompt" --startingDirectory  "D:\python\project\.venv\Scripts" cmd /k "activate  && cd D:\python\project & python selector.py"
:: %cd% refers to the current working directory (variable)
:: %~dp0 refers to the full path to the batch file's directory (static)
:: %~dpnx0 and %~f0 both refer to the full path to the batch directory and file name (static).

wt new-tab --profile "Command Prompt" --startingDirectory  "%~dp0.venv\Scripts" cmd /k "activate  && cd %~dp0 && python python-flask/runner.py"
