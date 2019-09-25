title: 运维开发和钉钉
date: 2019-09-25 16:24:10
---

![运维开发+钉钉](/uploads/images/devops-dingding.png "cover")

最近使用钉钉的群聊机器人来做运维平台的通知消息端， 瞬间对钉钉这个软件有了好感。 为什么说有了好感， 因为之前听说钉钉搞什么『必须微笑打卡』， 让我对钉钉很排斥。 而钉钉之所以占领企业即时通信领域， 这和钉钉的开放和易于接入有关的， 当开源版本的微信程序和官方的封杀斗智斗勇的时候， 钉钉已经提供了， 一个 URL 的接口， 就可以轻松接入到群聊的机器人功能。

虽然企业微信也支持自定义机器人 webhook ， 但企业微信不支持 ActionCard 类型的消息样式. 这是一种可接受一组操作的消息体, 很强大.

## 应用在运维开发的场景.

- 监控报警 (图片， 链接)
- 数据报表
- 工作流进度通知
- 后台任务接口通知
- 更多通知场景..

## 注册应用

直接在群聊的配置页面里， 增加机器人。 然后复制 webhook URL。


## 程序接入

钉钉提供一个webhook URL，通过 POST 相关的数据来发送消息， 消息支持非常多的样式，自定义性非常高。 包括普通的文本消息， markdown 和 actionCard 消息，并且支持 mention (@提及) 功能， 非常适合监控和通知。

```python
import requests


HOST = 'https://oapi.dingtalk.com/robot/send?access_token='


class DingWebhook:

    def __init__(self, token):
        self.url = f'{HOST}{token}'

    def send(self, payload):
        resp = requests.post(
            self.url,
            json=payload,
            headers={
                'Content-Type': "application/json"
            }
        )

        resp.raise_for_status()

        return resp.json()


if __name__ == '__main__':
    ding = DingWebhook(token='******************************')

    content = f'有新的权限待审批， 请[审批](http://xx.com/new-permissions) \n@188****4265'

    payload = {
        "actionCard": {
            "title": "Vision 权限审批",
            "text": content,
            "hideAvatar": "0",
            "btnOrientation": "0",
            "btns": [
                {
                    "title": "去审批",
                    "actionURL": "https://vision.teambition.net/check/" # admin/web/permission/?is_valid__exact=0
                },
            ]
        },
        "at": {
            "atMobiles": [
                "188****4265", 
            ], 
        "isAtAll": False
        },
        "msgtype": "actionCard"
    }

    ding.send(payload=payload)
```

## 写在最后

机器人不支持私信功能， 必须通过群聊发送信息。 不过这个可以通过 atMobiles 来达到分配任务的目的。 可以获取轮班人员信息， 发送信息前组织数据的 atMobiles 来实现轮班提醒. 不得不说， 钉钉对开发人员是非常友好的，降低了公司的接入钉钉的开发成本。
