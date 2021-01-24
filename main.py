import argparse
from typing import List

from processes import (
    create_thumbnails,
    AllPhotoSelector,
    ThumbnailCreator,
    FileExistenceChecker,
    IgnoreExistenceChecker,
    NullThumbnailRecorder,
)


def main(input_path: str, output_path: str, file_types: List[str], ignore_existence: bool) -> None:
    selector = AllPhotoSelector(source_directory=input_path, file_types=file_types)
    creator = ThumbnailCreator(dimensions=(250, 250), target_directory=output_path)
    if ignore_existence:
        existence_checker = IgnoreExistenceChecker()
    else:
        existence_checker = FileExistenceChecker(thumbs_directory=output_path, file_types=file_types)
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
    parser.add_argument(
        "--ignore_existence", action="store_true", help="If True, recreate thumbnail even if it already exists."
    )

    args = parser.parse_args()
    main(args.input_path, args.output_path, args.file_types, args.ignore_existence)
    return


if __name__ == "__main__":
    cli()
