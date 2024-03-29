import eel
import desktop
import pos_system

app_name="html"
end_point="index.html"
size=(700,600)

@ eel.expose
def master_from_csv(csv_name):
    pos_system.master_from_csv(csv_name)

@ eel.expose
def main02(csv_name,order_code,order_count):
    pos_system.main02(csv_name,order_code,order_count)

@ eel.expose
def main03():
    pos_system.main03()

@ eel.expose
def main04(deposit):
    pos_system.main04(deposit)

desktop.start(app_name,end_point,size)
#desktop.start(size=size,appName=app_name,endPoint=end_point)