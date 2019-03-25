class StopPipelineError(Exception):
    """
    An expected pipeline error.
    """
    def __init__(self, message: str):
        self.message = message