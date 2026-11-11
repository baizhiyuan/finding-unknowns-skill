from pathlib import Path


def test_readme_exists():
    text = Path(__file__).with_name("README.md").read_text()
    assert text.startswith("# Tiny Notes\n")
