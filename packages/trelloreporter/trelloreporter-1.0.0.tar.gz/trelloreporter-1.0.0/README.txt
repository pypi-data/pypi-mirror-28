# Trello Reporter

## Copyright

Copyright &copy; 2017 Internet Solutions (Pty) Ltd. All rights reserved.

## License

Licensed under the Apache Software License 2.0. See LICENSE for details.

## Installation
### Requirements
Trello Reporter requires python 3.5>. The installation instructions were all conducted using `3.6.3` and `pip 9.0.1`. 

An app directory to store app logs, app data and app configuration. This is under `/opt/trelloreporter`. As such, the 
installation of `trelloreporter` requires an account with privileges to:
    
   1. Create `/opt` if it doesn't exist
   2. Create the `trelloreporter` directory under `/opt`
   3. Create subdirectories under `trelloreporter`:
    
            trelloreporter/
            ├── config
            │   └── trelloreporter.yml
            └── data
                ├── log
                │   └── trelloreporter.log
                └── trelloreporter.db 

### Instructions
1. Clone the repo and enter the repo
    ```
    git clone git@gitlab.platform.is:platformengineering/trelloreporter.git
    cd trelloreporter
    ```
2. Compile the source code and enter the directory containing the archive
    ```
    python3.6 setup.py sdist
    cd dist
    sudo pip3.6 install trelloreporter-1.0.0.tar.gz 
    ```
3. The `trelloreporter` binary is installed under `/usr/bin`. The `trelloreporter` utility can be immediately called, 
assuming one's `PATH` includes `/usr/bin`
    ```
    [philanim@dev dist]$ trelloreporter 
    Trello Reader 

     Usage: trelloreporter [option] --config <config.yml>
     config.Yaml is the Yaml configuration file
     Options:
       -b            Print boards
       -l            Print lists
       -c            Print cards
       -s            Generate an excel spreadsheet
       -e            Subscribe to the TrelloReporter via email
       -r            Remove a subscriber from the database
       --pretty      Pretty-Print the json data
       --config      Specify a Yaml file containing the API credentials
    
    Example: 
    trelloreporter -b --pretty --config myconfigfile.yml
    ```
#### Removed Members
Members who have been removed from board access, but are still allocated to cards do not have their names generated. The
Member ID read from the Trello API is used. This is done deliberately to flag members who have (resigned?) been removed
from the organisation but have not been removed from certain cards.

## Configuration
The client attempts to read some environment varibles by default. Failing this, the client will use the config file 
found under the `config` directory. It is a good idea to change the parameters under the `trelloreporter.yaml` file in 
the `config` directory to valid parameters.

### Trello configuration
The following environement variables are sought by the main program. These are defined under the `api` section of the 
Yaml file:
* `TRELLO_CONFIG`: the path to the configuration file. This file is, by default found under the `config` directory of 
the project.
* `TRELLO_TOKEN` : the token of the Trello API
* `TRELLO_KEY` : the API key of the Trello API
* `TRELLO_URL` : the URL endpoint to call for the Trello API
* `TRELLO_ORG` : the organisation as it appears in Trello

### Elasticsearch configuration
The following environmental variables are sought by the main program. These parameters are found under the :
* `ES_USERNAME` : the username of the elasticsearch user
* `ES_PASSWORD` : the password of the elasticsearch user
* `ES_ENDPOINT` : the endpoint address
* `ES_PORT`: the port to communicate with the endpoint over
* `ES_INDEX`: the index to write all documents to, within elasticsearch

### Logging configuration
The `logging.config` module is used to instantiate logging. The `dictConfig` method is passed a dictionary which is 
read from the `trelloreporter.yml` file under the `log_config` key. Documentation of how this is done can be found 
[here](https://docs.python.org/3.5/library/logging.config.html#logging-config-dictschema). 
* `version` this should always be set to 1; it should be an integer value representing the schema version of dictConfig.
* `handlers` the logging handlers to use
  * `default` a default handler for stream output.
    * `class` the `logging.StreamHandler` is used
    * `formatter` the `default` formatter defined below is used
    * `level` this can be changed to increase and decrease verbosity of the output. Default is `INFO`
    * `stream` the stream handler to use. The default is `stdout`
  * `file` a handler for file output
    * `class` the class used is `logging.FileHandler`
    * `formatter` the default formatter is used
    * `filename` by default, this is `/var/log/trelloreporter.log`. This file should be present in the OS and the write
    permissions should allow the user executing the application to write to the file.
    * `level` the default log-level is `DEBUG` for maximum verbosity
* `formatters` the formatters used by the handlers. 
  * `default` one formatter is defined as the default
    * `format` the format for log messages. This is constructed to be TIME application_name DEBUG_LEVEL message. For 
    further reference look [here](https://docs.python.org/3.5/library/logging.html#logging.Formatter)
* `loggers` this section defines all the loggers to register. There should only be one logger: `trelloreporter`. All 
the loggers defined in the classes look for this logger when logging.
  * `trelloreporter` the name of the logger
    * `handlers` the handlers to associated to the logger. All the handlers defined under the `handlers` section should
    be listed.
    * `level` this is the logging level of the application. Handlers who have a level which is lower than the set level
    will not log any data. Handlers with an equivalent or higher loglevel will be used to log data.
    
### Mail configuration
The following variables can be configured for email delivery of the generated spreadsheet. These appear under the `mail`
key of the yaml configuration file.
* `from` the from address of the email
* `recipients` the recipients of the email message
* `subject` the subject line of the email
* `relay` the mail relay host to use for SMTP delivery

### Known Issues
