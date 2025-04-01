interface Container {
    id: string;
    name: string;
    image: string;
    status: string;
    created: string;
}

interface Image {
    id: string;
    repository: string;
    tag: string;
    size: string;
    created: string;
}

export class DockerManager {
    private containers: Container[] = [
        {
            id: 'abc123def456',
            name: 'web-server',
            image: 'nginx:latest',
            status: 'Up 2 hours',
            created: '2024-03-31 10:00:00'
        },
        {
            id: 'def456ghi789',
            name: 'db-server',
            image: 'postgres:15',
            status: 'Up 2 hours',
            created: '2024-03-31 10:00:00'
        },
        {
            id: 'ghi789jkl012',
            name: 'redis-cache',
            image: 'redis:latest',
            status: 'Exited (0) 2 days ago',
            created: '2024-03-29 10:00:00'
        }
    ];

    private dockerImages: Image[] = [
        {
            id: 'sha256:1234567890abcdef',
            repository: 'nginx',
            tag: 'latest',
            size: '142MB',
            created: '2024-03-30 15:00:00'
        },
        {
            id: 'sha256:abcdef1234567890',
            repository: 'postgres',
            tag: '15',
            size: '379MB',
            created: '2024-03-30 15:00:00'
        },
        {
            id: 'sha256:7890abcdef123456',
            repository: 'ubuntu',
            tag: '22.04',
            size: '77.8MB',
            created: '2024-03-30 15:00:00'
        },
        {
            id: 'sha256:1234567890abcdef',
            repository: 'alpine',
            tag: '42',
            size: '5.6MB',
            created: '2024-03-30 15:00:00'
        }
    ];

    private availableImages = ['ubuntu', 'debian', 'alpine', 'fedora'];

    private currentImage: string = '';

    public ps(all: boolean = false): string {
        if (all) {
            return this.formatContainers(this.containers);
        }
        return this.formatContainers(this.containers.filter(c => c.status.startsWith('Up')));
    }

    public images(): string {
        return this.formatImages(this.dockerImages);
    }

    public run(image: string): string {
        if (!this.availableImages.includes(image)) {
            return `Unable to find image '${image}' locally\nError: No such image: ${image}`;
        }

        this.currentImage = image;
        const name = this.generateName();
        
        if (this.containers.some(c => c.name === name)) {
            return `Error: container name "${name}" is already in use by container ${this.containers.find(c => c.name === name)?.id.slice(0, 12)}\n`;
        }

        const newContainer: Container = {
            id: this.generateId(),
            name: name,
            image: image,
            status: 'Up 1 minute',
            created: new Date().toISOString().slice(0, 19).replace('T', ' ')
        };

        this.containers.push(newContainer);
        return `${newContainer.id}\n`;
    }

    private formatContainers(containers: Container[]): string {
        if (containers.length === 0) {
            return 'CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS   NAMES\n';
        }

        return containers.map(c => 
            `${c.id.slice(0, 12)}   ${c.image}   "/bin/bash"   ${c.created}   ${c.status}   -   ${c.name}`
        ).join('\n') + '\n';
    }

    private formatImages(images: Image[]): string {
        if (images.length === 0) {
            return 'REPOSITORY   TAG       IMAGE ID   CREATED   SIZE\n';
        }

        return images.map(i => 
            `${i.repository}   ${i.tag}   ${i.id.slice(0, 12)}   ${i.created}   ${i.size}`
        ).join('\n') + '\n';
    }

    private generateId(): string {
        return Math.random().toString(36).substring(2, 14) + 
               Math.random().toString(36).substring(2, 14);
    }

    private generateName(): string {
        if (this.currentImage === 'alpine') {
            const existingAlpineContainers = this.containers.filter(c => c.name.startsWith('django_alpine'));
            if (existingAlpineContainers.length === 0) {
                return 'django_alpine';
            }
            return `django_alpine_${existingAlpineContainers.length + 1}`;
        }
        const adjectives = ['happy', 'clever', 'brave', 'swift', 'gentle'];
        const nouns = ['penguin', 'dolphin', 'tiger', 'eagle', 'lion'];
        const adjective = adjectives[Math.floor(Math.random() * adjectives.length)];
        const noun = nouns[Math.floor(Math.random() * nouns.length)];
        return `django_${adjective}_${noun}`;
    }
} 