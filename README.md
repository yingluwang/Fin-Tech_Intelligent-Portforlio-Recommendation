# Project Goal
---
Personalized user's investment portfolio based on sentiment analysis to their personal twitter account and the result of a short risk tolerance questionnaire.

# Setup
---
## Prerequisite

**Python3** installed

## Installing Python

First, check to see if **Python3** is already installed on your machine:

```` sh
# Mac Terminal:
which python3 # check for Python Version 3.x

# Windows Command Prompt:
where python
````

If **Python3** is not installed, follow the OS-specific instructions below to install it.

If Python version 2.x is installed, [please upgrade to 3.x](https://wiki.python.org/moin/Python2orPython3)

Once **Python3** is installed, you should be able to run `python3` and `pip3`, from the command-line. And you should be able to check which version of each you have installed:

```shell
# Using Python 3:
python3 --version #> Python 3.x.x
pip3 --version #> pip 9.0.1 from /usr/local/lib/python3.6/site-packages (python 3.6)
```
### Windows OS

Download Python 3 from the [Python website](https://www.python.org/downloads/).

Note: Make sure you check the option, "Add Python 3.6 to PATH" when you are installing Python from the downloaded installer.

### Mac OS

You may download Python 3 from the [Python website](https://www.python.org/downloads/), but you are encouraged to use the [Homebrew](https://brew.sh/) package manager to install it.

Check to see if Homebrew is installed:

```` sh
which brew
````

Install Homebrew if necessary:

```` sh
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
````

[Use Homebrew to install Python 2.x or 3.x](http://docs.brew.sh/Homebrew-and-Python.html) and follow any post-installation instructions:

To install Python 2.x (not recommended):

```` sh
brew install python
brew linkapps python
````

To install Python 3.x (recommended):

```` sh
brew install python3
````

> NOTE: If you choose to install Python 3 on a Mac using Homebrew, be aware that if you see references to running `python` you should instead run `python3`, and if you see references to `pip` you should instead run `pip3`.

## Setup Twitter Environment Variables

Set a new environment variables called for Twitter API Authorization:

```shell
# Mac Terminal:
echo export TWITTER_API_KEY="F29b8D6lDVJ1T6BNzXN5a9xcX" >> ~/.bash_profile
echo export TWITTER_API_SECRET="SxVsXszZ6fw5X48SvINQuXXTFqPVL3dH8JTcnEArr5H1SFMEmK" >> ~/.bash_profile
echo export TWITTER_ACCESS_TOKEN="890374586323398657-DWt985sWMhbeBq1T26jYUdfuMlk2TDc" >> ~/.bash_profile
echo export TWITTER_ACCESS_TOKEN_SECRET="88d81mDuJSuGEqqkkX1FqbVxXIMFGwbi8TbMyTm7guha0" >> ~/.bash_profile
# ... or more commonly, place inside ~/.bash_profile the following contents:
export TWITTER_API_KEY=F29b8D6lDVJ1T6BNzXN5a9xcX
export TWITTER_API_SECRET=SxVsXszZ6fw5X48SvINQuXXTFqPVL3dH8JTcnEArr5H1SFMEmK
export TWITTER_ACCESS_TOKEN=890374586323398657-DWt985sWMhbeBq1T26jYUdfuMlk2TDc
export TWITTER_ACCESS_TOKEN_SECRET=88d81mDuJSuGEqqkkX1FqbVxXIMFGwbi8TbMyTm7guha0

# Windows Command Prompt:
set TWITTER_API_KEY="F29b8D6lDVJ1T6BNzXN5a9xcX"
set TWITTER_API_SECRET="SxVsXszZ6fw5X48SvINQuXXTFqPVL3dH8JTcnEArr5H1SFMEmK"
set TWITTER_ACCESS_TOKEN="890374586323398657-DWt985sWMhbeBq1T26jYUdfuMlk2TDc"
set TWITTER_ACCESS_TOKEN_SECRET="88d81mDuJSuGEqqkkX1FqbVxXIMFGwbi8TbMyTm7guha0"
# or use `setx NYU_INFO_2335="SecretPassword123"` to set this variable globally
```

>NOTE: On a Mac, you should be able to see and manage environment variables within a hidden file called
`~/.bash_profile`. To navigate to this file:
open ~/.bash_profile
touch ~/.bash_profile

After setting a new environment variable, exit and re-open your command-line application for the changes to take affect.

### Getting

You will know it works if you can access the environment variable from the command-line:

```shell
# Mac Terminal:
echo $TWITTER_API_KEY #> F29b8D6lDVJ1T6BNzXN5a9xcX

# Windows Command Prompt:
echo %TWITTER_API_KEY% #> F29b8D6lDVJ1T6BNzXN5a9xcX
```

## RoboVest Installation Instructions

(Assuming python is installed)

-Clone Robovest repository to your local machine;
-Using CLI, navigate to the fork you just cloned;
-Install flask editable using “pip3 install --editable .” in a virtual environment
-Setup Environment Variables using “export FLASK_APP=robovest
export FLASK_DEBUG=true”;
-Type “flask initdb” to initialize the database; Should expect an instruction “Initialized the database.”
-Type “flask run”; Should expect following options:
“* Serving Flask app "robovest"
 * Forcing debug mode on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 315-246-517”
-Copy http://127.0.0.1:5000/ to your web browser to start using the APP.
