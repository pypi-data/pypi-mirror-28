For regular installs:
    ``sudo pip install ca-apm-agent`` (sudo because we want to ensure that the agent script/binary is created in PATH)
For installs from this git repo:
    ``sudo pip install git+https://github-isl-01.ca.com/APM/PythonAgent.git``
For Dev environment installs:
    Do a traditional git clone first:
        ``git clone https://github-isl-01.ca.com/APM/PythonAgent.git``
    Then
        ``cd PythonAgent`` (change to the directory)

        ``sudo pip install -e .``
    The above lets you create a link in the python lib to point to the project directory so that you can make changes to
    the library and see the results without unnecessary copy/pastes
