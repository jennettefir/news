import os
import json
import click
from typing import Optional
from translate_transition import ReWriter


@click.command()
@click.argument('source', type=click.Path(exists=True))
@click.argument('target', type=click.Path(exists=True), required=False)
@click.argument('sequence', type=click.Path(exists=True), required=False)
def rewrite(source, target: Optional[str] = None, sequence: Optional[str] = None):
    with open(source, 'r') as source_file:
        source_text = source_file.read().strip()
    if len(source_text) == 0:
        print("File not found or is empty")
        return
    if target is None:
        source_abspath = os.path.abspath(source)
        source_parent_dir = os.path.dirname(source_abspath)
        source_basename = os.path.basename(source_abspath)
        filename_and_ext = os.path.splitext(source_basename)
        target = os.path.join(source_parent_dir, filename_and_ext[0] + '_rewrite' + filename_and_ext[1])
    sequence_json = None
    if sequence is not None:
        with open(sequence, "r") as sequence_file:
            sequence_text = sequence_file.read().strip()
            if len(sequence_text) == 0:
                print("Sequence file has incorrect format")
            try:
                sequence_json = json.loads(sequence_text)
            except Exception as _e:
                print("Sequence file has incorrect format")
    if sequence_json is not None:
        re_writer = ReWriter(source_text, sequence_json)
    else:
        re_writer = ReWriter(source_text)
    target_text = re_writer.run()
    with open(target, "w+") as target_file:
        target_file.write(target_text)


if __name__ == "__main__":
    rewrite()
