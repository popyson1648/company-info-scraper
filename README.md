# company-info-scraper

## Overview

Google Programmable Search Engineを利用して企業情報を収集するツールです。  

私はマイナビのドメインに絞ったProgrammable Search Engineを使用しています。そのため、検索クエリやスクレイピング対象の要素はサイトの構造に依存しています。

## Usage

1. `.env` にAPIキーとCSE IDを記入
2. `company_list.txt` に企業名を1行ずつ記入
3. 

    ```shell
    docker build -t company-info-scraper .
    docker run --rm -v $(pwd):/app" company-info-scraper python main.pyb
    ```

- 取得結果は `output/output.txt` に保存されます。
- robots.txtのCrawl-delayに従い、ページ取得の間隔を制御しています。

## License

MIT License

