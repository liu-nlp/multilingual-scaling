# Multilingual Scaling

This repository contains and links to resources used in our paper "Grow Up and Merge: Scaling Strategies for Efficient Language Adaptation" ([citation](#citation)), such as model checkpoints, data, and configuration files for reproducing our work.

<h4 align="center">
    <p>
        <a href="#checkpoints">Checkpoints</a> •
        <a href="#petraining">Pretraining</a> •
        <a href="#merging">Merging</a> •
        <a href="#evaluation-datasets">Evaluation Datasets</a>
    <p>
</h4>

## Checkpoints

All checkpoints trained for our experiments can be found in the [Grow Up and Merge collection](https://huggingface.co/collections/liu-nlp/grow-up-and-merge) on the Hugging Face Hub.

## Pretraining

Our (continued) pre-training experiments were performed using our modified version of the [Nanotron framework](https://github.com/liu-nlp/nanotron). The configuration files can be found in the [`training_configs`](/training_configs) directory.

### Training Data
We used fineweb-edu-dedup and python-edu from the [SmolLM-Corpus](https://huggingface.co/datasets/HuggingFaceTB/smollm-corpus) as English and Code data. The English data was split into subsets of 80% and 20% using [train_test_split()](https://huggingface.co/docs/datasets/v4.4.1/en/package_reference/main_classes#datasets.Dataset.train_test_split) from the datasets library.

The UUIDs for the two English splits are available [here](https://huggingface.co/datasets/liu-nlp/fineweb-data-80-20-split-indices).

We used [FineWeb2](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) for target-language data and shuffled the data for Estonian, Faroese, Icelandic and Persian using [shuffle()](https://huggingface.co/docs/datasets/v4.4.1/en/package_reference/main_classes#datasets.Dataset.shuffle) from the datasets library.

As replay data for Swedish (the target language with the largest amount of available data), we randomly sampled 1% of the 80% English split and 5% of the Code data. Replay data for the other target languages was sampled from the replay data used for Swedish (English and Code sampled separately), scaled down linearly depending on the amount of training documents for each target language. For Persian we thus sampled 99%, for Estonian 17%, for Icelandic 5% and for Faroese 1% of the replay data used for Swedish. All sampling was done using [train_test_split()](https://huggingface.co/docs/datasets/v4.4.1/en/package_reference/main_classes#datasets.Dataset.train_test_split) from the datasets library.

We used the [preprocessing script from Nanotron](https://github.com/liu-nlp/nanotron/blob/main/tools/preprocess_data.py) to convert the pre-training data to Nanoset format for training.

We computed the amount of training data for each language using our implementation of [UniMax sampling](https://arxiv.org/abs/2304.09151) which can be found [here](https://github.com/kgnlp/unimax). Based on that, we set the UniMax character budget to 617.5 billion and the maximum number of epochs to 6. We continue pretraining our models for 1 epoch on Swedish and Persian, 6 epochs on Faroese and Icelandic, and approximately 4.45 epochs on Estonian. The same amount of data is also used for pre-training the multilingual models.

## Merging

Our merging experiments were performed using [mergekit](https://github.com/arcee-ai/mergekit). All merges can be reproduced using the merge configuration files in the [`mergekit_configs`](/mergekit_configs) directory.

## Evaluation Datasets

The BLiMP evaluation dataset is available at  [liu-nlp/blimp-single-error](https://huggingface.co/datasets/liu-nlp/blimp-single-error), and the minimal-pair–style mParaRel dataset is available at [liu-nlp/minimal_pair_mpararel](https://huggingface.co/datasets/liu-nlp/minimal_pair_mpararel).

# Citation

```bibtex
  @misc{glocker2025growmergescalingstrategies,
        title={Grow Up and Merge: Scaling Strategies for Efficient Language Adaptation}, 
        author={Kevin Glocker and Kätriin Kukk and Romina Oji and Marcel Bollmann and Marco Kuhlmann and Jenny Kunz},
        year={2025},
        eprint={2512.10772},
        archivePrefix={arXiv},
        primaryClass={cs.CL},
        url={https://arxiv.org/abs/2512.10772}, 
  }
```
