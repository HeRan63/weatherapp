import customtkinter as ctk
import tkinter as tk
from weather_app import WeatherApp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

class WeatherGUI:
    def __init__(self, root):
        # 设置主题颜色模式
        ctk.set_appearance_mode("light")  # 设置外观模式为亮色
        ctk.set_default_color_theme("blue")  # 设置默认颜色主题
        
        self.root = root
        self.root.title("天气预报")
        self.root.geometry("1200x800")
        self.weather_app = WeatherApp()
        
        # 颜色定义
        self.colors = {
            "bg_light": "#F5F5F7",
            "card_bg": "#FFFFFF",
            "primary": "#007AFF",
            "secondary": "#5856D6",
            "text": "#1D1D1F",
            "text_secondary": "#86868B"
        }
        
        # 天气符号映射
        self.weather_symbols = {
            "晴朗": "☀️",
            "多云": "☁️",
            "小雨": "🌧️",
            "中雨": "🌧️"
        }
        
        # 创建主框架
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color=self.colors["bg_light"],
            corner_radius=0
        )
        self.main_frame.pack(fill="both", expand=True)
        
        # 创建界面元素
        self.create_widgets()
        
    def create_widgets(self):
        # 创建左侧面板
        self.left_panel = ctk.CTkFrame(
            self.main_frame,
            width=300,
            corner_radius=20,
            fg_color=self.colors["card_bg"]
        )
        self.left_panel.pack(side="left", fill="y", padx=20, pady=20)
        
        # 城市选择标题
        ctk.CTkLabel(
            self.left_panel,
            text="选择城市",
            font=("SF Pro Display", 20, "bold"),
            text_color=self.colors["text"]
        ).pack(pady=(20, 10))
        
        # 城市选择按钮
        self.city_buttons = []
        for city in self.weather_app.weather_data.keys():
            btn = ctk.CTkButton(
                self.left_panel,
                text=self.weather_app.weather_data[city]["name"],
                font=("SF Pro Display", 14),
                height=40,
                corner_radius=10,
                command=lambda c=city: self.show_weather(c)
            )
            btn.pack(padx=20, pady=5, fill="x")
            self.city_buttons.append(btn)
        
        # 出行建议框
        ctk.CTkLabel(
            self.left_panel,
            text="出行建议",
            font=("SF Pro Display", 20, "bold"),
            text_color=self.colors["text"]
        ).pack(pady=(30, 10))
        
        self.advice_text = ctk.CTkTextbox(
            self.left_panel,
            font=("SF Pro Display", 13),
            width=260,
            height=300,
            corner_radius=10
        )
        self.advice_text.pack(padx=20, pady=10)
        
        # 创建右侧主内容区
        self.right_panel = ctk.CTkFrame(
            self.main_frame,
            corner_radius=20,
            fg_color=self.colors["card_bg"]
        )
        self.right_panel.pack(side="left", fill="both", expand=True, padx=(0, 20), pady=20)
        
        # 创建右侧内容的滚动容器
        self.right_scroll = ctk.CTkScrollableFrame(
            self.right_panel,
            fg_color="transparent"
        )
        self.right_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建天气信息显示区
        self.weather_info = ctk.CTkFrame(
            self.right_scroll,
            corner_radius=15,
            fg_color="transparent",
            height=200  # 限制高度
        )
        self.weather_info.pack(fill="x", padx=20, pady=10)
        
        # 城市名称和天气图标
        self.city_name_label = ctk.CTkLabel(
            self.weather_info,
            text="",
            font=("SF Pro Display", 36, "bold"),
            text_color=self.colors["text"]
        )
        self.city_name_label.pack(pady=(20, 0))
        
        self.weather_icon_label = ctk.CTkLabel(
            self.weather_info,
            text="",
            font=("Segoe UI Emoji", 64)
        )
        self.weather_icon_label.pack()
        
        # 温度显示
        self.temp_label = ctk.CTkLabel(
            self.weather_info,
            text="",
            font=("SF Pro Display", 72, "bold"),
            text_color=self.colors["primary"]
        )
        self.temp_label.pack()
        
        # 创建详细信息网格
        self.details_grid = ctk.CTkFrame(
            self.right_scroll,
            fg_color="transparent",
            height=150  # 限制高度
        )
        self.details_grid.pack(fill="x", padx=20, pady=10)
        
        # 配置网格列的权重，使其均匀分布
        self.details_grid.grid_columnconfigure(0, weight=1)
        self.details_grid.grid_columnconfigure(1, weight=1)
        self.details_grid.grid_columnconfigure(2, weight=1)
        self.details_grid.grid_columnconfigure(3, weight=1)
        
        # 创建四个信息卡片，使用新的布局
        self.create_info_card(self.details_grid, "湿度", "", 0, 0)
        self.create_info_card(self.details_grid, "风速", "", 0, 1)
        self.create_info_card(self.details_grid, "日出日落", "", 0, 2)
        self.create_info_card(self.details_grid, "紫外线", "", 0, 3)
        
        # 创建图表区域
        self.chart_frame = ctk.CTkFrame(
            self.right_scroll,
            corner_radius=15,
            fg_color=self.colors["card_bg"],
            height=300  # 调整高度
        )
        self.chart_frame.pack(fill="x", padx=20, pady=10)
        
        # 创建图表标题
        self.chart_title = ctk.CTkLabel(
            self.chart_frame,
            text="未来2小时天气预测",
            font=("SF Pro Display", 16, "bold"),
            text_color=self.colors["text"]
        )
        self.chart_title.pack(pady=(10, 0))
        
        # 创建用于显示HTML的框架
        self.browser_frame = ctk.CTkFrame(
            self.chart_frame,
            fg_color="transparent"
        )
        self.browser_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建7天预报区域
        self.forecast_label = ctk.CTkLabel(
            self.right_scroll,
            text="7天预报",
            font=("SF Pro Display", 20, "bold"),
            text_color=self.colors["text"]
        )
        self.forecast_label.pack(padx=20, pady=(20, 10), anchor="w")
        
        # 创建7天预报表格框架
        self.forecast_table_frame = ctk.CTkFrame(
            self.right_scroll,
            corner_radius=15,
            fg_color=self.colors["card_bg"]
        )
        self.forecast_table_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # 创建表格列标题
        columns = ["日期", "天气", "最高温", "最低温", "降水概率", "风速"]
        for i, col in enumerate(columns):
            label = ctk.CTkLabel(
                self.forecast_table_frame,
                text=col,
                font=("SF Pro Display", 12, "bold"),  # 加粗标题
                text_color=self.colors["text_secondary"]
            )
            label.grid(row=0, column=i, padx=15, pady=10, sticky="w")
        
        # 设置列宽
        self.forecast_table_frame.grid_columnconfigure(0, weight=2)  # 期
        self.forecast_table_frame.grid_columnconfigure(1, weight=2)  # 天气
        self.forecast_table_frame.grid_columnconfigure(2, weight=1)  # 最高温
        self.forecast_table_frame.grid_columnconfigure(3, weight=1)  # 最低温
        self.forecast_table_frame.grid_columnconfigure(4, weight=1)  # 降水概率
        self.forecast_table_frame.grid_columnconfigure(5, weight=1)  # 风速
        
        # 创建7行用于显示天气数据
        self.forecast_rows = []
        for i in range(7):
            row_labels = []
            for j in range(len(columns)):
                label = ctk.CTkLabel(
                    self.forecast_table_frame,
                    text="",
                    font=("SF Pro Display", 13),
                    text_color=self.colors["text"]
                )
                label.grid(row=i+1, column=j, padx=15, pady=8, sticky="w")
                row_labels.append(label)
            self.forecast_rows.append(row_labels)
        
        # 显示默认城市
        self.show_weather(list(self.weather_app.weather_data.keys())[0])
        
    def create_info_card(self, parent, title, value, row, col):
        frame = ctk.CTkFrame(
            parent,
            corner_radius=15,
            fg_color=self.colors["bg_light"],
            width=150,  # 设置固定宽度
            height=100  # 设置固定高度
        )
        frame.grid(row=row, column=col, padx=10, pady=10)
        frame.grid_propagate(False)  # 防止frame被内容压缩
        
        # 创建内部框架来居中内容
        inner_frame = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )
        inner_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title_label = ctk.CTkLabel(
            inner_frame,
            text=title,
            font=("SF Pro Display", 14),
            text_color=self.colors["text_secondary"]
        )
        title_label.pack(pady=5)
        
        value_label = ctk.CTkLabel(
            inner_frame,
            text=value,
            font=("SF Pro Display", 16, "bold"),
            text_color=self.colors["text"]
        )
        value_label.pack(pady=5)
        
        setattr(self, f"{title}_value_label", value_label)
        
    def update_forecast_chart(self, data):
        # 清除旧图表
        for widget in self.chart_frame.winfo_children():
            if isinstance(widget, tk.Widget) and widget != self.chart_title:
                widget.destroy()
        
        # 创建新图表
        fig = Figure(figsize=(10, 4), dpi=100)
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']  # 设置多个备选字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()
        
        # 获取数据
        times = data['forecast']['times']
        temps = data['forecast']['temperature']
        precip = data['forecast']['precipitation']
        
        # 设置样式
        fig.patch.set_facecolor('none')  # 设置图表背景透明
        ax1.set_facecolor('none')  # 设置绘图区背景透明
        
        # 绘制温度曲线
        line1, = ax1.plot(times, temps, color='#FF6B6B', linewidth=2, marker='o', 
                          markersize=6, label='温度')
        ax1.set_ylabel('温度 (°C)', color='#FF6B6B', fontsize=10, fontproperties='Microsoft YaHei')
        ax1.tick_params(axis='y', labelcolor='#FF6B6B')
        
        # 绘制降水概率曲线
        line2, = ax2.plot(times, precip, color='#4ECDC4', linewidth=2, marker='s', 
                          markersize=6, label='降水概率')
        ax2.set_ylabel('降水概率 (%)', color='#4ECDC4', fontsize=10, fontproperties='Microsoft YaHei')
        ax2.tick_params(axis='y', labelcolor='#4ECDC4')
        
        # 设置网格
        ax1.grid(True, linestyle='--', alpha=0.3)
        
        # 设置x轴标签
        ax1.set_xlabel('时间', fontsize=10, fontproperties='Microsoft YaHei')
        
        # 旋转x轴标签
        plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
        
        # 添加图例
        lines = [line1, line2]
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper right', frameon=True, 
                  facecolor='white', edgecolor='none', fontsize=9,
                  prop={'family': 'Microsoft YaHei'})  # 设置图例字体
        
        # 调整布局
        fig.tight_layout()
        
        # 创建canvas并显示
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def update_weekly_forecast(self, data):
        """更新7天预报表格"""
        for i, day in enumerate(data['weekly_forecast']):
            row = self.forecast_rows[i]
            weather_symbol = self.weather_symbols.get(day['description'], "❓")
            
            # 更新每一行的数据
            row[0].configure(text=day['date'])  # 日期
            row[1].configure(text=f"{weather_symbol} {day['description']}")  # 天气
            row[2].configure(text=f"{day['max_temp']}°C")  # 最高温
            row[3].configure(text=f"{day['min_temp']}°C")  # 最低温
            row[4].configure(text=f"{day['rain_prob']}%")  # 降水概率
            row[5].configure(text=f"{day['wind_speed']} m/s")  # 风速
    
    def get_uv_description(self, uv_index):
        if uv_index <= 2:
            return "低"
        elif uv_index <= 5:
            return "中等"
        elif uv_index <= 7:
            return "高"
        elif uv_index <= 10:
            return "很高"
        else:
            return "极高"
    
    def get_travel_advice(self, weather_data):
        """根据天气数据生成出行建议"""
        weather = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        uv_index = weather_data['weekly_forecast'][0]['uv_index']
        rain_prob = weather_data['weekly_forecast'][0]['rain_prob']
        
        advice = []
        
        # 基于温度的建议
        if temp >= 30:
            advice.append("• 天气炎热，注意防暑降温")
            advice.append("• 建议随身携带水壶补充水分")
        elif temp <= 10:
            advice.append("• 天气较冷，注意保暖")
            advice.append("• 建议穿着厚实的衣物")
        
        # 基于天气状况的建议
        if weather == "晴朗":
            advice.append("• 天气晴好，适合外出活动")
            if uv_index >= 7:
                advice.append("• 紫外线强烈，注意防晒")
        elif weather == "多云":
            advice.append("• 天气较好，适合外出")
            advice.append("• 建议随身携带薄外套")
        elif weather in ["小雨", "中雨"]:
            advice.append("• 记得携带雨具")
            advice.append("• 道路可能湿滑，注意安全")
        
        # 基于降水概率的建议
        if rain_prob > 50:
            advice.append("• 降水概率较大，建议带伞")
        
        # 基于紫外线的建议
        if uv_index <= 2:
            advice.append("• 紫外线弱，适合外出活动")
        elif uv_index <= 5:
            advice.append("• 紫外线中等，建议涂抹防晒霜")
        elif uv_index <= 7:
            advice.append("• 紫外线较强，建议做好防晒措施")
        else:
            advice.append("• 紫外线很强，尽量减少外出")
        
        return "\n".join(advice)
    
    def show_weather(self, city):
        # 获取天气数据
        data = self.weather_app.weather_data[city]
        weather_type = data['weather'][0]['description']
        today_data = data['weekly_forecast'][0]  # 获取今天的预报数据
        
        # 更新背景颜色
        bg_color = self.get_background_color(weather_type)
        self.main_frame.configure(fg_color=bg_color)  # 更新主框架背景色
        
        # 更新天气符号
        weather_symbol = self.weather_symbols.get(weather_type, "❓")
        self.weather_icon_label.configure(text=weather_symbol)
        
        # 更新显示
        self.city_name_label.configure(text=data['name'])
        self.temp_label.configure(text=f"{data['main']['temp']}°C")
        
        # 更新信息卡片的值
        getattr(self, "湿度_value_label").configure(
            text=f"{data['main']['humidity']}%"
        )
        getattr(self, "风速_value_label").configure(
            text=f"{data['wind']['speed']} m/s"
        )
        getattr(self, "日出日落_value_label").configure(
            text=f"{today_data['sunrise']} - {today_data['sunset']}"
        )
        
        uv_desc = self.get_uv_description(today_data['uv_index'])
        getattr(self, "紫外线_value_label").configure(
            text=f"{today_data['uv_index']} ({uv_desc})"
        )
        
        # 更新预测图表
        self.update_forecast_chart(data)
        
        # 更新7天预报
        self.update_weekly_forecast(data)
        
        # 更新出行建议
        preset_advice = "\n".join(data['travel_advice'])
        self.advice_text.configure(state="normal")
        self.advice_text.delete("0.0", "end")
        self.advice_text.insert("0.0", preset_advice)
        self.advice_text.configure(state="disabled")
    
    def get_background_color(self, weather_type):
        """根据天气类型返回背景颜色"""
        if "晴" in weather_type:
            return "#87CEEB"  # 天蓝色
        elif "云" in weather_type:
            return "#B0C4DE"  # 淡钢蓝
        elif "雨" in weather_type:
            return "#A9A9A9"  # 灰色
        elif "雪" in weather_type:
            return "#FFFFFF"  # 白色
        else:
            return "#F0F2F6"  # 默认背景色

def main():
    root = ctk.CTk()
    app = WeatherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 