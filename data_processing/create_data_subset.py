#!/usr/bin/env python
import sys
from collections.abc import Sequence
from argparse import ArgumentParser
from typing import Any, Iterator

from datasets import Dataset, DatasetDict, load_dataset


def _up_to_characters(
    dataset: Dataset, maximum_characters: int
) -> Iterator[dict[str, Any]]:
    character_count = 0
    for sample in dataset.to_iterable_dataset():
        character_count += len(sample["text"])
        if character_count >= maximum_characters:
            return

        yield sample


def simple_subset(
    dataset_name: str,
    output: str,
    subset_size: int,
    subset_type: str = "documents",
    split: str = "train",
    config: str | None = None,
    num_shards: int = 16,
) -> None:
    dataset = load_dataset(dataset_name, config, split=split)
    assert isinstance(dataset, Dataset), (
        f"Single split dataset expected but got {type(dataset)}"
    )
    if subset_type == "documents":
        subset = dataset.select(range(subset_size))
    else:
        subset = Dataset.from_generator(lambda: _up_to_characters(dataset, subset_size))
        assert isinstance(subset, Dataset), (
            f"Single split dataset expected but got {type(subset)}"
        )

    DatasetDict({split: subset}).save_to_disk(output, num_shards={split: num_shards})


def main(args: Sequence[str] | None = None) -> None:
    if args is None:
        args = sys.argv[1:]

    parser = ArgumentParser()
    parser.add_argument("dataset")
    parser.add_argument("output")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--num-documents", type=int)
    group.add_argument("-c", "--num-characters", type=int)
    parser.add_argument("--split", default="train")
    parser.add_argument("--config")

    arguments = parser.parse_args(args)

    if arguments.num_documents is not None:
        subset_size = arguments.num_documents
        subset_type = "documents"
    else:
        subset_size = arguments.num_characters
        subset_type = "characters"

    simple_subset(
        arguments.dataset,
        arguments.output,
        subset_size,
        subset_type,
        arguments.split,
        arguments.config,
    )


if __name__ == "__main__":
    main()
