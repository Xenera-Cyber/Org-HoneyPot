from coeai import LLMinfer
from knowledge_base import knowledge_documents
from config import COEAI_API_KEY

llm = LLMinfer(api_key=COEAI_API_KEY)


def retrieve_context(command):

    kb_text = ""

    for doc in knowledge_documents:
        kb_text += f"""
Command: {doc['command']}
Description: {doc['description']}
Example Output:
{doc['example_output']}
---
"""

    prompt = f"""
You are a Linux command classifier.

Your job:
- Match the given command with the most relevant Linux command from the knowledge base.
- Return ONLY the matching command name.
- Do NOT explain anything.

Command:
{command}

Knowledge Base:
{kb_text}

Output format:
<command_name_only>
"""

    response = llm.generate(
        model="deepseek-r1:70b",
        prompt=prompt,
        max_tokens=20000
    )

    return response["choices"][0]["message"]["content"].strip()


def generate_deception(command):

    matched_command = retrieve_context(command)

    # find matching KB entry
    context_doc = None
    for doc in knowledge_documents:
        if doc["command"] in matched_command:
            context_doc = doc
            break

    if not context_doc:
        return f"bash: {command}: command not found"

    prompt = f"""
    You are a real Linux terminal.

    STRICT RULES:
    - Do NOT explain anything
    - Do NOT describe anything
    - Output must look exactly like a Linux terminal
    - No extra text
    - Use ONLY realistic services (sshd, nginx, mysql, bash, systemd)
    - Keep output consistent with the reference format

    Command executed:
    {command}

    Reference format:
    {context_doc['example_output']}

    Generate terminal output.
    """

    response = llm.generate(
        model="deepseek-r1:70b",
        prompt=prompt,
        max_tokens=20000
    )

    return response["choices"][0]["message"]["content"].strip()
