FROM node:22-alpine
WORKDIR /app
COPY package.json ./
COPY src ./src
COPY world ./world
COPY tests ./tests
COPY R5_GUIDING_LIGHT.docx ./R5_GUIDING_LIGHT.docx
RUN mkdir -p /app/data
EXPOSE 8765
ENV PORT=8765 HOST=0.0.0.0 DATA_DIR=/app/data
CMD ["node","src/server.mjs"]
