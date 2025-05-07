# Python NLIP Repositories 

This repository contains one component of the various python repositories for NLIP Proof of Concept implementation. The various repositories are: 

* nlip_sdk: this provides a software development kit in python that implements the abstractions of NLIP message, submessages along with a factory to ease the creation of NLIP messages and submessages 
* nlip_client: this provides a package that simplifies the task of sending NLIP messages using the base underlying protocol. The current implementation uses httpx as the base transfer package. 
* nlip_server: this provides a paclage that simplifies the task of writing a server-side NLIP application. This provides the abstractions of a NLIPApplication and a NLIP Session. An application consists of multiple sessions. 

The above three are the components needed to write a client or a server. To write a client, you need to use nlip_sdk and nlip_client. To write a server side application, you need to use nlip_sdk and nlip_server. 

The following repositories contain a few simple clients and server side applications: 

* nlip_soln: this provides a few simple prototype server side solutions using the nlip_server package 
* text_client: this provides a simple text based chatbot to interface with a NLIP server 
* kivy_client: this provides a python kivy based visual client to interact with an NLIP server

# NLIP Server  

Welcome to the NLIP Server! This project is a basic implementation of NLIP server side protocol. 

This package provides a library that can easily be customized to 
create your own NLIP based Solution. 

The package depends on the NLIP SDK package. 


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
## Publishing the Package

To publish the package to PyPI, ensure that your changes are committed and then create a version tag. You can do this with the following commands:

```bash
git tag v0.1.0  # Replace with new version
git push origin v0.1.0
```
## Defining a new Server Side Solution 

To define a new solution, you need to provide two subclasses of the provided abstract classes: NLIPApplicaiton and NLIPSession. 

These two classes are defined in module server

The main routine of the solution should call the start_server routine in module server to create an instance of the solution server-side application. start_server takes a subclass of NLIP_Application as an argument. 

An example simple echo application is included in the file echo.py

To run the echo server, use the following command

```bash
poetry run fastapi dev nlip_server/echo.py
```


