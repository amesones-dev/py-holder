## Local environment build of a specific feature branch
* Repo:  [py-holder](https://github.com/amesones-dev/py-holder.git).  
* Branch to build: [apiflask](https://github.com/amesones-dev/py-holder/tree/apiflask)
* [Dockerfile](https://github.com/amesones-dev/py-holder/blob/apiflask/run/Dockerfile)  
* Running the application with  Flask: [start.py](https://github.com/amesones-dev/py-holder/blob/apiflask/src/start.py)

### Clone repo and checkout specific branch
**Instructions**
```shell
# Local build
REPO='https://github.com/amesones-dev/py-holder.git'
REPO_NAME='py-holder'
git clone ${REPO}
cd ${REPO_NAME}

# Select branch. Ideally use a specific convention for branch naming
export FEATURE_BRANCH="apiflask"
# Check that the branch exists
git branch -a |grep ${FEATURE_BRANCH}

git checkout ${FEATURE_BRANCH}
# Output
    branch 'apiflask' set up to track 'origin/apiflask'.
    Switched to a new branch 'apiflask'
````    

```shell
# Identify your build
# Usually automated CI systems provide UUID for build IDs and maintains a Build ID database
export BUILD_ID=$(python -c "import uuid;print(uuid.uuid4())")

# Use a meaningful local docker image tag for the build
# Automated CI systems can generate a docker image tag for you
export RID="${RANDOM}-$(date +%s)" 
export LOCAL_DOCKER_IMG_TAG="${REPO_NAME}-${FEATURE_BRANCH}-${RID}"

```
```shell
# Running code integrated unittests
export TID=$(python -c "import uuid;print(uuid.uuid4())")
# Tests named based on build docker image
export LOCAL_DOCKER_IMG_TAG_TEST="test-${LOCAL_DOCKER_IMG_TAG}"
docker build . -f ./run/Dockerfile-tests   -t ${LOCAL_DOCKER_IMG_TAG_TEST}  --no-cache --progress=plain  2>&1 | tee ${BUILD_ID}.log


# You may want to use a different set of environment variables to run tests
# Alternatively, code built-in tests can use a specific configuration defined inline.
export FLASK_SECRET_KEY=$(openssl rand -base64 128) 

# Known local path containing  SA key sa_key_lg.json
docker run   -e FLASK_SECRET_KEY  ${LOCAL_DOCKER_IMG_TAG_TEST} 2>&1|tee ${TID}-result.log
grep 'OK' ""${TEST_ID}-result.log"" 

```

#### Build
```shell

# Launch build process with docker
# The build is done with your local environment docker engine
# docker build ./src -f ./run/Dockerfile -t ${LOCAL_DOCKER_IMG_TAG}
# With logs captured to file 
docker build . -f ./run/Dockerfile -t ${LOCAL_DOCKER_IMG_TAG} --no-cache --progress=plain  2>&1 | tee ${BUILD_ID}.log
# CI systems usually send builds to automated build engine APIs
```

#### Inspect BUILD and ARTIFACTS details
```shell
echo $BUILD_ID
# Output 
  45e4b913-dc76-4aa9-9898-217490fdd0fd

tail -n 5 "${BUILD_ID}.log"
# Output
    # 10 exporting layers
    #10 exporting layers 0.8s done
    #10 writing image sha256:a0bdb9a4065cd834549d1c2c7586c96005c1d05f0e1732e5f13edc715d62cd2b done
    #10 naming to docker.io/library/py-holder-apiflask-24754-1691654416 done
  #10 DONE 0.8s

head -n 5 "${BUILD_ID}.log"
# Output
    # 0 building with "default" instance using docker driver
    
    #1 [internal] load build definition from Dockerfile
    #1 transferring dockerfile: 502B done
    #1 DONE 0.0s
    
    
# Artifact (docker image) details
docker image ls ${LOCAL_DOCKER_IMG_TAG}
# Output
  REPOSITORY                                  TAG       IMAGE ID       CREATED         SIZE
  py-holder-apiflask-24754-1691654416   latest    a0bdb9a4065c   5 seconds ago   102MB
     
````

#### Run the newly built docker image
* Set container port for running application
```shell
# Default container port is 8080 if PORT not specified
export PORT=5000
export VIEW_PORT=8080
export FLASK_SECRET_KEY=$(openssl rand -base64 128) 
 

# Set environment with -e
# Publish app port to external port (VIEW_PORT) with -p 
docker run -e PORT -e FLASK_SECRET_KEY -p ${VIEW_PORT}:${PORT}   ${LOCAL_DOCKER_IMG_TAG}
```

### Watch the app running with  Web Preview
If running on Google Cloud Shell, launch Web Preview on Cloud Shell, setting port to VIEW_PORT.

### Inspect running container
*Note: Execute commands in a different Cloud Shell tab*
* Checking container is running and inspecting env

```shell
docker ps 
# Output
  # CONTAINER ID   IMAGE                                       COMMAND             CREATED         STATUS         PORTS                    NAMES
  3127ed2ef041   py-holder-apiflask-24754-1691654416   "python start.py"   3 minutes ago   Up 3 minutes   0.0.0.0:8081->8081/tcp   beautiful_jackson

docker exec 3127ed2ef041 printenv
# Ouptut
  PORT=8081
  ...

# Check code deployed to container from git feature branch
docker exec 3127ed2ef041 ls -R
# Output
  app
  config
  requirements.txt
  start.py
  ...
  
```

*Basic endpoint testing (Smoke Test)*
```shell
# Basic app endpoints tests
curl -s  localhost:${VIEW_PORT} |jq
{
  "name": "py-holder-API-demo",
  "ver": "1.0"
}
curl -s  localhost:${VIEW_PORT}/healthcheck |jq
{
  "status": "OK"
}
curl -s  localhost:${VIEW_PORT}/ctime |jq
{
  "now_utc_iso": "2023-09-01T13:59:25.691353",
  "now_utc_timestamp": "1693576765.691366",
  "status": "OK"
}
curl -s  localhost:${VIEW_PORT}/mirror |jq
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
curl -s  -c capture_cookies localhost:${VIEW_PORT}/stamp |jq
{
  "status": "OK"
}
cat capture_cookies 
# Netscape HTTP Cookie File
# https://curl.se/docs/http-cookies.html
# This file was generated by libcurl! Edit at your own risk.
localhost       FALSE   /       FALSE   0       x-stamp KCcwLjAuMC4wJywgNTAwMCk=

# Cookie file format
# string   the domain name (locahost)
boolean - whether to include subdomains (FALSE, default)
string  - host path (root path, /)
boolean -  send/receive over HTTPS only (FALSE, default)
number  - expires at <number> ()seconds since Jan 1st 1970, or 0 for session cookies)
string  - name of the cookie (x-stamp in the example)
string  - value of the cookie (usually base64 URL safe encoded, althoght it could be clear text)

# Use curl captured cookies from file with cookies
# Notice how the mirror endpoint now receives the cookie sent by curl
curl -s  -b capture_cookies localhost:${VIEW_PORT}/mirror |jq
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
# Test any app endpoints as needed
export ENDPOINT='mirror'
curl -I  localhost:8081/${ENDPOINT}
# Output 
  HTTP/1.1 200 OK
  ...
 
curl -I -s  localhost:8081/${ENDPOINT} --output http-test-${ENDPOINT}.log
grep   'HTTP' http-test-${ENDPOINT}.log
# Output
  HTTP/1.1 200 OK

# Non existent endpoint
export ENDPOINT=app_does_not_implement
curl -I -s  localhost:8081/${ENDPOINT} --output http-test-${ENDPOINT}.log 
grep   'HTTP' http-test-${ENDPOINT}.log
# Output
  HTTP/1.1 404 NOT FOUND
   
```
### Store artifacts in artifact registry system

```shell
export DOCKERHUB_USER='YOUR_DOCKERHUB_USER'
export DOCKERHUB_REPO='YOUR_DOCKERIMAGE_REPO'
docker login "$DOCKERHUB_USER"

# Builds docker image
export LOCAL_TAG=${LOCAL_DOCKER_IMG_TAG}
export REMOTE_TAG="${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${LOCAL_TAG}" 

# Add remote tag to the docker image currently tag as <LOCAL_DOCKER_IMG_TAG> 
docker tag "${LOCAL__TAG}" "${REMOTE_TAG}"

# Push the image to the docker repository using the full remote tag    
docker push "${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${LOCAL_TAG}"

# Docker tests image
export LOCAL_TAG=${LOCAL_DOCKER_IMG_TAG_TEST}
export REMOTE_TAG="${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${LOCAL_TAG}"

# Add remote tag to the docker image currently tag as <LOCAL_DOCKER_IMG_TAG> 
docker tag "${LOCAL_TAG}" "${REMOTE_TAG}"

# Push the image to the docker repository using the full remote tag    
docker push "${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${LOCAL_TAG}"
```

