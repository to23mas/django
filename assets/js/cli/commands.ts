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
        'python --version': 'Zobrazí verzi Pythonu',
        'python manage.py makemigrations': 'Vytvoří migrace pro všechny aplikace',
        'python manage.py makemigrations <app_name>': 'Vytvoří migrace pro danou aplikaci',
        'npm list': 'Zobrazí seznam nainstalovaných knihoven',
        'npm list <knihovna>': 'Zobrazí informace o konkrétní knihovně',
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
        } else if (cmd === 'python') {
            if (args[0] === '--version') {
                return this.pythonVersion();
            }
            if (args[0] === 'manage.py' && args[1] === 'makemigrations') {
                return this.makemigrations(args[2]);
            }
            return this.python();
        } else if (cmd === 'npm' && args[0] === 'list') {
            return this.npmList(args[1]);
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

    private pythonVersion(): string {
        return 'Python 3.11.8\r\n';
    }

    private python(): string {
        return 'Python interpret není v tuto chvíli k dispozici. Použijte příkaz s parametry.\r\n';
    }

    private makemigrations(appName?: string): string {
        const migrations = {
            'blog': [
                'Migrations for \'blog\':',
                '  blog/migrations/0001_initial.py',
                '    - Create model Post',
                '    - Create model Category',
                '    - Add field categories to post'
            ],
            'users': [
                'Migrations for \'users\':',
                '  users/migrations/0001_initial.py',
                '    - Create model Profile',
                '    - Add field user to profile'
            ],
            'django': [
                'Migrations for \'django\':',
                '  django/migrations/0023_django_added_name.py',
                '    - Add field name to django',
            ]
        };

        if (appName) {
            if (appName in migrations) {
                return migrations[appName].join('\r\n') + '\r\n';
            }
            return `No migrations detected for app '${appName}'\r\n`;
        }

        return Object.values(migrations)
            .map(lines => lines.join('\r\n'))
            .join('\r\n\r\n') + '\r\n';
    }

    private npmList(packageName?: string): string {
        const packages = {
            'autoprefixer': '10.4.21',
            'postcss': '8.5.3',
            'react': '18.2.0',
            'react-dom': '18.2.0',
            'typescript': '5.3.3',
            'webpack': '5.90.3',
            'babel-loader': '9.1.3',
            '@babel/core': '7.24.0',
            '@babel/preset-react': '7.23.3',
            '@babel/preset-typescript': '7.23.3',
            'eslint': '8.57.0',
            'prettier': '3.2.5',
            'jest': '29.7.0',
            '@testing-library/react': '14.2.1',
            'axios': '1.6.7',
            'next': '14.1.0',
            'vue': '3.4.21',
            'angular': '17.2.0',
            'svelte': '4.2.12',
            'express': '4.18.3',
            'tailwindcss': '4.0.1',
            'mongoose': '8.2.1',
            'prisma': '5.10.2',
            'graphql': '16.8.1',
            'apollo-server': '3.13.0',
            'redux': '5.0.1',
            'mobx': '6.12.0',
            'styled-components': '6.1.8',
            'material-ui': '5.15.11',
            'chakra-ui': '2.8.2',
            'd3': '7.8.5',
            'lodash': '4.17.21',
            'moment': '2.30.1',
            'date-fns': '3.3.1',
            'socket.io': '4.7.4',
            'ws': '8.16.0',
            'nodemon': '3.1.0',
            'dotenv': '16.4.5',
            'winston': '3.11.0',
            'jest-dom': '6.4.2',
            'cypress': '13.6.6',
            'storybook': '7.6.17',
            'husky': '9.0.11',
            'lint-staged': '15.2.2',
            'commitlint': '18.6.1'
        };

        if (packageName) {
            if (packageName in packages) {
                return `${packageName}@${packages[packageName]}\r\n`;
            }
            return `npm ERR! code E404\r\nnpm ERR! 404 Not Found: ${packageName}@latest\r\n`;
        }

        return Object.entries(packages)
            .map(([name, version]) => `├── ${name}@${version}`)
            .join('\r\n') + '\r\n';
    }

    getCurrentPath(): string {
        return this.fs.getAbsolutePath();
    }
} 