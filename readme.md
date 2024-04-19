## Venv

`source ./venv/bin/activate.fish`

## Access mongo

```bash
docker exec -it django-mongodb-1 mongosh
```
1. `use inpv`
2. `db.projects.find`
