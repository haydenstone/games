FROM node:22-alpine
WORKDIR /app
COPY package.json ./
COPY src ./src
COPY tests ./tests
COPY world ./world
COPY R5_GUIDING_LIGHT.docx ./R5_GUIDING_LIGHT.docx
RUN mkdir -p /app/data /run/r5
ENV PORT=8765 DATA_DIR=/app/data CODEX_PATH=/codex/codex.json R5_PROVISION_FILE=/run/r5/developer-otp
EXPOSE 8765
CMD ["node","src/server.mjs"]
