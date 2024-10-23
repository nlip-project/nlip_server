# NLIP Server  

Welcome to the NLIP Server! This project is a straightforward implementation of the Natural Language Interaction Protocol (NLIP) specification, built with FastAPI in Python.

The repository includes a sample chatbot and integration solutions located in the solutions directory.


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

Once the Python environment is set up, you can run the server.

## Running the Chatbot Server
**Note:** This solution assumes that you have an Ollama Server running and properly configured. For more details, please see the README.md in the solutions directory.

You can start the chat server with:
    ```bash
    poetry run start-chat
    ```

To start chat with specific model
    ```bash
    CHAT_MODEL=llama2 poetry run start-chat
    ```

## Running the integration server 
    ```bash
    poetry run start-integration
    ```

## Format Code

This project uses [Black](https://black.readthedocs.io/en/stable/) to format the code. You can format the code with the following command:

    ```bash
    poetry run format
    ```

## Publishing the Package

To publish the package to PyPI, ensure that your changes are committed and then create a version tag. You can do this with the following commands:

    ```bash
    $ git tag v0.1.0  # Replace with new version
    $ git push origin v0.1.0
    ```

## Defining a new Solution 
To define a new solution, you need to provide a subclass of NLIPApplicaiton which needs to define its specialized version of NLIPSession. Both NLIPApplication and NLIPSession are defined in module nlip. 

The main routine of the solution should call the start_server routine in module server to create an instance of the solution server-side application. 

