# NLIP Server  

Welcome to the NLIP Server! This project is a basic implementation of NLIP server side protocol. 

This package provides a library that can easily be customized to 
create your own NLIP based Solution. 

The package depends on the NLIP client package. 


## Installation

This project uses [Poetry](https://python-poetry.org/docs/) for dependency management. First, please [install Poetry](https://python-poetry.org/docs/#installation).

To set up the Python project, create a virtual environment using the following commands.

1. Create the virtual environment:
    ```bash
    poetry env use python
    ```
  
2. Install the application dependencies
    ```bash
    poetry install
    ```
## Defining a new Server Side Solution 

To define a new solution, you need to provide two subclasses of the provided abstract classes: NLIPApplicaiton and NLIPSession. 

These two classes are defined in module server

The main routine of the solution should call the start_server routine in module server to create an instance of the solution server-side application. start_server takes a subclass of NLIP_Application as an argument. 
