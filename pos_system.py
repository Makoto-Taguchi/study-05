import pandas as pd
import datetime
import eel

now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
receipt_path = './receipt/receipt_' + now + '.txt'

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_count_list =[]
        self.item_master=item_master
        self.sum_price=0

    # レシートに書き込みする関数
    def write_to_receipt(self,txt):
        with open(receipt_path, 'a')as f:
            f.write(str(txt) + '\n')

    # オーダー番号から商品情報を取得する（課題１）
    def get_item_data(self,order_code):
        for m in self.item_master:
            if order_code==m.item_code:
                return m.item_name,m.price

    # オーダーをコンソールから入力
    def input_order(self,order_code,order_count):
        item_info = self.get_item_data(order_code)
        eel.view_order_js("{0[0]} : 単価 {0[1]} 円 が {1} 個注文登録されました".format(item_info,order_count))
        # 注文した商品コード、個数をリストに追加
        self.item_order_list.append(order_code)
        self.item_count_list.append(order_count)

    # オーダー登録した商品一覧表示
    def view_order(self):
        self.order_number=1
        for item_order, item_count in zip(self.item_order_list, self.item_count_list):
            eel.view_summary_js("{}品目目------------------".format(str(self.order_number)))
            # item_order_listに格納された商品コードからその商品の金額取得
            order_info = self.get_item_data(item_order)
            eel.view_summary_js("{0[0]} : 一個 {0[1]} 円".format(order_info))
            # 商品ごとの合計金額算出
            order_price = order_info[1]*int(item_count)
            eel.view_summary_js("         個数: {0} 合計金額: {1} 円".format(item_count,order_price))
            # 全合計金額を加算
            self.sum_price += order_price
            self.order_number += 1
        print("総計：{} 円".format(str(self.sum_price)))
        eel.view_summary_js("総計：{} 円".format(str(self.sum_price)))

    def pay_change(self,deposit):
        change = int(deposit) - self.sum_price
        print("お釣り：{} 円".format(change))
        eel.view_receipt_js("総計：{}円".format(self.sum_price))
        eel.view_receipt_js("お預かり金額：{}円".format(deposit))
        eel.view_receipt_js("お釣り：{} 円".format(change))


# マスタ登録
# CSVファイル名入力後、「決定」ボタン押下で呼び出し
def master_from_csv(csv_name):
    print("------- マスタ登録開始 ---------")
    item_master = []
    csv_path = './' + csv_name

    df=pd.read_csv(csv_path,dtype={"item_code":object})
    print(list(df["item_name"])) # (テスト出力)リストを出すには"list"をつける
    for item_code,item_name,price in zip(list(df["item_code"]),list(df["item_name"]),list(df["price"])):
            item_master.append(Item(item_code,item_name,price))
            eel.view_input_js("{}({})".format(item_name,item_code))
    eel.view_input_js("------- マスタ登録完了 ---------")

    # orderインスタンスはmain02~04で使うためグローバル変数に
    global order
    order=Order(item_master)


### メイン処理
# def main01(csv_name):
#     # マスタ登録
#     master_csv_path = './' + csv_name
#     item_master=master_from_csv(master_csv_path)
#     return item_master

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