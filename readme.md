## Venv

`source ./venv/bin/activate.fish`

## UI - assets

```bash
npm run built
make assets
```

## Access mongo

```bash
docker exec -it django-mongodb-1 mongosh
```
1. `use inpv`
2. `db.projects.find`
