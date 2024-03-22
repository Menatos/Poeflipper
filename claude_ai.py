import os
from os.path import dirname, join

import anthropic
from dotenv import load_dotenv

from helpers import log_output as log

env_path = join(dirname(__file__), ".env")
load_dotenv(env_path)

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

log_path = "logs/prompts.log"


# models
# claude-3-opus-20240229	claude-3-sonnet-20240229	claude-3-haiku-20240307

message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1000,
    temperature=0.0,
    #   system="Respond only in Yoda-speak.",
    messages=[
        {
            "role": "user",
            "content": "Write me a python function that allows me to upload a csv for you to analyze",
        }
    ],
)

print(message)

message_data = {
    "id": message.id,
    "content_text": message.content[0].text,
    "content_type": message.content[0].type,
    "model": message.model,
    "role": message.role,
    "stop_reason": message.stop_reason,
    "stop_sequence": message.stop_sequence,
    "type": message.type,
    "usage": str(message.usage),
}
log.log_json(message_data, log_path)
