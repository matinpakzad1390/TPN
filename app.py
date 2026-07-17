import json
import os # اضافه شد برای چک کردن وجود فایل
from flask import Flask, request, render_template

app = Flask(__name__)

# بارگذاری اطلاعات کاربران
try:
    with open('users.json', 'r', encoding='utf-8') as f:
        user_data = json.load(f)
except Exception as e:
    print(f"خطا در خواندن فایل JSON: {e}")
    user_data = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        code = request.form.get("code")
        user_info = user_data.get(code)

        if user_info:
            template_name = user_info["template"]
            # --- بخش جادویی برای عیب‌یابی ---
            template_path = os.path.join(app.template_folder, template_name)
            
            if not os.path.exists(template_path):
                return f"خطای سیستم: فایل قالب '{template_name}' پیدا نشد! برو توی پوشه templates و چک کن ببین اسمش درسته یا نه. 🧐"
            # ------------------------------

            return render_template(template_name, 
                                   display_name=user_info.get("display_name", "کاربر"),
                                   details=user_info.get("details", ""))
        else:
            return "کد اشتباهه! دوباره تلاش کن. 🧐"
            
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
