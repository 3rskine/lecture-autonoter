# Stage 1: downloader - 下載靜態編譯的 ffmpeg
FROM alpine:latest AS downloader
RUN apk add --no-cache curl tar xz
WORKDIR /tmp
RUN curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -o ffmpeg.tar.xz \
     && tar -xf ffmpeg.tar.xz \
     && mv ffmpeg-*-amd64-static/ffmpeg ffmpeg_static \
     && mv ffmpeg-*-amd64-static/ffprobe ffprobe_static \
     && rm -rf ffmpeg-*-amd64-static ffmpeg.tar.xz

# Stage 2: final - 基於官方 n8n 映像
FROM docker.n8n.io/n8nio/n8n:latest
USER root
COPY --from=downloader /tmp/ffmpeg_static /usr/local/bin/ffmpeg
COPY --from=downloader /tmp/ffprobe_static /usr/local/bin/ffprobe
RUN chmod +x /usr/local/bin/ffmpeg /usr/local/bin/ffprobe

USER node
