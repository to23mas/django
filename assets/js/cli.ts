import { Terminal } from 'xterm';
import { CommandHandler } from './cli/commands';
import { WebLinksAddon } from 'xterm-addon-web-links';
import { SearchAddon } from 'xterm-addon-search';
import { addBlocklyFlashMessage, clearBlocklyFlashMessage } from './flash_messages';

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

        const commandHandler = new CommandHandler(term);
        const terminalElement = document.getElementById('terminal');
        if (!terminalElement) return;

        // Attach terminal to container
        term.open(terminalElement);

        const getPrompt = () => {
            const path = commandHandler.getCurrentPath();
            return `${path}$ `;
        };

        // Show initial prompt with path
        term.write(getPrompt());

        // Add command history
        const commandHistory: string[] = [];
        let historyIndex = -1;

        // Keep track of current line
        let currentLine = '';
        let savedLine = '';

        // Handle terminal input
        term.onKey(({key, domEvent}) => {
            const ev = domEvent as KeyboardEvent;

            // Handle arrow up/down for history
            if (ev.keyCode === 38) { // Up arrow
                if (historyIndex === -1) {
                    savedLine = currentLine;
                }
                if (commandHistory.length > 0 && historyIndex < commandHistory.length - 1) {
                    historyIndex++;
                    currentLine = commandHistory[commandHistory.length - 1 - historyIndex];
                    // Clear current line and write new one
                    term.write('\x1b[2K\r' + getPrompt() + currentLine);
                }
                return;
            } else if (ev.keyCode === 40) { // Down arrow
                if (historyIndex > 0) {
                    historyIndex--;
                    currentLine = commandHistory[commandHistory.length - 1 - historyIndex];
                    term.write('\x1b[2K\r' + getPrompt() + currentLine);
                } else if (historyIndex === 0) {
                    historyIndex = -1;
                    currentLine = savedLine;
                    term.write('\x1b[2K\r' + getPrompt() + currentLine);
                }
                return;
            }

            if (ev.keyCode === 13) { // Enter
                term.write('\r\n');
                const cmd = currentLine.trim();
                if (cmd) {
                    // Add command to history
                    commandHistory.push(cmd);
                    historyIndex = -1;
                    savedLine = '';

                    const output = commandHandler.executeCommand(cmd);
                    if (cmd === 'clear') {
                        // After clear, just show the prompt
                        term.write(getPrompt());
                    } else if (output) {
                        term.write(output);
                        term.write(getPrompt());
                    } else {
                        term.write(getPrompt());
                    }
                } else {
                    term.write(getPrompt());
                }
                currentLine = '';
            }
            // Handle Backspace
            else if (ev.keyCode === 8) {
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

            const validateButton = document.getElementById('validateButton');
            const defaultText = validateButton?.querySelector('.default-text');
            const spinner = validateButton?.querySelector('.spinner');

            if (defaultText) defaultText.classList.add('hidden');
            if (spinner) spinner.classList.remove('hidden');

            clearBlocklyFlashMessage();

            const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
            const formData = new URLSearchParams({
                answer: answerInput.value.trim(),
                chapter_id: (window as any).chapterId,
                lesson_id: (window as any).lessonId,
                project_id: (window as any).projectId,
                course_db: (window as any).courseName,
                csrfmiddlewaretoken: csrfToken || ''
            });

            try {
                const response = await fetch('/projects/lesson/validate-cli', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': csrfToken || ''
                    },
                    body: formData
                });

                const data = await response.json();
                if (data.status === 'success') {
                    if (data.redirect) {
                        const nextButtonContainer = document.getElementById('nextButtonContainer');
                        if (!document.querySelector('body > div.h-full > div.chapter-buttons.mx-auto.md\\:w-4\\/6 > form > button')) {
                            const anchor = document.createElement('a');
                            anchor.href = data.url;
                            anchor.className = 'green_button';
                            anchor.textContent = 'Další Kapitola';
                            nextButtonContainer.appendChild(anchor);
                        }
                        addBlocklyFlashMessage('Správně.', true);
                    } else {
                        addBlocklyFlashMessage('Správně.', true);
                    }
                } else {
                    addBlocklyFlashMessage(data.message || 'Nesprávná odpověď.');
                }
            } catch (error) {
                console.error('Error submitting answer:', error);
                addBlocklyFlashMessage('Došlo k chybě při odesílání odpovědi.');
            } finally {
                if (defaultText) defaultText.classList.remove('hidden');
                if (spinner) spinner.classList.add('hidden');
            }
        });
    });
} 