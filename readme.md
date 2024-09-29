# Installation

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
```
apt install node
npm install
```

## Django
```bash
python3 -m pip install Django
```

# Python
## Venv
`source ./venv/bin/activate.fish`

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
