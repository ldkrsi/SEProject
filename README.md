# 軟體工程期末專題

## 工具

* 程式碼放在GitHub
* 用SourceTree來取代直接下git commands
    * 不收費軟體，但安裝過程需註冊該公司的帳號領認證碼
    * Google搜尋`sourcetree 安裝教學`找方法來安裝並註冊
    * Google搜尋`sourcetree github`找方法來連結SourceTree和GitHub
    * 如果你之前還沒安裝過git或sourcetree幫你裝了全新的git，那完成安裝和認證後還要git config你的name和email才可以進行`git push`的動作
        ```
        $ git config --global user.name "John Doe"
        $ git config --global user.email johndoe@example.com
        ```
* 網頁後端使用Python3 + Flask
    * 先去安裝Python3
    * 用pip安裝Flask
        * 用Windows的話找到Python3安裝完後的資料夾，裡面有一個Scripts資料夾，用cmd進該資料夾後打`pip install Flask`
        * 用Mac或Linux系列系統的話就直接用指令列`sudo pip install Flask`
* 網頁前端使用[Materialize CSS](http://materializecss.com/)

## 協作流程

### 環境說明

* master branch是上鎖的，只有admin(ldkrsi)帳號可以對他修改
* 每個人有自己的branch，用自己的ID命名

### 協作流程

以下假設所有人都把這份GitHub上的程式碼clone到自己電腦上，並在屬於自己的branch下寫code

1. 寫好一個新功能
2. commit後push到GitHub上
3. 發表一個pull request給master branch
4. admin收到pull request後會檢查程式碼，沒問題的話就會merge入master

當發現master有資料被merge或出現被admin修改的行為時，每個人請務必把master merge進自己的工作的branch裡，避免程式碼新舊版本的衝突