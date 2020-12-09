#!/usr/bin/env bash


if [[ -z "${PIP_EXTRA_INDEX_URL}" ]]; then
  EXTRA_PIP=https://pypi.org/simple
  echo 'Setting the value for build arg PIP_EXTRA_INDEX_URL as '${EXTRA_PIP}
else
  read -p "Enter username for private pypi(${PIP_EXTRA_INDEX_URL}): " PYPI_USER
  read -s -p "Enter password for private pypi(${PIP_EXTRA_INDEX_URL}): " PYPI_PASS
  EXTRA_PIP=https://${PYPI_USER}:${PYPI_PASS}@${PIP_EXTRA_INDEX_URL##*https://}
fi


docker build \
--build-arg PIP_EXTRA_INDEX_URL=${EXTRA_PIP} \
-t aganitha/aganitha-hocr -f dockerbuild/gpu/Dockerfile dockerbuild/gpu
