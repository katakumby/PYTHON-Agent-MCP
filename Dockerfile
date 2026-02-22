# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.10-alpine AS uv
# Install local CA certificates
COPY localca.pem /usr/local/share/ca-certificates/localca.crt
RUN update-ca-certificates

# Set environment variables so Python libraries use the updated CA bundle
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV CERTINFO=/etc/ssl/certs/ca-certificates.crt

# Install the project into `/app`
WORKDIR /app

# Create a non-root user 'app'
RUN adduser -D -h /home/app -s /bin/sh app

#chown the app directory
RUN chown -R app:app /app   

USER app


# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Enable UV native TLS
ENV UV_NATIVE_TLS=true
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Generate proper TOML lockfile first
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=README.md,target=README.md \
    uv lock

# Install the project's dependencies using the lockfile
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project --no-dev --no-editable

# Then, copy the rest of the project source code and install it
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-dev --no-editable

# Remove unnecessary files from the virtual environment before copying
RUN find /app/.venv -type d -name '__pycache__' -prune -exec rm -rf {} + || true && \
    find /app/.venv -type f -name '*.pyc' -delete || true && \
    find /app/.venv -type f -name '*.pyo' -delete || true && \
    echo "Cleaned up .venv"




# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Disable Python output buffering for proper stdio communication
ENV PYTHONUNBUFFERED=1



# Default to running the 'agent' if no other arguments are provided to docker run
CMD ["uv", "run", "/app/buissnes_agent/a2a_agent/", "--host", "agent"]
