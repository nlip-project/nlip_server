#!/bin/bash 

export CHAT_MODEL='mistral'
fastapi dev chatbot.py --port 8000