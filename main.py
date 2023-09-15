import tkinter as tk
from tkinter import ttk
import spider
import unittest
def search():
    difficulty = difficulty_var.get()
    keyword = keyword_var.get()
    spider.main(difficulty,keyword)


window = tk.Tk()
window.title("CWY的洛谷爬虫程序")

# 难度选择下拉菜单
difficulty_label = tk.Label(window, text="题目难度：")
difficulty_label.grid(column=0, row=0, padx=10, pady=10)
difficulty_var = tk.StringVar(window)
difficulty_choices = ["入门", "普及−", "普及/提高−", "普及+/提高", "提高+/省选−", "省选/NOI−", "NOI/NOI+/CTSC"]
difficulty_var.set(difficulty_choices[0])  # 默认选中第一个选项
difficulty_dropdown = tk.OptionMenu(window, difficulty_var, *difficulty_choices)
difficulty_dropdown.grid(column=1, row=0)

# 关键词输入框
keyword_label = tk.Label(window, text="关键词：")
keyword_label.grid(column=0, row=1, padx=10, pady=10)
keyword_var = tk.StringVar(window)
keyword_entry = tk.Entry(window, textvariable=keyword_var)
keyword_entry.grid(column=1, row=1)

# 算法标签输入框
algorithm_label = tk.Label(window, text="算法标签：")
algorithm_label.grid(column=0, row=2, padx=10, pady=10)
algorithm_var = tk.StringVar(window)
algorithm_entry = tk.Entry(window, textvariable=algorithm_var)
algorithm_entry.grid(column=1, row=2)

# 筛选按钮
search_button = tk.Button(window, text="启动！", command=search)
search_button.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

# 运行GUI窗口
window.mainloop()

if __name__ == '__main__':
    search()