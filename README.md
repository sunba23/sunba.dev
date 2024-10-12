# sunba.dev
This repository contains files for my self hosted terminal themed website.
## Description
This project is a web terminal that uses django channels on the backend for real time interaction with xterm.js on the frontend. It uses nginx as a reverse proxy. It uses Jenkins for CI. Each service is contenerized and managed with docker compose. I tried to include all the security measures i could think off: ssl encryption, rate limiting, directory traversal prevention and websocket message throttling. If you see room for improvement, please submit an issue or a PR.
## Development
1. clone the [dev](https://github.com/sunba23/sunba.dev/tree/dev) branch
```bash
git clone --single-branch --branch dev https://github.com/sunba23/sunba.dev
cd sunba.dev
```
2. create `.env` file in the project root, containing `DJANGO_KEY`
3. run the containers with `docker compose up -d`

all done! visit http://localhost:5173 in your browser.
