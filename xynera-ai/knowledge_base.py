knowledge_documents = [

    {
        "command": "ps",
        "description": "Displays running processes in Linux.",
        "example_output": """
USER       PID %CPU %MEM COMMAND
root         1  0.0  0.1 /sbin/init
root       221  0.0  0.2 sshd
mysql      334  0.4  1.3 mysqld
www-data   510  0.1  0.3 nginx
"""
    },

    {
        "command": "netstat",
        "description": "Shows active network connections.",
        "example_output": """
Proto Local Address      State
tcp   0.0.0.0:22         LISTEN
tcp   0.0.0.0:80         LISTEN
tcp   127.0.0.1:3306     LISTEN
"""
    },

    {
        "command": "ls",
        "description": "Lists files in a directory.",
        "example_output": """
home
var
etc
tmp
"""
    },

    {
        "command": "whoami",
        "description": "Displays the current user.",
        "example_output": "ubuntu"
    },

    {
        "command": "uname",
        "description": "Displays system information.",
        "example_output": "Linux ubuntu-server 5.15.0-91-generic"
    }

]
