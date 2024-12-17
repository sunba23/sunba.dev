import os
import time
from collections import deque
from fastapi import WebSocketDisconnect

class TerminalManager:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.current_dir = base_dir
        self.command_timestamps = deque(maxlen=5)

    def get_relative_path(self):
        return os.path.relpath(self.current_dir, self.base_dir) or '.'

    def get_relative_path_display(self):
        relative_path = self.get_relative_path()
        return f'~/{relative_path}' if relative_path != '.' else '~'

    async def process_command(self, command: str):
        current_time = time.time()
        self.command_timestamps.append(current_time)

        if len(self.command_timestamps) >= 3 and (self.command_timestamps[-1] - self.command_timestamps[-3]) < 1:
            raise WebSocketDisconnect(code=1000, reason="Rate limit exceeded")

        if command == 'ls':
            return self.list_directory()
        elif command.startswith('cd '):
            path = command.split(' ', 1)[1]
            return self.change_directory(path)
        elif command == 'pwd':
            return self.print_working_directory()
        elif command == 'help':
            return self.get_help_message()
        elif command == 'project':
            return self.get_project_info()
        elif command.startswith('cat '):
            filename = command.split(' ', 1)[1]
            return self.read_file(filename)
        else:
            return f'Command not found: {command}'

    def list_directory(self):
        try:
            items = os.listdir(self.current_dir)
            return '  '.join(items)
        except Exception as e:
            return f"Error listing directory: {e}"

    def change_directory(self, path: str):
        if path.startswith('/'):
            path = path.lstrip('/')
            new_path = os.path.join(self.base_dir, path)
        else:
            new_path = os.path.join(self.current_dir, path) if path != '..' else os.path.dirname(self.current_dir)

        new_path = os.path.abspath(new_path)

        if os.path.commonpath([new_path, self.base_dir]) != self.base_dir:
            return 'Access denied: you cannot navigate outside of the root directory.'

        if os.path.isdir(new_path):
            self.current_dir = new_path
            return ''
        else:
            return f'Directory not found: {path}'

    def print_working_directory(self):
        relative_path = self.get_relative_path()
        return '/webfs' if relative_path == '.' else f'/webfs/{relative_path}'

    def read_file(self, filename: str):
        file_path = os.path.join(self.current_dir, filename)
        if not os.path.commonpath([file_path, self.base_dir]) == self.base_dir:
            return 'Access denied: You cannot read files outside of the root directory.'
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    return content.replace('\n', '\r\n')
            except Exception as e:
                return f"Error reading file: {e}"
        else:
            return f'No such file: {filename}'

    def get_project_info(self):
        return [
            {"backend": "Python, FastAPI, WebSockets, OS module"},
            {"frontend": "HTML+css, xterm.js, Vite, WebSockets"},
            {"infrastructure": "Docker, Docker compose, Nginx for deployment"},
            {"CI": "Jenkins"}
        ]

    def get_help_message(self):
        return [
            {"command": "project", "description": "Display project information message"},
            {"command": "ls", "description": "List files and directories"},
            {"command": "cd", "description": "Change directory"},
            {"command": "pwd", "description": "Print the current working directory"},
            {"command": "cat <file>", "description": "Display the content of a file"},
            {"command": "help", "description": "Display this help message"}
        ]
