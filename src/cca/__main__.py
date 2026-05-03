"""Entry point for `python -m cca`.

Erlaubt CLI-Aufruf via `python -m cca <command>` als Alternative zum
`cca`-Script-Entry-Point.
"""

from cca.cli import main

if __name__ == "__main__":
    main()
