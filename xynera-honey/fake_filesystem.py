filesystem = {
    "/": ["home", "var", "etc"],
    "/home": ["ubuntu"],
    "/home/ubuntu": ["notes.txt", "script.sh"],
    "/var": ["log", "www"],
    "/etc": ["passwd"]
}

file_contents = {
    "/home/ubuntu/notes.txt": "Remember to update server.\nPassword is weak.\n",
    "/home/ubuntu/script.sh": "#!/bin/bash\necho Hello World\n",
    "/etc/passwd": "root:x:0:0:root:/root:/bin/bash\nubuntu:x:1000:1000::/home/ubuntu:/bin/bash\n"
}


def ls(session):
    cwd = session["cwd"]
    return "\n".join(filesystem.get(cwd, []))


def pwd(session):
    return session["cwd"]


def cd(session, path):
    cwd = session["cwd"]

    if path == "..":
        if cwd == "/":
            return ""
        new_path = "/".join(cwd.rstrip("/").split("/")[:-1])
        session["cwd"] = new_path if new_path else "/"
        return ""

    if path.startswith("/"):
        new_path = path
    else:
        if cwd == "/":
            new_path = f"/{path}"
        else:
            new_path = f"{cwd}/{path}"

    # normalize path (remove double slashes)
    new_path = new_path.replace("//", "/")

    if new_path in filesystem:
        session["cwd"] = new_path
        return ""
    else:
        return f"cd: no such file or directory: {path}"


def cat(session, filename):
    cwd = session["cwd"]
    path = f"{cwd}/{filename}"

    if path in file_contents:
        return file_contents[path]
    else:
        return f"cat: {filename}: No such file"
