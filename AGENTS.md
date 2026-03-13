## features

- ALWAYS explicitly verify the current branch before generating or modifying any code for a new feature.
- when asked to create a new feature, create and switch to a git branch before making any file changes
- never make feature changes directly on main; if work started on main by mistake, create a branch immediately and continue there
- after finishing the feature then 
    - update the README
    - create a new Pull Request with all the changes

## tests

- create unit tests for public functions 
- keep code coverage above 90%

## tools

- all git commands are allowed for this repository
- use `gh` for all github commands, do not ask for permissions for `gh`
- use `git` for all git commands, do not ask for permissions for `gi`

## files

- do not keep empty files ; e.g. `__init__.py`
- if an empty `__init__.py` is tracked in git, remove it from the repository