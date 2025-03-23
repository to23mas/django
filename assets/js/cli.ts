import { Terminal } from 'xterm';
import { CommandHandler } from './cli/commands';
import { WebLinksAddon } from 'xterm-addon-web-links';
import { SearchAddon } from 'xterm-addon-search';

export function initCli() {
    document.addEventListener('DOMContentLoaded', () => {
        if (typeof Terminal === 'undefined') {
            console.error('Terminal is not defined! Check xterm.js import.');
            return;
        }

        const term = new Terminal({
            cursorBlink: true,
            fontSize: 14,
            fontFamily: 'Menlo, Monaco, "Courier New", monospace',
            theme: {
                background: '#1e1e1e',
                foreground: '#ffffff'
            },
            scrollback: 1000,
            convertEol: true,
            cols: 80,
            rows: 24,
            allowTransparency: true,
            rightClickSelectsWord: true,
            copyOnSelect: false,
            selectionStyle: {
                background: '#666666',
                foreground: '#ffffff'
            }
        });

        // Add addons
        term.loadAddon(new WebLinksAddon());
        const searchAddon = new SearchAddon();
        term.loadAddon(searchAddon);

        // Enable copy on Ctrl+C when text is selected
        term.attachCustomKeyEventHandler((event: KeyboardEvent) => {
            if (event.type === 'keydown' && event.ctrlKey && event.key === 'c') {
                if (term.hasSelection()) {
                    navigator.clipboard.writeText(term.getSelection());
                    return false;
                }
            }
            return true;
        });

        const commandHandler = new CommandHandler();
        const terminalElement = document.getElementById('terminal');
        if (!terminalElement) return;

        // Attach terminal to container
        term.open(terminalElement);

        // Show initial prompt
        term.write('$ ');

        // Keep track of current line
        let currentLine = '';

        // Handle terminal input
        term.onKey(({key, domEvent}) => {
            // Handle Enter
            if (domEvent.keyCode === 13) {
                term.write('\r\n');
                const cmd = currentLine.trim();
                if (cmd) {
                    const output = commandHandler.executeCommand(cmd);
                    if (output) {
                        term.write(output);
                    }
                }
                currentLine = '';
                term.write('$ ');
            }
            // Handle Backspace
            else if (domEvent.keyCode === 8) {
                if (currentLine.length > 0) {
                    currentLine = currentLine.slice(0, -1);
                    term.write('\b \b');
                }
            }
            // Handle normal input
            else {
                currentLine += key;
                term.write(key);
            }
        });

        // Handle form submission
        const form = document.getElementById('cli-form') as HTMLFormElement;
        if (!form) return;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const answerInput = document.getElementById('answer-input') as HTMLTextAreaElement;
            if (!answerInput) return;

            const answer = answerInput.value.trim();
            const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

            try {
                const response = await fetch('/validate-cli-answer/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken || ''
                    },
                    body: JSON.stringify({
                        answer,
                        command: 'ls -la',
                        chapterId: (window as any).chapterId,
                        lessonId: (window as any).lessonId,
                        projectId: (window as any).projectId
                    })
                });

                const data = await response.json();
                if (data.correct) {
                    alert('Correct!');
                } else {
                    alert('Try again!');
                }
            } catch (error) {
                console.error('Error submitting answer:', error);
                alert('An error occurred while submitting your answer.');
            }
        });
    });
} 