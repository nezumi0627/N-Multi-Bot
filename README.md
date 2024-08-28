# N-Multi-Bot

[English: README-en.md](README-en.md)

このプロジェクトは、LINE グループチャットで動作する多機能ボットのためのコマンドハンドラーシステムです。

## インストール

1. リポジトリをクローン:

   ```bash
   git clone https://github.com/nezumi0627/N-Multi-Bot.git
   cd N-Multi-Bot
   ```

2. 依存関係をインストール:

   ```bash
   pip install -r requirements.txt
   ```

3. CHRLINE-Patch ライブラリをインストール:

   ```bash
   pip install git+https://github.com/WEDeach/CHRLINE-Patch.git
   ```

4. `main.py`を実行し、ボット情報を設定します。

## 使用方法

1. `main.py`を編集し、ボット情報を設定します。
2. `main.py`を実行してボットを起動します。
3. LINE グループチャットで`!help`コマンドを使用して、利用可能なコマンドを確認します。

## 依存関係

- Python 3.x
- CHRLINE-Patch ライブラリ
- その他の依存関係は`requirements.txt`に記載されています

## セットアップ

1. `./data/auther.json`ファイルを作成し、管理者とオーナーの MID を設定します:

   ```json
   {
     "admin": ["adminMID1", "adminMID2"],
     "owner": ["ownerMID1", "ownerMID2"]
   }
   ```

2. 環境変数または`config.json`ファイルで LINE アカウントの認証情報を設定します。

## セキュリティ

- E2EE キーの自動セットアップ機能があります。
- メッセージの暗号化と復号化をサポートしています。

## プロジェクト構造

- `main.py`: メインのボットロジックとコマンドハンドラー
- `messenger.py`: メッセージ送信機能を管理するクラス
- `data/auther.json`: 管理者とオーナーの設定ファイル

## 注意事項

- このボットは管理者とオーナーのみがコマンドを使用できます。
- CHRLINE-Patch ライブラリの使用に伴う責任は一切負いません。このプロジェクトは CHRLINE-Patch ライブラリとの関係は一切ありません。
- このプロジェクトはデバッグ目的で作成されています。実際のボット運用には公式の LINE API の使用をお勧めします。

## トラブルシューティング

- E2EE キーの設定に問題がある場合は、`setup_e2ee_key`メソッドを確認してください。
- データベースの読み込みエラーが発生した場合は、`data/auther.json`ファイルの存在と内容を確認してください。

## 連絡先

質問や提案がある場合は、[Issues](https://github.com/nezumi0627/N-Multi-Bot/issues)にてお問い合わせください。

## 更新履歴

- vβ (2023-08-29): 初期リリース

## 謝辞

CHRLINE-Patch ライブラリの開発者の皆様に感謝いたします。

## ライセンス

このプロジェクトは MIT ライセンスのもとで公開されています。詳細は[LICENSE](LICENSE)ファイルをご覧ください。

このソフトウェアは「現状のまま」提供されており、明示または黙示を問わず、いかなる種類の保証も伴いません。作者または著作権所有者は、契約行為、不法行為、またはそれ以外であっても、ソフトウェアに起因または関連し、あるいはソフトウェアの使用またはその他の扱いによって生じる一切の請求、損害、その他の義務について何らの責任も負わないものとします。

このプロジェクトを使用する際には、関連する法令を遵守し、指示に従ってください。
