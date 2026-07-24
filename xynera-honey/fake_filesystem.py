"""
fake_filesystem.py

Enhanced with Ownership & Metadata Consistency
"""

from copy import deepcopy
from datetime import datetime
from posixpath import basename, dirname, normpath
from typing import Optional, Dict, List, Any, Tuple
import threading
import json

from cache_manager import get_cache_manager, cached

# ==========================================================
# Template Data: Directory Listings (truncated for brevity)
# ==========================================================

filesystem = {
    "/": ["bin", "boot", "dev", "etc", "home", "opt", "tmp", "usr", "var"],
    "/home": ["ubuntu", "dev", "backup"],
    "/home/ubuntu": ["Desktop", "Documents", "Downloads", "Music", "Pictures", "Videos", "projects", ".ssh", ".config", ".cache", ".bash_history", ".bashrc", ".profile"],
    "/home/ubuntu/Desktop": ["todo.txt"],
    "/home/ubuntu/Documents": ["employee_directory.csv", "meeting_notes.txt", "server_inventory.csv"],
    "/home/ubuntu/Downloads": ["ubuntu_server_notes.pdf", "backup.zip"],
    "/home/ubuntu/Music": [],
    "/home/ubuntu/Pictures": ["office.jpg"],
    "/home/ubuntu/Videos": [],
    "/home/ubuntu/.ssh": ["authorized_keys", "id_rsa.pub"],
    "/home/ubuntu/.config": ["user-dirs.dirs"],
    "/home/ubuntu/.cache": [],
    "/etc": ["passwd", "hosts", "hostname"],
    "/var": ["log", "www"],
    "/var/log": ["auth.log", "syslog"],
    "/opt": ["backups"],
    "/opt/backups": ["db_backup.sql", "weekly_backup.tar.gz"]
}

file_contents = {
    "/home/ubuntu/Desktop/todo.txt": {"content": "- Patch nginx\n- Review firewall rules\n- Rotate SSH keys\n", "owner": "ubuntu", "group": "ubuntu", "permissions": "rw-r--r--"},
    "/home/ubuntu/Documents/employee_directory.csv": {"content": "ID,Name,Department,Email\n1001,Alice Johnson,Finance,alice.johnson@xynera.local\n", "owner": "ubuntu", "group": "ubuntu", "permissions": "rw-r--r--"},
    "/home/ubuntu/Documents/meeting_notes.txt": {"content": "Infrastructure Weekly Review\n- nginx upgrade planned\n", "owner": "ubuntu", "group": "ubuntu", "permissions": "rw-r--r--"},
    "/home/ubuntu/Documents/server_inventory.csv": {"content": "Hostname,Role,Location\nweb-prod-01,Web Server,Delhi\n", "owner": "ubuntu", "group": "ubuntu", "permissions": "rw-r--r--"},
    "/home/ubuntu/.bash_history": {"content": "apt update\napt upgrade -y\nsystemctl restart nginx\n", "owner": "ubuntu", "group": "ubuntu", "permissions": "rw-r--r--"},
    "/home/ubuntu/.bashrc": {"content": "export PATH=$PATH:/usr/local/bin\nalias ll='ls -la'\n", "owner": "ubuntu", "group": "ubuntu", "permissions": "rw-r--r--"},
    "/home/ubuntu/.profile": {"content": "if [ -f ~/.bashrc ]; then\n    . ~/.bashrc\nfi\n", "owner": "ubuntu", "group": "ubuntu", "permissions": "rw-r--r--"},
    "/home/ubuntu/.ssh/authorized_keys": {"content": "ssh-rsa AAAAB3NzaC1yc2E... ubuntu@web-prod-01\n", "owner": "ubuntu", "group": "ubuntu", "permissions": "rw-r--r--"},
    "/home/ubuntu/.ssh/id_rsa.pub": {"content": "ssh-rsa AAAAB3NzaC1yc2E... ubuntu@web-prod-01\n", "owner": "ubuntu", "group": "ubuntu", "permissions": "rw-r--r--"},
    "/home/ubuntu/.config/user-dirs.dirs": {"content": "XDG_DESKTOP_DIR=\"$HOME/Desktop\"\n", "owner": "ubuntu", "group": "ubuntu", "permissions": "rw-r--r--"},
    "/etc/passwd": {"content": "root:x:0:0:root:/root:/bin/bash\nubuntu:x:1000:1000:Ubuntu User:/home/ubuntu:/bin/bash\n", "owner": "root", "group": "root", "permissions": "rw-r--r--"},
    "/etc/hosts": {"content": "127.0.0.1 localhost\n127.0.1.1 web-prod-01\n", "owner": "root", "group": "root", "permissions": "rw-r--r--"},
    "/etc/hostname": {"content": "web-prod-01\n", "owner": "root", "group": "root", "permissions": "rw-r--r--"},
    "/var/log/auth.log": {"content": "Jun 15 08:01:22 sshd[2211]: Accepted password for ubuntu\n", "owner": "root", "group": "root", "permissions": "rw-r--r--"},
    "/var/log/syslog": {"content": "Jun 15 nginx restarted\n", "owner": "root", "group": "root", "permissions": "rw-r--r--"},
    "/opt/backups/db_backup.sql": {"content": "CREATE DATABASE customers;\n", "owner": "root", "group": "root", "permissions": "rw-r--r--"}
}

# ==========================================================
# Constants
# ==========================================================

HOME_DIR = "/home/ubuntu"
DEFAULT_OWNER = "ubuntu"
DEFAULT_GROUP = "ubuntu"
DEFAULT_FILE_PERMISSIONS = "rw-r--r--"
DEFAULT_DIR_PERMISSIONS = "rwxr-xr-x"

SYSTEM_USERS = {
    "root": {"uid": 0, "gid": 0, "home": "/root", "shell": "/bin/bash"},
    "ubuntu": {"uid": 1000, "gid": 1000, "home": "/home/ubuntu", "shell": "/bin/bash"},
    "dev": {"uid": 1001, "gid": 1001, "home": "/home/dev", "shell": "/bin/bash"},
    "admin": {"uid": 1002, "gid": 1002, "home": "/home/admin", "shell": "/bin/bash"},
    "support": {"uid": 1003, "gid": 1003, "home": "/home/support", "shell": "/bin/bash"},
    "backupuser": {"uid": 1004, "gid": 1004, "home": "/home/backupuser", "shell": "/bin/bash"},
    "mysql": {"uid": 110, "gid": 115, "home": "/nonexistent", "shell": "/bin/false"},
    "postgres": {"uid": 111, "gid": 116, "home": "/var/lib/postgresql", "shell": "/bin/bash"},
    "nginx": {"uid": 114, "gid": 119, "home": "/var/cache/nginx", "shell": "/usr/sbin/nologin"},
}


class Metadata:
    def __init__(self, owner: str = DEFAULT_OWNER, group: str = DEFAULT_GROUP, 
                 permissions: str = DEFAULT_FILE_PERMISSIONS, created_at: Optional[datetime] = None,
                 modified_at: Optional[datetime] = None, uid: Optional[int] = None, gid: Optional[int] = None):
        now = datetime.now()
        self.owner = owner
        self.group = group
        self.permissions = permissions
        self.created_at = created_at or now
        self.modified_at = modified_at or self.created_at
        self.uid = uid or self._get_uid(owner)
        self.gid = gid or self._get_gid(group)
        self._version = 1
    
    def _get_uid(self, username: str) -> int:
        return SYSTEM_USERS.get(username, {}).get("uid", 1000)
    
    def _get_gid(self, groupname: str) -> int:
        return SYSTEM_USERS.get(groupname, {}).get("gid", 1000)
    
    def clone(self) -> 'Metadata':
        return Metadata(owner=self.owner, group=self.group, permissions=self.permissions,
                       created_at=self.created_at, modified_at=self.modified_at, uid=self.uid, gid=self.gid)
    
    def touch(self):
        self.modified_at = datetime.now()
        self._version += 1
    
    def chown(self, owner: Optional[str] = None, group: Optional[str] = None):
        if owner:
            self.owner = owner
            self.uid = self._get_uid(owner)
        if group:
            self.group = group
            self.gid = self._get_gid(group)
        self.touch()
    
    def chmod(self, permissions: str):
        self.permissions = permissions
        self.touch()


class Node:
    def __init__(self, name: str, parent=None, metadata: Optional[Metadata] = None):
        self.name = name
        self.parent = parent
        self.metadata = metadata or Metadata()
        self._node_id = id(self)
    
    @property
    def owner(self) -> str:
        return self.metadata.owner
    @owner.setter
    def owner(self, value: str):
        self.metadata.chown(owner=value)
    
    @property
    def group(self) -> str:
        return self.metadata.group
    @group.setter
    def group(self, value: str):
        self.metadata.chown(group=value)
    
    @property
    def permissions(self) -> str:
        return self.metadata.permissions
    @permissions.setter
    def permissions(self, value: str):
        self.metadata.chmod(value)
    
    def is_file(self) -> bool:
        return False
    def is_directory(self) -> bool:
        return False
    
    def path(self) -> str:
        if self.parent is None:
            return "/"
        parts = []
        node = self
        while node.parent is not None:
            parts.append(node.name)
            node = node.parent
        return "/" + "/".join(reversed(parts))
    
    def get_metadata_version(self) -> int:
        return self.metadata._version


class File(Node):
    def __init__(self, name: str, content: str = "", parent=None, metadata: Optional[Metadata] = None):
        metadata = metadata or Metadata(permissions=DEFAULT_FILE_PERMISSIONS)
        super().__init__(name=name, parent=parent, metadata=metadata)
        self.content = content
    
    def is_file(self) -> bool:
        return True
    
    def clone(self, parent=None) -> 'File':
        return File(name=self.name, content=self.content, parent=parent, metadata=self.metadata.clone())
    
    @property
    def size(self) -> int:
        return len(self.content.encode("utf-8"))


class Directory(Node):
    def __init__(self, name: str, parent=None, metadata: Optional[Metadata] = None):
        metadata = metadata or Metadata(permissions=DEFAULT_DIR_PERMISSIONS)
        super().__init__(name=name, parent=parent, metadata=metadata)
        self.children: Dict[str, Node] = {}
    
    def is_directory(self) -> bool:
        return True
    
    def add_child(self, node: Node):
        node.parent = self
        self.children[node.name] = node
        self.metadata.touch()
    
    def remove_child(self, name: str) -> Optional[Node]:
        if name in self.children:
            node = self.children.pop(name)
            node.parent = None
            self.metadata.touch()
            return node
        return None
    
    def clone(self, parent=None) -> 'Directory':
        copied = Directory(name=self.name, parent=parent, metadata=self.metadata.clone())
        for child in self.children.values():
            copied.children[child.name] = child.clone(parent=copied)
        return copied


class FileSystem:
    def __init__(self, root=None, session_id: Optional[str] = None):
        self.root = root or Directory(name="", parent=None)
        self._cache = get_cache_manager()
        self._lock = threading.RLock()
        self._modified_paths: set = set()
        self._session_id = session_id or "default"
        self._ownership_cache: Dict[str, Tuple[str, str]] = {}
    
    @classmethod
    def from_template(cls, template_filesystem=None, template_file_contents=None, session_id=None):
        template_filesystem = template_filesystem or filesystem
        template_file_contents = template_file_contents or file_contents
        fs = cls(session_id=session_id)
        
        for directory_path, children in template_filesystem.items():
            parent = fs._ensure_directory(directory_path)
            for child_name in children:
                child_path = fs.join_path(directory_path, child_name)
                if child_path in template_filesystem:
                    fs._ensure_directory(child_path)
                elif child_name not in parent.children:
                    if child_path in template_file_contents:
                        file_data = template_file_contents[child_path]
                        if isinstance(file_data, dict):
                            metadata = Metadata(owner=file_data.get("owner", DEFAULT_OWNER),
                                              group=file_data.get("group", DEFAULT_GROUP),
                                              permissions=file_data.get("permissions", DEFAULT_FILE_PERMISSIONS))
                            parent.add_child(File(name=child_name, content=file_data.get("content", ""), metadata=metadata))
                        else:
                            parent.add_child(File(name=child_name, content=file_data))
                    elif "." in child_name:
                        parent.add_child(File(name=child_name, content=""))
                    else:
                        parent.add_child(Directory(name=child_name))
        
        for file_path, file_data in template_file_contents.items():
            parent_path = dirname(file_path) or "/"
            file_name = basename(file_path)
            parent = fs._ensure_directory(parent_path)
            existing = parent.children.get(file_name)
            if isinstance(existing, File):
                if isinstance(file_data, dict):
                    existing.content = file_data.get("content", existing.content)
                    existing.metadata.owner = file_data.get("owner", existing.metadata.owner)
                    existing.metadata.group = file_data.get("group", existing.metadata.group)
                    existing.metadata.permissions = file_data.get("permissions", existing.metadata.permissions)
                else:
                    existing.content = file_data
            elif existing is None:
                if isinstance(file_data, dict):
                    metadata = Metadata(owner=file_data.get("owner", DEFAULT_OWNER),
                                      group=file_data.get("group", DEFAULT_GROUP),
                                      permissions=file_data.get("permissions", DEFAULT_FILE_PERMISSIONS))
                    parent.add_child(File(name=file_name, content=file_data.get("content", ""), metadata=metadata))
                else:
                    parent.add_child(File(name=file_name, content=file_data))
        return fs
    
    def clone(self) -> 'FileSystem':
        return FileSystem(root=self.root.clone(parent=None), session_id=self._session_id + "_clone")
    
    @staticmethod
    def join_path(parent_path: str, name: str) -> str:
        if parent_path == "/":
            return f"/{name}"
        return f"{parent_path.rstrip('/')}/{name}"
    
    def normalize_path(self, path: str) -> str:
        cache_key = f"normalize:{path}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached
        if not path:
            result = HOME_DIR
        else:
            normalized = normpath(path)
            if normalized == ".":
                result = "/"
            elif not normalized.startswith("/"):
                result = "/" + normalized
            else:
                result = normalized
        self._cache.set(cache_key, result, ttl=60)
        return result
    
    def resolve_path(self, cwd: str, path: str) -> str:
        cache_key = f"resolve:{cwd}:{path}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached
        if path == "":
            result = HOME_DIR
        elif path == "~":
            result = HOME_DIR
        elif path.startswith("~/"):
            result = self.normalize_path(f"{HOME_DIR}/{path[2:]}")
        elif path.startswith("/"):
            result = self.normalize_path(path)
        else:
            result = self.normalize_path(self.join_path(cwd, path))
        self._cache.set(cache_key, result, ttl=60, dependencies=[cwd])
        return result
    
    def _ensure_directory(self, path: str) -> Directory:
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
    
    @cached(dependencies_key="path", ttl=60)
    def get_node(self, path: str) -> Optional[Node]:
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
    
    @cached(dependencies_key="path", ttl=30)
    def exists(self, path: str) -> bool:
        return self.get_node(path) is not None
    
    @cached(dependencies_key="path", ttl=30)
    def is_directory(self, path: str) -> bool:
        node = self.get_node(path)
        return isinstance(node, Directory)
    
    @cached(dependencies_key="path", ttl=30)
    def is_file(self, path: str) -> bool:
        node = self.get_node(path)
        return isinstance(node, File)
    
    @cached(dependencies_key="path", ttl=30)
    def get_ownership(self, path: str) -> Optional[Tuple[str, str]]:
        node = self.get_node(path)
        if node is None:
            return None
        return (node.owner, node.group)
    
    @cached(dependencies_key="path", ttl=30)
    def get_permissions(self, path: str) -> Optional[str]:
        node = self.get_node(path)
        if node is None:
            return None
        return node.permissions
    
    def _invalidate_path(self, path: str):
        with self._lock:
            self._cache.invalidate_dependent(path)
            parent_path = dirname(path)
            if parent_path != path:
                self._cache.invalidate_dependent(parent_path)
            self._modified_paths.add(path)
            if path in self._ownership_cache:
                del self._ownership_cache[path]
    
    def _remove_node_by_path(self, path: str) -> bool:
        """Remove a node by walking the tree (doesn't rely on parent references)"""
        normalized = self.normalize_path(path)
        if normalized == "/":
            return False
        
        parts = normalized.strip("/").split("/")
        if len(parts) == 1:
            if parts[0] in self.root.children:
                del self.root.children[parts[0]]
                self.root.metadata.touch()
                return True
            return False
        
        current = self.root
        for i, part in enumerate(parts[:-1]):
            if not isinstance(current, Directory):
                return False
            current = current.children.get(part)
            if current is None:
                return False
        
        if isinstance(current, Directory) and parts[-1] in current.children:
            del current.children[parts[-1]]
            current.metadata.touch()
            return True
        
        return False
    
    # ==========================================================
    # Directory Operations
    # ==========================================================
    
    def pwd(self, cwd: str) -> str:
        return cwd
    
    def cd(self, cwd: str, path: str = "") -> Tuple[str, str]:
        target_path = self.resolve_path(cwd, path)
        target = self.get_node(target_path)
        if target is None:
            return cwd, f"cd: no such file or directory: {path}"
        if not isinstance(target, Directory):
            return cwd, f"cd: not a directory: {path}"
        return target.path(), ""
    
    def ls(self, cwd: str, path: str = "", show_all: bool = False, long_format: bool = False) -> str:
        target_path = self.resolve_path(cwd, path) if path else cwd
        display_name = path or target_path
        
        cache_key = f"ls:{target_path}:{show_all}:{long_format}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached
        
        target = self.get_node(target_path)
        if target is None:
            result = f"ls: cannot access '{display_name}': No such file or directory"
            self._cache.set(cache_key, result, ttl=10, dependencies=[target_path])
            return result
        
        if isinstance(target, File):
            result = self._format_long(target) if long_format else target.name
            self._cache.set(cache_key, result, ttl=30, dependencies=[target_path])
            return result
        
        nodes = list(target.children.values())
        if not show_all:
            nodes = [node for node in nodes if not node.name.startswith(".")]
        
        if not long_format:
            result = "\n".join(node.name for node in nodes)
        else:
            entries = []
            if show_all:
                entries.extend([
                    self._format_long(target, display_name="."),
                    self._format_long(target.parent or target, display_name=".."),
                ])
            entries.extend(self._format_long(node) for node in nodes)
            result = "\n".join(entries)
        
        self._cache.set(cache_key, result, ttl=30, dependencies=[target_path])
        return result
    
    # ==========================================================
    # File Operations
    # ==========================================================
    
    def cat(self, cwd: str, path: str) -> str:
        target_path = self.resolve_path(cwd, path)
        cache_key = f"cat:{target_path}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached
        
        target = self.get_node(target_path)
        if target is None:
            result = f"cat: {path}: No such file"
            self._cache.set(cache_key, result, ttl=10, dependencies=[target_path])
            return result
        if isinstance(target, Directory):
            result = f"cat: {path}: Is a directory"
            self._cache.set(cache_key, result, ttl=10, dependencies=[target_path])
            return result
        
        self._cache.set(cache_key, target.content, ttl=30, dependencies=[target_path])
        return target.content
    
    def touch(self, cwd: str, path: str) -> str:
        if not path:
            return "touch: missing file operand"
        
        target_path = self.resolve_path(cwd, path)
        with self._lock:
            target = self.get_node(target_path)
            if target is not None:
                target.metadata.touch()
                self._invalidate_path(target_path)
                return ""
            
            parent = self.get_node(dirname(target_path) or "/")
            if parent is None:
                return f"touch: cannot touch '{path}': No such file or directory"
            if not isinstance(parent, Directory):
                return f"touch: cannot touch '{path}': Not a directory"
            
            metadata = Metadata(owner=DEFAULT_OWNER, group=DEFAULT_GROUP)
            parent.add_child(File(name=basename(target_path), content="", metadata=metadata))
            self._invalidate_path(target_path)
            return ""
    
    def mkdir(self, cwd: str, path: str) -> str:
        if not path:
            return "mkdir: missing operand"
        
        target_path = self.resolve_path(cwd, path)
        with self._lock:
            if self.exists(target_path):
                return f"mkdir: cannot create directory '{path}': File exists"
            
            parent = self.get_node(dirname(target_path) or "/")
            if parent is None:
                return f"mkdir: cannot create directory '{path}': No such file or directory"
            if not isinstance(parent, Directory):
                return f"mkdir: cannot create directory '{path}': Not a directory"
            
            metadata = Metadata(owner=DEFAULT_OWNER, group=DEFAULT_GROUP, permissions=DEFAULT_DIR_PERMISSIONS)
            parent.add_child(Directory(name=basename(target_path), metadata=metadata))
            self._invalidate_path(target_path)
            return ""
    
    def rm(self, cwd: str, path: str, recursive: bool = False, force: bool = False) -> str:
        if not path:
            return "rm: missing operand"
        
        target_path = self.resolve_path(cwd, path)
        if target_path == "/":
            return "rm: it is dangerous to operate recursively on '/'"
        
        with self._lock:
            target = self.get_node(target_path)
            if target is None:
                return "" if force else f"rm: cannot remove '{path}': No such file or directory"
            if isinstance(target, Directory) and not recursive:
                return f"rm: cannot remove '{path}': Is a directory"
            
            # Use the _remove_node_by_path method
            if self._remove_node_by_path(target_path):
                self._invalidate_path(target_path)
                return ""
            else:
                return f"rm: cannot remove '{path}': Operation failed"
    
    def mv(self, cwd: str, source: str, destination: str) -> str:
        """Move file/directory using tree walking for removal"""
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
        
        with self._lock:
            # Determine target parent and name
            if isinstance(destination_node, Directory):
                new_parent = destination_node
                new_name = source_node.name
            else:
                parent_dir = dirname(destination_path) or "/"
                new_parent = self.get_node(parent_dir)
                new_name = basename(destination_path)
            
            if new_parent is None:
                return f"mv: cannot move '{source}' to '{destination}': No such file or directory"
            if not isinstance(new_parent, Directory):
                return f"mv: cannot move '{source}' to '{destination}': Not a directory"
            
            # Prevent moving directory into itself
            if isinstance(source_node, Directory) and self._is_descendant(new_parent, source_node):
                return f"mv: cannot move '{source}' to a subdirectory of itself, '{destination}'"
            
            # Remove existing destination if it exists
            if new_name in new_parent.children:
                new_parent.remove_child(new_name)
            
            # CRITICAL FIX: Remove source using tree walking (doesn't rely on parent refs)
            if not self._remove_node_by_path(source_path):
                return f"mv: cannot remove '{source}': Operation failed"
            
            # Update name and add to new parent
            source_node.name = new_name
            source_node.parent = new_parent
            new_parent.add_child(source_node)
            source_node.metadata.touch()
            
            # Invalidate cache
            self._invalidate_path(source_path)
            self._invalidate_path(destination_path)
            
            return ""
    
    def cp(self, cwd: str, source: str, destination: str, recursive: bool = False) -> str:
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
        
        with self._lock:
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
            self._invalidate_path(destination_path)
            return ""
    
    # ==========================================================
    # Ownership & Permission Operations
    # ==========================================================
    
    def chown(self, cwd: str, path: str, owner: Optional[str] = None, group: Optional[str] = None) -> str:
        if not path:
            return "chown: missing operand"
        if not owner and not group:
            return f"chown: missing operand after '{path}'"
        
        target_path = self.resolve_path(cwd, path)
        target = self.get_node(target_path)
        if target is None:
            return f"chown: cannot access '{path}': No such file or directory"
        
        with self._lock:
            target.metadata.chown(owner=owner, group=group)
            self._invalidate_path(target_path)
            return ""
    
    def chmod(self, cwd: str, path: str, permissions: str) -> str:
        if not path or not permissions:
            return "chmod: missing operand"
        
        target_path = self.resolve_path(cwd, path)
        target = self.get_node(target_path)
        if target is None:
            return f"chmod: cannot access '{path}': No such file or directory"
        
        with self._lock:
            target.metadata.chmod(permissions)
            self._invalidate_path(target_path)
            return ""
    
    # ==========================================================
    # System File Integration
    # ==========================================================
    
    def get_passwd_entry(self, username: str) -> Optional[str]:
        if username in SYSTEM_USERS:
            user = SYSTEM_USERS[username]
            return f"{username}:x:{user['uid']}:{user['gid']}:{username} User:{user['home']}:{user['shell']}"
        return None
    
    def get_passwd_file(self) -> str:
        lines = []
        for username, user in SYSTEM_USERS.items():
            lines.append(f"{username}:x:{user['uid']}:{user['gid']}:{username} User:{user['home']}:{user['shell']}")
        return "\n".join(lines)
    
    def get_hostname(self) -> str:
        return "web-prod-01"
    
    def get_hosts_file(self) -> str:
        return "127.0.0.1 localhost\n127.0.1.1 web-prod-01\n10.0.0.10 db-prod-01\n10.0.0.11 backup-01"
    
    # ==========================================================
    # Utility Methods
    # ==========================================================
    
    def _format_long(self, node: Node, display_name: Optional[str] = None) -> str:
        node_type = "d" if isinstance(node, Directory) else "-"
        size = 4096 if isinstance(node, Directory) else node.size
        timestamp = node.modified_at.strftime("%b %d %H:%M")
        return f"{node_type}{node.permissions} 1 {node.owner} {node.group} {size:>5} {timestamp} {display_name or node.name}"
    
    def _is_descendant(self, possible_child: Node, parent: Node) -> bool:
        current = possible_child
        while current is not None:
            if current is parent:
                return True
            current = current.parent
        return False
    
    def get_cache_stats(self) -> Dict:
        return self._cache.get_stats()
    
    def clear_cache(self):
        with self._lock:
            self._cache.clear()
            self._modified_paths.clear()
            self._ownership_cache.clear()
    
    def verify_consistency(self) -> Dict:
        issues = []
        def check_node(node: Node, path: str):
            if node.parent and node.parent.children.get(node.name) != node:
                issues.append(f"Orphaned node: {path}")
            if isinstance(node, Directory):
                for child in node.children.values():
                    check_node(child, node.path() + "/" + child.name)
        check_node(self.root, "/")
        return {
            "consistent": len(issues) == 0,
            "issues": issues,
            "total_nodes": self._count_nodes(self.root),
            "cache_entries": self._cache.get_stats()["entries"]
        }
    
    def _count_nodes(self, node: Node) -> int:
        count = 1
        if isinstance(node, Directory):
            for child in node.children.values():
                count += self._count_nodes(child)
        return count


ORIGINAL_FILESYSTEM = FileSystem.from_template()

def create_filesystem(session_id: Optional[str] = None) -> FileSystem:
    return ORIGINAL_FILESYSTEM.clone()