import eel

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
        # 1. 入力個数チェック
        if int(order_count) < 1:
            eel.alert_count_js()
            return False
        else:
            pass

        # 2. 入力商品コードチェック
        found = False
        for m in self.item_master:
            # 入力したコードがマスタにあれば登録
            if order_code in m.item_code:
                found = True
                item_info = self.get_item_data(order_code)
                eel.view_order_js(f"{item_info[0]} : 単価 {item_info[1]} 円 が {order_count} 個注文登録されました")
                # 注文した商品コード、個数をリストに追加
                self.item_order_list.append(order_code)
                self.item_count_list.append(order_count)
                break
        # コードがマスタになければアラート表示
        if found:
            pass
        else:
            eel.alert_code_js()
            return False

    # オーダー登録した商品一覧表示
    def view_order(self):
        self.order_number=1
        for item_order, item_count in zip(self.item_order_list, self.item_count_list):
            eel.view_summary_js(f"{str(self.order_number)}品目目------------------")
            # item_order_listに格納された商品コードからその商品の金額取得
            order_info = self.get_item_data(item_order)
            eel.view_summary_js(f"{order_info[0]} : 一個 {order_info[1]} 円")
            # 商品ごとの合計金額算出
            order_price = order_info[1]*int(item_count)
            eel.view_summary_js(f"         個数: {item_count} 合計金額: {order_price} 円")
            # 全合計金額を加算
            self.sum_price += order_price
            self.order_number += 1
        print(f"総計：{str(self.sum_price)} 円")
        eel.view_summary_js(f"総計：{str(self.sum_price)} 円")

    def pay_change(self,deposit):
        change = int(deposit) - self.sum_price
        eel.view_receipt_js(f"総計：{self.sum_price}円")
        eel.view_receipt_js(f"お預かり金額：{deposit}円")
        eel.view_receipt_js(f"お釣り：{change} 円")
