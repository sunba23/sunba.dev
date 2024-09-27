import { Terminal } from '@xterm/xterm';
import { FitAddon } from '@xterm/addon-fit';

const term = new Terminal();
const fitAddon = new FitAddon();

term.loadAddon(fitAddon);

term.open(document.getElementById('terminal-container'));

fitAddon.fit();

const socket = new WebSocket('ws://web:8000/ws/terminal/');

socket.onmessage = function(event) {
    term.write(event.data);
    fitAddon.fit();
};

term.onData(data => {
    socket.send(data);
});

window.addEventListener('resize', () => {
    fitAddon.fit();
});
