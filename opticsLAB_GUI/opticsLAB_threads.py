"""
OpticsLAB Execution Helper module.
All background threading concepts have been completely removed from the application.
Functions run directly and synchronously in the main window thread.
"""

# Synchronous helper that replaces legacy background worker threads
def run_async(target, args=(), kwargs=None, on_success=None, on_error=None):
    args = args or ()
    kwargs = kwargs or {}
    try:
        result = target(*args, **kwargs)
        if on_success:
            on_success(result)
        return result
    except Exception as exc:
        if on_error:
            on_error(exc)
        else:
            print(f"[Execution Error]: {exc}")
        return None
