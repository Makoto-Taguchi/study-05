import pandas as pd
import datetime
import eel
import classTest

now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
receipt_path = './receipt/receipt_' + now + '.txt'

# マスタ登録
# CSVファイル名入力後、「決定」ボタン押下で呼び出し
def master_from_csv(csv_name):
    print("------- マスタ登録開始 ---------")
    item_master = []
    csv_path = './' + csv_name

    df=pd.read_csv(csv_path,dtype={"item_code":object})
    print(list(df["item_name"])) # (テスト出力)リストを出すには"list"をつける
    for item_code,item_name,price in zip(list(df["item_code"]),list(df["item_name"]),list(df["price"])):
            item_master.append(classTest.Item(item_code,item_name,price))
            eel.view_input_js(f"{item_name}({item_code})")
    eel.view_input_js("------- マスタ登録完了 ---------")
    print(list(df["item_code"]))
    # orderインスタンスはmain02~04で使うためグローバル変数に
    global order
    order=classTest.Order(item_master)


# 商品コード、個数入力後、「オーダー登録」ボタン押下で呼び出し
def main02(csv_name,order_code,order_count):
    # オーダー登録
    order.input_order(order_code,order_count)


# 「合計金額表示」ボタン押下で呼び出し
def main03():
    # オーダー表示
    order.view_order()


# 支払い金額入力後、「決定」ボタン押下で呼び出し
def main04(deposit):
    # 支払いからお釣り計算
    order.pay_change(deposit)

# if __name__ == "__main__":
#     main()