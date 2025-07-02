ARG NODE_VERSION=24

FROM node:${NODE_VERSION}-alpine AS builder

WORKDIR /code

COPY package*.json ./
RUN npm clean-install

COPY . ./
RUN npm run build

FROM pierrezemb/gostatic:latest AS runtime

LABEL description="Notivae - Web-UI"
LABEL website="https://notivae.github.io/"

COPY --from=builder /code/dist/ /srv/http/

HEALTHCHECK CMD wget --spider -q http://localhost:80/ || exit 1

EXPOSE 80

CMD ["-port", "80"]
