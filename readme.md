# Installation

docker:   27.5
npm:      9.6
GNU Make: 4.3

1) javaScript and CSS

install javaScript dependencies (min npm version === 9.6)
```bash
npm install
```

build assets
```bash
make assets
```

2) build stadnalone containers

```bash
make build-validator
```

3) setup environment

copy `.env.local` into `.env`

```bash
cp .env.local .env
```

4) run application

```bash
make dev
```


## Docker

```bash
apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt-cache policy docker-ce
apt install docker-ce
systemctl status docker
```

## Pip
```bash
sudo apt install python3-pip
```

## Npm / node / javascript
```bash
apt install node
npm install
```

## Django
```bash
python3 -m pip install Django
```

# Python
## Venv

activete python virual environment for [fish shell](https://fishshell.com/)

```bash
source ./venv/bin/activate.fish
```

# UI
## assets
### scripts

```bash
npm run built
```

### styles

```bash
make assets
```

# Database
## Access mongo

```bash
docker exec -it django-mongodb-1 mongosh
```
1. `use inpv`
2. `db.projects.find`

# Emails

[Using brevo](https://www.brevo.com/)
Emails are turned off by default. Enable them by setting up brevo and `.env`

```env
REGISTRATION=enabled
BREVO_KEY= brevo API key
BREVO_SENDER= Your email connected to brevo
```

