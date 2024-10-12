import json
import os
import time
from collections import deque
from channels.generic.websocket import AsyncWebsocketConsumer

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../webfs'))

class TerminalConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_timestamps = deque(maxlen=5)

    async def connect(self):
        self.current_dir = BASE_DIR
        await self.accept()
        await self.send(text_data=json.dumps({
            'response': "Connected to the terminal. Type 'help' for a list of commands.",
            'current_dir': self.get_relative_path_display()
        }))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        current_time = time.time()
        self.command_timestamps.append(current_time)

        if len(self.command_timestamps) >= 3 and (self.command_timestamps[-1] - self.command_timestamps[-3]) < 1:
            await self.send(text_data=json.dumps({
                'response': "oops! no spamming! you will get disconnected now.",
                'current_dir': self.get_relative_path_display()
            }))
            await self.close()
            return

        try:
            data = json.loads(text_data)
            command = data.get('command', '')
            response = await self.process_command(command)
            await self.send(text_data=json.dumps({
                'response': response,
                'current_dir': self.get_relative_path_display()
            }))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'response': "Invalid command format. Please send a valid command.",
                'current_dir': self.get_relative_path_display()
            }))

    async def process_command(self, command):
        if command == 'ls':
            return self.list_directory()
        elif command.startswith('cd '):
            path = command.split(' ', 1)[1] if len(command.split(' ')) > 1 else ''
            return self.change_directory(path)
        elif command == 'cd ..':
            return self.change_directory('..')
        elif command == 'pwd':
            return self.print_working_directory()
        elif command == 'help':
            return self.get_help_message()
        elif command == 'project':
            return self.get_project_info()
        elif command.startswith('cat '):
            filename = command.split(' ', 1)[1] if len(command.split(' ')) > 1 else ''
            return self.read_file(filename)
        else:
            return f'Command not found: {command}'

    def list_directory(self):
        try:
            items = os.listdir(self.current_dir)
            return '  '.join(items)
        except Exception as e:
            return f"Error listing directory: {e}"

    def change_directory(self, path):
        if path.startswith('/'):
            path = path.lstrip('/')
            new_path = os.path.join(BASE_DIR, path)
        else:
            new_path = os.path.join(self.current_dir, path) if path != '..' else os.path.dirname(self.current_dir)

        new_path = os.path.abspath(new_path)

        if os.path.commonpath([new_path, BASE_DIR]) != BASE_DIR:
            return 'Access denied: you cannot navigate outside of the root directory.'

        if os.path.isdir(new_path):
            self.current_dir = new_path
            return ''  # No message on successful navigation
        else:
            return f'Directory not found: {path}'

    def print_working_directory(self):
        relative_path = self.get_relative_path()
        return f'/webfs' if relative_path == '.' else f'/webfs/{relative_path}'

    def read_file(self, filename):
        file_path = os.path.join(self.current_dir, filename)
        if not os.path.commonpath([file_path, BASE_DIR]).startswith(BASE_DIR):
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

    def get_relative_path(self):
        return os.path.relpath(self.current_dir, BASE_DIR) or '.'

    def get_relative_path_display(self):
        relative_path = self.get_relative_path()
        return f'~/{relative_path}' if relative_path != '.' else '~'

    def get_project_info(self):
        project_info = [
            {"backend": "Python, Django, Django channels, Daphne, OS module"},
            {"frontend": "HTML+css, xterm.js, Vite, WebSockets"},
            {"infrastructure": "Docker, Docker compose, Nginx for deployment"},
            {"CI": "Jenkins"}
        ]
        return project_info

    def get_help_message(self):
        help_message = [
            {"command": "project", "description": "Display project information message"},
            {"command": "ls", "description": "List files and directories"},
            {"command": "cd", "description": "Change directory"},
            {"command": "pwd", "description": "Print the current working directory"},
            {"command": "cat <file>", "description": "Display the content of a file"},
            {"command": "help", "description": "Display this help message"}
        ]
        return help_message

