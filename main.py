import argparse
from typing import List

from processes import (
    create_thumbnails,
    AllPhotoSelector,
    ThumbnailCreator,
    IgnoreExistenceChecker,
    NullThumbnailRecorder,
)


def main(input_path: str, output_path: str, file_types: List[str]) -> None:
    # TODO allowed file types.
    selector = AllPhotoSelector(source_directory=input_path, file_types=file_types)
    creator = ThumbnailCreator(dimensions=(250, 250), target_directory=output_path)
    existence_checker = IgnoreExistenceChecker()
    recorder = NullThumbnailRecorder()

    create_thumbnails(selector, creator, existence_checker, recorder)
    return


def cli() -> None:
    parser = argparse.ArgumentParser()
    # Required
    parser.add_argument("input_path", type=str, help="Path containing raw photo files.")
    parser.add_argument("output_path", type=str, help="Path where thumbnails are to be stored.")
    # Optional
    parser.add_argument("-t", "--file_types", nargs="+", default=["jpg", "png"], help="Allowed file extensions.")

    args = parser.parse_args()
    main(args.input_path, args.output_path, args.file_types)
    return


if __name__ == "__main__":
    cli()
