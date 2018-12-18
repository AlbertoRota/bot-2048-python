profile-snakeviz:
    python -m cProfile -o output.pstats bot/main.py
    snakeviz output.pstats

profile-qcachegrind:
    python -m cProfile -o output.pstats bot/main.py
    pyprof2calltree -i output.pstats -o callgrind.output