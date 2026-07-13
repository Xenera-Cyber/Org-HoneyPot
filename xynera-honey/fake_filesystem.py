"""
fake_filesystem.py

Purpose:
    Provides the simulated filesystem used by the honeypot shell.

    The module exposes:
      - `filesystem` / `file_contents`: the static template data describing
        the "factory default" directory tree and file contents.
      - `FileSystem`: a per-session, mutable, tree-based filesystem built
        from that template. Each attacker session gets its own clone
        (see `create_filesystem()`), so files/directories one attacker
        creates, deletes, or edits (touch/mkdir/rm/mv/cp) never leak into
        another attacker's session, and `ls -l` reflects real metadata
        (owner, permissions, size, modified time) that updates as the
        attacker interacts with it.

Responsibility boundary:
    This module owns filesystem structure/content/metadata simulation.
    Command parsing and session wiring live in command_router.py and
    session_manager.py respectively.
"""

from copy import deepcopy
from datetime import datetime
from posixpath import basename, dirname, normpath


# ==========================================================
# Template Data: Directory Listings
# ==========================================================
filesystem = {
    "/": [
        "bin",
        "boot",
        "dev",
        "etc",
        "home",
        "opt",
        "tmp",
        "usr",
        "var"
    ],
    "/home": [
        "ubuntu",
        "dev",
        "backup"
    ],
    "/home/ubuntu": [
        "Desktop",
        "Documents",
        "Downloads",
        "Music",
        "Pictures",
        "Videos",
        "projects",
        ".ssh",
        ".config",
        ".cache",
        ".bash_history",
        ".bashrc",
        ".profile"
    ],
    "/home/ubuntu/Desktop": [
        "todo.txt"
    ],
    "/home/ubuntu/Documents": [
        "employee_directory.csv",
        "meeting_notes.txt",
        "server_inventory.csv"
    ],
    "/home/ubuntu/Downloads": [
        "ubuntu_server_notes.pdf",
        "backup.zip"
    ],
    "/home/ubuntu/Music": [],
    "/home/ubuntu/Pictures": [
        "office.jpg"
    ],
    "/home/ubuntu/Videos": [],
    "/home/ubuntu/.ssh": [
        "authorized_keys",
        "id_rsa.pub"
    ],
    "/home/ubuntu/.config": [
        "user-dirs.dirs"
    ],
    "/home/ubuntu/.cache": [],
    "/etc": [
        "passwd",
        "hosts",
        "hostname"
    ],
    "/var": [
        "log",
        "www"
    ],
    "/var/log": [
        "auth.log",
        "syslog"
    ],
    "/opt": [
        "backups"
    ],
    "/opt/backups": [
        "db_backup.sql",
        "weekly_backup.tar.gz"
    ]
}

# ==========================================================
# Template Data: File Contents
# ==========================================================
file_contents = {
    "/home/ubuntu/Desktop/todo.txt": """
- Patch nginx
- Review firewall rules
- Rotate SSH keys
""",

    "/home/ubuntu/Documents/employee_directory.csv": """
ID,Name,Department,Email
1001,Alice Johnson,Finance,alice.johnson@xynera.local
1002,John Smith,IT,john.smith@xynera.local
1003,Sarah Davis,Operations,sarah.davis@xynera.local
1004,Michael Brown,HR,michael.brown@xynera.local
1005,Emma Wilson,Engineering,emma.wilson@xynera.local
""",

    "/home/ubuntu/Documents/meeting_notes.txt": """
Infrastructure Weekly Review
- nginx upgrade planned next month
- verify backup integrity
- review SSL renewal process
- monitor database replication
""",

    "/home/ubuntu/Documents/server_inventory.csv": """
Hostname,Role,Location
web-prod-01,Web Server,Delhi
db-prod-01,Database Server,Delhi
backup-01,Backup Node,Mumbai
""",

    "/home/ubuntu/.bash_history": """
apt update
apt upgrade -y
systemctl restart nginx
nano /etc/nginx/nginx.conf
tail -f /var/log/auth.log
mysql -u root
""",

    "/home/ubuntu/.bashrc": """
# ~/.bashrc
export PATH=$PATH:/usr/local/bin
alias ll='ls -la'
alias grep='grep --color=auto'
""",

    "/home/ubuntu/.profile": """
# ~/.profile
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi
""",

    "/home/ubuntu/.ssh/authorized_keys": """
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxxxxxxxxxxxxxxxxxxxxxxxx ubuntu@web-prod-01
""",

    "/home/ubuntu/.ssh/id_rsa.pub": """
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCyyyyyyyyyyyyyyyyyyyyyyyy ubuntu@web-prod-01
""",

    "/home/ubuntu/.config/user-dirs.dirs": """
XDG_DESKTOP_DIR="$HOME/Desktop"
XDG_DOWNLOAD_DIR="$HOME/Downloads"
XDG_DOCUMENTS_DIR="$HOME/Documents"
""",

    "/etc/passwd": """
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug Reporting:/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:Systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:101:103:Systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:102:106:D-Bus Message Bus:/nonexistent:/usr/sbin/nologin
syslog:x:103:110:Syslog:/home/syslog:/usr/sbin/nologin
_apt:x:104:65534::/nonexistent:/usr/sbin/nologin
uuidd:x:105:111:UUID Daemon:/run/uuidd:/usr/sbin/nologin
tcpdump:x:106:112::/nonexistent:/usr/sbin/nologin
tss:x:107:113:TPM Software Stack:/var/lib/tpm:/bin/false
landscape:x:108:114:Landscape Client:/var/lib/landscape:/usr/sbin/nologin
pollinate:x:109:1:Pollinate:/var/cache/pollinate:/bin/false
mysql:x:110:115:MySQL Server:/nonexistent:/bin/false
postgres:x:111:116:PostgreSQL Administrator:/var/lib/postgresql:/bin/bash
redis:x:112:117:Redis Server:/var/lib/redis:/usr/sbin/nologin
docker:x:113:118:Docker Engine:/var/lib/docker:/usr/sbin/nologin
nginx:x:114:119:Nginx Service:/var/cache/nginx:/usr/sbin/nologin
ubuntu:x:1000:1000:Ubuntu User:/home/ubuntu:/bin/bash
dev:x:1001:1001:Developer:/home/dev:/bin/bash
admin:x:1002:1002:System Administrator:/home/admin:/bin/bash
support:x:1003:1003:Support Engineer:/home/support:/bin/bash
backupuser:x:1004:1004:Backup Operator:/home/backupuser:/bin/bash
""",

    "/etc/hosts": """
127.0.0.1 localhost
127.0.1.1 web-prod-01
10.0.0.10 db-prod-01
10.0.0.11 backup-01
""",

    "/etc/hostname": """
web-prod-01
""",

    "/var/log/auth.log": """
Jun 15 08:01:22 sshd[2211]: Accepted password for ubuntu
Jun 15 08:15:13 sshd[2214]: Accepted password for dev
Jun 15 09:01:55 CRON[1001]: Job Started
""",

    "/var/log/syslog": """
Jun 15 nginx restarted
Jun 15 mysql service started
Jun 15 backup completed successfully
""",

    "/opt/backups/db_backup.sql": """
CREATE DATABASE customers;
USE customers;
CREATE TABLE users(
 id INT PRIMARY KEY,
 name VARCHAR(100),
 email VARCHAR(100)
);
"""
}


# ==========================================================
# Dynamic, Per-Session Filesystem
# ==========================================================
HOME_DIR = "/home/ubuntu"
DEFAULT_OWNER = "ubuntu"
DEFAULT_GROUP = "ubuntu"
DEFAULT_FILE_PERMISSIONS = "rw-r--r--"
DEFAULT_DIR_PERMISSIONS = "rwxr-xr-x"


class Metadata:
    """Owner/group/permission/timestamp bookkeeping for a filesystem node."""

    def __init__(
        self,
        owner=DEFAULT_OWNER,
        group=DEFAULT_GROUP,
        permissions=DEFAULT_FILE_PERMISSIONS,
        created_at=None,
        modified_at=None,
    ):
        now = datetime.now()
        self.owner = owner
        self.group = group
        self.permissions = permissions
        self.created_at = created_at or now
        self.modified_at = modified_at or self.created_at

    def clone(self):
        return Metadata(
            owner=self.owner,
            group=self.group,
            permissions=self.permissions,
            created_at=self.created_at,
            modified_at=self.modified_at,
        )

    def touch(self):
        self.modified_at = datetime.now()


class Node:
    """Common behaviour shared by File and Directory tree nodes."""

    def __init__(self, name, parent=None, metadata=None):
        self.name = name
        self.parent = parent
        self.metadata = metadata or Metadata()

    @property
    def owner(self):
        return self.metadata.owner

    @owner.setter
    def owner(self, value):
        self.metadata.owner = value

    @property
    def group(self):
        return self.metadata.group

    @group.setter
    def group(self, value):
        self.metadata.group = value

    @property
    def permissions(self):
        return self.metadata.permissions

    @permissions.setter
    def permissions(self, value):
        self.metadata.permissions = value

    @property
    def created_at(self):
        return self.metadata.created_at

    @created_at.setter
    def created_at(self, value):
        self.metadata.created_at = value

    @property
    def modified_at(self):
        return self.metadata.modified_at

    @modified_at.setter
    def modified_at(self, value):
        self.metadata.modified_at = value

    def is_file(self):
        return False

    def is_directory(self):
        return False

    def path(self):
        if self.parent is None:
            return "/"

        parts = []
        node = self
        while node.parent is not None:
            parts.append(node.name)
            node = node.parent
        return "/" + "/".join(reversed(parts))


class File(Node):
    def __init__(self, name, content="", parent=None, metadata=None):
        metadata = metadata or Metadata(permissions=DEFAULT_FILE_PERMISSIONS)
        super().__init__(name=name, parent=parent, metadata=metadata)
        self.content = content

    def is_file(self):
        return True

    def clone(self, parent=None):
        return File(
            name=self.name,
            content=self.content,
            parent=parent,
            metadata=self.metadata.clone(),
        )

    @property
    def size(self):
        return len(self.content.encode("utf-8"))


class Directory(Node):
    def __init__(self, name, parent=None, metadata=None):
        metadata = metadata or Metadata(permissions=DEFAULT_DIR_PERMISSIONS)
        super().__init__(name=name, parent=parent, metadata=metadata)
        self.children = {}

    def is_directory(self):
        return True

    def add_child(self, node):
        node.parent = self
        self.children[node.name] = node
        self.metadata.touch()

    def remove_child(self, name):
        node = self.children.pop(name)
        node.parent = None
        self.metadata.touch()
        return node

    def clone(self, parent=None):
        copied = Directory(
            name=self.name,
            parent=parent,
            metadata=self.metadata.clone(),
        )
        for child in self.children.values():
            copied.children[child.name] = child.clone(parent=copied)
        return copied


class FileSystem:
    """
    A mutable, tree-based filesystem. Each attacker session owns one
    instance (via `create_filesystem()`), cloned from a shared template
    so every session starts from the same "factory" layout but diverges
    independently as the attacker creates/edits/deletes files.
    """

    def __init__(self, root=None):
        self.root = root or Directory(name="", parent=None)

    @classmethod
    def from_template(cls, template_filesystem=None, template_file_contents=None):
        template_filesystem = template_filesystem or filesystem
        template_file_contents = template_file_contents or file_contents

        fs = cls()

        for directory_path, children in template_filesystem.items():
            parent = fs._ensure_directory(directory_path)
            for child_name in children:
                child_path = fs.join_path(directory_path, child_name)
                if child_path in template_filesystem:
                    fs._ensure_directory(child_path)
                elif child_name not in parent.children:
                    if child_path in template_file_contents:
                        content = template_file_contents[child_path]
                        parent.add_child(File(name=child_name, content=content))
                    elif "." in child_name:
                        parent.add_child(File(name=child_name, content=""))
                    else:
                        parent.add_child(Directory(name=child_name))

        for file_path, content in template_file_contents.items():
            parent_path = dirname(file_path) or "/"
            file_name = basename(file_path)
            parent = fs._ensure_directory(parent_path)
            existing = parent.children.get(file_name)
            if isinstance(existing, File):
                existing.content = content
            elif existing is None:
                parent.add_child(File(name=file_name, content=content))

        return fs

    def clone(self):
        return FileSystem(root=self.root.clone(parent=None))

    @staticmethod
    def join_path(parent_path, name):
        if parent_path == "/":
            return f"/{name}"
        return f"{parent_path.rstrip('/')}/{name}"

    def _ensure_directory(self, path):
        normalized = self.normalize_path(path)
        if normalized == "/":
            return self.root

        current = self.root
        for part in normalized.strip("/").split("/"):
            child = current.children.get(part)
            if child is None:
                child = Directory(name=part, parent=current)
                current.add_child(child)
            if not isinstance(child, Directory):
                raise ValueError(f"{normalized}: Not a directory")
            current = child
        return current

    def normalize_path(self, path):
        if not path:
            return HOME_DIR
        normalized = normpath(path)
        if normalized == ".":
            return "/"
        if not normalized.startswith("/"):
            normalized = "/" + normalized
        return normalized

    def resolve_path(self, cwd, path):
        if path == "":
            return HOME_DIR
        if path == "~":
            return HOME_DIR
        if path.startswith("~/"):
            return self.normalize_path(f"{HOME_DIR}/{path[2:]}")
        if path.startswith("/"):
            return self.normalize_path(path)
        return self.normalize_path(self.join_path(cwd, path))

    def get_node(self, path):
        normalized = self.normalize_path(path)
        if normalized == "/":
            return self.root

        current = self.root
        for part in normalized.strip("/").split("/"):
            if not isinstance(current, Directory):
                return None
            current = current.children.get(part)
            if current is None:
                return None
        return current

    def exists(self, path):
        return self.get_node(path) is not None

    def is_directory(self, path):
        node = self.get_node(path)
        return isinstance(node, Directory)

    def is_file(self, path):
        node = self.get_node(path)
        return isinstance(node, File)

    def pwd(self, cwd):
        return cwd

    def cd(self, cwd, path=""):
        target_path = self.resolve_path(cwd, path)
        target = self.get_node(target_path)
        if target is None:
            return cwd, f"cd: no such file or directory: {path}"
        if not isinstance(target, Directory):
            return cwd, f"cd: not a directory: {path}"
        return target.path(), ""

    def ls(self, cwd, path="", show_all=False, long_format=False):
        target_path = self.resolve_path(cwd, path) if path else cwd
        target = self.get_node(target_path)
        display_name = path or target_path

        if target is None:
            return f"ls: cannot access '{display_name}': No such file or directory"
        if isinstance(target, File):
            return self._format_long(target) if long_format else target.name

        nodes = list(target.children.values())
        if not show_all:
            nodes = [node for node in nodes if not node.name.startswith(".")]

        if not long_format:
            return "\n".join(node.name for node in nodes)

        entries = []
        if show_all:
            entries.extend([
                self._format_long(target, display_name="."),
                self._format_long(target.parent or target, display_name=".."),
            ])
        entries.extend(self._format_long(node) for node in nodes)
        return "\n".join(entries)

    def cat(self, cwd, path):
        target_path = self.resolve_path(cwd, path)
        target = self.get_node(target_path)
        if target is None:
            return f"cat: {path}: No such file"
        if isinstance(target, Directory):
            return f"cat: {path}: Is a directory"
        return target.content

    def touch(self, cwd, path):
        if not path:
            return "touch: missing file operand"

        target_path = self.resolve_path(cwd, path)
        target = self.get_node(target_path)
        if target is not None:
            target.metadata.touch()
            return ""

        parent = self.get_node(dirname(target_path) or "/")
        if parent is None:
            return f"touch: cannot touch '{path}': No such file or directory"
        if not isinstance(parent, Directory):
            return f"touch: cannot touch '{path}': Not a directory"

        parent.add_child(File(name=basename(target_path), content=""))
        return ""

    def mkdir(self, cwd, path):
        if not path:
            return "mkdir: missing operand"

        target_path = self.resolve_path(cwd, path)
        if self.exists(target_path):
            return f"mkdir: cannot create directory '{path}': File exists"

        parent = self.get_node(dirname(target_path) or "/")
        if parent is None:
            return f"mkdir: cannot create directory '{path}': No such file or directory"
        if not isinstance(parent, Directory):
            return f"mkdir: cannot create directory '{path}': Not a directory"

        parent.add_child(Directory(name=basename(target_path)))
        return ""

    def rm(self, cwd, path, recursive=False, force=False):
        if not path:
            return "rm: missing operand"

        target_path = self.resolve_path(cwd, path)
        if target_path == "/":
            return "rm: it is dangerous to operate recursively on '/'"

        target = self.get_node(target_path)
        if target is None:
            return "" if force else f"rm: cannot remove '{path}': No such file or directory"
        if isinstance(target, Directory) and not recursive:
            return f"rm: cannot remove '{path}': Is a directory"

        target.parent.remove_child(target.name)
        return ""

    def mv(self, cwd, source, destination):
        if not source or not destination:
            return "mv: missing file operand"

        source_path = self.resolve_path(cwd, source)
        source_node = self.get_node(source_path)
        if source_node is None:
            return f"mv: cannot stat '{source}': No such file or directory"
        if source_path == "/":
            return "mv: cannot move '/': Device or resource busy"

        destination_path = self.resolve_path(cwd, destination)
        destination_node = self.get_node(destination_path)
        if isinstance(destination_node, Directory):
            new_parent = destination_node
            new_name = source_node.name
        else:
            new_parent = self.get_node(dirname(destination_path) or "/")
            new_name = basename(destination_path)

        if new_parent is None:
            return f"mv: cannot move '{source}' to '{destination}': No such file or directory"
        if not isinstance(new_parent, Directory):
            return f"mv: cannot move '{source}' to '{destination}': Not a directory"
        if isinstance(source_node, Directory) and self._is_descendant(new_parent, source_node):
            return f"mv: cannot move '{source}' to a subdirectory of itself, '{destination}'"

        existing = new_parent.children.get(new_name)
        if isinstance(existing, Directory) and isinstance(source_node, File):
            return f"mv: cannot overwrite directory '{destination}' with non-directory"
        if isinstance(existing, File) and isinstance(source_node, Directory):
            return f"mv: cannot overwrite non-directory '{destination}' with directory"
        if existing is not None:
            new_parent.remove_child(existing.name)

        source_node.parent.remove_child(source_node.name)
        source_node.name = new_name
        new_parent.add_child(source_node)
        source_node.metadata.touch()
        return ""

    def cp(self, cwd, source, destination, recursive=False):
        if not source or not destination:
            return "cp: missing file operand"

        source_path = self.resolve_path(cwd, source)
        source_node = self.get_node(source_path)
        if source_node is None:
            return f"cp: cannot stat '{source}': No such file or directory"
        if isinstance(source_node, Directory) and not recursive:
            return f"cp: -r not specified; omitting directory '{source}'"

        destination_path = self.resolve_path(cwd, destination)
        destination_node = self.get_node(destination_path)
        if isinstance(destination_node, Directory):
            new_parent = destination_node
            new_name = source_node.name
        else:
            new_parent = self.get_node(dirname(destination_path) or "/")
            new_name = basename(destination_path)

        if new_parent is None:
            return f"cp: cannot create regular file '{destination}': No such file or directory"
        if not isinstance(new_parent, Directory):
            return f"cp: cannot create regular file '{destination}': Not a directory"

        existing = new_parent.children.get(new_name)
        if existing is not None:
            new_parent.remove_child(existing.name)

        copied = source_node.clone(parent=None)
        copied.name = new_name
        copied.metadata = deepcopy(copied.metadata)
        copied.metadata.touch()
        new_parent.add_child(copied)
        return ""

    def _is_descendant(self, possible_child, parent):
        current = possible_child
        while current is not None:
            if current is parent:
                return True
            current = current.parent
        return False

    def _format_long(self, node, display_name=None):
        node_type = "d" if isinstance(node, Directory) else "-"
        size = 4096 if isinstance(node, Directory) else node.size
        timestamp = node.modified_at.strftime("%b %d %H:%M")
        return (
            f"{node_type}{node.permissions} 1 {node.owner} {node.group} "
            f"{size:>5} {timestamp} {display_name or node.name}"
        )


# Built once at import time; every session clones it rather than
# reparsing the template, so per-session filesystems stay cheap to create.
ORIGINAL_FILESYSTEM = FileSystem.from_template()


def create_filesystem():
    """Return a fresh, independent FileSystem for a new attacker session."""
    return ORIGINAL_FILESYSTEM.clone()