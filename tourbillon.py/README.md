# TourbiChain - 時戳 oracle 服務

## 安裝

1. Python: 3.8
1. Pkg: pipenv

安裝完 `pipenv` 之後，執行：

```
pipenv install
```

進入開發環境：

```
pipenv shell
```

執行測試：

```
pipenv run test
```

## Module Toubillon - 服務方

### 啟動服務

#### 1. ganache-cli

```
./run-ganache.sh
```

#### 2. tourbillon

```
./run-tourbillon.sh
```

### 使用者界面

[Index](http://127.0.0.1:5000/)

> UI 開啟後會自動更新，因此無須使用 F5 更新畫面

### API (開發中)

[API](http://127.0.0.1:5000/tourbillon)

## Module VeriChain - 驗證方

### 執行驗證

#### 1. veri-chain

```
./veri-treasure.sh
```