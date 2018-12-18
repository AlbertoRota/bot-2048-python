profile-snakeviz:
    python -m cProfile -o output.pstats bot/main.py
    snakeviz output.pstats

profile-qcachegrind:
    python -m cProfile -o bot-2048-python.cprof bot/main.py
    pyprof2calltree -i bot-2048-python.cprof -o callgrind.bot-2048-python