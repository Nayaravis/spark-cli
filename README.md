# Spark - Idea Capture Tool

A lightweight command-line tool for developers to quickly capture and organize coding ideas without leaving the terminal.

## Features

- Quick idea capture with simple commands
- Project-based organization
- Collection grouping for related ideas
- Search and filtering capabilities
- SQLite database storage

## Installation

1. Clone the repository:
```
git clone <your-repo-url>
cd python lib/cli.py
```

2. Install dependencies:
```
pipenv install && pipenv shell
```

## Quick Start

1. Initialize a new project:
```
python lib/cli.py init
```

2. Add your first idea:
```
python lib/cli.py add "What if we used microservices for auth?"
```

3. View your ideas:
```
python lib/cli.py list
```

## Usage

```
# Initialize project
python lib/cli.py init

# Add ideas
python lib/cli.py add "Your idea here"
python lib/cli.py add --collection "architecture" "Specific idea"

# List ideas
python lib/cli.py list
python lib/cli.py list --collection "bugs"
python lib/cli.py list --today

# Manage collections
python lib/cli.py collections
python lib/cli.py collections create "performance-ideas"
python lib/cli.py collections add 5 "performance-ideas"

# Search and manage
python lib/cli.py search "authentication"
python lib/cli.py show 12
python lib/cli.py edit 8
python lib/cli.py delete 3
```

## Configuration

Each project has a `.spark` file containing project name and default collection. Created automatically with `python lib/cli.py init`.

## Development

Create virtual environment:
```
python -m venv .venv or pipenv install
source .venv/bin/activate or pipenv shell
````
## License

MIT License