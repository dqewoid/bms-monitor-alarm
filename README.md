# BMS故障监控与告警系统

基于Python + python-can的BMS实时监控系统，自动检测温度/电压/故障码异常，记录告警日志。

## 功能特性

- **实时监控**：循环接收CAN报文，解析DBC信号
- **智能告警**：温度>80°C、故障码≠0时触发告警
- **日志记录**：自动保存异常事件到CSV（时间、温度、故障码、告警内容）
- **统计分析**：分析日志，输出告警次数、最高温度、平均温度

## 运行方法

```bash
pip install python-can cantools
python monitor_alarm.py
python alarm_analysis.py
```
## 测试报告截图

![测试报告1](screenshot-1.png)

![测试报告2](screenshot-2.png)


