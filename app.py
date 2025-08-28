name: Run Mizuiro Script with Slack Notification

on:
  push:
    branches:
      - main

jobs:
  run-script:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install slack_sdk

    - name: Run Mizuiro Script
      id: run_mizuiro
      run: |
        set +e
        python 水色.py
        echo "EXIT_CODE=$?" >> $GITHUB_ENV
        set -e

    - name: Notify Slack
      uses: slackapi/slack-github-action@v1.26.0
      with:
        channel-id: ${{ secrets.SLACK_CHANNEL }}
        slack-message: |
          水色.py 実行結果: ${{ env.EXIT_CODE == '0' && '✅ 成功したよ' || '❌ 失敗したよ' }}
      env:
        SLACK_BOT_TOKEN: ${{ secrets.SLACK_TOKEN }}
