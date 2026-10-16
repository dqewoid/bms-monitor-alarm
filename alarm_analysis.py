import csv

# 读CSV
with open('alarm_log.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = [row for row in reader if row['序号']]  # 过滤空行

# 统计
total_alarms = len(rows)
temperatures = [float(row['温度(℃)']) for row in rows]
max_temp = max(temperatures)
avg_temp = sum(temperatures) / len(temperatures)

# 输出
print(f"告警总次数：{total_alarms}")
print(f"最高温度：{max_temp}℃")
print(f"平均温度：{avg_temp:.1f}℃")