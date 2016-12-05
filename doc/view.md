# 畫面設計說明

每個畫面都要顯示Menu

每個表單都要可以輸入密碼

會用到`<input type="hidden" name="" value="">`

## 首頁

`/`

* 查詢帳號表單：乙太坊Address(input text)
    - 成功 -> 帳號頁面
    - 失敗 -> 回首頁
* 申請帳號表單：乙太坊Address(input text)

## 帳號頁面

`/str:<address>`

* 乙太坊Address
* 帳號Address
* 個人資料
* link：上傳論文
* link：修改個人資料
* 查詢論文表單(僅密碼)
    - 失敗 -> 回到帳號頁面 
* 查看所有發出的邀請表單(僅密碼)
    - 失敗 -> 回到帳號頁面
* 查看所有收到的邀請表單(僅密碼)
    - 失敗 -> 回到帳號頁面

## 上傳論文頁面

`/str:<address>/upload`

* 乙太坊Address
* 帳號Address
* 表單：論文連結(input text)、hash code(input text)、metadata(textarea)
    - 成功 -> 換到論文頁面
    - 失敗 -> 回到帳號頁面

## 修改個人資料頁面

`/str:<address>/update`

* 乙太坊Address
* 帳號Address
* 表單：個人資料(textarea)
    - 不論成功或失敗都回到個人資料頁面

## 論文頁面

`/str:<address>/papers`

* 乙太坊Address
* 帳號Address
* 會顯示該帳號下的所有論文
* 顯示論文的連結、hash code、metadata
* 每篇論文後加上邀請連結，轉跳到邀請頁面

## 邀請申請頁面

`/str:<address>/invite`

* 乙太坊Address
* 帳號Address
* 論文Address
* 表單：對方address(input text),價格

## 查看所有發出的邀請頁面

`/str:<address>/invites`

* 乙太坊Address
* 帳號Address
* 顯示論文的連結、hash code、metadata
* 顯示受邀人address、提出時間
* 每個後面加上取消邀請表單(僅密碼)

## 查看所有收到的邀請頁面

`/str:<address>/requests`

* 乙太坊Address
* 帳號Address
* 顯示論文的連結、hash code、metadata
* 顯示邀請人address、提出時間
* 每個後面加上取消邀請表單(僅密碼)
* 每個後面加上審查連結，連到審查頁面

## 審查頁面

`/str:<address>/requests/str:<invite address>`

* 乙太坊Address
* 帳號Address
* 論文Address
* 邀請人帳號Address
* 表單：accept/reject(input radio)、留言(text area)

