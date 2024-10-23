# Chatbot Proxy 

This provides an implementation of the fastapi application which acts like a front-end to an existing LLM Service. 

The system supports a configuration of 

[Client]----[NLIP-Server]---[LLM Server]


The default configuration assumes that there is a Ollama service running locally. You can set environmental variable to point to the location of the LLM Service. 

The environmental variables are: 

CHAT_HOST: The host where the LLM Service is running. Default localhost 
CHAT_PORT: The port where LLM Service is running. Default is 11434
CHAT_MODEL: The model used by the LLM Service. Default is mistral. 