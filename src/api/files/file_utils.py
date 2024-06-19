from src.exceptions.invariant_error import InvariantError

class FileUtils:
  def __init__(self) -> None:
    pass

  @staticmethod
  def validate_filename(filename: str):
    if "preprocessing-" in filename:
      raise InvariantError("filename contains 'preprocessing-'").throw()
    if ".pdf" not in filename:
      raise InvariantError("file format must be .pdf").throw()