#!/bin/bash 

export CHAT_MODEL='llama3'
fastapi dev chatbot.py --port 9000