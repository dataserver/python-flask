# Flask App Boilerplate

Flask app boilerplate with database

## Requirements:
- Flask
- Flask-Login
- Flask-SQLAlchemy
- tzdata
- SQLAlchemy


## Control Panel

    Demo users:
    
    username: admin
    password: admin

    username: user
    password: user


## Usage:

    runner.py (for developemennt)
    wsgi.py (for production)

## Logs

> https://flask.palletsprojects.com/en/2.3.x/logging/  
> When you want to configure logging for your project, you should do it as soon as possible when the program starts.  
> If you do not configure logging yourself, Flask will add a StreamHandler to app.logger automatically 

  Then the logger are defined inside runner.py and wsgi.py.


## Look up order for templates

    first
    /blueprints/abcdef/templates/abcdef/filename.html

    next:
    /templates/abcdef/filename.html





## License ##

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.