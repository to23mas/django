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

        // Keep track of current line
        let currentLine = '';

        // Handle terminal input
        term.onKey(({key, domEvent}) => {
            if (domEvent.keyCode === 13) { // Enter
                term.write('\r\n');
                const cmd = currentLine.trim();
                if (cmd) {
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
                        addBlocklyFlashMessage('Správně.', true);
                        setTimeout(() => {
                            window.location.href = data.url;
                        }, 1000);
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