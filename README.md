[![CI Status](https://github.com/sunba23/sunba.dev/actions/workflows/build_push_deploy.yml/badge.svg)](https://github.com/sunba23/sunba.dev/actions/workflows/build_push_deploy.yml)
[![Last Commit](https://img.shields.io/github/last-commit/sunba23/sunba.dev)](https://github.com/sunba23/sunba.dev/commits/master)
[![License](https://img.shields.io/badge/License-MIT%2FX11-blue.svg)](https://github.com/sunba23/sunba.dev/blob/master/LICENSE)

# sunba.dev
A terminal-style personal website. Hosted locally!

> [!WARNING]  
> Please note:
> staging site is down because I need RAM for other hosted stuff :)

## Product
Try it out yourself!
- main site: [sunba.dev](https://sunba.dev)
- ~~staging site: [staging.sunba.dev](https://staging.sunba.dev:8443)~~

## Tech Stack
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![WebSocket](https://img.shields.io/badge/WebSocket-010101?style=for-the-badge&logo=socket.io&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-000000?style=for-the-badge&logo=ansible&logoColor=white)
![Traefik](https://img.shields.io/badge/Traefik-24A1C1?style=for-the-badge&logo=traefik&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-009639?style=for-the-badge&logo=jenkins&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![xterm.js](https://img.shields.io/badge/xterm.js-000000?style=for-the-badge&logo=terminal&logoColor=white)

## Features
Site:
- Terminal-like interface with real-time updates via WebSocket connection
- Navigation through actual directories from backend node
- Responsiveness

Backend and DevOps aspects for better developer and user experience:
- Maintainability and extendability with clear, modular and easy to understand separation between resources
- Ease of testing with local dev ~~as well as [staging site](https://staging.sunba.dev:8443)~~
- Fully automated deployments with best CI/CD practices

## Local Development

### Prerequisites
- [Docker compose](https://docs.docker.com/compose/).

### Setup
Clone the repository and run docker compose:
```bash
git clone https://github.com/sunba23/sunba.dev.git
cd sunba.dev
docker compose up -d
```
Access the development site at `http://localhost:3000`
## Deployment

The project is deployed with:
- Ansible for infrastructure setup automation
- K3s Kubernetes single-node cluster
- Traefik as the ingress controller for each environment (~~staging~~, prod)
- GitHub Actions for CI/CD, as well as optional locally hosted Jenkins.

## License
This project is licensed under the MIT/X11 License - see the [LICENSE](LICENSE) file for details.
