from setuptools import setup

setup(
    name="politibot",
    version="0.0.0",
    description="Tools for pulling data from multiple political and legislative APIs",
    author="Jake Kara",
    author_email="jake@jakekara.com",
    install_requires=["requests"],
    license="GPL-3",
    packages=["Politibot.ProPublica",
              "Politibot.ApiTools",
              "Politibot.Fec",
              "Politibot.ConnAssembly",
              "Politibot"]
)
