########################################################################################################################
# CA APM Python Agent Configuration File

# Warning: if you nest values like X.Y = A, you should not apply values to X like X = B.
# Eg 1:  X = A
#        X.Y = B will cause an an error and will cause the agent to discard this configuration file
# Eg 2:  X.Y = A
#        X = B will cause an overwrite of X and you will lose X.Y =A
########################################################################################################################
#
######################
# Properties for Agent are listed below
#   @@@ If preceded by #HOT then they are hot properties otherwise the agent requires a restart

# Hostname and Port number required to connect to Collector Agent/ APMIA Package
# Host is to be provided in '' eg: 'google.com' or '127.0.0.1'
host='127.0.0.1'
# Leave port as is unless you changed it in the Collector Agent/ APMIA
port=5005

# Application Name to be displayed in EM
# Please change it to reflect your App Name
# To be provided in '' eg: 'App Name'
app_name='Default'

# Agent worker(s) sleep time in SECONDS
# The time period after which the Python Agent should send data to the Collector Agent
sleep_time=2


#################################################
### Logging Section
# Properties that affect Logging
# Logging is configured using dictConfig
# https://docs.python.org/2/library/logging.config.html#dictionary-schema-details
# The below is converted to a dictionary that resembles the snippet in the above link
# The below notation was used so that there was uniformity across CA's products
# log.handlers.file.filename and log.loggers.python_agent.level can be changed to fit your needs.
# Other Values here should be changed with caution.

log.version=1
log.disable_existing_loggers=False

## log formatters sub-section
# formatter name=simple
log.formatters.simple.format='%(asctime)s [%(levelname)s] [PID-%(process)d] [%(threadName)s] [%(name)s]  %(message)s'
log.formatters.simple.datefmt='%m/%d/%y %I:%M:%S %p %Z'

## log handler sub-section
# handler name=console . These are the properties for logs that go to the console
log.handlers.console.class=logging.StreamHandler
log.handlers.console.level=WARNING
log.handlers.console.formatter=simple
log.handlers.console.stream='ext://sys.stdout'

# handler name=file . These are the properties for logs that go to a file
log.handlers.file.class=ca_apm_agent.logging_handlers.RotatingFileHandler
log.handlers.file.formatter=simple
log.handlers.file.level=DEBUG
# The below logfile will get created in the directory you run the command to start your agent.
# Relative paths are allowed. Providing an absolute path will override the above behavior.
# It assumes that it has necessary permissions to create intermediary folders that do not exist. 
log.handlers.file.filename=ca_apm_logs/python_agent.log
log.handlers.file.maxBytes=50000000
log.handlers.file.backupCount=2

## Actual logger sub-section
# logger name=python_agent . This is the actual logger that is used by the agent. It uses the above defined (seen below)
# Change the below level to DEBUG for detailed logs, if required.
log.loggers.python_agent.level=INFO
log.loggers.python_agent.handlers=['console','file']
log.loggers.python_agent.propagate=False

### End Logging section

