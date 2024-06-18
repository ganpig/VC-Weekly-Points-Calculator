from easygui import buttonbox, enterbox, multenterbox
from matplotlib import pyplot


def 算分(播放, 评论, 弹幕, 收藏, 硬币, 点赞):
    修正B = min(收藏 / 播放 * 250, 50)
    修正C = min(硬币 / 播放 * 150, 20)

    # 播放得点
    基础得分 = 播放
    if 基础得分 > 10000:
        播放得点 = 基础得分 * 0.5 + 5000
    else:
        播放得点 = 基础得分
    if 修正B < 10:
        播放得点 = 播放得点 * 修正B * 0.1

    修正A = ((播放得点 + 收藏) / (播放得点 + 收藏 + 弹幕 * 10 + 评论 * 20)) ** 2

    # 点赞得点
    基础得分 = 点赞
    if 基础得分 > 2000:
        点赞得点 = 基础得分 * 2 + 4000
    else:
        点赞得点 = 基础得分 * 4
    if 修正C < 5:
        点赞得点 = 点赞得点 * 修正C * 0.2

    评论得点 = 评论 * 25 * 修正A
    弹幕得点 = 弹幕 * 修正A
    收藏得点 = 收藏 * 修正B
    硬币得点 = 硬币 * 修正C
    总得点 = 播放得点 + 评论得点 + 弹幕得点 + 收藏得点 + 硬币得点 + 点赞得点
    return locals()


指标 = ['播放', '评论', '弹幕', '收藏', '硬币', '点赞']


def main():
    数据 = multenterbox('请填写数据（留空则自动获取）', '周刊得点计算器', 指标)
    if not 数据:
        return
    if not any(数据):
        from json import loads
        from urllib.request import Request, urlopen
        BV号 = enterbox('请填写 BV 号', '周刊得点计算器')
        if not BV号:
            return
        视频数据 = loads(urlopen(Request(f'https://api.bilibili.com/x/web-interface/view?bvid={BV号}', headers={
                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'})).read().decode())['data']['stat']
        数据 = list(map(lambda 指标名: 视频数据[指标名], [
                  'view', 'reply', 'danmaku', 'favorite', 'coin', 'like']))
        数据 = multenterbox('请填写数据', '周刊得点计算器', 指标, 数据)
        if not 数据:
            return
    数据 = list(map(int, 数据))
    结果 = 算分(*数据)
    for 变量名 in 结果:
        if 变量名.endswith('得点'):
            globals()[变量名] = round(结果[变量名])
        else:
            globals()[变量名] = round(结果[变量名], 2)
    while 选项 := buttonbox(f'{总得点=}\n\n{播放得点=}\n{评论得点=}\n{弹幕得点=}\n{收藏得点=}\n{硬币得点=}\n{点赞得点=}\n\n{修正A=}\n{修正B=}\n{修正C=}\n\n点击按钮绘制趋势图象', '周刊得点计算器', 指标):
        当前值 = 数据[指标.index(选项)]
        目标值 = enterbox('请输入目标值', '周刊得点计算器')
        if not 目标值:
            continue
        else:
            目标值 = int(目标值)
        步长 = max((目标值-当前值) // 1000, 1)
        X坐标 = list(range(当前值, 目标值, 步长))
        Y坐标 = []
        for 模拟值 in X坐标:
            模拟数据 = 数据[:]
            模拟数据[指标.index(选项)] = 模拟值
            模拟得点 = 算分(*模拟数据)['总得点']
            Y坐标.append(模拟得点)
        字体 = {'family': 'simsun'}
        pyplot.xlabel(选项, fontdict=字体)
        pyplot.ylabel('总得点', fontdict=字体)
        pyplot.plot(X坐标, Y坐标)
        pyplot.show()


if __name__ == '__main__':
    main()
