SERVER_NAME = "name"
SERVER_HOST = "host"
SERVER_PORT = "port"
SERVER_MODEL = "model"
DEF_HOST = "localhost"
DEF_PORT = 11434

servers = [
    {
        SERVER_NAME: "Llama3Server",
        SERVER_HOST: DEF_HOST,
        SERVER_PORT: DEF_PORT,
        SERVER_MODEL: "llama3",
    },
    {
        SERVER_NAME: "MistralServer",
        SERVER_HOST: DEF_HOST,
        SERVER_PORT: DEF_PORT,
        SERVER_MODEL: "mistral",
    },
    {
        SERVER_NAME: "QWenServer",
        SERVER_HOST: DEF_HOST,
        SERVER_PORT: DEF_PORT,
        SERVER_MODEL: "qwen2",
    },
    {
        SERVER_NAME: "GraniteServer",
        SERVER_HOST: DEF_HOST,
        SERVER_PORT: DEF_PORT,
        SERVER_MODEL: "granite-code",
    },
]
