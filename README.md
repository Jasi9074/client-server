# 🆕 Initializing Project

### Step 1: Clone the project

Using HTTPS Connection:

```sh
git clone https://github.com/Jasi9074/client-server
```

Using SSH Connection:

```sh
git clone git@github.com:Jasi9074/client-server
```

### Step 2: Initialize Virtual Environment (Recommended)

Install Python and execute following commands:

```sh
python -m pip install virtualenv
python -m venv venv
```

### Step 3: Activate Virtual Environment

Using the command based on your current shell

```sh
# CMD
ENV\Scripts\activate.bat
# Powershell
.\ENV\Scripts\Activate.ps1
# Bash and Zsh
source ENV/bin/activate
# Fish
source ENV/bin/activate.fish
```

### Step 4: Install Requirements

```sh
pip install -r requirements.txt
```

### Step 5: Initialize Server Database

```sh
python manage.py migrate
```

### Step 6: Run Server (on Local Network)

```sh
./run
```
