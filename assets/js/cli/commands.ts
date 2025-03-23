import { FileSystem } from './filesystem';
import { Terminal } from './terminal';

export class CommandHandler {
    private fs: FileSystem;
    private term: Terminal;

    constructor(terminal: Terminal) {
        this.fs = new FileSystem();
        this.term = terminal;
    }

    executeCommand(command: string): string {
        const parts = command.trim().split(' ');
        const cmd = parts[0];
        const args = parts.slice(1);

        switch (cmd) {
            case 'clear':
                this.term.clear();
                return '';
            case 'ls':
                return this.ls(args);
            case 'cd':
                return this.cd(args);
            case 'pwd':
                return this.pwd();
            default:
                return `Command not found: ${cmd}\r\n`;
        }
    }

    private ls(args: string[]): string {
        const showHidden = args.includes('-a') || args.includes('--all');
        const showLong = args.includes('-l');
        const output = this.fs.listDirectory(showHidden);
        return output + '\r\n';
    }

    private cd(args: string[]): string {
        if (args.length !== 1) {
            return 'cd: missing directory argument\r\n';
        }

        const success = this.fs.changeDirectory(args[0]);
        if (!success) {
            return `cd: ${args[0]}: No such directory\r\n`;
        }
        return '';
    }

    private pwd(): string {
        return this.fs.getAbsolutePath() + '\r\n';
    }
} 