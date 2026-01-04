# Console Commands

## Git

- `git config --list`
- `git pull origin BRANCH_NAME --rebase`
- `git pull --no-rebase`
- `git checkout ANOTHER_BRANCH_NAME`
- `git commit -m "COMMIT_MESSAGE"`
- `git rebase -i HEAD~10`
- `git push --force`
- `git reset HEAD^`
- `git reset --hard origin/BRANCH_NAME`
- `git tag`

## NPM - NVM

- `node -v`, `node --version`, `npm version`
- `npm cache clean --force`
- `npm outdated`
- `npm update`
- `npm i --legacy-peer-deps`
- `npm list --all`
- `npm list --depth 1`
- `npm list --parseable`
- `npm list --json`
- `npm list -g`
- `npm install npm@latest -g`
- `npm audit fix --force`
- `npm install -g npm-check-updates`, `ncu -u`, `npm install`
- `nvm list`
- `nvm install 6.9.2`
- `nvm use 6.9.1`

## Angular

- `ng g c home --standalone`
- `ng add @angular-eslint/schematics`
- `ng update @angular-eslint/schematics`

## Docker

- `docker container ls`
- `docker container rm <container_id>`
- `docker container stop <container_id>`
- `docker container run --rm -it -p 8080:80 nginx`
- `docker compose up`
- `docker compose down`
- `docker compose ps`
- `docker compose logs [service_name]`
- `docker compose logs --tail=5`
- `docker compose logs --follow`
- `docker system prune`
- `docker system prune --volumes`
- `docker image inspect nginx | jq -C '.[].Config'`
- `docker network ls`
- `docker volume ls`
- `docker volume rm <name>`

## Firebase

- `firebase login`
- `firebase init (hosting)`
- `firebase deploy`
