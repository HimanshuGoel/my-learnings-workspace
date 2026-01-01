# Console Commands

Essential console commands for commonly used tools.

## Table of Contents

1. [Firebase](#firebase)
1. [Angular](#angular)
1. [Git](#git)
1. [Node](#node)
1. [Chrome](#chrome)
1. [Docker](#docker)

## Firebase

- `firebase login`
- `firebase init (hosting)`
- `firebase deploy`

## Angular

- `npx nx init --integrated`
- `npx nx test`
- `npx nx serve`
- `npx nx graph`
- `npx create-nx-workspace@latest`
- `ng g c home --standalone`
- `ng add @angular-eslint/schematics`
- `ng update @angular-eslint/schematics`

## Git

- `git tag`
- `git config --list`
- `git commit -m "DWB-343: Pulumi stack file"`
- `git reset HEAD^`
- `git checkout another_branch`
- `git config core.filemode false`
- `git rebase -i HEAD~10`
- `git push --force`
- `git pull --no-rebase`
- `git pull origin BRANCH_NAME --rebase`
- `git reset --hard origin/BRANCH_NAME`

## Node

- `npm cache clean --force`
- `npm outdated`
- `npm update`
- `npm i --legacy-peer-deps`
- `node -v`, `node --version`, `npm version`
- Using `nvm`:
  - Install: `nvm install 6.9.2`
  - Set default: `nvm alias default 6.9.2`
  - `nvm use 6.9.1`
  - `nvm list`
- Listing npm packages:
  - `npm list --all`
  - `npm list --depth 1`
  - `npm list --parseable`
  - `npm list --json`
  - `npm list -g`
- Install/update npm:
  - `npm install npm@latest -g`
  - `npm audit fix --force`
- Update packages with `npm-check-updates` (ncu):
  1. `npm install -g npm-check-updates`
  1. `ncu -u`
  1. `npm install`

## Chrome

- Angular DOM Debugging

  ```typescript
  const component = ng.getComponent($0);
  console.log(component);

  const component = $0;
  ng.applyChanges(component);

  const context = ng.getContext($0);
  console.log(context);

  const metadata = ng.getDirectiveMetadata($0);
  console.log(metadata);
  ```

## Docker

- Start a container with Nginx: `docker container run --rm -it -p 8080:80 nginx`
- General commands:
  - List containers: `docker container ls`
  - Remove a container: `docker container rm <container_id>`
  - Stop a container: `docker container stop <container_id>`
- Docker Compose:
  - Start: `docker compose up`
  - Stop: `docker compose down`
  - View services: `docker compose ps`
  - Logs:
    - `docker compose logs [service_name]`
    - Tail: `docker compose logs --tail=5`
    - Follow: `docker compose logs --follow`
- System cleanup:
  - Remove unused data: `docker system prune`
  - Remove volumes: `docker system prune --volumes`
- Container management:
  - Rename: `docker container commit web1 custom-nginx`
  - Inspect image: `docker image inspect nginx | jq -C '.[].Config'`
  - Copy files: `docker container cp index.html web1:/usr/share/nginx/html/index.html`
- Other:
  - View networks: `docker network ls`, `docker inspect platform_default`
  - View volumes: `docker volume ls`
  - Remove volume: `docker volume rm <name>`
  - `docker pc`
  - `docker exec -it mss-api-gateway sh` then `curl -vvv fop-authentication-ldap:2389`
