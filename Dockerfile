# Entorno reproducible para desarrollar el linter.
# Fija la version de LLVM: los headers internos de Clang no tienen API estable,
# asi que "compila en mi maquina" depende literalmente de este numero.
FROM ubuntu:24.04

ARG LLVM_VERSION=21

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates wget gnupg lsb-release software-properties-common \
        build-essential cmake ninja-build git python3 \
    && wget -qO /tmp/llvm.sh https://apt.llvm.org/llvm.sh \
    && chmod +x /tmp/llvm.sh \
    && /tmp/llvm.sh ${LLVM_VERSION} \
    && apt-get install -y --no-install-recommends \
        llvm-${LLVM_VERSION}-dev \
        libclang-${LLVM_VERSION}-dev \
        clang-${LLVM_VERSION} \
        clang-tidy-${LLVM_VERSION} \
        clang-tools-${LLVM_VERSION} \
    && rm -rf /var/lib/apt/lists/* /tmp/llvm.sh

# clang-tools trae clang-query y scan-build; clang-tidy trae el binario homonimo.
ENV PATH="/usr/lib/llvm-${LLVM_VERSION}/bin:${PATH}"
ENV CMAKE_PREFIX_PATH="/usr/lib/llvm-${LLVM_VERSION}/lib/cmake"
ENV CC=clang
ENV CXX=clang++

WORKDIR /work
