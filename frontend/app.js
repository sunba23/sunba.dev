import { Terminal } from '@xterm/xterm/lib/xterm.js';
import { FitAddon } from '@xterm/addon-fit';

const catppuccinMacchiato = {
    background: '#24273a',
    foreground: '#cad3f5',
    cursor: '#ed8796',
    selection: '#494d64',
    black: '#494d64',
    red: '#ed8796',
    green: '#a6da95',
    yellow: '#eed49f',
    blue: '#8aadf4',
    magenta: '#f5bde6',
    cyan: '#8bd5ca',
    white: '#b8c0e0',
    brightBlack: '#5b6078',
    brightRed: '#ed8796',
    brightGreen: '#a6da95',
    brightYellow: '#eed49f',
    brightBlue: '#8aadf4',
    brightMagenta: '#f5bde6',
    brightCyan: '#8bd5ca',
    brightWhite: '#a5adcb'
};

const term = new Terminal({
    cursorBlink: true,
    theme: catppuccinMacchiato,
    fontSize: 16,
    fontFamily: '"JetBrainsMono Nerd Font", monospace'
});

const terminalContainer = document.getElementById('terminal-container');

const fitAddon = new FitAddon();
term.loadAddon(fitAddon);

if (terminalContainer) {
    term.open(terminalContainer);
    fitAddon.fit();
}

const socket = new WebSocket('wss://sunba.dev/ws/terminal/');


socket.onopen = () => {
    term.writeln('Welcome to my terminal themed page.');
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

