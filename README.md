# CZ4071-Project-1

### Notice
`preprocessing.py` and `faculty.py` are well-commented since they are for analysing purposes. `project.py` and
`interface.py` are only for GUI purposes and are less documented. The users are recommended to go through the report before running.

The project, and its dependencies/provided pickles are tested on multiple Windows10 machines.

### Set Up

#### Environment creation
```
conda env create -n <ur_env_name> -f environment.yml
conda activate <ur_env_name>
```
(PyCharm only) After creation of new environment:
* go to Settings -> Project:<project_name> -> Change Project Interpreter.
* Add python.exe under `PATH_TO_ANACONDA/envs/UR_ENV` as interpreter.

### Run
To start the Analysing Tool:
```
python project.py
```
