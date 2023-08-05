### Overview

codegenit is a development tool for use with "Specification First REST APIs"

Given a OpenAPI specification file (fka swagger) a skeleton server stub project is created. On subsequent runs, the project will be updated as needed from the newly generated stub project.

#### First run

1) The CODEGEN_DIR is deleted and a new server stub is created and placed in the CODEGEN_DIR using the swagger codegen docker image (https://hub.docker.com/r/swaggerapi/swagger-codegen-cli/)
2) The PROJECT_DIR is created, if it doesn't exist
3) All models are copied from CODEGEN_DIR/models to PROJECT_DIR/models
4) All controllers are copied from CODEGEN_DIR/controllers to PROJECT_DIR/controllers
5) `__init__.py`, `__main__.py`, `encoder.py`, and `util.py` are copied from the CODEGEN_DIR to the PROJECT_DIR.
6) The CODEGEN_DIR/swagger directory is copied to PROJECT_DIR/swagger (this directory contains the `swagger.yaml` file)
7) The CODEGEN_DIR/requirements.txt is copied to PROJECT_DIR/requirements.txt.

After the initial run, the project can be started:

`python -m PROJECT_DIR`

#### Subsequent runs

1) The CODEGEN_DIR is deleted and a new server stub is created and placed in the CODEGEN_DIR using the swagger codegen docker image (https://hub.docker.com/r/swaggerapi/swagger-codegen-cli/)
2) All models are copied from CODEGEN_DIR/models to PROJECT_DIR/models
3) Missing functions are added to each of the PROJECT_DIR/controllers
4) `from xxx import xxx` statements are updated for each of the PROJECT_DIR/controllers
5) missing `import` statements are added for each of the PROJECT_DIR/controllers
6) Docstrings are updated for each of the PROJECT_DIR/controllers functions
7) changed arguments are noted for each of the PROJECT_DIR/controller functions
8) The CODEGEN_DIR/swagger directory is copied to PROJECT_DIR/swagger (this directory contains the `swagger.yaml` file)


### Getting started

```
python3 -m venv venv
source venv/bin/activate
pip install codegenit
wget --output-document api.yml https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v2.0/yaml/petstore.yaml
mv petstore.yaml api.yml
codegenit --check
codegenit
```


### Usage
```
$ codegenit --help
usage: codegenit [-h] [-c CODEGEN_DIR] [-p PROJECT_DIR] [-s SWAGGER_FILE]
                 [--check]

Generate a python project from a swagger file.

optional arguments:
  -h, --help            show this help message and exit
  -c CODEGEN_DIR, --codegen_dir CODEGEN_DIR
                        A folder in which to place the codegend project. (default: ./swagger_codegen/)
  -p PROJECT_DIR, --project_dir PROJECT_DIR
                        A folder in which to place the codegend project. (default: ./)
  -s SWAGGER_FILE, --swagger_file SWAGGER_FILE
                        A folder in which to place the codegend project. (default ./api.yml)
  --check               Run in check mode, no changes to PROJECT_DIR (except trailing whitespace removal)
```

### Sample run

```
(venv) ➜  codegenit_test codegenit
[  deleted   ] EXISITNG CODEGEN DIRECTORY
[  created   ] CODEGEN DIRECTORY
[  running   ] CODEGEN DOCKER CONTAINER
[   exists   ] /Users/bthornto/github/codegenit_test/swagger_server
[  created   ] /Users/bthornto/github/codegenit_test/swagger_server/__init__.py
[  created   ] /Users/bthornto/github/codegenit_test/swagger_server/__main__.py
[  created   ] /Users/bthornto/github/codegenit_test/swagger_server/encoder.py
[  created   ] /Users/bthornto/github/codegenit_test/swagger_server/util.py
[  updated   ] /Users/bthornto/github/codegenit_test/swagger_server/swagger
[  updated   ] /Users/bthornto/github/codegenit_test/swagger_server/models
[  created   ] /Users/bthornto/github/codegenit_test/swagger_server/controllers
[  created   ] /Users/bthornto/github/codegenit_test/swagger_server/controllers/__init__.py
[  created   ] /Users/bthornto/github/codegenit_test/swagger_server/controllers/pets_controller.py
```
