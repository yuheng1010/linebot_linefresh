from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from foodlinebot.models import *
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage,TemplateSendMessage,ButtonsTemplate,PostbackTemplateAction,MessageTemplateAction,FlexSendMessage,DatetimePickerAction

import random

 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
 
@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
            
                mtext=event.message.text
                uid=event.source.user_id
                profile=line_bot_api.get_profile(uid)
                name=profile.display_name
                pic_url=profile.picture_url
                blist='金煌芒果 $450\n包種茶 $300'
                money='750' 
                    
                message=[]
                info=''
                if User_Info.objects.filter(uid=uid).exists()==False:
                    User_Info.objects.create(uid=uid,name=name,pic_url=pic_url,mtext=mtext,blist=blist,money=money)
                    message.append(TextSendMessage(text='會員資料新增完畢'))
                elif User_Info.objects.filter(uid=uid).exists()==True:
                    message.append(TextSendMessage(text='已經養了一隻小豬了哦!'))
                    user_info = User_Info.objects.filter(uid=uid)
                    for user in user_info:
                        info = 'UID=%s\n名字=%s\n消費紀錄:\n%s'%(user.uid,user.name,user.blist)
                        message.append(TextSendMessage(text=info))
                        #message.append(TextSendMessage(text='消費紀錄:金煌芒果 $400'))
                #line_bot_api.reply_message(event.reply_token,message)
                        mn=user.money
                        
                        if int(mn) < 1000 :
                            Url='https://www.myefbc.com/wp-content/uploads/2016/03/piggy-bank.jpg'
                            ratio=str(round(int(mn)/10))
                        if int(mn) > 1000 and int(mn)<3000:
                            Url='https://png.pngtree.com/png-vector/20191018/ourmid/pngtree-piggy-bank-icon-for-your-design-websites-and-projects-png-image_1829671.jpg'
                            ratio=str(round((int(mn)-1000)/20))
                        if int(mn) > 3000 and int(mn)<5000:
                            Url='https://png.pngtree.com/element_our/20190528/ourlarge/pngtree-cartoon-piggy-bank-icon-design-image_1168651.jpg'
                            ratio=str(round((int(mn)-3000)/20))
                        
                        
            
                        if event.message.text=='小豬撲滿':
                           content = {
                              
                              "type": "bubble",
                              "header": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                  {
                                    "type": "image",
                                    "url": Url,
                                    "flex": 1,
                                    "size": "full",
                                    "aspectRatio": "2:1",
                                    "aspectMode": "cover"
                                  }
                                ],
                                "paddingAll": "0px"
                              },
                              "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                  {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                      {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                          {
                                            "type": "text",
                                            "text": "Little Pig",
                                            "size": "xl",
                                            "color": "#1B4332",
                                            "weight": "bold"
                                          }
                                        ]
                                      },
                                      {
                                        "type": "text",
                                        "text": ratio+"%",
                                        "margin": "lg",
                                        "size": "xs",
                                        "color": "#1B4332"
                                      }
                                    ]
                                  },
                                  {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                      {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                          {
                                            "type": "filler"
                                          }
                                        ],
                                        "width": str(int(mn)/10)+"%",
                                        "height": "6px",
                                        "backgroundColor": "#ffffff5A"
                                      }
                                    ]
                                  },
                                  {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                      {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                          {
                                            "type": "text",
                                            "text": "回饋金額:$"+mn,
                                            "margin": "lg",
                                            "size": "sm",
                                            "color": "#1B4332"
                                          }
                                        ]
                                      }
                                    ],
                                    "margin": "xl",
                                    "backgroundColor": "#ffffff1A",
                                    "cornerRadius": "2px",
                                    "paddingAll": "13px"
                                  },
                                  {
                                    "type": "button",
                                    "action": {
                                      "type": "postback",
                                      "label": "消費紀錄",
                                      "data":"消費紀錄",
                                      "text": "消費紀錄"
                                    }
                                  },
                                  {
                                    "type": "button",
                                    "action": {
                                      "type": "postback",
                                      "label": "id條碼",
                                      "data":"id條碼",
                                      "text": "id條碼"
                                    }
                                  }
                                  
                                ],
                                "backgroundColor": "#CFE1B9"
                              }
                            
                            }
                           line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='龜龜龜龜龜龜',contents=content))
                        if event.message.text=='消費紀錄':
                           content={
                              "type": "bubble",
                              "size": "kilo",
                              "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                  {
                                    "type": "image",
                                    "url": "https://www.myefbc.com/wp-content/uploads/2016/03/piggy-bank.jpg",
                                    "size": "full",
                                    "aspectMode": "cover",
                                    "aspectRatio": "1:1",
                                    "gravity": "center"
                                  },
                                  {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [],
                                    "position": "absolute",
                                    "background": {
                                      "type": "linearGradient",
                                      "angle": "0deg",
                                      "endColor": "#00000000",
                                      "startColor": "#00000099"
                                    },
                                    "width": "100%",
                                    "height": "40%",
                                    "offsetBottom": "0px",
                                    "offsetStart": "0px",
                                    "offsetEnd": "0px"
                                  },
                                  {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                      {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                          {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                              {
                                                "type": "text",
                                                "text": "使用者名稱:"+user.name,
                                                "size": "md",
                                                "color": "#ffffff",
                                                "weight": "bold",
                                                "style": "normal"
                                              },
                                              {
                                                "type": "text",
                                                "text": "\n消費紀錄:\n"+user.blist,
                                                "size": "md",
                                                "color": "#ffffff",
                                                "weight": "bold",
                                                "style": "normal"
                                              }
                                            ]
                                          },
                                          {
                                            "type": "box",
                                            "layout": "horizontal",
                                            "contents": []
                                          }
                                        ],
                                        "spacing": "xs",
                                        "width": "1500px"
                                      }
                                    ],
                                    "position": "absolute",
                                    "offsetBottom": "0px",
                                    "offsetStart": "0px",
                                    "offsetEnd": "0px",
                                    "paddingAll": "20px"
                                  }
                                ],
                                "paddingAll": "0px"
                              }
                            }
                           line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='龜龜龜龜龜龜',contents=content))
                           #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
                           #line_bot_api.reply_message(event.reply_token,message)
                        if event.message.text=='食':
                           content={
                               
                                  "type": "carousel",
                                  "contents": [
                                    {
                                      "type": "bubble",
                                      "size": "micro",
                                      "hero": {
                                        "type": "image",
                                        "url": "https://pic.pimg.tw/ksdelicacy/1546911744-2441157712.jpg",
                                        "size": "full",
                                        "aspectMode": "cover",
                                        "aspectRatio": "320:213"
                                      },
                                      "body": {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                          {
                                            "type": "text",
                                            "text": "六龜香檳鳥",
                                            "weight": "bold",
                                            "size": "md",
                                            "wrap": True
                                          },
                                          {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                              {
                                                "type": "icon",
                                                "size": "xs",
                                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                              },
                                              {
                                                "type": "icon",
                                                "size": "xs",
                                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                              },
                                              {
                                                "type": "icon",
                                                "size": "xs",
                                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                              },
                                              {
                                                "type": "icon",
                                                "size": "xs",
                                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                              },
                                              {
                                                "type": "icon",
                                                "size": "xs",
                                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                                              },
                                              {
                                                "type": "text",
                                                "text": "4.0",
                                                "size": "xs",
                                                "color": "#8c8c8c",
                                                "margin": "md",
                                                "flex": 0
                                              }
                                            ]
                                          },
                                          {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                              {
                                                "type": "box",
                                                "layout": "baseline",
                                                "spacing": "sm",
                                                "contents": [
                                                  {
                                                    "type": "text",
                                                    "text": "地址： 844高雄市六龜區裕濃路81巷14之7號",
                                                    "wrap": True,
                                                    "color": "#8c8c8c",
                                                    "size": "xxs",
                                                    "flex": 5
                                                  }
                                                ]
                                              },
                                              {
                                                "type": "button",
                                                "action": {
                                                  "type": "uri",
                                                  "label": "了解更多",
                                                  "uri": "https://www.fusun-farm.com.tw/"
                                                },
                                                "position": "relative"
                                              }
                                            ]
                                          }
                                        ],
                                        "spacing": "sm",
                                        "paddingAll": "13px"
                                      }
                                    },
                                    {
                                      "type": "bubble",
                                      "size": "micro",
                                      "hero": {
                                        "type": "image",
                                        "url": "https://img.wreadit.com/member/59/blogId/ihappydaytw/150786/article_crawler/150786-08e89c88c12db61426fbbc6f13009cc2.jpg",
                                        "size": "full",
                                        "aspectMode": "cover",
                                        "aspectRatio": "320:213"
                                      },
                                      "body": {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                          {
                                            "type": "text",
                                            "text": "六龜梅子燒豆腐",
                                            "weight": "bold",
                                            "size": "sm",
                                            "wrap": True
                                          },
                                          {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                              {
                                                "type": "icon",
                                                "size": "xs",
                                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                              },
                                              {
                                                "type": "icon",
                                                "size": "xs",
                                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                              },
                                              {
                                                "type": "icon",
                                                "size": "xs",
                                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                              },
                                              {
                                                "type": "icon",
                                                "size": "xs",
                                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                              },
                                              {
                                                "type": "icon",
                                                "size": "xs",
                                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                                              },
                                              {
                                                "type": "text",
                                                "text": "4.0",
                                                "size": "sm",
                                                "color": "#8c8c8c",
                                                "margin": "md",
                                                "flex": 0
                                              }
                                            ]
                                          },
                                          {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                              {
                                                "type": "box",
                                                "layout": "baseline",
                                                "spacing": "sm",
                                                "contents": [
                                                  {
                                                    "type": "text",
                                                    "wrap": True,
                                                    "color": "#8c8c8c",
                                                    "size": "xxs",
                                                    "flex": 5,
                                                    "text": "地址： 84443高雄市六龜區新開路86號"
                                                  }
                                                ]
                                              },
                                              {
                                                "type": "button",
                                                "action": {
                                                  "type": "uri",
                                                  "label": "了解更多",
                                                  "uri": "http://www.mspa.com.tw/"
                                                },
                                                "position": "relative",
                                                "margin": "none"
                                              }
                                            ]
                                          }
                                        ],
                                        "spacing": "sm",
                                        "paddingAll": "13px"
                                      }
                                    },
                                    {
                                      "type": "bubble",
                                      "size": "micro",
                                      "hero": {
                                        "type": "image",
                                        "size": "full",
                                        "aspectMode": "cover",
                                        "aspectRatio": "320:213",
                                        "url": "https://pic.pimg.tw/tsaijie229/1572358056-1687180995_l.jpg"
                                      },
                                      "body": {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                          {
                                            "type": "text",
                                            "text": "六龜源通香腸",
                                            "weight": "bold",
                                            "size": "sm"
                                          },
                                          {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                              {
                                                "type": "icon",
                                                "size": "xs",
                                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                              },
                                              {
                                                "type": "icon",
                                                "size": "xs",
                                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                              },
                                              {
                                                "type": "icon",
                                                "size": "xs",
                                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                              },
                                              {
                                                "type": "icon",
                                                "size": "xs",
                                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                              },
                                              {
                                                "type": "icon",
                                                "size": "xs",
                                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                                              },
                                              {
                                                "type": "text",
                                                "text": "4.0",
                                                "size": "sm",
                                                "color": "#8c8c8c",
                                                "margin": "md",
                                                "flex": 0
                                              }
                                            ]
                                          },
                                          {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                              {
                                                "type": "box",
                                                "layout": "baseline",
                                                "spacing": "sm",
                                                "contents": [
                                                  {
                                                    "type": "text",
                                                    "text": "地址： 844高雄市六龜區57 號",
                                                    "wrap": True,
                                                    "color": "#8c8c8c",
                                                    "size": "xxs",
                                                    "flex": 5
                                                  }
                                                ]
                                              },
                                              {
                                                "type": "button",
                                                "action": {
                                                  "type": "uri",
                                                  "label": "了解更多",
                                                  "uri": "https://eattnn.com/0922-871-451/"
                                                }
                                              }
                                            ]
                                          }
                                        ],
                                        "spacing": "sm",
                                        "paddingAll": "13px"
                                      }
                                    }
                                  ]
                               }
                           line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='龜龜龜龜龜龜',contents=content))
                        if event.message.text == '行':
                           content={
                              "type": "bubble",
                              "size": "kilo",
                              "header": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                  {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                      {
                                        "type": "text",
                                        "text": "FROM",
                                        "color": "#ffffff66",
                                        "size": "sm"
                                      },
                                      {
                                        "type": "text",
                                        "text": "我的位置",
                                        "color": "#ffffff",
                                        "size": "xl",
                                        "flex": 4,
                                        "weight": "bold"
                                      }
                                    ]
                                  },
                                  {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                      {
                                        "type": "text",
                                        "text": "TO",
                                        "color": "#ffffff66",
                                        "size": "sm"
                                      },
                                      {
                                        "type": "text",
                                        "text": "六龜",
                                        "color": "#ffffff",
                                        "size": "xl",
                                        "flex": 4,
                                        "weight": "bold"
                                      }
                                    ]
                                  }
                                ],
                                "paddingAll": "20px",
                                "backgroundColor": "#606C38",
                                "spacing": "md",
                                "height": "154px",
                                "paddingTop": "22px"
                              },
                              "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                  {
                                    "type": "text",
                                    "text": "Total: 4 hour",
                                    "color": "#b7b7b7",
                                    "size": "xs"
                                  },
                                  {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                      {
                                        "type": "text",
                                        "text": "12:00",
                                        "size": "sm",
                                        "gravity": "center"
                                      },
                                      {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                          {
                                            "type": "filler"
                                          },
                                          {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [],
                                            "cornerRadius": "30px",
                                            "height": "12px",
                                            "width": "12px",
                                            "borderColor": "#EF454D",
                                            "borderWidth": "2px"
                                          },
                                          {
                                            "type": "filler"
                                          }
                                        ],
                                        "flex": 0
                                      },
                                      {
                                        "type": "text",
                                        "text": "我",
                                        "gravity": "center",
                                        "flex": 4,
                                        "size": "sm"
                                      }
                                    ],
                                    "spacing": "lg",
                                    "cornerRadius": "30px",
                                    "margin": "xl"
                                  },
                                  {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                      {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                          {
                                            "type": "filler"
                                          }
                                        ],
                                        "flex": 1
                                      },
                                      {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                          {
                                            "type": "box",
                                            "layout": "horizontal",
                                            "contents": [
                                              {
                                                "type": "filler"
                                              },
                                              {
                                                "type": "box",
                                                "layout": "vertical",
                                                "contents": [],
                                                "width": "2px",
                                                "backgroundColor": "#B7B7B7"
                                              },
                                              {
                                                "type": "filler"
                                              }
                                            ],
                                            "flex": 1
                                          }
                                        ],
                                        "width": "12px"
                                      },
                                      {
                                        "type": "text",
                                        "text": "Train 3hours",
                                        "gravity": "center",
                                        "flex": 4,
                                        "size": "xs",
                                        "color": "#8c8c8c"
                                      }
                                    ],
                                    "spacing": "lg",
                                    "height": "64px"
                                  },
                                  {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                      {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                          {
                                            "type": "text",
                                            "text": "15:00",
                                            "gravity": "center",
                                            "size": "sm"
                                          }
                                        ],
                                        "flex": 1
                                      },
                                      {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                          {
                                            "type": "filler"
                                          },
                                          {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [],
                                            "cornerRadius": "30px",
                                            "width": "12px",
                                            "height": "12px",
                                            "borderWidth": "2px",
                                            "borderColor": "#6486E3"
                                          },
                                          {
                                            "type": "filler"
                                          }
                                        ],
                                        "flex": 0
                                      },
                                      {
                                        "type": "text",
                                        "text": "高雄車站",
                                        "gravity": "center",
                                        "flex": 4,
                                        "size": "sm"
                                      }
                                    ],
                                    "spacing": "lg",
                                    "cornerRadius": "30px"
                                  },
                                  {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                      {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                          {
                                            "type": "filler"
                                          }
                                        ],
                                        "flex": 1
                                      },
                                      {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                          {
                                            "type": "box",
                                            "layout": "horizontal",
                                            "contents": [
                                              {
                                                "type": "filler"
                                              },
                                              {
                                                "type": "box",
                                                "layout": "vertical",
                                                "contents": [],
                                                "width": "2px",
                                                "backgroundColor": "#6486E3"
                                              },
                                              {
                                                "type": "filler"
                                              }
                                            ],
                                            "flex": 1
                                          }
                                        ],
                                        "width": "12px"
                                      },
                                      {
                                        "type": "text",
                                        "text": "Metro 1hr",
                                        "gravity": "center",
                                        "flex": 4,
                                        "size": "xs",
                                        "color": "#8c8c8c"
                                      }
                                    ],
                                    "spacing": "lg",
                                    "height": "64px"
                                  },
                                  {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                      {
                                        "type": "text",
                                        "text": "16:00",
                                        "gravity": "center",
                                        "size": "sm"
                                      },
                                      {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                          {
                                            "type": "filler"
                                          },
                                          {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [],
                                            "cornerRadius": "30px",
                                            "width": "12px",
                                            "height": "12px",
                                            "borderColor": "#6486E3",
                                            "borderWidth": "2px"
                                          },
                                          {
                                            "type": "filler"
                                          }
                                        ],
                                        "flex": 0
                                      },
                                      {
                                        "type": "text",
                                        "text": "六龜",
                                        "gravity": "center",
                                        "flex": 4,
                                        "size": "sm"
                                      }
                                    ],
                                    "spacing": "lg",
                                    "cornerRadius": "30px"
                                  }
                                ]
                              }
                            }
                           line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='好累',contents=content))
                        if event.message.text == '樂':
                           content={
                          "type": "bubble",
                          "size": "kilo",
                          "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                              {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                  {
                                    "type": "image",
                                    "url": "https://images.1111.com.tw/media/share/10/1089dcd399e942f18ad24a82a0589f36.jpg",
                                    "size": "full",
                                    "aspectMode": "cover",
                                    "aspectRatio": "2:1",
                                    "action": {
                                      "type": "uri",
                                      "label": "action",
                                      "uri": "https://www.1111job.com.tw/fun/fun.asp?kit=oth&uNo=3346"
                                    }
                                  },
                                  {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                      {
                                        "type": "image",
                                        "url": "https://www.maolin-nsa.gov.tw/att/pic//11004817.jpg",
                                        "size": "full",
                                        "aspectMode": "cover",
                                        "aspectRatio": "150:98",
                                        "gravity": "center"
                                      },
                                      {
                                        "type": "image",
                                        "url": "https://6.blog.xuite.net/6/f/c/6/23127615/blog_1834140/txt/383800767/27.jpg",
                                        "size": "full",
                                        "aspectMode": "cover",
                                        "aspectRatio": "150:98",
                                        "gravity": "center"
                                      }
                                    ],
                                    "flex": 1
                                  }
                                ]
                              }
                            ],
                            "paddingAll": "0px"
                          }
                        }
                           line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='龜龜龜龜龜龜',contents=content))
                        if event.message.text == '住':
                           message = TemplateSendMessage(alt_text='請選擇入住日期',
                           template=ButtonsTemplate(title='請選擇入住日期',
                           text='選擇日期', actions=[
                           DatetimePickerAction(label='時間選擇',data='date_postback',mode='date')]
                           ))
                           line_bot_api.reply_message(event.reply_token, message)
                    #line_bot_api.reply_message(  # 回復傳入的訊息文字
                    #    event.reply_token,
                    #   TextSendMessage(text=event.message.text)
               # )
                        if event.message.text =='id條碼':
                            content={
                              "type": "bubble",
                              "size": "kilo",
                              "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                  {
                                    "type": "image",
                                    "url": "https://www.ez2o.com/LIB/QrCode/wyZkvV4qstqHf3apt7ud7cHBCE7r7Yj7aTSJRgYxsLhdAclg2IbO69?q=L",
                                    "size": "full",
                                    "aspectMode": "cover",
                                    "aspectRatio": "1:1",
                                    "gravity": "center"
                                  },
                                  {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [],
                                    "position": "absolute",
                                    "background": {
                                      "type": "linearGradient",
                                      "angle": "0deg",
                                      "endColor": "#00000000",
                                      "startColor": "#00000099"
                                    },
                                    "width": "100%",
                                    "height": "40%",
                                    "offsetBottom": "0px",
                                    "offsetStart": "0px",
                                    "offsetEnd": "0px"
                                  },
                                  {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                      {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                          {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [],
                                            "spacing": "xs"
                                          }
                                        ],
                                        "spacing": "xs"
                                      }
                                    ],
                                    "position": "absolute",
                                    "offsetBottom": "0px",
                                    "offsetStart": "0px",
                                    "offsetEnd": "0px",
                                    "paddingAll": "20px"
                                  }
                                ],
                                "paddingAll": "0px"
                              }
                            }
                            line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='龜龜龜龜龜龜',contents=content))
                            
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
# Create your views here.
