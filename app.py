from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    base_url = 'https://finance.naver.com/sise/sise_market_sum.naver?sosok=1'
    page_number = 1

    results = []  # Store the results to display in the template

    while True:
        url = f'{base_url}&page={page_number}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('table.type_2 tr')

        for row in rows[1:]:
            columns = row.select('td')
            if len(columns) >= 12:
                종목명 = columns[1].text.strip()
                상장주식수_1000 = int(columns[7].text.replace(',', '').strip()) * 1000
                거래량 = int(columns[9].text.replace(',', '').strip())

                if 거래량 >= (상장주식수_1000 / 2):
                    비율 = 거래량 / 상장주식수_1000
                    results.append({
                        '종목명': 종목명,
                        '상장주식수*1000': f'{상장주식수_1000:,.0f}',
                        '거래량': f'{거래량:,.0f}',
                        '비율': f'{비율:.2%}'
                    })

        next_button = soup.select_one('table.Nnavi td.pgRR a')
        if next_button is None:
            break
        page_number += 1

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
