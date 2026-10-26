
def initialise_middleware(app):
    """
    Initialise the middleware for the application.

    Args:
        app: The Flask application instance.
    """
    from .logger import log_requests 

    # Register the middleware functions
    app.middleware("http")(log_requests)