# 用法

安装 selenium

``` bash
pip install selenium webdriver-manager
```

## 配置

将 `secret_template.py` 重命名为 `secret.py`， 并修改为个人配置。

其中有关**苏康码相关数据**的部分，可以通过[如何 DIY 一个苏康码与行程码“双码合一”的健康码 APP](https://blog.vvzero.com/2022/04/08/diy-to-combine-sukangma-and-xingchengma/) 或者 HttpCanary+[TrustMeAlready](https://github.com/ViRb3/TrustMeAlready) 来获取。

行程码似乎没有合适的方法直接获取（需要手机验证码进行验证），如果有合适的获取方法，欢迎提 PR。

## 运行

```
python autoRequest.py
```

## 一些问题

- 无头（headless）有一些问题，因此没有开启该选项
- 不确定能不能在仅开启命令行的服务器上运行
