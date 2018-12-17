profile:
    python -m cProfile -o output.pstats bot/main.py
    snakeviz output.pstats