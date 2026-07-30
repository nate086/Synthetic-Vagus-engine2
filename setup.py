from setuptools import setup, find_packages

setup(
    name="sve",
    version="0.1.0",
    description="Synthetic Vagus Engine for safer model steering and structural engineering guardrails.",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
        ],
    },
    python_requires=">=3.8",
)
