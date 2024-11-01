FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --only main ; fi"

ENV PYTHONPATH=/app

#COPY ./scripts/ /app/

COPY ./alembic.ini /app/

COPY ./prestart.sh /app/

COPY ./tests-start.sh /app/

COPY ./app /app/app


# additional description

    # curl -sSL https://install.python-poetry.org：

        # curl 是一个命令行工具，用于从 URL 下载内容。
        # -sSL 是 curl 的选项：
        # -s（silent）：安静模式，不显示进度条。
        # -S（show errors）：在出错时显示错误信息。
        # -L（location）：如果服务器返回重定向信息，自动跟随重定向。
        # 这个命令的作用是下载 Poetry 的安装脚本。

    # | POETRY_HOME=/opt/poetry python：

        # 管道符号 | 表示将前一个命令的输出作为下一个命令的输入。
        # POETRY_HOME=/opt/poetry 设置环境变量 POETRY_HOME，指定 Poetry 的安装目录为 /opt/poetry。
        # python 表示使用 Python 解释器来运行下载的安装脚本。
        # 这一步的作用是将 Poetry 安装到 /opt/poetry 目录下。


    #cd /usr/local/bin：

        # 切换到 /usr/local/bin 目录(容器内)。这个目录通常包含全局可执行文件，是系统 PATH 环境变量的一部分，确保这些命令可以从任何地方运行。

    # ln -s /opt/poetry/bin/poetry：
        
        # ln 是创建链接的命令。
        # -s（symbolic）：创建符号链接（软链接）。
        # /opt/poetry/bin/poetry：链接的目标，即刚刚安装的 Poetry 可执行文件的位置。
        #这一步的作用是创建一个全局符号链接，使得可以通过在终端中直接输入 poetry 来运行 Poetry，而不需要指定完整路径。

    
    #poetry config virtualenvs.create false：

        # 这是一个配置命令，用于设置 Poetry 的选项。
        # virtualenvs.create false：设置为 false，表示 Poetry 在安装依赖时不创建虚拟环境。
        # 由于 Docker 容器本身就是一个隔离的环境，通常不需要再创建虚拟环境。
        # 这一步的作用是告诉 Poetry 在当前容器环境中直接安装依赖，而不需要使用单独的虚拟环境。