import requests 
import json
import urllib
import tkinter as tk
from tkinter import filedialog

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
}
def login_post(username, password, schoolid=None):
    session = requests.Session()
    password=urllib.parse.quote(password)
    r = session.post(f'http://passport2.chaoxing.com/api/login?name={username}&pwd={password}&schoolid={schoolid}&verify=0', headers=header)
    if r.status_code == 200:
        user_info = json.loads(r.text)
        return session, user_info['realname'], user_info['schoolid'], user_info['uid']
    else:
        return None, None, None, None
# 打开窗口
def select_file():
    # 创建 Tkinter 根窗口
    root = tk.Tk()
    # 隐藏根窗口
    root.withdraw()
    # 确保主窗口不会被关闭
    root.update()
    # 定义图片文件的扩展名
    file_types = [
        ('Image files', '*.jpg *.jpeg *.png *.gif'),
        ('All files', '*.*')
    ]
    # 弹出文件选择对话框，只显示图片文件类型
    file_path = filedialog.askopenfilename(filetypes=file_types)
    # 完成后关闭根窗口
    root.destroy()
    return file_path
def obj(token, puid, file):
    # 构造文件对象
    files = {
        "file": ("file.png", open(file, "rb"))  # 打开文件用于读取二进制数据
    }
    # 构造请求数据
    data = {
        "puid": puid
    }
    # 发送文件上传请求
    u = session.post('https://pan-yz.chaoxing.com/upload?_token={}'.format(token), data=data, files=files, headers=header,verify=True, allow_redirects=False)
    # 解析响应
    r = json.loads(u.text)
    if r['result']:
        object_id = r['objectId']  # 提取objectId
        print(f'图片上传成功，objectId: {object_id}')
        return object_id
    else:
        print(f'图片上传失败，页面提示: {r["msg"]}')
        return None
def get_puid():
    # 请求PUID API URL
    url = 'https://sso.chaoxing.com/apis/login/userLogin4Uname.do'
    # 发送请求并解析响应
    response = session.get(url, headers=header,verify=True, allow_redirects=False)
    data = response.json()
    try:
        puid = data["msg"]["puid"]
        return puid
    except KeyError:
        print("未能获取到puid，响应数据可能不包含'msg'键，或者'msg'键的值不包含'puid'。")
        # 打印出响应的JSON数据来帮助调试
        print(data)
        return None
def Token():
    # Token API URL
    url = 'https://pan-yz.chaoxing.com/api/token/uservalid'
    # 发送请求并解析响应
    response = session.get(url, headers=header,verify=True, allow_redirects=False)
    data = response.json()
    return data["_token"]
# 获取打卡列表
def get_checkin_list(classId):
    session.post(f'https://appcd.chaoxing.com/punch-class/index?classId={classId}',headers=header)
    r = session.post('https://appcd.chaoxing.com/punch-class/participated-list',headers=header)
    json_data = r.text

    # 将JSON字符串转换为Python字典
    data = json.loads(json_data)

    # 提取'datas'键中的列表
    checkin_list = data.get('datas', [])

    # 遍历列表，提取每个项目的'id'、'name'和'dynamicPlaceholder'
    result = []
    for item in checkin_list:
        id = item.get('id')
        name = item.get('name')
        needPubDynamic=item.get('needPubDynamic')
        needRead=item.get('needRead')
        needSubmitWords=item.get('needSubmitWords')
        needUploadAnnex=item.get('needUploadAnnex')
        result.append({'id': id, 'name': name,'needPubDynamic':needPubDynamic,'needRead':needRead,'needSubmitWords':needSubmitWords,'needUploadAnnex':needUploadAnnex})

    # 打印结果
    for res in result:
        print(f'ID: {res["id"]}, Name: {res["name"]}')
    return result
# 打卡请求
def punch_request(result,data):
    id = result[0]['id']
    session.get(f'https://appcd.chaoxing.com/punch-class/{id}',headers=header)
    if data is None:
        b=session.post(f'https://appcd.chaoxing.com/punch-class/{id}/ing',headers=header)
        print(b.text)
    else:
        c = session.post( f'https://appcd.chaoxing.com/punch-class/{id}/dynamic/release', data=data, headers=header)
        print(c.text)
# 详细打卡请求
def detail_punch_request(result, text,bookName=None, readTime=None, pageBegin=None, pageEnd=None):
    # 从result中提取所需参数
    result_entry = result[0]
    punch_id = result_entry['id']
    need_pub_dynamic = result_entry['needPubDynamic']
    need_read = result_entry['needRead']
    need_submit_words = result_entry['needSubmitWords']
    need_upload_annex = result_entry['needUploadAnnex']

    # 初始化dynamic_json结构
    dynamic_json = {
        "punchId": punch_id,
        "annexes": [],
        "id": None,
        "content": "",
        "bookName": "",
        "readTime": "",
        "pageBegin": "",
        "pageEnd": ""
    }

    if need_pub_dynamic:
        print("需要发布到动态")

        # 处理阅读相关字段
        if need_read:
            print("需要阅读")
            dynamic_json['bookName'] = bookName
            dynamic_json['readTime'] = readTime
            dynamic_json['pageBegin'] = pageBegin
            dynamic_json['pageEnd'] = pageEnd

        # 处理提交文字
        if need_submit_words:
            print("需要提交文字")
            dynamic_json['content'] = text
        else:
            dynamic_json['content'] = ""  # 不需要提交文字时清空

        # 处理上传附件
        if need_upload_annex:
            print("需要上传附件")
            file = select_file()
            cloud_disk_id = obj(Token(), get_puid(), file=file)
            if cloud_disk_id:
                dynamic_json['annexes'].append({
                    "dynamicAnnexType": "picture",
                    "cloudDiskId": cloud_disk_id,
                    "url": f"http://p.ananas.chaoxing.com/star3/origin/{cloud_disk_id}"
                })
            else:
                print("警告:缺少附件ID,未添加附件")
    else:
        print("不需要发布到动态")
        return None
    # 构建最终请求数据
    data = {
        "dynamicJsonStr": json.dumps(dynamic_json, ensure_ascii=False)
    }

    return data


if __name__ == '__main__':
    # 登录账号
    username = ''
    # 密码
    password = ''
    # 课程ID
    classId=''
    # 打卡内容
    text='测试'
    # 阅读相关字段
    bookName='测试'
    readTime='123'
    pageBegin='1'
    pageEnd='2'

    session, realname, schoolid, uid = login_post(username, password)
    result=get_checkin_list(classId)
    data=detail_punch_request(result, text,bookName,readTime,pageBegin,pageEnd)
    punch_request(result,data)



