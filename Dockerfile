# Entorno reproducible para desarrollar el linter.
# Fija la version de LLVM: los headers internos de Clang no tienen API estable,
# asi que "compila en mi maquina" depende literalmente de este numero.
FROM ubuntu:24.04

ARG LLVM_VERSION=21

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates wget gnupg lsb-release software-properties-common \
        build-essential cmake ninja-build git python3 python3-pip \
        libgtest-dev \
    && wget -qO /tmp/llvm.sh https://apt.llvm.org/llvm.sh \
    && chmod +x /tmp/llvm.sh \
    && /tmp/llvm.sh ${LLVM_VERSION} \
    && apt-get install -y --no-install-recommends \
        llvm-${LLVM_VERSION}-dev \
        libclang-${LLVM_VERSION}-dev \
        clang-${LLVM_VERSION} \
        clang-tidy-${LLVM_VERSION} \
        clang-tools-${LLVM_VERSION} \
        llvm-${LLVM_VERSION}-tools \
    && rm -rf /var/lib/apt/lists/* /tmp/llvm.sh \
    && pip3 install --break-system-packages lit==18.1.8

# Calidad: formato del plugin y tipos del arnés (capa aparte para no reinstalar LLVM).
RUN apt-get update && apt-get install -y --no-install-recommends clang-format-${LLVM_VERSION} \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --break-system-packages mypy==1.11.2

# clang-tools trae clang-query y scan-build; clang-tidy trae el binario homonimo.
ENV PATH="/usr/lib/llvm-${LLVM_VERSION}/bin:${PATH}"
ENV CMAKE_PREFIX_PATH="/usr/lib/llvm-${LLVM_VERSION}/lib/cmake"
ENV CC=clang
ENV CXX=clang++

WORKDIR /work
