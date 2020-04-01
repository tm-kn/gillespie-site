## Requirements

- Python 3.6+
- Node.js 12 (you can use [nvm](https://github.com/nvm-sh/nvm) - `nvm install 12`, `nvm use 12`)

## Installation

Create virtual environment.

```sh
python3 -m venv venv
```

Activate virtual environment.

```sh
. venv/bin/activate
```

Install requirements within virtual environment.

```sh
pip install -r requirements.txt
```

Install front-end dependencies.

```sh
npm install
```

Compile static files.

```sh
npm run build
```

## Running dev server

Activate virtual environment

```sh
. venv/bin/activate
```

Start the server.

```sh
FLASK_ENV=development flask run
```

## Running front-end watcher

If you want to make change static files (e.g. JavaScript), please run a build
watcher that will re-build static assets on a file change.

```sh
npm start
```
