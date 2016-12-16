from bs4 import BeautifulSoup
from urllib import request, parse
import json
import sqlite3
import sys


def search_food_json(search_word):
    url = 'http://fooddb.mext.go.jp/freeword/fword_select.pl'
    post_data = {
        'SEARCH_WORD': search_word,
        'function1': '検索',
        'USER_ID': '',
    }
    encoded_data = parse.urlencode(post_data).encode(encoding='ascii')

    html = request.urlopen(url, data=encoded_data).read().decode('utf-8')

    soup = BeautifulSoup(html, 'html.parser')

    food_json = []
    for item_no in [item.attrs['value'] for item in soup.findAll('input', attrs={'name': 'ITEM_NO'})]:
        url = 'http://fooddb.mext.go.jp/details/details.pl?ITEM_NO=%s' % item_no
        html = request.urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.find('table', id='nut').findAll('tr')
        nut_infos = []
        for tr in trs[1:]:
            dic = {}
            for td in tr.findAll('td'):
                if 'class' in td.attrs :
                    if td.attrs['class'][0] == 'pr_name':
                        dic['name'] = td.text
                    if td.attrs['class'][0] == 'pr_gr_name':
                        dic['name'] = td.text
                    if td.attrs['class'][0] == 'num':
                        dic['num'] = td.text
                    if td.attrs['class'][0] == 'marker':
                        dic['num'] = 0
                    if td.attrs['class'][0] == 'pr_unit':
                        dic['unit'] = td.text
            if 'name' in dic:
                nut_infos.append(dic)
        food_json.append({
            'food_name': soup.find('title').text.split(' - ')[0],
            'nutrition': nut_infos
        })
    return json.dumps(food_json, ensure_ascii=False, indent=2)

if __name__ == '__main__':

    word = sys.argv[1]

    food_data = json.loads(search_food_json(word))[0]
    food_name = food_data['food_name']
    food_nutrition = food_data['nutrition']

    for n in food_nutrition:
        if n['name'] == 'エネルギー':
            energy = n['num']
        """三大栄養素"""
        if n['name'] == 'たんぱく質':
            protein = n['num']
        if n['name'] == '脂質':
            fat = n['num']
        if n['name'] == '炭水化物':
            carbohydrates = n['num']
        """ビタミン"""
        if n['name'] == 'レチノール活性当量': # ビタミンA
            vitaminA = n['num']
        if n['name'] == 'D':
            vitaminD = n['num']
        if n['name'] == 'α' and n['unit'] == 'mg': # ビタミンE
            vitaminE = n['num']
        if n['name'] == 'K':
            vitaminK = n['num']
        if n['name'] == 'B1':
            vitaminB1 = n['num']
        if n['name'] == 'B2':
            vitaminB2 = n['num']
        if n['name'] == 'ナイアシン':
            niacin = n['num']
        if n['name'] == 'B6':
            vitaminB6 = n['num']
        if n['name'] == 'B12':
            vitaminB12 = n['num']
        if n['name'] == '葉酸':
            folate = n['num']
        if n['name'] == 'パントテン酸':
            pantothenic = n['num']
        if n['name'] == 'ビオチン':
            biotin = n['num']
        if n['name'] == 'C':
            vitaminC = n['num']
        """ミネラル"""
        if n['name'] == 'ナトリウム':
            sodium = n['num']
        if n['name'] == 'カリウム':
            potassium = n['num']
        if n['name'] == 'カルシウム':
            calcium = n['num']
        if n['name'] == 'マグネシウム':
            magnesium = n['num']
        if n['name'] == 'リン':
            phosphorus = n['num']
        if n['name'] == '鉄':
            iron = n['num']
        if n['name'] == '亜鉛':
            zinc = n['num']
        if n['name'] == '銅':
            copper = n['num']
        if n['name'] == 'マンガン':
            manganese = n['num']
        if n['name'] == 'ヨウ素':
            iodine = n['num']
        if n['name'] == 'セレン':
            selenium = n['num']
        if n['name'] == 'クロム':
            chromium = n['num']
        if n['name'] == 'モリブデン':
            molybdenum = n['num']

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    sql = 'insert into api_food (name, item_id, price, gram, energy, protein, fat, carbohydrates, vitaminA, vitaminD, vitaminE, vitaminK, vitaminB1, vitaminB2, niacin, vitaminB6, vitaminB12, folate, pantothenic, biotin, vitaminC, sodium, potassium, calcium, magnesium, phosphorus, iron, zinc, copper, manganese, iodine, selenium, chromium, molybdenum) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    food_info = (food_name, 0, 0, 100, energy, protein, fat, carbohydrates, vitaminA, vitaminD, vitaminE, vitaminK, vitaminB1, vitaminB2, niacin, vitaminB6, vitaminB12, folate, pantothenic, biotin, vitaminC, sodium, potassium, calcium, magnesium, phosphorus, iron, zinc, copper, manganese, iodine, selenium, chromium, molybdenum)
    c.execute(sql, food_info)
    conn.commit()
    conn.close()
