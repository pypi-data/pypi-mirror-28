# jlp  --- pip like Julia Package Manager
A package management system used to install and manage software packages for Julia.

<p>
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Julia_prog_language.svg/1280px-Julia_prog_language.svg.png" width="300"/>
</p>

## Requirement
- Julia 0.4+
- Python 2.7+ or Python 3.5+
- pip or pip3

## Installation

```sh
pip install jlp
```


## Usage
```
Usage:
  jlp <command> [options]

Commands:
  install                     Install packages.
  uninstall                   Uninstall packages.
  update                      Update installed packages.
  remove                      Alias remove.
  freeze                      Output installed packages in requirements format.
  list                        Alias freeze.
```

## Examples
### Show installed packages and version 
```sh
jlp list > REQUIRE
jlp freeze > REQUIRE
jlp freeze --format json > packages.json
jlp freeze -f yaml > requirements.yml
```

### Install packages
```sh
jlp install Pandas
jlp install Pandas IJulia==1.6.2 Requests
jlp install -r REQUIRE
jlp install -r packages.json
jlp install -r requirements.yml
```

### Uninstall packages
```sh
jlp uninstall Pandas
jlp uninstall Pandas PyCall
jlp remove Pandas PyCall
```

### Update installed packages
```sh
jlp update
```
