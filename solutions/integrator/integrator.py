from app.schemas import nlip

from app.schemas.genai import SimpleGenAI
from app.server import setup_server
from solutions.integrator import config as cfg


class IntegratorApplication(nlip.NLIP_Application):
    def startup(self):
        self.servers = cfg.servers

    def shutdown(self):
        return None

    def create_session(self) -> nlip.NLIP_Session:
        return IntegratorSession(servers=self.servers)


class IntegratorSession(nlip.NLIP_Session):

    def __init__(self, servers: list):
        self.server_cfg = servers
        self.models_dict = {
            x[cfg.SERVER_NAME]: x[cfg.SERVER_MODEL] for x in self.server_cfg
        }

    def create_server(self, server_cfg: dict):
        return SimpleGenAI(server_cfg[cfg.SERVER_HOST], server_cfg[cfg.SERVER_PORT])

    def start(self):
        self.server_dict = {
            x[cfg.SERVER_NAME]: self.create_server(x) for x in self.server_cfg
        }

    def execute(self, msg: nlip.NLIP_Message | nlip.NLIP_BasicMessage) -> nlip.NLIP_Message | nlip.NLIP_BasicMessage:
        question = nlip.collect_text(msg)
        responses = dict()
        for x in self.server_dict.keys():
            try:
                model = self.models_dict[x]
                server = self.server_dict[x]
                responses[x] = server.generate(model, question)
            except Exception as e:
                print(f"Exception when getting answer from server {x}\n -- {e}")
        response = self.voted_response(question, responses)
        return nlip.nlip_encode_text(response)

    def stop(self):
        self.server_cfg = list()

    def voted_response(self, question: str, responses: dict):
        votes = [
            (x, responses[x], self.count_votes(x, question, responses[x]))
            for x in responses.keys()
        ]
        votes = sorted(votes, key=lambda x: x[2], reverse=True)
        if len(votes) > 0:
            winner = votes[0]
            answer = f"Answer Provided by {winner[0]} -- which is:\n {winner[1]}"
            return answer
        return f"No model was able to provide an answer"

    def count_single_vote(self, validator: str, question: str, answer: str):
        prompt = f"""A LLM was asked this question: {question}. 
        It replied with: {answer}. Is the answer correct?
        Reply in only one word using Yes or No."""

        server = self.server_dict[validator]
        model = self.models_dict[validator]
        try:
            answer = server.generate(model, prompt)
            return answer.startswith("Yes")
        except Exception as e:
            print(f"Error in collecting response from {validator}\n -- {e}")
            return False

    def count_votes(self, server: str, question: str, answer: str):
        count = 0
        for validator in self.server_dict.keys():
            if validator != server:
                try:
                    vote = self.count_single_vote(validator, question, answer)
                    if vote:
                        count = count + 1
                except Exception as e:
                    print(f"Exception when validating from server {validator}\n -- {e}")
        return count


app = setup_server(IntegratorApplication())
