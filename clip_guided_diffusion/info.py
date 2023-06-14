"""Displays information about an image generated by CLIP Guided Diffusion."""

import argparse
import json
from pathlib import Path
import shlex
import sys

from PIL import ExifTags, Image


def command_for_saved_args(args):
    args = dict(args)
    ss = []
    ss.append("clip_guided_diffusion")
    ss.append(args.pop("prompt"))
    for k, v in args.items():
        if v is not None:
            if isinstance(v, bool) and not v:
                continue
            if k in {"compile", "device", "output", "save_all"}:
                continue
            if k == "model_type" and v == "eps":
                continue
            ss.append("--" + k.translate(str.maketrans("_", "-")))
            if isinstance(v, list):
                ss.extend(map(str, v))
            elif isinstance(v, bool):
                pass
            else:
                ss.append(str(v))
    return shlex.join(ss)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("image", type=Path, help="the image to display information about")
    args = p.parse_args()

    image = Image.open(args.image)
    exif = image.getexif()

    software = exif.get(ExifTags.Base.Software, "")
    if not software.startswith("CLIP Guided Diffusion"):
        print(f"Image {args.image} was not generated by CLIP Guided Diffusion.")
        sys.exit(1)

    prompt = exif.get(ExifTags.Base.ImageDescription, "")
    maker_note = json.loads(exif.get(ExifTags.Base.MakerNote, "{}"))

    print("Prompt:", prompt)
    print("Command:", command_for_saved_args(maker_note["args"]))


if __name__ == "__main__":
    main()
