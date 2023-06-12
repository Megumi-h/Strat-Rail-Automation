import time
import is_in_map.is_in_map as mapp
import Route.Space_Station.Black_Tower_Route as Btr
import os


# 加载阶段
print('Loading, please wait...')
for i in range(1, 5):
    print(f'Loading: {i * 20}%...')
    time.sleep(0.5)  # 模拟耗时操作，这里延迟500毫秒
print("Loading: 99%...")
time.sleep(2.3)
print("Loading: 100%%...")
os.system('cls')  # 清空控制台输出
print('Loading completed!')
# 加载阶段结束

# 欢迎
print("欢迎使用本脚本，作者qq42072341.\n(请勿使用近战角色，作者测试只用了娜塔莎，其他远程角色自测)")
time.sleep(2)
print("=========================================================")
# 欢迎结束

# 判断用户选择功能
while True:
    choice = input('请选择功能：\n1.锄地\n2.模拟宇宙\n')
    time.sleep(1)
    if choice == '1':
        Map_selection = input("请选择从哪个地图开始：\n1.空间站「黑塔」\n2.雅利洛VI\n3.仙舟「罗浮」\n")
        if Map_selection == '1':
            mapp.is_in_map()
            Btr.planet1()
            Btr.space_station()
        break
    elif choice == '2':
        break
    else:
        print('选择错误，请重新选择')
# 判断用户选择功能结束
# mapp.is_in_map()
# Btr.planet1()
# Btr.space_station()
