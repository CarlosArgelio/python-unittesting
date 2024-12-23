# Install coverage

```py
pip install coverage
coverage run -m unittest discover tests
coverage run --source src -m unittest # con esto decimos donde esta la fuente del codigo
coverage report

coverage html
```

version con pytest https://github.com/JimcostDev/unit-testing
documentacion https://docs.pytest.org/en/latest/