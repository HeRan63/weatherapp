import json
from datetime import datetime

class WeatherApp:
    def __init__(self):
        # 加载测试数据
        try:
            with open('weather_data.json', 'r', encoding='utf-8') as f:
                self.weather_data = json.load(f)
        except FileNotFoundError:
            self.weather_data = {}

    def get_weather(self, city):
        try:
            # 将城市名转换为首字母大写
            city = city.capitalize()
            if city in self.weather_data:
                return self.format_weather_data(self.weather_data[city])
            else:
                return f"错误: 未找到城市 {city} 的天气数据"
                
        except Exception as e:
            return f"发生错误: {str(e)}"
    
    def format_weather_data(self, data):
        return f"""
城市: {data['name']}
温度: {data['main']['temp']}°C
天气: {data['weather'][0]['description']}
湿度: {data['main']['humidity']}%
风速: {data['wind']['speed']} m/s
        """

def main():
    app = WeatherApp()
    city = input("请输入城市名称 (Beijing/Shanghai/Guangzhou): ")
    weather_info = app.get_weather(city)
    print(weather_info)

if __name__ == "__main__":
    main() 