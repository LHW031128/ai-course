import base64
import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')

# 토스 결제위젯 공식 테스트 시크릿 키 (v2 전용)
WIDGET_SECRET_KEY = os.environ.get("TOSS_SECRET_KEY", "test_gsk_docs_OaPz8L5KdmQXkzRz3y47BMw6")
encoded_key = base64.b64encode(f"{WIDGET_SECRET_KEY}:".encode('utf-8')).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    payment_key = request.args.get('paymentKey')
    order_id = request.args.get('orderId')
    amount = request.args.get('amount')

    # 브라우저에서 온 금액을 그대로 믿지 않고 서버 기준 금액과 비교
    if amount != "1000":
        return render_template('fail.html', message='결제 금액이 일치하지 않습니다.')

    # 토스페이먼츠 결제 승인 API 호출
    url = "https://api.tosspayments.com/v1/payments/confirm"
    headers = {
        "Authorization": f"Basic {encoded_key}",
        "Content-Type": "application/json"
    }
    data = {
        "paymentKey": payment_key,
        "orderId": order_id,
        "amount": amount
    }

    response = requests.post(url, json=data, headers=headers)
    res_data = response.json()

    if response.status_code == 200:
        return render_template('success.html', result=res_data)
    else:
        return render_template('fail.html', message=res_data.get('message', '결제 승인 실패'))

@app.route('/fail')
def fail():
    message = request.args.get('message', '결제가 실패했습니다.')
    return render_template('fail.html', message=message)

if __name__ == '__main__':
    app.run(debug=True, port=5000)