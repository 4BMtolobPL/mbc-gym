# MBC Gym

...

## Preparation

### uv 설치

https://docs.astral.sh/uv/getting-started/installation/

## Installation

### 의존성 설치

```bash
uv sync --group dev
```

### 환경변수 설정

SECRET_KEY, WTF_CSRF_SECRET_KEY

## Run

```bash
uv run flask run --debug
```

## Add dependency

패키지 추가

```bash
uv add <package-name>
```

개발용 패키지 추가

```bash
uv add --group dev <package-name> 
```