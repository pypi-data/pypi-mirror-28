# simplecmd

Simple wrapper around subprocess. A single function is provided:

```python
run(*args, **kwargs)
```

Pass a command name and its arguments as `args`.

Optional `kwargs`:

- `cwd`: current working directory (string)
- `capture`: capture stdout and return it (bool)
- `capture_stderr`: redirect stderr to stdout and return it (bool)
- `env`: environment variables (dict)
