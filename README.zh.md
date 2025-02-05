
# DayTrade Analyzer Web

这是一个用于日内交易分析和模拟的Web 应用程序。支持获取美股数据、展示 K 线图及技术指标，并进行交易模拟。

## 功能特点

- **数据获取：**  
  获取美股数据（1 分钟间隔，最近 7 天）。
- **数据展示：**  
  绘制 K 线图并显示技术指标（如 MA、MACD、RSI 等）。
- **交易模拟：**  
  针对最多 5 个日期进行交易模拟，输入买入价格、止损百分比和止盈百分比。
- **灵活的数据存储：**  
  数据可存入 CSV 文件或 PostgreSQL 数据库，配置通过 `config.yaml` 文件进行。

## 安装说明

1. 克隆仓库：
   ```bash
   git clone git@github.com:nineteenwj/DaytradeAnalyzerWeb.git
   cd DaytradeAnalyzerWeb
2. 创建并激活虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或者
   venv\Scripts\activate     # Windows
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
4. 编辑 config.yaml，选择存储方式（"csv" 或 "postgres"）并设置数据库参数。
5. 如果使用 PostgreSQL，请在 daytradeanalyzerweb/settings.py 中更新 DATABASES 设置。
6. 执行数据库迁移：
   ```bash
   python manage.py migrate
7. 启动开发服务器：
   ```bash
   python manage.py runserver
8. 在浏览器中打开 http://localhost:8000。

## 使用方法
- 在主页中，输入股票代码并选择日期范围。
- 点击 Get Stock Data 获取并存储数据。
- 数据展示区会显示 K 线图及技术指标。
- 右侧的交易模拟面板允许用户针对 5 个日期进行模拟交易，选择日期（下拉菜单）并输入买入价格、止损和止盈百分比。
- 点击 Simulate All 执行交易模拟，结果会显示在相应位置。

## 配置说明
配置文件 config.yaml 控制数据存储方式：
- storage_method：可选 "csv" 或 "postgres"
- csv_data_dir：CSV 文件存储目录
- database：PostgreSQL 数据库连接参数（当 storage_method 为 "postgres" 时使用）

## 许可证
本项目采用 GNU 通用公共许可证 v3.0。
