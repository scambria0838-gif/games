#!/usr/bin/env bash
set -e
for z in prompttogame-FINAL.zip prompttogame-deploy.zip ue5pilot-v2.0-with-premium.zip ue5pilot-v1.0.zip prompttogame-deploy-FINAL.zip; do
  echo "===== $z ====="
  unzip -l "$z" | awk 'NR>3 {print $4}' | sed '/^$/d' | head -25
  echo "-- counts --"
  echo -n "files: "; unzip -l "$z" | awk 'NR>3 && $4 !~ /\/$/ && $4 != "" {c++} END{print c+0}'
  echo -n "py: "; unzip -l "$z" | awk 'NR>3 && $4 ~ /\.py$/ {c++} END{print c+0}'
  echo -n "html: "; unzip -l "$z" | awk 'NR>3 && $4 ~ /\.html$/ {c++} END{print c+0}'
  echo -n "css: "; unzip -l "$z" | awk 'NR>3 && $4 ~ /\.css$/ {c++} END{print c+0}'
  echo -n "js: "; unzip -l "$z" | awk 'NR>3 && $4 ~ /\.js$/ {c++} END{print c+0}'
  echo
 done
