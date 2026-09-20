"""blogpipe: the daily blog pipeline's deterministic side, as one typed package.

Migration in progress (epic "Unblock, slim, and re-aim the daily blog pipeline at an
outside reader", Phase 1). The historical script paths cron and the bash wrappers call
stay in place as thin shims over this package, so entry points never change.

BYTECODE: the producer contract runs INSIDE the isolated run workspace, whose write-set
is verified file by file. A `__pycache__` written there fails the run. Every entry point
must set `sys.dont_write_bytecode = True` BEFORE importing this package (the shims do),
or be started as `python3 -B -m blogpipe ...`. Setting it here would be too late: this
file's own bytecode is written before its first line runs.
"""
