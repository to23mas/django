export interface FileSystemNode {
    name: string;
    type: 'file' | 'directory';
    content?: string;
    children?: { [key: string]: FileSystemNode };
    permissions: string;
    owner: string;
    group: string;
    size: number;
    modified: string;
}

export class FileSystem {
    private root: { [key: string]: FileSystemNode };
    private currentPath: string[];

    constructor() {
        this.root = {
            'home': {
                type: 'directory',
                name: 'home',
                permissions: 'drwxr-xr-x',
                owner: 'user',
                group: 'user',
                size: 4096,
                modified: 'Mar 24 10:00',
                children: {
                    'user': {
                        type: 'directory',
                        name: 'user',
                        permissions: 'drwxr-xr-x',
                        owner: 'user',
                        group: 'user',
                        size: 4096,
                        modified: 'Mar 24 10:00',
                        children: {
                            'documents': {
                                type: 'directory',
                                name: 'documents',
                                permissions: 'drwxr-xr-x',
                                owner: 'user',
                                group: 'user',
                                size: 4096,
                                modified: 'Mar 24 10:00',
                                children: {
                                    'readme.txt': {
                                        type: 'file',
                                        name: 'readme.txt',
                                        content: 'Welcome to the system!',
                                        permissions: '-rw-r--r--',
                                        owner: 'user',
                                        group: 'user',
                                        size: 21,
                                        modified: 'Mar 24 10:00'
                                    }
                                }
                            },
                            'hello.py': {
                                type: 'file',
                                name: 'hello.py',
                                content: 'print("Hello, World!")',
                                permissions: '-rw-r--r--',
                                owner: 'user',
                                group: 'user',
                                size: 23,
                                modified: 'Mar 24 10:00'
                            }
                        }
                    }
                }
            }
        };
        this.currentPath = ['home', 'user'];
    }

    getCurrentDirectory(): FileSystemNode | null {
        let current: any = this.root;
        for (const part of this.currentPath) {
            if (!current[part] || current[part].type !== 'directory') {
                return null;
            }
            current = current[part].children;
        }
        return current;
    }

    getAbsolutePath(): string {
        return '/' + this.currentPath.join('/');
    }

    changeDirectory(path: string): boolean {
        if (path === '..') {
            if (this.currentPath.length > 1) {
                this.currentPath.pop();
                return true;
            }
            return false;
        }

        const current = this.getCurrentDirectory();
        if (!current || !current[path] || current[path].type !== 'directory') {
            return false;
        }

        this.currentPath.push(path);
        return true;
    }

    listDirectory(showHidden: boolean = false): string {
        const current = this.getCurrentDirectory();
        if (!current) return 'Error: Invalid directory';

        const entries = Object.values(current);
        if (!showHidden) {
            entries.filter(entry => !entry.name.startsWith('.'));
        }

        return entries.map(entry => {
            if (entry.type === 'directory') {
                return `${entry.permissions}  ${entry.owner} ${entry.group}  ${entry.size.toString().padStart(6)} ${entry.modified} ${entry.name}/`;
            } else {
                return `${entry.permissions}  ${entry.owner} ${entry.group}  ${entry.size.toString().padStart(6)} ${entry.modified} ${entry.name}`;
            }
        }).join('\r\n');
    }
} 