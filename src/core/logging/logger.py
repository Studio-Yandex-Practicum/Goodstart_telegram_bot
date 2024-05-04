def log_errors(f):
<<<<<<< HEAD
    """Decorator to log errors raised by the decorated function."""
=======
    """Log errors decorator raised by the decorated function."""
>>>>>>> dev

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f"Произошла ошибка: {e}"
            print(error_message)
            raise e

    return inner
