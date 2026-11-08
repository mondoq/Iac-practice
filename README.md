# IaC 練習（Terraform ＋ ネットワーク自動化）

[![Terraform CI](https://github.com/mondoq/Iac-practice/actions/workflows/terraform-ci.yml/badge.svg)](https://github.com/mondoq/Iac-practice/actions/workflows/terraform-ci.yml)
[![Portfolio](https://github.com/mondoq/Iac-practice/actions/workflows/portfolio.yml/badge.svg)](https://mondoq.github.io/Iac-practice/)

クラウドネットワークエンジニアを目指して、インフラをコードで扱う練習をしています。
Terraform で Docker・AWS のリソースを作り、Python（Netmiko）でネットワーク機器の操作を自動化します。

📝 **ポートフォリオ: https://mondoq.github.io/Iac-practice/**

---

## 今やっていること

| # | ディレクトリ | 内容 | 使うもの | 状況 |
|---|---|---|---|---|
| 01 | `01-docker-basics/` | Docker でネットワークと nginx コンテナを作り、Terraform の基本サイクルを体験 | Terraform ＋ Docker | 変数の定義を作り直し中 |
| 02 | `02-ec2-02/` | AWS プロバイダの設定と、最新の Amazon Linux 2023 の AMI を探す `data` ブロック | Terraform ＋ AWS | 書き途中（EC2 本体はこれから） |
| 03 | `03-ec2/` | 東京リージョンのデフォルト VPC に EC2（t3.micro）を1台立てる | Terraform ＋ AWS | コード作成済み |
| 04 | `04-NetWork/` | Netmiko で Cisco ルーターに SSH 接続し、状態確認と設定投入を自動化 | Python ＋ Netmiko | 練習中 |

### 01: Docker で基本サイクル

```
docker_network（≒ VPC / サブネット）
   └── docker_container nginx（≒ EC2）── ports（≒ セキュリティグループ）
```

```bash
cd ~/Iac-practice/01-docker-basics
terraform init     # プロバイダを .terraform/ にダウンロード
terraform plan     # 何が作られるかを確認
terraform apply    # 実行
terraform destroy  # 片付け
```

### 02・03: AWS で EC2

```
AMI（Amazon Linux 2023）──起動イメージ──> EC2 t3.micro
                                          └ 東京リージョン / デフォルト VPC / デフォルトサブネット
```

- 02 は `data "aws_ami"` で AMI を検索する部分を練習中
- 03 は AMI の検索から EC2 の作成までを1つにまとめたもの（`provider.tf` と `main.tf` に分割）
- AWS の認証情報が必要。作ったら `terraform destroy` で必ず片付ける

### 04: Netmiko でネットワーク自動化

| ファイル | 内容 |
|---|---|
| `NetMiko-01.py` | ルーター2台（R1・R2）に接続し、`show ip interface brief` を実行 |
| `NetMiko-02.py` | 特権モードに入り、インターフェースの設定を投入して保存 |
| `NetMiko-03.py` | 接続の基本形（使い方のひな形） |

※ 接続先やパスワードはサンプルの値です。実機で使うときは、パスワードをコードに書かず、環境変数などから読み込みます。

---

## 進め方

基本サイクル: `init` → `plan` → `apply` →（確認）→ `destroy`

各フォルダの `NOTE.md` に、学んだことを書いています。

---

## 仕組み（自動公開）

保存 → `scripts/autosync.sh` が自動で commit・push → GitHub Actions が記事を生成 → GitHub Pages に公開

| ファイル | 役割 |
|---|---|
| `scripts/autosync.sh` / `autosync.service` | 10秒ごとに変更を確認し、自動で commit・push する |
| `scripts/build_portfolio.py` | 各演習フォルダから、ポートフォリオの記事を生成する |
| `.github/workflows/terraform-ci.yml` | `terraform fmt` / `validate` / tflint でチェックする |
| `.github/workflows/portfolio.yml` | 記事を GitHub Pages に公開する |
| `PROFILE.md` | ポートフォリオに載せるプロフィール |

- `NN-名前/` という名前のフォルダが、記事の対象になる
- `NOTE.md` に書いた内容は、記事の「学んだこと」に載る

自動コミットの登録（最初に1回だけ）:
```bash
mkdir -p ~/.config/systemd/user
ln -sf ~/Iac-practice/scripts/autosync.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now autosync
```
`systemctl --user status autosync`（状態）/ `journalctl --user -u autosync -f`（ログ）/ `systemctl --user stop autosync`（一時停止）
