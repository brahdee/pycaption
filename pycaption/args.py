import argparse


def _parse_args():
    parser = argparse.ArgumentParser("pycaption")
    parser.add_argument(
        "-i",
        "--input",
        help="the filepath of the gif to edit",
        type=str,
        default=None,
        required=True,
    )
    parser.add_argument(
        "-u",
        "--uncaption",
        help="remove the caption from a gif instead of captioning",
        action=argparse.BooleanOptionalAction,
        type=bool,
        default=False,
        required=False,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="what the name of the final gif should be",
        type=str,
        default=None,
        required=False,
    )
    parser.add_argument(
        "-c",
        "--caption",
        help="what the text should say (if captioning)",
        type=str,
        default=[],
        required=False,
        nargs="*",
    )
    args = parser.parse_args()

    if args.caption == []:
        args.caption = None
    else:
        args.caption = " ".join(args.caption)

    return args.uncaption, args.input, args.caption, args.output
