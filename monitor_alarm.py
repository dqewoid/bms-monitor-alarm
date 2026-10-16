

import can
import cantools
import csv
import time

# ========== 第一步：加载DBC ==========
db = cantools.database.load_file(r'C:\Users\39154\PycharmProjects\PythonProject\battery_test.dbc')
msg_def = db.get_message_by_name('Battery_Status')
print("DBC加载成功")

# ========== 第二步：打开CAN通道 ==========
bus = can.interface.Bus(interface='virtual', channel='vcan0')
print("CAN通道打开成功")

# ========== 第三步：准备日志文件 ==========
# 用 'w' 模式打开，如果文件不存在就新建，存在就覆盖
log_file = open('alarm_log.csv', 'w', newline='', encoding='utf-8')
log_writer = csv.writer(log_file)
# 写表头
log_writer.writerow(['序号', '时间', '温度(℃)', '故障码', '告警内容'])
print("日志文件已准备")

# ========== 第四步：持续发报文 + 监控 ==========
alarm_count = 0  # 告警计数器

for i in range(20):  # 模拟发20条报文
    # 造数据：温度从60℃逐步升到110℃（每条约+2.6℃）
    temp = int(60 + i * 2.6) + 40  # 原始值 = 实际温度 + 40（因为DBC偏移-40）

    # 保证原始值在0-255之间
    if temp > 255:
        temp = 255

    data = [0x64, 0x00, 0x00, 0x64,  0x00, temp,0x00, 0x00]

    # 发报文
    msg = can.Message(arbitration_id=0x100, data=data, is_extended_id=False)
    bus.send(msg)
    print(f"data 完整内容：{data}")
    print(f"  原始数据: {data}, 温度字节: {data[5]}")

    # 用DBC解析
    decoded = db.decode_message(msg.arbitration_id, msg.data)
    temp = decoded['Temperature']
    fault = decoded['Fault_Code']

    # 打印当前状态
    print(f"第{i + 1}条：温度={temp}℃，故障码={fault}")

    # 判断告警
    alarm_msg = ""
    if temp > 80:
        alarm_msg = f"温度超过80℃！当前={temp}℃"
        alarm_count += 1
        print(f"  ⚠️ 告警：{alarm_msg}")
    if fault != 0:
        alarm_msg += f" | 故障码={fault}"
        print(f"  ⚠️ 故障码异常：{fault}")

    # 如果有告警，写入日志
    if alarm_msg:
        log_writer.writerow([i + 1, time.strftime('%H:%M:%S'), temp, fault, alarm_msg])

    time.sleep(0.1)  # 每条间隔0.1秒，模拟真实报文周期

# ========== 第五步：收尾 ==========
log_file.close()
bus.shutdown()
print(f"\n通道已关闭，共记录 {alarm_count} 条告警，已保存到 alarm_log.csv")










