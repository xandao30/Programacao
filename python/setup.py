from cx_Freeze import setup, Executable

# Configuração do executável
executables = [
    Executable(
        script="autoImport.py",  # Nome do seu script
        base="Win32GUI"  # Para Tkinter (sem console visível no Windows)
    )
]

# Lista de pacotes usados no seu código
packages = ["mysql.connector", "tkinter", "pandas", "openpyxl", "os"]

# Configuração do projeto
setup(
    name="PublicadorJoomla",
    version="1.0",
    description="Publicador de Artigos para Joomla 3",
    options={
        "build_exe": {
            "packages": packages,  # Inclui explicitamente os pacotes
            "include_files": [],  # Arquivos extras, se necessário (ex.: ícones)
        }
    },
    executables=executables
)