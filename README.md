# ftbq-sort
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)

日本語 | [English](README_EN.md)

`ftbq-sort` は、MinecraftのModパック開発などで使用される [FTB Quests](https://www.curseforge.com/minecraft/mc-mods/ftb-quests) の言語ファイル（`lang/xx_xx.json`）を、クエストの進行順やGUIの配置に合わせて自動的に美しく整列（ソート）するCLIツールです。

Minecraft v1.13-1.20のjson形式のlangファイルに対応しています。

## ✨ 特徴 (Features)

langファイルのJSONキーはバラバラになってしまいがちです。本ツールはクエストの `.snbt` ファイルを解析し、以下の賢いロジックでlangファイルを再構築します。

* **チャプターとグループの整列**: `chapter_groups.snbt` と各チャプターの `order_index` を読み取り、ゲーム内のGUI（左側のタブ）と全く同じ順番でチャプターブロックを並べます。
* **トポロジカルソート（依存関係の解決）**: クエストの前提条件（dependencies）を解析し、有向非巡回グラフ（DAG）を構築。派生クエストよりも先に前提クエストのテキストが配置されるよう、自然な進行順に並び替えます。
* **キーの論理的なソート**: 1つのクエスト内で `title` -> `subtitle` -> `description0` -> `description1` -> `その他(タスク等)` の順になるよう、人間にとって最も読みやすい優先度で配置します。
* **チャプター固有キーの分離**: チャプター自体のタイトルなどは各チャプターブロックの先頭に、完全に独立したグローバルキー（グループ名など）はファイルの末尾に配置されます。

## 🚀 インストール (Installation)

Python 3.8以上が必要です。環境を汚さない `uv` または `pipx` を使用したインストールを推奨します。

```bash
uv tool install git+https://github.com/he1se1/ftbq-sort.git
```

```bash
pipx install git+https://github.com/he1se1/ftbq-sort.git
```

## 🛠 使い方 (Usage)

インストールすると、グローバルに `ftbq-sort` コマンドが使用できるようになります。

```bash
ftbq-sort <questsディレクトリのパス> <入力langファイルのパス> <出力langファイルのパス>
```

### 引数の説明

* `quests_dir`: FTB Questsの `quests` フォルダのパスを指定します。（中に `chapter_groups.snbt` や `chapters/` フォルダが含まれている階層です）
* `lang_in`: ソートしたい元の言語ファイル（JSON）のパスを指定します。
* `lang_out`: 整列済みのデータを出力する先のファイルパスを指定します。（入力ファイルと同じパスを指定して上書きすることも可能です）

### 実行例

```bash
ftbq-sort ./config/ftbquests/quests ./kubejs/assets/kubejs/lang/ja_jp.json ./kubejs/assets/kubejs/lang/ja_jp_sorted.json
```
(あとで `ja_jp_sorted.json` を `ja_jp.json` にリネームして上書きしないとゲームに反映されないことに注意してください)

## 📝 依存ライブラリ
* [ftb-snbt-lib](https://pypi.org/project/ftb-snbt-lib/)