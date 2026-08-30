FROM node:22-alpine
WORKDIR /app
COPY package.json ./
COPY src ./src
COPY tests ./tests
COPY world ./world
COPY R5_GUIDING_LIGHT.docx ./R5_GUIDING_LIGHT.docx
RUN mkdir -p /app/data /codex
EXPOSE 8765
ENV PORT=8765 HOST=0.0.0.0 DATA_DIR=/app/data CODEX_PATH=/codex/codex.json
CMD ["node","src/server.mjs"]
