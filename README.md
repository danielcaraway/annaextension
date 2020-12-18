## README

### IMPETUS:
I want a consolidated shopping list

### V1 GOAL:

1. INPUT: User enters 5 distinct urls for recipes they are making this week
2. OUTPUT: Aggregated shopping list


## HOW TO:


1. Make & start virtual environment, install flask

```bash
python3 -m venv v-env
source v-env/bin/activate
pip3 install flask gunicorn
```

2. Make app.py

``` python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, world!"

if __name__ == "__main__":
    app.run(debug=True)
```

3. Push it live
   1. git init
   2. touch .gitignore Procfile
   3. switch github users (if you're crazy like me)
   4. add Procfile for heroku `web: gunicorn app:app`
   5. `pip3 freeze > requirements.txt`
   6. `heroku create amazing-app-name`
   7. `git add . && git commit -m "FLASK PARTY" && git push heroku master`