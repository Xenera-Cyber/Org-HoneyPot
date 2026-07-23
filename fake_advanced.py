import re

def chmod(args):
    """
    Simulates the Linux chmod command with realistic symbolic and numeric parsing.
    Maintains standard GNU Coreutils error formatting.
    """
    if not args:
        return "chmod: missing operand\nTry 'chmod --help' for more information."
    
    parts = args.split()
    if len(parts) < 2:
        return f"chmod: missing operand after '{parts[0]}'\nTry 'chmod --help' for more information."
    
    mode = parts[0]
    target = " ".join(parts[1:])
    
    # Regex to validate numeric (e.g., 777, 0644) or symbolic (e.g., u+x, g-rw, a=rwx)
    numeric_pattern = re.compile(r'^[0-7]{3,4}$')
    symbolic_pattern = re.compile(r'^([ugoa]*[-+=][rwxXst]*)+$')
    
    if not (numeric_pattern.match(mode) or symbolic_pattern.match(mode)):
        return f"chmod: invalid mode: '{mode}'\nTry 'chmod --help' for more information."
        
    # Simulate realistic permission errors on critical system files
    if target.startswith("/root") or target in ["/etc/shadow", "/etc/passwd"]:
        return f"chmod: changing permissions of '{target}': Operation not permitted"
        
    # Linux 'chmod' is silent on success
    return ""


def nc(args):
    """
    Simulates netcat (nc) client and server responses.
    Handles standard reverse shell and bind shell listener patterns.
    """
    if not args:
        return (
            "usage: nc [-46CdDhklnrStUuvz] [-I length] [-i interval] [-O length]\n"
            "          [-P proxy_username] [-p source_port] [-q seconds] [-s source]\n"
            "          [-T toskeyword] [-V rtable] [-W recvlimit] [-w timeout]\n"
            "          [-X proxy_protocol] [-x proxy_address[:port]]\n"
            "          [destination] [port]"
        )
    
    parts = args.split()
    
    # Server/Listener mode simulation (e.g., nc -lvp 4444)
    is_listening = any('l' in part for part in parts if part.startswith('-'))
    is_verbose = any('v' in part for part in parts if part.startswith('-'))
    
    if is_listening:
        port = "unknown"
        if '-p' in parts:
            try:
                port_idx = parts.index('-p') + 1
                port = parts[port_idx]
            except IndexError:
                return "nc: option requires an argument -- 'p'"
        else:
            # Handle bundled flags like -lvp 4444
            for i, part in enumerate(parts):
                if '-l' in part and 'p' in part:
                    try:
                        port = parts[i + 1]
                    except IndexError:
                        pass
        
        if is_verbose:
            return f"Listening on [0.0.0.0] (family 2, port {port})"
        return "" # Standard nc -l is completely silent until connection

    # Client mode simulation
    if len(parts) >= 2:
        target_port = parts[-1]
        target_ip = parts[-2]
        
        if not target_port.isdigit():
            return f"nc: port number invalid: {target_port}"
            
        if '-z' in parts and is_verbose:
            return f"Connection to {target_ip} {target_port} port [tcp/*] succeeded!"
        elif is_verbose:
            return f"Connection to {target_ip} {target_port} port [tcp/*] succeeded!"
        else:
            return "" # Interactive shell hang simulation
            
    return "nc: missing port or hostname"


def get_common_error(command, target, error_type):
    """
    Centralized handler to simulate exact bash error consistency.
    """
    errors = {
        "not_found": f"{command}: command not found",
        "permission_denied": f"bash: {target}: Permission denied",
        "no_file": f"{command}: {target}: No such file or directory",
        "is_directory": f"{command}: {target}: Is a directory"
    }
    return errors.get(error_type, f"{command}: unknown error")