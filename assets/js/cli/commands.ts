import { FileSystem } from './filesystem';
import { Terminal } from 'xterm';
import { DockerManager } from './docker';

export class CommandHandler {
    private fs: FileSystem;
    private term: Terminal;
    private dockerManager: DockerManager;
    private commands: { [key: string]: string } = {
        'clear': 'Vyčistí obrazovku terminálu',
        'ls': 'Vypíše obsah adresáře',
        'cd': 'Změna adresáře (cd <adresář>)',
        'pwd': 'Vypíše aktuální cestu',
        'cat': 'Vypíše obsah souboru (cat <soubor>)',
        'python --version': 'Zobrazí verzi Pythonu',
        'python manage.py makemigrations <app_name>': 'Vytvoří migrace pro danou aplikaci',
        'python manage.py startapp <app_name>': 'Vytvoří novou Django aplikaci',
        'python manage.py test': 'Spustí testy',
        'pylint <python_file>': 'Spustí kontrolu kódu pomocí Pylint',
        'npm list': 'Zobrazí seznam nainstalovaných knihoven',
        'npm list <knihovna>': 'Zobrazí informace o konkrétní knihovně',
        'pip': 'Správce Python balíčků',
        'docker': 'Správa Docker kontejnerů',
        'npm run <script>': 'Spustí daný skript',
    };

    constructor(terminal: Terminal) {
        this.fs = new FileSystem();
        this.term = terminal;
        this.dockerManager = new DockerManager();
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
            if (args[0] === 'manage.py') {
                if (!this.isInProjectRoot()) {
                    return 'Error: manage.py file not found in current directory.\r\nMake sure you are in the directory containing manage.py\r\n';
                }
                
                if (args[1] === 'makemigrations') {
                    return this.makemigrations(args[2]);
                }
                if (args[1] === 'startapp') {
                    return this.startapp(args[2]);
                }
                if (args[1] === 'test') {
                    return this.runTests();
                }
                if (args[1] === 'tailwind' && args[2] === 'start') {
                    return this.handleTailwindStart();
                }
            }
            return this.python();
        } else if (cmd === 'npm') {
            if (args[0] === 'list') {
                return this.npmList(args[1]);
            } else if (args[0] === 'run') {
                if (!this.isNpmProject()) {
                    return 'Error: package.json not found in current directory.\r\n';
                }
                if (args[1] === 'build:game') {
                    return this.npmBuildGame();
                }
                return `npm ERR! missing script: ${args[1]}\r\n`;
            }
            return this.npmHelp();
        } else if (cmd === 'pip') {
            if (args[0] === 'list') {
                return this.pipList();
            }
            return this.pipHelp();
        } else if (cmd === 'docker') {
            return this.docker(args);
        } else if (cmd === 'pylint') {
            if (!args[0]) {
                return 'Error: No Python file specified.\r\nUsage: pylint <python_file>\r\n';
            }
            return this.runPylint(args[0]);
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
        return 'Špatně zadaný příkaz python.\r\n';
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

    private pipHelp(): string {
        return 'Usage:\n  pip <command>\n\nCommands:\n  list                        List installed packages.\n\r\n';
    }

    private pipList(): string {
        const packages = [
            'asgiref           3.7.2',
            'Django            5.0.3',
            'django-cors       0.1',
            'django-rest       0.8.7',
            'djangorest        3.14.0',
            'Pillow            10.2.0',
            'pip               24.0',
            'psycopg2          2.9.9',
            'pymongo           4.6.1',
            'python-dotenv     1.0.1',
            'redis             5.0.1',
            'setuptools        69.1.1',
            'sqlparse          0.4.4',
            'typing_extensions 4.9.0',
            'wheel             0.42.0'
        ];
        return packages.join('\r\n') + '\r\n';
    }

    private docker(args: string[]): string {
        if (args.length === 0) {
            return 'Usage: docker [command] [options]\n\nCommands:\n  ps        List containers\n  images    List images\n  run       Run a container\n';
        }

        const command = args[0];
        const options = args.slice(1);

        switch (command) {
            case 'ps':
                return this.dockerManager.ps(options.includes('-a'));
            case 'images':
                return this.dockerManager.images();
            case 'run':
                if (options.length === 0) {
                    return 'Error: No image specified\nUsage: docker run [OPTIONS] IMAGE [COMMAND] [ARG...]';
                }
                return this.dockerManager.run(options[0]);
            default:
                return `docker: unknown command "${command}"\nRun 'docker' for usage information.`;
        }
    }

    private startapp(appName?: string): string {
        if (!appName) {
            return 'Error: You must provide an app name.\r\nUsage: python manage.py startapp <app_name>\r\n';
        }

        const current = this.fs.getCurrentDirectory();
        if (current && current[appName]) {
            return `Error: '${appName}' already exists.\r\n`;
        }

        const hash = appName === 'users' ? 'f8d9e7c6' : Math.random().toString(36).substring(2, 10);

        return `${hash}\r\n`;
    }

    getCurrentPath(): string {
        return this.fs.getAbsolutePath();
    }

    private isInProjectRoot(): boolean {
        return this.fs.fileExists('manage.py');
    }

    private handleTailwindStart(): string {
        return `> theme@3.8.0 start
> npm run dev

> theme@3.8.0 dev
> cross-env NODE_ENV=development tailwindcss --postcss -i ./src/styles.css -o ../static/css/dist/secret_styles.css -w

Rebuilding...

Done in 403ms.`;
    }

    private isNpmProject(): boolean {
        const current = this.fs.getCurrentDirectory();
        if (!current) return false;
        return current['package.json'] !== undefined;
    }

    private npmBuildGame(): string {
        if (!this.isNpmProject()) {
            return 'Error: package.json not found in current directory.\r\n';
        }

        const hash = '42fa301';
        return [
            '> game@1.0.0 build:game',
            '> vite build',
            '',
            'vite v5.1.4 building for production...',
            '',
            '✓ 0 modules transformed.',
            'dist/index.html                   0.46 kB │ gzip:  0.30 kB',
            `dist/assets/index-${hash}.js      1.45 kB │ gzip:  0.72 kB`,
            `dist/assets/index-${hash}.css     0.23 kB │ gzip:  0.15 kB`,
            '',
            '✓ built in 234ms',
            '',
            'Build completed successfully!',
            `Hash: ${hash}`,
            ''
        ].join('\r\n');
    }

    private npmHelp(): string {
        return 'Usage: npm <command>\n\nCommands:\n  list        List installed packages\n  run         Run a script from package.json\n';
    }

    private runTests(): string {
        return [
            'Creating test database for alias \'default\'...',
            'System check identified no issues (0 silenced).',
            '',
            'test_create_post (blog.tests.PostTests) ... ok',
            'test_delete_post (blog.tests.PostTests) ... ok',
            'test_edit_post (blog.tests.PostTests) ... FAIL',
            'test_list_posts (blog.tests.PostTests) ... ok',
            'test_user_login (users.tests.UserTests) ... ok',
            'test_user_registration (users.tests.UserTests) ... ok',
            '',
            '======================================================================',
            'FAIL: test_edit_post (blog.tests.PostTests)',
            '----------------------------------------------------------------------',
            'AssertionError: 404 != 200',
            '',
            '----------------------------------------------------------------------',
            'Ran 6 tests in 0.234s',
            '',
            'FAILED (failures=1)',
            'Destroying test database for alias \'default\'...',
            ''
        ].join('\r\n');
    }

    private runPylint(file: string): string {
        if (!file.endsWith('.py')) {
            return `Error: ${file} is not a Python file.\r\n`;
        }

        if (!this.fs.fileExists(file)) {
            return `Error: ${file} does not exist.\r\n`;
        }

        if (file === 'example.py') {
            return [
                '************* Module example',
                'example.py:1:0: C0111: Missing module docstring (missing-docstring)',
                '',
                '------------------------------------------------------------------',
                'Your code has been rated at 9.00/10',
                '',
                ''
            ].join('\r\n');
        }

        return [
            `************* Module ${file.replace('.py', '')}`,
            `${file}:15:4: C0116: Missing function or method docstring (missing-docstring)`,
            `${file}:23:8: W0621: Redefining name \'request\' from outer scope (redefined-outer-name)`,
            `${file}:45:4: C0103: Function name "create_post" doesn\'t conform to snake_case naming style (invalid-name)`,
            '',
            '------------------------------------------------------------------',
            'Your code has been rated at 7.50/10',
            '',
            ''
        ].join('\r\n');
    }
} 