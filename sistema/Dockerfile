# Centinela C++: el servicio web sobre la imagen del checker (LLVM 21 + Clang 21.1.8).
# Se construye desde la raíz del repositorio: docker compose build sistema
FROM node:22.17.1-bookworm-slim AS node

FROM checker-base
COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s ../lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
 && ln -s ../lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx

# El plugin se compila dentro de la imagen: enlaza contra el Clang de esta misma imagen.
WORKDIR /opt/centinela
COPY norma norma
COPY plugin plugin
RUN cmake -S plugin -B /opt/plugin -G Ninja -DCMAKE_BUILD_TYPE=Release >/dev/null \
 && cmake --build /opt/plugin --target ContainerInvalidation \
 && test -f /opt/plugin/libContainerInvalidation.so

# Dependencias del monorepo (npm workspaces) y el código.
WORKDIR /opt/centinela/sistema
COPY sistema/package.json sistema/package-lock.json ./
COPY sistema/paquetes paquetes
COPY sistema/frontend/package.json frontend/package.json
RUN npm ci --no-audit --no-fund
COPY sistema/tsconfig.json sistema/vitest.config.ts ./
COPY sistema/pruebas pruebas
COPY sistema/demo demo
COPY sistema/no-funcionales no-funcionales
COPY ejemplos /opt/centinela/ejemplos

# El panel web (React): se compila aquí y Fastify lo sirve en «/».
COPY sistema/frontend frontend
RUN npm run build -w @centinela/panel

ENV CENTINELA_PLUGIN=/opt/plugin/libContainerInvalidation.so \
    CENTINELA_CLANG=clang++ \
    CENTINELA_BD=/datos/centinela.db \
    CENTINELA_FRONTEND=/opt/centinela/sistema/frontend/dist \
    NODE_ENV=production
VOLUME /datos
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD node -e "fetch('http://127.0.0.1:8080/salud').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"
CMD ["npx", "tsx", "paquetes/app/src/principal.ts"]
