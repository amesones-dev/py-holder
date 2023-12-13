[![AZ Container Instance CI/CD Pipeline](https://github.com/amesones-dev/py-holder/actions/workflows/az-ci-cd.yml/badge.svg)](https://github.com/amesones-dev/py-holder/actions/workflows/az-ci-cd.yml)

# py-holder
#### Tools for developing python Flask apps in public Cloud

 

### Basic placeholder python app
This project is a basic Python Flask web application template to use as blueprint for new projects or as a basic 
placeholder for different kinds of environments and CI/CD procedures, focused on backend development and environment 
troubleshooting procedures.

Apart from the python code, basic templates for Docker, Kubernetes, Google GKE, Cloud Run environments and CI/CD systems
like Jenkins, GitHub Actions, Google Cloud Build, Google Cloud Deploy are to be provided during the project lifetime, to
compare Compute environments and CI/CD solutions procedures.

### The python application
It implements a light JSON web application built with Flask with several useful endpoints when developing in a Cloud 
environment.  
The list is constantly under revision. For now, these endpoints are implemented:

**Endpoints**
```console
/              returns HTTP code 200 + json payload with app info

/healthcheck   returns HTTP code 200 + json payload with status info

/ctime         returns HTTP code 200 + json payload with current time info

/mirror        returns HTTP code 200 + json with info about the incoming request processed, including cookies

/redirect      returns HTTP code 302 and sets location to root path

/stamp         returns HTTP code 200 and sets response cookie (key and value from app configuration)
```



**App configuration keys used** 
```shell
# App name for HTML views, it appears on titles, links, etc.
VIEW_APP_NAME = os.environ.get('VIEW_APP_NAME') or 'py-holder-demo'

# App info
APP_NAME = os.environ.get('APP_NAME') or 'py-holder-demo'
APP_VER = os.environ.get('APP_VER') or '1.0'

# Cookie settings for /stamp endpoint
STAMP_COOKIE_KEY = os.environ.get('STAMP_COOKIE_KEY') or 'x-stamp'
STAMP_COOKIE_VALUE = os.environ.get('STAMP_COOKIE_VALUE') or base64.urlsafe_b64encode(APP_NAME.encode())
 ```

## Running the application locally  

### Use Google Cloud Shell
* Create a [Google Cloud](https://console.cloud.google.com/home/dashboard)  platform account if you do not already have it.
* [Create a Google Cloud project](https://developers.google.com/workspace/guides/create-project) or use an existing one.
* To start coding right away, launch [Google Cloud Shell](https://console.cloud.google.com/home/).  

 
### ...or use your own development environment
#### Requirements

* Install python packages.

    ```console
    sudo apt update
    sudo apt install python3 python3-dev python3-venv
    ```
    
* Install pip 

    *Note*: Debian provides a package for pip

    ```shell
    sudo apt install python-pip
    ```
    Alternatively pip can be installed with the following method
    ```shell
    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3 get-pip.py
    ```
  
*Note: Console snippets for Debian/Ubuntu based distributions.*
### Clone git repo from Github
At this point either you are using Cloud Shell or you have a local development environment with python and Cloud SDK.
  ```shell
  git clone https://github.com/amesones-dev/py-holder.git
   ```

### Create a pyhon virtual environment

User your cloned git repository folder for your source code and Python [venv](https://docs.python.org/3/library/venv.html)
virtual environment to isolate python dependencies. 

```console
cd py-holder
python -m venv [venv-name]
source [venv-name]/bin/activate
```
Usual values for [venv-name] are `venv`, `dvenv`, `venv39` for a python 3.9 version virtual environment, etc.

### Install python requirements
```console
# From py-holder/src folder
pip install -r requirements.txt
```

### App configuration
At this point you are ready to configure and run the application.

### Running the app
  * Set Flask environment variables
   ```console
   export  FLASK_SECRET_KEY=$(openssl rand -base64 128)
   export  FLASK_APP=app:create_app
   ```

  * Run with flask
   ```console
   flask run   
   ```

  * Or run with gunicorn
   ```console
   gunicorn start:app   
   ```

*Use example*
```shell
# HTTP 
export ENDPOINT='healthcheck'
curl  "http://localhost:${PORT}/${ENDPOINT}"

# HTTPS 
curl  "https://localhost:${PORT}/${ENDPOINT}"

# HTTPS self-signed  certificate
curl --insecure "https://localhost:${PORT}/${ENDPOINT}"


# Basic app endpoints tests
curl -s  localhost:${PORT} |jq
{
  "name": "py-holder-APP-demo",
  "ver": "1.0"
}
curl -s  localhost:${PORT}/healthcheck |jq
{
  "status": "OK"
}
curl -s  localhost:${PORT}/ctime |jq
{
  "now_utc_iso": "2023-09-01T13:59:25.691353",
  "now_utc_timestamp": "1693576765.691366",
  "status": "OK"
}
curl -s  localhost:${PORT}/mirror |jq
{
  "0_id": "8784090160585",
  "1_server": [
    "0.0.0.0",
    5000
  ],
  "2_path": "/mirror",
  "3_method": "GET",
  "5_headers": {
    "Accept": "*/*",
    "Host": "localhost:8080",
    "User-Agent": "curl/7.74.0"
  },
  "6_cookies": {}
}

# Ask curl to use cookies and capture them to file
curl -s  -c capture_cookies localhost:${PORT}/stamp |jq
{
  "status": "OK"
}

cat capture_cookies 
# Output
# ...
# localhost       FALSE   /       FALSE   0       x-stamp KCcwLjAuMC4wJywgNTAwMCk=


# Use curl captured cookies from file with cookies
# Notice how the mirror endpoint now receives the cookie sent by curl
curl -s  -b capture_cookies localhost:${PORT}/mirror |jq
{
  "0_id": "8784090161032",
  "1_server": [
    "0.0.0.0",
    5000
  ],
  "2_path": "/mirror",
  "3_method": "GET",
  "5_headers": {
    "Accept": "*/*",
    "Cookie": "x-stamp=KCcwLjAuMC4wJywgNTAwMCk=",
    "Host": "localhost:8080",
    "User-Agent": "curl/7.74.0"
  },
  "6_cookies": {
    "x-stamp": "KCcwLjAuMC4wJywgNTAwMCk="
  }
}

# Non existent endpoint
export ENDPOINT=app_does_not_implement
curl -I -s  localhost:${PORT}/${ENDPOINT} --output http-test-${ENDPOINT}.log 
grep   'HTTP' http-test-${ENDPOINT}.log
# Output
  HTTP/1.1 404 NOT FOUND

```







