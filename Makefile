.PHONY: install test lint format clean build upload docs

# 安装依赖
install:
	pip install -e ".[dev,all]"

# 运行测试
test:
	pytest tests/ -v --cov=devmind --cov-report=term-missing

# 运行测试并生成HTML报告
test-html:
	pytest tests/ -v --cov=devmind --cov-report=html

# 代码检查
lint:
	flake8 devmind tests
	mypy devmind

# 代码格式化
format:
	black devmind tests

# 清理构建产物
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# 构建包
build: clean
	python -m build

# 上传到PyPI (需要配置)
upload: build
	python -m twine upload dist/*

# 生成文档
docs:
	python -m devmind.cli doc devmind/ --output docs/

# 安装预提交钩子
pre-commit:
	pre-commit install

# 运行所有检查
check: format lint test

# 帮助信息
help:
	@echo "Available targets:"
	@echo "  install     - Install package with dev dependencies"
	@echo "  test        - Run tests with coverage"
	@echo "  test-html   - Run tests and generate HTML coverage report"
	@echo "  lint        - Run flake8 and mypy"
	@echo "  format      - Format code with black"
	@echo "  clean       - Clean build artifacts"
	@echo "  build       - Build distribution packages"
	@echo "  upload      - Upload to PyPI"
	@echo "  docs        - Generate documentation"
	@echo "  check       - Run format, lint, and test"
