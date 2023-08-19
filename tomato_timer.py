#!/usr/bin/env python3

import subprocess
import sys
import termios
import time
import tty

import pyfiglet  # type: ignore

# 初始化 ASCII 字体渲染器
figlet = pyfiglet.Figlet(font="doh")

caffeinate_process = subprocess.Popen(["caffeinate", "-i"])

# 全局变量
completed_tomatoes = 0
tomato_time = 25  # 默认番茄时间为25分钟
rest_time = 5  # 默认休息时间为5分钟

# 鼓励语句列表
encouragements = [
    "今天的专注将为明天的成就做铺垫。",
    "坚持是成功的秘诀，你正在走在正确的道路上。",
    "专注让你的才华发光发热，继续前进吧！",
    "每个番茄都是你成功的一小步。",
    "专注是实现梦想的钥匙，继续锁定目标吧！",
    "每个专注的瞬间都是你成长的见证。",
    "相信自己，专注不止是目标，更是旅程。",
    "今天的努力是明天自己最好的礼物。",
    "坚持专注，你的梦想就在不远处。",
    "你的决心，将为你创造无限可能。",
]

def set_timer_values():
    """
    设置番茄时间和休息时间的值。
    """
    global tomato_time, rest_time
    tomato_time = int(input("请输入番茄时间（分钟）："))
    rest_time = int(input("请输入休息时间（分钟）："))

def get_key():
    """
    获取按键输入。
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def say_and_print(message):
    """
    打印消息并使用 'say' 命令朗读消息。
    """
    print(message)
    subprocess.run(["say", message])

def display_time(minutes_left, seconds_left):
    """
    显示剩余时间的 ASCII 艺术数字。
    """
    time_display = f"{minutes_left} : {seconds_left}"
    ascii_time = figlet.renderText(time_display)
    message = f"番茄时间剩余：\n{ascii_time}"
    subprocess.run(["clear"])  # 清除屏幕内容
    print(message)

def tomato_timer(minutes):
    """
    番茄计时器。
    """
    global completed_tomatoes
    completed_tomatoes += 1

    start_time = time.time()
    end_time = start_time + minutes * 60

    encouragement_index = completed_tomatoes % len(encouragements)
    encouragement = encouragements[encouragement_index]

    message = f"现在开始第 {completed_tomatoes} 个番茄！{encouragement}"
    say_and_print(message)

    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        minutes_left = remaining_time // 60
        seconds_left = remaining_time % 60
        display_time(minutes_left, seconds_left)
        time.sleep(1)

    message = "番茄时间结束！请操作电脑。"
    say_and_print(message)

    choice = input("按下回车继续，按下 'q' 后回车退出：")
    if choice == "q":
        message = "好的，下次再见！"
        say_and_print(message)
        global caffeinate_process
        caffeinate_process.terminate()
        sys.exit()
    else:
        message = f"你已经完成了 {completed_tomatoes} 个番茄，继续加油！"
        say_and_print(message)
        message = f"休息一下，{rest_time}分钟后进入下一轮番茄时间！"
        say_and_print(message)

        remaining_time = rest_time * 60
        while remaining_time > 0:
            minutes_left = remaining_time // 60
            seconds_left = remaining_time % 60
            display_time(minutes_left, seconds_left)
            time.sleep(1)
            remaining_time -= 1

            if remaining_time == 14:
                for _ in range(5):
                    subprocess.run(["afplay", "/System/Library/Sounds/Submarine.aiff"])

        message = "休息时间结束！请操作电脑。"
        say_and_print(message)
        _ = input("按下回车继续：")
        tomato_timer(tomato_time)

if __name__ == "__main__":
    # 设置番茄时间和休息时间
    set_timer_values()
    
    # 启动番茄计时器
    tomato_timer(tomato_time)
