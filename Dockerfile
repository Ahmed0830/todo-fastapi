FROM public.ecr.aws/lambda/python:3.12
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock* ./

RUN uv sync --frozen --no-dev

COPY main.py .

EXPOSE 8000

CMD ["main.handler"]

