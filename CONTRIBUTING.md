# Contributing to Slack File Downloader

Thank you for considering contributing to this project! Your help is appreciated and welcome.

## 🛠️ Getting Started

1. **Fork** the repository.
2. **Clone** your fork:  

    ```bash
    git clone https://github.com/your-username/slack-file-downloader.git
    cd slack-file-downloader
    ```

3. Create a virtual environment and install dependencies:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -e .[dev]
    ```

## 💡 Ways to Contribute

- Fix bugs or report them via GitHub Issues
- Add tests or improve test coverage
- Improve documentation or examples
- Refactor for better readability or performance

## 🔧 Running Tests

We use unittest and pytest:

```bash
python -m unittest discover
```

## ✅ Code Style

- Format code with black
- Check types with mypy
- Run flake8 for linting (optional)

```bash
black slackFiles tests
mypy slackFiles
```

## 🚀 Making a Pull Request

1. Create a new branch from main:

    ```bash
    git checkout -b feature/my-feature
    ```

2. Make your changes.
3. Commit with a meaningful message:

    ```bash
    git commit -m "Add feature X"
    ```

4. Push and open a pull request:

    ```bash
    git push origin feature/my-feature
    ```

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.
