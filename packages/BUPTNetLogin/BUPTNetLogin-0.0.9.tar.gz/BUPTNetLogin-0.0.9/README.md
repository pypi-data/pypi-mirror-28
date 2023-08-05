# BUPTLoginByPython3

北邮网关登陆程序，Python3版本
> windows环境下且无python可以使用 [windows版本](https://github.com/zwk19023393/BUPTNetLoginByWPF)

## 安装
支持pip一键安装，输入：
```html
    pip3 install BUPTNetLogin
```

## 使用方法
### 登录命令（BUPT Net Login）
- 带参数运行
```
    bnl [校园网账户] [密码]
```

- 不带参数运行
```
    bnl
```
> 如果是第一次登陆将会提示输入账户密码，登录过后会保存账户信息到`~/bnl.ini`

### 修改登录账户（Change User）
```
    bnl [校园网账户] [密码]
```
使用带参数运行，登录成功后会自动更新`~/bnl.ini`。也可以直接修改`~/bnl.ini`

### 注销命令（BUPT Net Logout）
```
bnlo
```

### 更新
```html
    pip3 install BUPTNetLogin --upgrade
```

## 依赖库
安装BUPTNetLogin时将自动安装以下Python库
- BeautifulSoup4
- lxml

> 更多请前往 [个人博客](http://www.ingbyr.com)
