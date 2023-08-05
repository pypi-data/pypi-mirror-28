[![Waffle.io - Columns and their card count](https://badge.waffle.io/setminami/Jsonica.png?columns=all)](https://waffle.io/setminami/Jsonica?utm_source=badge)

# Jsonica
[en](./README.md)

# なにができるか？

# 利用とセットアップ
[Usage Sample](./Usage_Samples.md)

## やりたいこととなにがうれしいか
  - テストや設定データの中で興味があるところのみにこだわり、平易に管理したい
    - 雑音を排除し、必要条件を満たすことに集中できる
  - Excelなど抽象表現からJSON, Yaml, md...etcの具象表現を振り分け自動生成したい
    - データに人為的な偏りを与えたり、人工的な仮説に即したデータ作成が簡単にできるようなツールから逆算的にデータ作成がしたい
      - Excel自身巨大なデータをサマったり、統計的なデータ作成に向いている
    - 抽象表現を建てることにより、∃具象表現のみを必要とするだけで他は必要になるまで出力の必要がなくなる
    - 抽象的に興味の対象を記述することで、未認知含め∀具象表現はそれぞれの下層レイヤでの限定都合で整形することに集中できる
  - 小粒度ファイルを多人数にmap, reduceして作業の集中と並列化を図る
    - 例えば、初期化したexcelからsheetをばらして配って各自入力、回収時finalizeすると巨大なJSONファイルが出力されるとか。
    - 詳細仕様は一部の人間だけが握って正確に記述することで、各自は担当する部位だけ知っていればすむような、知識の分散管理を図りたい

see also. [Appendix. mindmap](./Appendixies.md)

## excel構築と編集
  - 1階層1sheetとして管理すること
  - root itemを示すsheetは`root`をシート名とすること
    - `-r sheet名`で指定、`-r`がない場合のみxlsxは`root`という名前のsheetを持たなければならない
  - カラムはキーとして解釈されること
    - 各カラムには、該当itemについてのjsonschemaを**コメントで**書き入れる
    - コミュニケーションのため、コメント各行頭に`#`を付けることでjsonschema以外のコメント行とし、この行はJSON生成時解釈しないものとする
    - xlsx初期化コマンドで、yamlからjsonschemaの設定内容が読み込まれ、上述コメントが埋め込まれたテンプレートファイルを生成する
  - 1階層下にitemを持たせる場合は別sheetとし、item名カラムにsheetへのハイパーリンクを張ること
    - schemaで'type':'array'の場合はsheet内全てのitem配列、'object'の場合はsheet**最後のrow**をobjectとして追加される
    - 1階層下を配列にしたくない場合はカラム行とに対応するschemaに`"type":"object"`と指定する
  - cell内に文字列で`sheet://sheet名`とすることにより個別sheetを指すこと
    - Excelからいちいちメニューを選んで別シートへのハイパーリンクを張るのが思いのほかめんどくさい
    - 操作ライブラリでのhyperlink記述がExcel記入方法、OSにより揺れることがあるため、リンクする際は手動とする
    - `sheet://`以降をそのままsheet名とするため、encode上whitespaceを許す
    - typoが見つかった場合は、コマンドのエラーとして上げる see. エラー
  - Excelの仕様に振られないため、余計なマクロは極力上書きしない

## Sample Files
  - 用意するファイルと `jsonica.py gen -of csv -hr 2` 出力例
    - [xlsx & genarated json](https://github.com/setminami/Jsonica/tree/master/Samples)
  - local git環境に設定調整を強要しないxlsx git管理の模索
    - [xlsx git management (trial)](https://github.com/setminami/Jsonica/tree/master/output/cheatsheet.xlsx)
  - xlsx初期化用template yamlファイル
    - [template.yaml](https://github.com/setminami/Jsonica/blob/master/template.yaml)
  - xlsxに基づいて出力される生成json についてのjsonschema (TBD)

## [Usage Sample](./Usage_Samples.md)
## [Appendix.](./Appendixies.md)
