# ftbq-sort
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)

[日本語](README.md) | English

`ftbq-sort` is a CLI tool that automatically and beautifully sorts language files (`lang/xx_xx.json`) for [FTB Quests](https://www.curseforge.com/minecraft/mc-mods/ftb-quests) used in Minecraft modpack development. It aligns the keys with the quest progression and in-game GUI layout.

Supports `.json` format lang files for Minecraft v1.13-1.20.

## ✨ Features

JSON keys in lang files often become disorganized and messy during development. This tool parses the quest `.snbt` files and reconstructs the lang file using the following smart logic:

* **Chapter and Group Alignment**: Reads `chapter_groups.snbt` and the `order_index` of each chapter to arrange the chapter blocks in the exact same order as the in-game GUI (the left-hand tabs).
* **Topological Sorting (Dependency Resolution)**: Parses quest `dependencies` to build a Directed Acyclic Graph (DAG). It sorts the quests so that prerequisite quests appear before the derived quests, ensuring a natural progression flow.
* **Logical Key Sorting**: Prioritizes keys within a single quest for maximum human readability. They are ordered as follows: `title` -> `subtitle` -> `description0` -> `description1` -> `Others (tasks, etc.)`.
* **Separation of Chapter-Specific Keys**: Chapter titles are placed at the beginning of their respective chapter blocks, while completely independent global keys (such as group names) are moved to the bottom of the file.

## 🚀 Installation

Python 3.8 or higher is required. We recommend using `pipx` to keep your environment clean.

```bash
pipx install git+https://github.com/he1se1/ftbq-sort.git
```

To update the tool, run the following command:

```bash
pipx upgrade ftbq-sort
```

## 🛠 Usage

Once installed, the `ftbq-sort` command will be available globally.

```bash
ftbq-sort <path_to_quests_dir> <path_to_input_lang_file> <path_to_output_lang_file>
```

### Arguments

* `quests_dir`: Path to the FTB Quests `quests` folder (the directory containing `chapter_groups.snbt` and the `chapters/` folder).
* `lang_in`: Path to the original language file (JSON) you want to sort.
* `lang_out`: Path where the sorted data will be saved. (You can specify the same path as the input file to overwrite it directly.)

### Example

```bash
ftbq-sort ./config/ftbquests/quests ./kubejs/assets/kubejs/lang/en_us.json ./kubejs/assets/kubejs/lang/en_us_sorted.json
```
*(Note: If you output to a different file like `en_us_sorted.json`, remember to rename it back to `en_us.json` and overwrite the original file, or the changes won't reflect in the game.)*

## 📝 Dependencies
* [ftb-snbt-lib](https://pypi.org/project/ftb-snbt-lib/)