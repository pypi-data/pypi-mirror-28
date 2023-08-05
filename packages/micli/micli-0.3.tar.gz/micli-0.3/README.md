# desc

A simple mail sender running on CLI

## usage 

* received mail content from file
    ```
    micli -s <subject> -r <recipient1[, recipient2, recipient3]> < <mail_contents>
    ```
* if you has short content just used pip
    ```
    echo <"mail content"> | micli -s <subject> -r <recipient1[, recipient2, recipient3]>
    ```
* if you dont know what format about conf, see below

```
[DEFAULT]
smtp_server = smtp.qq.com
smtp_port   = 465
username    = binglingjiumei@qq.com
password    = yzumgavzhbqebfad
```

## end

if you has some question, Please contact to me [hienha@163.com](mailto:hienha@163.com)
