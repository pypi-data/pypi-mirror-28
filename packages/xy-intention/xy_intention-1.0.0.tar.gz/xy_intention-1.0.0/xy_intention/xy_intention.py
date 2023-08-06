import requests
import json
import base64


'''文字意图分析'''
def intention(text=''):
    INITENTION_DESC = ['未知','天气','音乐','股票','新闻']
    ELEMENT_DESC = {
    0:'未知',
    1:'歌词',
    2:'下载地址',
    3:'乐器',
    4:'歌曲',
    5:'人名',
    6:'时间',
    7:'地点',
    8:'风格',
    9:'数字',
    10:'视频',
    11:'民族',
    12:'专辑',
    13:'序数词',
    14:'综艺',
    15:'乐队',
    16:'景点',
    17:'电影',
    18:'电视剧',
    19:'百科',
    34:'股票名称',
    35:'股票代码',
    36:'指数',
    37:'价格',
    38:'行情',
    40:'山',
    41:'湖',
    42:'是否',
    43:'餐馆',
    44:'菜名',
    45:'儿歌',
    46:'故事',
    47:'相声',
    48:'评书',
    49:'有声内容',
    128:'类别词',
    129:'关系词',
    130:'省略词'
    }
    if not text:
        return -1
    url = 'https://www.phpfamily.org/intention.php'
    data = {}
    data['text']=text
    r = requests.post(url, data=data)
    res = r.json()
    # print(res)
    if res['ret'] == 0 and res['data']:

        res_tokens = res['data']
        res_dict = {}
        res_dict['intent'] = INITENTION_DESC[res_tokens['intent']]
        res_dict['element'] = []
        for val in res_tokens['com_tokens']:
            val['com_type'] = ELEMENT_DESC[val['com_type']]
            res_dict['element'].append(val)

        return res_dict
    else:
        return -1



def main():
    res = intention('明天北京天气怎么样？')
    print(res)


if __name__ == '__main__':
    main()
