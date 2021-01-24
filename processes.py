from abc import ABC, abstractmethod
from typing import List, Tuple
import os
import glob

from PIL import Image


class PhotoSelector(ABC):
    @abstractmethod
    def select(self) -> List[str]:
        """Return list of full filenames of photos."""


class AllPhotoSelector(PhotoSelector):
    def __init__(self, source_directory: str, file_types: List[str]) -> None:
        self._folder = source_directory
        self._file_types = file_types
        return

    def select(self) -> List[str]:
        filenames = [os.path.join(self._folder, x) for x in os.listdir(self._folder)]
        output = []
        for filename in filenames:
            for ext in self._file_types:
                if filename.lower().endswith(ext):
                    output.append(filename)
                    break
        return output


class ThumbnailCreator:
    def __init__(self, dimensions: Tuple[int, int], target_directory: str) -> None:
        self._dimensions = dimensions
        self._target = target_directory
        return

    def create(self, filename: str) -> str:
        """Create thumbnail of a given file, return full filename of created file."""
        basename = os.path.basename(filename)
        thumbfile = os.path.join(self._target, "tn_" + basename)

        image = Image.open(filename)
        try:
            image.thumbnail(self._dimensions)
        except OSError:
            return ""
        image.save(thumbfile)
        return thumbfile


class ExistenceChecker(ABC):
    @abstractmethod
    def thumbnail_exists(self, filename: str) -> bool:
        """Check if raw file has already been converted into a thumbnail and that the thumbnail exists."""


class IgnoreExistenceChecker(ExistenceChecker):
    def thumbnail_exists(self, filename: str) -> bool:
        return False


class FileExistenceChecker(ExistenceChecker):
    """Check for thumb existence by reference to filenames in thumb folders."""

    def __init__(self, thumbs_directory: str, file_types: List[str]) -> None:
        self._folder = thumbs_directory
        self._files: List[str] = []
        self._loaded = False
        self._file_types = file_types
        return

    def _load(self) -> None:
        self._files = []
        for file_type in self._file_types:
            self._files.extend(os.path.basename(x) for x in glob.glob(self._folder + f"/**/*.{file_type}", recursive=True))
        self._loaded = True
        return

    def thumbnail_exists(self, filename: str) -> bool:
        if self._loaded is False:
            self._load()
        # TODO DRY
        basename = os.path.basename(filename)
        thumbfile = "tn_" + basename

        return thumbfile in self._files


class ThumbnailRecorder(ABC):
    @abstractmethod
    def record(self, raw_filename: str, thumb_filename: str) -> None:
        """Record connection between raw file and thumb file."""


class NullThumbnailRecorder(ThumbnailRecorder):
    def record(self, raw_filename: str, thumb_filename: str) -> None:
        return


def create_thumbnails(
    selector: PhotoSelector,
    thumb_creator: ThumbnailCreator,
    existence_checker: ExistenceChecker,
    thumb_recorder: ThumbnailRecorder,
) -> None:
    print("Process: create_thumbnails")
    raw_files = selector.select()
    count = len(raw_files)
    print(f"Files to process: {count}")
    for i, raw_file in enumerate(raw_files):
        print(f"{i} {raw_file}")
        if existence_checker.thumbnail_exists(raw_file):
            print("Skipping. Thumbnail already exists.")
            continue
        thumb_file = thumb_creator.create(raw_file)
        thumb_recorder.record(raw_file, thumb_file)
    return
