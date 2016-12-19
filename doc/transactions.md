# 交易紀錄頁面

使用一個叫redis的儲存體把要等很久的交易先記在裡面

每次去觀看頁面就會去檢查交易是否完成


## 安裝

```
sudo apt-get install redis-server
sudo pip install redis
```

## 使用

網址是`/transactions`，所有的寫入動作執行後務必`redirect`到這個頁面

* time：交易送出時間
* done：交易是否完成
* address：交易的查詢點
* description：交易的簡單描述