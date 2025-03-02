# 学习通自动打卡工具

这是一个用于自动在学习通平台上进行打卡的脚本。在使用前，请确保你已经阅读并理解了以下说明。

## 使用说明

### 1. 填写配置信息

在运行脚本之前，你需要填写 `打卡.py` 文件中的配置信息：

- `username`: 你的学习通账号，请填写你的手机号。
- `password`: 你的学习通密码。请注意，脚本目前没有对特殊字符进行转换，所以如果你的密码中含有特殊字符（如 `&*%￥`），建议你修改密码。如果你熟悉 Python，可以自行添加字符转换功能。
- `classId`: 你需要打卡的课程ID。你可以在网页版的学习通内获取到该ID，具体方法请自行探索。
- `text`: 打卡时发布的动态文字内容，这将显示动态在外部。
- `bookName`: 书名，对应你阅读的书籍名称。
- `readTime`: 阅读时长，表示你阅读了多久。
- `pageBegin`: 阅读起始页，表示你从哪一页开始阅读。
- `pageEnd`: 阅读结束页，表示你阅读到的最后一页。

### 2. 运行脚本

在填写完配置信息后，如给库是安装完全的情况下，你可以通过以下命令运行脚本：

```bash
python 打卡.py
