# fittify-backend
## Setup
The first thing to do is to clone the repository:
```sh
$ git clone https://github.com/Fittify/fittify-backend.git
$ cd fittify-backend
```

Create a virtual environment to install dependencies in and activate it:
```sh
conda create -n env python=3.9
conda activate env
```

Then update pip and install the dependencies:
```sh
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
cd backend
python manage.py migrate
python manage.py runserver
```

## Endpoints
```
    admin
    register
    login
    login/refresh
    logout
    user
    user/change_password
    user/<int:user_id>
    user/<int:user_id>/change_password
    users
```
