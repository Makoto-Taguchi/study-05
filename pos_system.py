import pandas as pd
import datetime
import eel

now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
receipt_path = './receipt/receipt_' + now + '.txt'

# master_csv_path = "./master.csv"

# 注文商品コード、個数格納用
item_order_list02 = []
item_count_list02 = []

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        # self.item_order_list=[]
        # self.item_count_list =[]
        self.item_master=item_master

    # レシートに書き込みする関数
    def write_to_receipt(self,txt):
        with open(receipt_path, 'a')as f:
            f.write(str(txt) + '\n')
    
    # オーダーされた商品コードと個数をそれぞれリストに格納
    # def add_item_order_list(self,item_code):
    #     self.item_order_list02.append(item_code)
    #     return self.item_order_list

    # def add_item_count_list(self,item_count):
    #     self.item_count_list02.append(item_count)
    #     return self.item_count_list
        
    # def view_item_list(self):
    #     for item in self.item_order_list:
    #         print("商品コード:{}".format(item))
    
    # オーダー番号から商品情報を取得する（課題１）
    def get_item_data(self,order_code):
        # print(item_new_order_list)
        for m in self.item_master:
            if order_code==m.item_code:
                # print(m.item_name + ":" + str(m.price))
                return m.item_name,m.price

    # オーダーをコンソールから入力
    def input_order(self,order_code,order_count):
        item_info = self.get_item_data(order_code)
        eel.view_order_js("{0[0]} : 単価 {0[1]} 円 が {1} 個注文登録されました".format(item_info,order_count))

        # オーダーした商品コード、個数をそれぞれリストに格納
        # main02とmain03両方で使うのでグローバル変数に
        global item_order_list02
        global item_count_list02

        item_order_list02.append(order_code)
        item_count_list02.append(order_count)

        # item_order_list02 = self.add_item_order_list(order_code)
        # item_count_list02 = self.add_item_count_list(order_count)

    
    # オーダー登録した商品一覧表示
    def view_order(self):
        # 注文の総計
        # main03とmain04両方で使うため、グローバル変数に
        global sum_price
        sum_price = 0
        # self.sum_price=0
        self.order_number=1
        for item_order, item_count in zip(item_order_list02, item_count_list02):
            # self.write_to_receipt("{}品目目------------------".format(str(self.order_number)))
            eel.view_summary_js("{}品目目------------------".format(str(self.order_number)))
            # item_order_listに格納されたコードからその商品の金額取得
            order_info = self.get_item_data(item_order)
            # self.write_to_receipt("{0[0]} : 一個 {0[1]} 円".format(order_info))
            eel.view_summary_js("{0[0]} : 一個 {0[1]} 円".format(order_info))
            # 商品ごとの合計金額算出
            order_price = order_info[1]*int(item_count)
            # self.write_to_receipt("         個数: {0} 合計金額: {1} 円".format(item_count,order_price))
            eel.view_summary_js("         個数: {0} 合計金額: {1} 円".format(item_count,order_price))
            # 全合計金額を加算
            sum_price += order_price
            self.order_number += 1
        print("総計：{} 円".format(str(sum_price)))
        eel.view_summary_js("総計：{} 円".format(str(sum_price)))
    
    def pay_change(self,deposit):
        change = int(deposit) - sum_price
        print("お釣り：{} 円".format(change))
        eel.view_receipt_js("総計：{}円".format(sum_price))
        eel.view_receipt_js("お預かり金額：{}円".format(deposit))
        eel.view_receipt_js("お釣り：{} 円".format(change))


# マスタ登録
def master_from_csv(csv_path):
    # マスタ登録する商品リスト
    # main01とmain02両方で使うため、グローバル変数に
    global item_master
    item_master = []

    df=pd.read_csv(csv_path,dtype={"item_code":object})
    print(list(df["item_name"])) # (テスト出力)リストを出すには"list"をつける
    for item_code,item_name,price in zip(list(df["item_code"]),list(df["item_name"]),list(df["price"])):
            item_master.append(Item(item_code,item_name,price))
            eel.view_input_js("{}({})".format(item_name,item_code))
    eel.view_input_js("------- マスタ登録完了 ---------")
    return item_master


### メイン処理
def main01(csv_name):
    # マスタ登録
    master_csv_path = './' + csv_name
    item_master=master_from_csv(master_csv_path)

def main02(order_code,order_count):
    order=Order(item_master)
    # オーダー登録
    order.input_order(order_code,order_count)

def main03():
    order=Order(item_master)
    # オーダー表示
    order.view_order()

def main04(deposit):
    order=Order(item_master)
    # 支払いからお釣り計算
    order.pay_change(deposit)
    
# if __name__ == "__main__":
#     main()