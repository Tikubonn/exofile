
# exofile

![](https://img.shields.io/badge/version-0.9.0-gray)
![](https://img.shields.io/badge/python-3.10-blue)
![](https://img.shields.io/github/license/tikubonn/exofile)

AviUtlのエクスポートファイルを編集するための基礎的なライブラリです。
このライブラリを使用することで、エクスポートファイルの読み込み・書き出し・編集を行うことができます。
ただし、文字通り基礎的な機能しか搭載されていませんので、より直観的な操作（例えばタイムライン上のオブジェクトを操作したり）をしたいのであれば[こちらのライブラリ](https://github.com/tikubonn/exolib)の使用を検討したほうがよいでしょう。

```python
from exofile import EXOFile 

with open("example.exo", "r", encoding="cp932") as stream:
  exofile = EXOFile.load(stream)

for sectionid, section in exofile.items():
  print(sectionid)
  for key, value in section.items():
    print(key, value)
```

## Usage 

### .exoファイルを読み込む・書き出す

`EXOFile.load`クラスメソッドを使用することでファイルを読み込むことができます。
`EXOFile.dump`メソッドを使用することでファイルにインスタンスを書き出すことができます。
ファイルの読み込み・書き出しともに文字コードの指定には注意しましょう。
.exoファイルは基本的に**cp932**でエンコードされています。

```python
from exofile import EXOFile

with open("example.exo", "r", encoding="cp932") as stream:
  exofile = EXOFile.load(stream)

with open("example2.exo", "w", encoding="cp932") as stream:
  exofile.dump(stream)
```

### .exoファイルを文字列から読み込む・書き出す

exofileは文字列化されたファイルからも読み込む・書き込むことができます。
文字列化されたファイルを読み込むには`EXOFile.loads`クラスメソッドを使用します。
逆にインスタンスを文字列に書き出すには`EXOFile.dumps`メソッドを使用します。

```python
from exofile import EXOFile

with open("example.exo", "r", encoding="cp932") as stream:
  data = stream.read()

exofile = EXOFile.loads(data) #load from str.
exofile.dumps() #dump to stdout if run on REPL.
```

### .exoファイルを新規作成する

exofileは既存のファイルから読み込むだけでなく、.exoファイルを新規作成することもできます。

```python
from exofile import EXOFile

with open("example2.exo", "w", encoding="cp932") as stream:
  exofile = EXOFile()
  exofile.dump(stream)
```

### .exoファイルを編集する

exofileはセクションを編集することもできます。
下記の例ではエクスポートファイルの横幅と縦幅を変更したのち別名保存しています。

```python
from exofile import EXOFile, Int

with open("example.exo", "r", encoding="cp932") as stream:
  exofile = EXOFile.load(stream)

exofile.set("exedit", "width", Int(1280))
exofile.set("exedit", "height", Int(720))

with open("example2.exo", "w", encoding="cp932") as stream:
  exofile.dump(stream)
```

### 編集用メソッド

exofileは編集のためにこれらのメソッドを提供しています。

| メソッド | 概要 | 
| ---- | ---- | 
| `EXOFile.set(section, key, value)`        | 指定されたセクションの属性に値を設定します。既にその属性に値が設定されていた場合、そのまま新しい値で上書きします。 | 
| `EXOFile.get(section, key, default=None)` | 指定されたセクションの属性値を取得します。その属性に値が設定されていなければ、第三引数の値が返されます。 | 
| `EXOFile.remove(section, key)`            | 指定されたセクションの属性を削除します。削除される属性がそのセクション最後の属性であれば、該当するセクションもついでに削除されます。 | 
| `EXOFile.contains(section, key)`          | 指定されたセクションの属性が存在するかを判定します。 | 

### データの直列化

exofileはエクスポートファイルのデータをより直観的に扱えるように、専用のデータ型を提供しています。
これらのデータ型は`.deserialize`クラスメソッドを使用することで、エクスポートファイルに含まれる生のテキストデータから普遍的なデータに変換することができます。
その逆もまた然り、これらのデータ型のインスタンスは`.serialize`メソッドを使用することで、普遍的なデータからエクスポートファイル向けのテキストデータに変換することもできます。

```python
from exofile import Color, Params

color = Color.deserialize("ffffff")
color.red #255 
color.green #255 
color.blue #255 
color.blue = 0
color.serialize() #ffff00

params = Params.deserialize("one=1;two=2;three=3;")
params["one"] #1
params["two"] #2
params["three"] #3
params["four"] = 4
params.serialize() #one=1;two=2;three=3;four=4;
```

### 直列化専用データ型

exofileは直列化のためにこれらのデータ型を提供しています。

| データ型 | 概要 |
| ---- | ---- | 
| `Int`    | 一般的な符号付整数です。 | 
| `Float`  | 一般的な浮動小数点数ですが、任意の引数`decimalpartdigits`を受け取ります。これは`.serialize`されたときの小数部の長さに影響をあたえます。 | 
| `String` | 一般的な文字列です。 | 
| `Text`   | 一般的な文字列と同じ振る舞いをしますが、`.serialize`されたときに長さ4096のテキストチャンクに変換されます。このデータ型はテキストオブジェクトの本文部分で使用されます。 | 
| `Color`  | アルファチャンネルを持たない、２４ビットカラーです。`.serialize`されたときに６桁のカラーコードに変換されます。 | 
| `Params` | 一般的な辞書型と同じ振る舞いをしますが、`.serialize`されたときに`;`で区切られたパラメーター文字列に変換されます。このデータ型はカスタムオブジェクト等の設定部分で使われます。 | 

## Install

```python
python setup.py install
```

```python
python setup.py test
```

## License 

The MIT License.
