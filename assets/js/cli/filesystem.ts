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
                                    'index.html': {
                                        type: 'file',
                                        name: 'index.html',
                                        content: 'Vítej v CLI!',
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
        // Handle .. to go up one directory
        if (path === '..' || path === '../') {
            if (this.currentPath.length > 1) {
                this.currentPath.pop();
                return true;
            }
            return false;
        }

        // Remove trailing slash if present
        const cleanPath = path.endsWith('/') ? path.slice(0, -1) : path;

        const current = this.getCurrentDirectory();
        if (!current || !current[cleanPath] || current[cleanPath].type !== 'directory') {
            return false;
        }

        this.currentPath.push(cleanPath);
        return true;
    }

    listDirectory(): string {
        const current = this.getCurrentDirectory();
        if (!current) return 'Error: Invalid directory';

        return Object.values(current)
            .map(entry => entry.name + (entry.type === 'directory' ? '/' : ''))
            .join('  ');
    }

    readFile(filename: string): string | null {
        const current = this.getCurrentDirectory();
        if (!current) return null;

        const file = current[filename];
        if (!file || file.type !== 'file') {
            return null;
        }

        return file.content || '';
    }
}
