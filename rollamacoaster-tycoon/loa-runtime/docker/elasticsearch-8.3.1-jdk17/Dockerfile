FROM eclipse-temurin:17-jre-jammy AS modern_jre

FROM docker.elastic.co/elasticsearch/elasticsearch:8.3.1

USER root

# Replace Elasticsearch 8.3.1's old bundled JVM.
RUN rm -rf /usr/share/elasticsearch/jdk

COPY --from=modern_jre /opt/java/openjdk /usr/share/elasticsearch/jdk

RUN chown -R elasticsearch:root /usr/share/elasticsearch/jdk

USER elasticsearch
