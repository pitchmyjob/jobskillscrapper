# Job & Skill scrapper

## Installation

### Clone `jobskillscrapper` project

```
cd <path/to/clone/project>
git clone git@github.com:pitchmyjob/jobskillscrapper.git
```

### Install Python 3

```
sudo apt-get install python3 # Ubuntu / Debian
brew install python3 # OS X
```

### Install virtualenvwrapper

```
pip3 install virtualenvwrapper
```

Edit your `.profile` :

```
nano ~/.profile
```

Paste the content bellow :

```
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3.6 # Change the path to match your installation
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv # Change the path to match your installation
source /usr/local/bin/virtualenvwrapper.sh # Change the path to match your installation
```

Execute profile

```
source ~/.profile
```

## Create `jobskillscrapper` virtualenv

```
mkvirtualenv jobskillscrapper -p python3 --no-site-packages
```

### Install all dependencies

```
cd <path_to_your_project>
pip install -r requirements.txt
python manage.py migrate
```

### Scrap profile

```
python manage.py scrap --service (viadeo|linkedin) <http://profile_link_entry_point> --settings=settings

# Examples :
python manage.py scrap --service linkedin https://fr.linkedin.com/in/yannis-tannier-7017a169
python manage.py scrap --service linkedin http://fr.viadeo.com/fr/profile/yannis.tannier
```
