from urllib import request
from bs4 import BeautifulSoup
from http import cookiejar
from threading import Thread
import re


# cookie管理
COOKIE = cookiejar.CookieJar()


class AddToBasketThread(Thread):
    def __init__(self, item_id, num):
        """
        商品をバスケットに追加するためのスレッド
        @param item_id 商品ID
        @param num 個数
        """
        super(AddToBasketThread, self).__init__()
        self.item_id = item_id
        self.num = num
        self.error = None

    def run(self):
        url = 'https://netsuper.daiei.co.jp/0338/item/basket.php'
        data = ('submit_addbasket%%5B%d%%5D=&e695b0e9878f%%5B%d%%5D=%d' % (self.item_id, self.item_id, self.num)).encode('utf-8')
        req = request.Request(url, data)

        opener = request.build_opener()
        opener.add_handler(request.HTTPCookieProcessor(COOKIE))
        self.response = opener.open(req).read().decode('utf-8')
        if '購入できる個数の上限を超えています' in self.response:
            self.error = 'Limit Over'
            raise(Exception('購入できる個数の上限を超過'))
        if '販売対象外の商品です' in self.response:
            self.error = 'Not Exist Item'
            raise(Exception('販売対象外の商品'))


def login(login_id, password):
    """
    ログイン
    @param login_id ログインID
    @param password パスワード
    @return HTML
    """
    url = 'https://netsuper.daiei.co.jp/index.php?secure=1'
    data = ('submit_member_login%%5B%%5D=member_login&loginCookie=1&login_id=%s&password=%s' % (login_id, password)).encode('utf-8')
    req = request.Request(url, data)

    opener = request.build_opener()
    opener.add_handler(request.HTTPCookieProcessor(COOKIE))

    response = opener.open(req).read().decode('utf-8')
    if '配達便の選択' in response:
        return True
    else:
        return False


def get_delivery_dates():
    """
    配達可能な日時の取得
    @return [配達可能な日時, ...]
    """
    url = 'https://netsuper.daiei.co.jp/0338/select_delivery.php'
    req = request.Request(url)

    opener = request.build_opener()
    opener.add_handler(request.HTTPCookieProcessor(COOKIE))

    conn = opener.open(req)
    soup = BeautifulSoup(conn.read().decode('utf-8'), "html.parser")
    deliv_dates = []
    for deliv in soup.findAll('input', attrs={'name': 'delivery'}):
        if not 'disabled' in deliv.attrs:
            deliv_dates.append(deliv.attrs['value'])
    return deliv_dates


def select_delivery_date(date):
    """
    配達日時の指定
    @param date 配達日時
    @return HTML
    """
    url = 'https://netsuper.daiei.co.jp/0338/select_delivery.php'
    data = ('default_event=doneDelivery&delivery=%s&submit_doneDelivery=%%E3%%80%%80' % date).encode('utf-8')
    req = request.Request(url, data)

    opener = request.build_opener()
    opener.add_handler(request.HTTPCookieProcessor(COOKIE))
    conn = opener.open(req)

    response = opener.open(req).read().decode('utf-8')
    if '別の便をお選びください' in response:
        raise(Exception('不正な配達日時'))
    return response


def get_order():
    """
    注文確定に関する情報を取得する
    @return (HTML, statefulID)
    """
    url = 'https://netsuper.daiei.co.jp/0338/order/order.php'
    req = request.Request(url)

    opener = request.build_opener()
    opener.add_handler(request.HTTPCookieProcessor(COOKIE))
    conn = opener.open(req)
    soup = BeautifulSoup(conn.read().decode('utf-8'), "html.parser")

    statefulID = soup.find('input', attrs={'name': 'StateFulID'}).attrs['value']
    date = soup.find('input', attrs={'name': 'delivery', 'checked': True}).attrs['value']

    data = ('submit_next=back&StateFulID=%s&payment=1&credit_use_type=1&delivery=%s' % (statefulID, date)).encode('utf-8')
    req = request.Request(url, data)

    opener.add_handler(request.HTTPCookieProcessor(COOKIE))

    return opener.open(req).read().decode('utf-8'), statefulID


def check_order():
    """
    注文内容を確認する
    @return 支払額詳細 dict()
    """
    html = get_order()[0]

    prices = {}
    soup = BeautifulSoup(html, 'html.parser')
    total = soup.find('td', attrs={'class': 'text20'}).findNext('td').text
    total = re.sub(r'[円,]', r'', total)

    receipt = {
        'total': total,
        'items': [],
    }

    item_name = soup.find(attrs={'class': 'order_font_name'})
    item_price = soup.find(attrs={'class': 'order_txt_c'})
    item_pay = soup.find(attrs={'class': 'order_txt_r'})
    while item_price != None:
        item_num = item_price.findNext(attrs={'class': 'order_txt_c'})
        receipt['items'].append(
            {
                'name': item_name.text.strip(),
                'price': re.sub(r'[円,]', r'', item_price.text),
                'num': re.sub(r'[円,]', r'', item_num.text),
                'pay': re.sub(r'[円,]', r'', item_pay.text),
            }
        )
        item_name = item_name.findNext(attrs={'class': 'order_font_name'})
        item_pay = item_pay.findNext(attrs={'class': 'order_txt_r'})
        item_price = item_num.findNext(attrs={'class': 'order_txt_c'})
    return receipt


def submit_order():
    """
    注文内容を確定する
    （配送確定になるので慎重に実行するように）
    @return HTML
    """
    statefulID = get_order()[1]
    url = 'https://netsuper.daiei.co.jp/0338/order/order.php'
    data = ('default_event=&StateFulID=%s&submit_order=%%E3%%80%%80' % statefulID).encode('utf-8')
    req = request.Request(url, data)

    opener = request.build_opener()
    opener.add_handler(request.HTTPCookieProcessor(COOKIE))

    response = opener.open(req).read().decode('utf-8')
    if not 'ご注文完了' in response:
        raise(Exception('注文エラー'))
    return response


def dump_html(response, output_file):
    """
    HTTPレスポンスからHTMLを取得し，ファイルに書き出す
    @param response HTTPレスポンス
    @param output_file 出力先ファイル
    """
    with open(output_file, 'w') as f:
        f.write(response)


def main():
    # login() → select_delivery_date() → submit_order() はこの順番で呼ぶこと（cookieを正しく構築するため）

    # ログイン
    login_id = '********'
    password = '********'
    login(login_id, password)

    # 配達可能な時刻の中で，一番早く配達される時刻を選択
    date = min(get_delivery_dates())

    # 配達時刻の確定
    select_delivery_date(date)

    # バスケットへの商品追加処理
    # アイテムID, 個数
    items = [
        (1207497, 3),
        (1107316, 4),
        (1065148, 2),
        (1072904, 1)
    ]

    # 高速化のためにバケットへの追加処理を並列化
    # あんまり同時リクエスト数 が大きくなるとエラーが出るかも
    threads = []
    for item_id, num in items:
        thread = AddToBasketThread(item_id, num)
        thread.start()
        threads.append(thread)
    [thread.join() for thread in threads]

    # 注文内容の確認（receiptの中に詳細な価格情報）
    receipt = check_order()

    # 注文の確定（本当に宅配されるので実行する際は注意）
    # dump_html(submit_order(), 'submit.html')