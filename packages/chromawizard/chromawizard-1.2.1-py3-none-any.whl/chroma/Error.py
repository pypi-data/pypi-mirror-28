class ChromaError(Exception):
    """Base class for exceptions in this module."""
    pass

class WrongImageShapeError(ChromaError):
    """
    Exception raised when images with wrong shape were loaded.

    Attributes:
        shape1 -- image shape of loaded image
        shape2 -- desired image shape
    """

    def __init__(self, shape1, shape2):
        self.shape1 = shape1
        self.shape2 = shape2

    def __str__(self):
        return "Image has different aspect ratio {}. {} was used!".format(self.shape1, self.shape2)


class ImageError(ChromaError):
    """
    Exception raised when image could not loaded.
    """
    pass


class CubeLayerError(ChromaError):
    """
    Exception raised when cube is instanced by less than two channels
    """
    def __str__(self):
        return "Needs 2 channels minimum!"