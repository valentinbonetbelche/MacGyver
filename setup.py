from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "MacGyver Labyrinth",
    version = "1",
    description = "Labyrinth MacGyver",
    executables = [Executable("application.py")],
)