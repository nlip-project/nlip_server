# NLIP Server  

This is a simple implementation of a NLIP Server written using fastapi in python

A sample chatbot solution is provided in soln directory



## Installation

To set up this python project, create a virtual environment for python using the following commands (You can use your own environment name instead of using the provided name of env_server: 

```
$ python -m venv env_server
$ source env_server/bin/activate
```

Next, install the required packages:
```
$ pip install -r requirements.txt
```

Now the python environment is setup and you can run the server

## Running the chatbot server 

Change to the directory soln/chat and invoke the following commands:
```
$ ./run_llama.sh 
```

or 
```
$ ./run_mistral.sh 
```

This will start the fast api server with chat on one of the two LLM models. 

Note: this solution assumes that you have an Ollama Server running at a server which needs to be configured. See the README.md in soln directory for more details. 


## Defining a new Solution 

To define a new solution, you need to provide a subclass of NLIPApplicaiton which needs to define its specialized version of NLIPSession. Both NLIPApplication and NLIPSession are defined in module nlip. 

The main routine of the solution should call the start_server routine in module server to create an instance of the solution server-side application. 

