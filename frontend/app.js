import { Terminal } from '@xterm/xterm/lib/xterm.js';
import { FitAddon } from '@xterm/addon-fit';

const universalDarkTheme = {
  background: '#000000',
  foreground: '#d0d0d0',
  cursor: '#ffcc00',
  selection: '#44475a',
  black: '#1a1a1a',
  red: '#ff5555',
  green: '#50fa7b',
  yellow: '#f1fa8c',
  blue: '#6272a4',
  magenta: '#ff79c6',
  cyan: '#8be9fd',
  white: '#f8f8f2',
  brightBlack: '#444444',
  brightRed: '#ff6e6e',
  brightGreen: '#69ff94',
  brightYellow: '#f4f99d',
  brightBlue: '#8be9fd',
  brightMagenta: '#ff92df',
  brightCyan: '#a4f7ff',
  brightWhite: '#ffffff'
};

const term = new Terminal({
  cursorBlink: true,
  theme: universalDarkTheme,
  fontSize: 16,
  fontFamily: '"JetBrainsMono Nerd Font", monospace'
});


const terminalContainer = document.getElementById('terminal-container');

const fitAddon = new FitAddon();
term.loadAddon(fitAddon);
console.log("test-log-2");

if (terminalContainer) {
  term.open(terminalContainer);
  fitAddon.fit();
  term.writeln('\x1b[1m\x1b[34msunba.dev - staging version! for fun and user testing.\x1b[0m');
  term.writeln('\x1b[5m\x1b[33mServer node: GMKtec NucBox G3 | Alpine Linux\x1b[0m');
  term.writeln('\x1b[2m\x1b[33mMade with: Xterm.js, FastAPI+daphne[websockets], Kubernetes (k3s), Ansible\x1b[0m');
  term.writeln('\x1b[2m\x1b[33mAuthor: Franek Suszko - https://github.com/sunba23\x1b[0m');
}

console.log("WebSocket URL:", import.meta.env.VITE_WS_URL);
const socket = new WebSocket(import.meta.env.VITE_WS_URL);

socket.onopen = () => {
  prompt();
};

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  const message = data.response;
  const currentDir = data.current_dir;

  if (Array.isArray(message)) {
    if (message[0] && message[0].command) {
      message.forEach(cmd => {
        term.writeln(`\x1b[36m${cmd.command}\x1b[0m - ${cmd.description}`);
      });
    } 
    else if (message[0] && message[0].backend) {
      message.forEach(info => {
        for (const [key, value] of Object.entries(info)) {
          term.writeln(`\x1b[36m${key}\x1b[0m - ${value}`);
        }
      });
    }
  } else {
    term.write(`\r${message}\n`);
  }
  prompt(currentDir);
};


socket.onerror = (error) => {
  console.error('WebSocket error:', error);
  term.writeln('\r\n[Error: WebSocket connection issue]');
  prompt();
};

const prompt = (currentDir = '~') => {
  term.write(`\r\n\x1b[34m${currentDir}\x1b[32m $ \x1b[0m`);
};

let inputBuffer = '';

term.onKey(e => {
  const char = e.key;

  if (char === '\r') {
    if (inputBuffer.trim()) {
      term.write('\r\n');
      if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ command: inputBuffer }));
      } else {
        term.writeln('[WebSocket is not connected]');
        prompt();
      }
    } else {
      prompt();
    }
    inputBuffer = '';
  } else if (char === '\u007f') {
    if (inputBuffer.length > 0) {
      inputBuffer = inputBuffer.slice(0, -1);
      term.write('\b \b');
    }
  } else if (char >= String.fromCharCode(0x20) && char <= String.fromCharCode(0x7e)) {
    inputBuffer += char;
    term.write(char);
  }
});

window.addEventListener('resize', () => {
  fitAddon.fit();
});

