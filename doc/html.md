# HTML
## 基本格式
```HTML
<!DOCTYPE html>
<html>
<head>
    <title></title>
    <!-- 這樣寫是註解 -->
</head>
<body>
    <!-- 網頁真正會顯示的區域 -->
</body>
</html>
```

## include套件
```HTML
<link rel="stylesheet" type="text/css" href="mystyle.css">
<script type="text/javascript" src="myjs.js"></script>
```

### 路徑
* `abc.html`
* `01/abc.html`
* `/abc.html`
* `./abc.html`
* `../abc.html`
* `//www.example.com/`

## HTML Tags
### 一般Tags
```HTML
<p></p>
<span></span>
<div></div>
<h1></h1> <h2></h2> <h3></h3> ..... <h6></h6>
```

### br, hr
* `<br>`：換行
* `<hr>`：水平線

### img, iframe
```HTML
<img src="abc.png">
<iframe src="https://example.com"></iframe>
```

### 語意
`<header></header>`、`<article></article>`、`<footer></footer>`

## Tag參數
* id
* name
* class
* style

## 表單
```HTML
<form action="index.php" method="post">
    <input type="checkbox" name="gender" id="gender" value="male" checked>
    <label for="gender">click</label>
    <input type="text" value="123">
    <textarea></textarea>
    <input type="submit" value="Submit">
</form>
```

### 直接範例

* [HTML Forms - w3schools](http://www.w3schools.com/html/html_forms.asp)
* [Forms - Materialize](http://materializecss.com/forms.html)

## 插入js, css
### css
```HTML
<style>
/* 註解 */
.some-class{
    color: #000;
}
#some-id{
    color: black;
}
body{
    color: #eeeeee;   
}
</style>
```

### js
```HTML
<script type="text/javascript">
// some javascript code
</script>
```

## Responsive Web Design
在`<head></head>`裡插入
```HTML
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
```

運用css裡的`@media`
```css
@media screen and (min-width: 480px){
    body{
        font-size: 16px;
    }
}
@media screen and (max-width: 480px){
    body{
        font-size: 20px;
    }
}
```

### Grid system

以[Bootstrap](http://getbootstrap.com/css/#grid)為例

## Materialize css
[Materialize](http://materializecss.com/)

* 有Grid system
* color system
* 現成的配色基礎
* 人性化表單
* 選單

## Browser

* default css
* F12

## 作業

一般頁面：模仿[GitHub首頁](https://github.com)

表單頁面：模仿[GitHub public profile edit](https://github.com/settings/profile)

## Jinja2

預習用 [Jinja2](http://jinja.pocoo.org/docs/dev/)
