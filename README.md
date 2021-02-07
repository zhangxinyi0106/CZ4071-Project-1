# CZ4071-Project-1

### Set Up

####Open the project
Under your working directory:
```
git clone https://github.com/zhangxinyi0106/CZ4071-Project-1.git
cd CZ4071-Project-1
```

####Environment creation
```
conda env create -n <ur_env_name> -f environment.yml
conda activate <ur_env_name>
```
After creation of new environment:
* go to Settings -> Project:<project_name> -> Change Project Interpreter.
* Add python.exe under `PATH_TO_PYTHON/envs/UR_ENV` as interpreter.

###Update Dependency

####Export updated dependency:
```
conda env export > environment.yml
```

####Update environment:
```
conda env update --file environment.yml
```
