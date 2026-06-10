# pip install cx_freeze
from cx_Freeze import setup, Executable

executaveis = [
    Executable(
        script="main.py",
        target_name="Batman_vs_Coringa.exe"
    )
]

setup(
    name="Batman vs Coringa",
    version="1.0",
    description="Jogo Batman vs Coringa",
    options={
        "build_exe": {
            "packages": ["pygame"],
            "include_files": ["bases", "recursos"]
        }
    },
    executables=executaveis
)
# python setup.py build
# python setup.py bdist_msi