# SystemStatus
收集多台系统信息，并提供API，可以多种方式展示结果
+ web/html/index.html 前端页面
+ ssd_oled.py 使用ssd1306 oled显示屏显示结果

main.py服务端启动后监听5000端口，启动node.py数据收集节点

node会收集系统信息提交给服务端，服务端通过luma库绘制图形显示在ssd1306上，或者编写index.html显示在浏览器

# 目录说明
+ client 数据收集程序
+ systemd unit文件，用于开启自启动
+ main.py 服务器主程序
