import { FileSystem } from './filesystem';
import { Terminal } from 'xterm';

export class CommandHandler {
    private fs: FileSystem;
    private term: Terminal;
    private commands: { [key: string]: string } = {
        'ls': 'Vypíše obsah adresáře',
        'cd': 'Změna adresáře (cd <adresář>)',
        'pwd': 'Vypíše aktuální cestu',
        'cat': 'Vypíše obsah souboru (cat <soubor>)',
        'clear': 'Vymaže obrazovku terminálu',
    };

    constructor(terminal: Terminal) {
        this.fs = new FileSystem();
        this.term = terminal;
    }

    executeCommand(command: string): string {
        const parts = command.trim().split(' ');
        const cmd = parts[0];
        const args = parts.slice(1);
        
        if (cmd === 'ls') {
            return this.ls();
        } else if (cmd === 'pwd') {
            return this.pwd();
        } else if (cmd === 'cd') {
            return this.cd(args[0] || '');
        } else if (cmd === 'cat') {
            return this.cat(args[0]);
        } else if (cmd === 'clear') {
            this.clear();
            return '';
        } else if (cmd === 'help') {
            return this.help();
        }
        return `Command not found: ${cmd}\r\n`;
    }

    private help(): string {
        const maxLength = Math.max(...Object.keys(this.commands).map(cmd => cmd.length));
        const helpText = Object.entries(this.commands)
            .map(([cmd, desc]) => `  ${cmd.padEnd(maxLength + 2)}${desc}`)
            .join('\r\n');
        
        return `Available commands:\r\n${helpText}\r\n`;
    }

    private ls(): string {
        const output = this.fs.listDirectory();
        return output + '\r\n';
    }

    private cd(path: string): string {
        if (!path) {
            return 'cd: missing directory argument\r\n';
        }

        const success = this.fs.changeDirectory(path);
        if (!success) {
            return `cd: ${path}: No such directory\r\n`;
        }
        return '';
    }

    private pwd(): string {
        return this.fs.getAbsolutePath() + '\r\n';
    }

    private cat(filename: string): string {
        if (!filename) {
            return 'cat: missing file operand\r\n';
        }
        
        const content = this.fs.readFile(filename);
        if (content === null) {
            return `cat: ${filename}: No such file\r\n`;
        }
        return content + '\r\n';
    }

    private clear(): void {
        this.term.clear();
    }

    getCurrentPath(): string {
        return this.fs.getAbsolutePath();
    }
} 