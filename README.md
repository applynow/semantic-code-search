このレポジトリはhttps://github.com/sturdy-dev/semantic-code-searchを参考にしています。

# セマンティックコード検索 (Semantic Code Search)

## 概要

`sem` は、自然言語を使用して Git リポジトリを検索できるコマンドラインアプリケーションです。例えば、以下のようなクエリを実行できます：

- 「API リクエストの認証はどこで行われている？」
- 「ユーザーオブジェクトをデータベースに保存する処理」
- 「Webhook イベントの処理」
- 「キューからジョブを読み込む処理はどこ？」

これにより、検索結果としてコードスニペットとその `ファイル:行番号` が視覚的に表示されます。
大規模なコードベースの探索に役立つのはもちろん、小規模なプロジェクトでも「どこに何を書いたか忘れた！」という場合に便利です。

### 基本的な使い方:

```bash
sem '検索クエリ'
```

このコマンドを実行すると、検索クエリに最も一致するコードスニペットのリストが表示されます。
リストから選択し、Return キーを押すと、お好みのエディタで開くことができます。

### 仕組み

このツールはニューラルネットワークを使用してコードの埋め込み (embeddings) を生成し、類似性を比較することで検索を行います。詳しくは 仕組み を参照してください。

    NB: すべての処理はローカル環境で行われ、インターネットにデータが送信されることはありません。

## インストール

semantic-code-search は pip を使用してインストールできます。

### Pip (MacOS, Linux, Windows)

```bash
pip3 install semantic-code-search
```

## 使い方

TL;DR (手っ取り早く使いたい場合)

```bash
cd /my/repo
sem '検索クエリ'
```

オプション一覧は sem --help で確認できます。

### コードの検索

リポジトリ内で次のように実行します：

```bash
sem '検索クエリ'
```

(クエリの引用符は省略可能)

> 注意: 必ず Git リポジトリのルートディレクトリで実行するか、-p オプションでリポジトリのパスを指定してください。

初回検索時の処理

初めて検索を実行する際は、以下の2つの処理が必要です：

- モデル (~500MB) のダウンロード (一度だけ)
- コードの埋め込み (embeddings) の生成
  → これは .embeddings ファイルとしてリポジトリのルートにキャッシュされ、次回以降の検索時に再利用されます。

プロジェクトのサイズによって、これらの処理には数秒〜数分かかることがあります。ただし、一度完了すれば、検索は非常に高速になります。

検索結果の例

```bash
foo@bar:~$ cd /my/repo
foo@bar:~$ sem 'コマンドライン引数の解析'
Embeddings not found in /Users/kiril/src/semantic-code-search. Generating embeddings now.
Embedding 15 functions in 1 batches. This is done once and cached in .embeddings
Batches: 100%|█████████████████████████████████████████████████████████| 1/1 [00:07<00:00,  7.05s/it]
```

### 検索結果のナビゲーション

検索結果はデフォルトで上位5件が表示され、以下の情報が含まれます：

- 類似度スコア
- ファイルパス
- 行番号
- コードスニペット

リストの移動には ↑ ↓ の矢印キーや vim 風のキーバインドが使用できます。
Return を押すと、該当のコードがエディタで開きます。

> NB: 使用するエディタは --editor オプションで指定可能です。

### コマンドラインオプション

```bash
usage: sem [-h] [-p PATH] [-m MODEL] [-d] [-b BS] [-x EXT] [-n N]
           [-e {vscode,vim}] [-c] [--cluster-max-distance THRESHOLD]
           [--cluster-min-lines SIZE] [--cluster-min-cluster-size SIZE]
           [--cluster-ignore-identical]
           ...

自然言語でコードベースを検索

位置引数:
  query_text           検索クエリ (自然言語で記述)

オプション:
  -h, --help           ヘルプを表示
  -p PATH, --path-to-repo PATH
                       検索対象の Git リポジトリのパスを指定
  -m MODEL, --model-name-or-path MODEL
                       使用するモデルの名前またはパス
  -d, --embed          コードベースの埋め込みを (再) 作成
  -b BS, --batch-size BS
                       埋め込み生成のバッチサイズ
  -x EXT, --file-extension EXT
                       ファイル拡張子でフィルタリング (例: "py" は Python ファイルのみ)
  -n N, --n-results N  表示する検索結果の数
  -e {vscode,vim}, --editor {vscode,vim}
                       検索結果を開くエディタ
  -c, --cluster        セマンティックに類似したコードをクラスタリング
  --cluster-max-distance THRESHOLD
                       クラスタリングの閾値 (0 は完全一致、小さいほど厳しくなる)
  --cluster-min-lines SIZE
                       指定した行数より小さいコードスニペットは無視
  --cluster-min-cluster-size SIZE
                       指定したサイズ未満のクラスターを無視
  --cluster-ignore-identical
                       完全に同じコード (距離0) を無視

```

### 仕組み

このアプリケーションは、トランスフォーマー モデルを使用して、コード内のメソッドや関数の埋め込みを生成します。
埋め込みとは、テキストやコードの意味を数値ベクトルとして表現したものです。

以下の記事で概念が分かりやすく説明されています：

> Illustrated Word2Vec - Jay Alammar [https://jalammar.github.io/illustrated-word2vec/](https://jalammar.github.io/illustrated-word2vec/)

### モデル

このツールは、sentence transformer モデルを使用してコードとクエリの埋め込みを作成します。
具体的には、以下のモデルを利用しています：
	•	krlvi/sentence-t5-base-nlpl-code_search_net
	•	ベースモデル: SentenceT5-Base (110M パラメータ)
	•	追加訓練データセット: code_search_net
	•	学習損失関数: MultipleNegativesRanking

--model オプションを使用すれば、他の sentence transformer モデルも試せます。

### バグと制限

    •	.embeddings はリポジトリの変更を自動更新しない (手動で sem --embed を実行する必要あり)
	•	対応言語: { 'python', 'javascript', 'typescript', 'ruby', 'go', 'rust', 'java', 'c', 'c++', 'kotlin' }
	•	対応エディタ: { 'vscode', 'vim' }
