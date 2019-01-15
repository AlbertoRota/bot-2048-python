from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize([
        "bot/helloworld.pyx",
        "bot/tables/move_table_c.pyx",
        "bot/tables/fitness_table_c.pyx",
        "bot/game/board_2048_c.pyx"
        ], annotate=True)
)
