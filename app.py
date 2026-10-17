import os
import re
from datetime import datetime

# إعدادات المسارات
README_FILE = 'README.md'
DIRECTORIES_TO_SCAN = ['English-Certificates', 'Arabic-Certificates', 'Awards']

def parse_filename(filename):
    """
    استخراج السنة، العنوان، ومزود الشهادة من اسم الملف.
    مثال: 2026-09-Edraak-Data-Science-Machine-Learning.pdf
    """
    # إزالة امتداد الملف
    name = os.path.splitext(filename)[0]
    
    # استخراج السنة (أول 4 أرقام)
    year_match = re.match(r'^(\d{4})', name)
    year = year_match.group(1) if year_match else "Unknown"
    
    # إزالة التاريخ من بداية الاسم
    clean_name = re.sub(r'^\d{4}-\d{2}-', '', name)
    
    # تقسيم الاسم لاستخراج المزود والعنوان (افتراضياً أول كلمة هي المزود)
    parts = clean_name.split('-')
    
    if len(parts) > 1:
        # تنظيف اسم المزود من كلمات مثل Award
        provider = parts[0].replace('Award', '').strip()
        if not provider:
            provider = parts[1]
            title = ' '.join(parts[2:])
        else:
            title = ' '.join(parts[1:])
    else:
        provider = "N/A"
        title = clean_name

    # تحسين شكل العنوان
    title = title.replace('-', ' ')
    
    return year, title, provider

def generate_markdown_table():
    """توليد جدول Markdown بناءً على الملفات الموجودة"""
    table_rows = ["| Year | Title | Provider | File |", "| :--- | :--- | :--- | :--- |"]
    
    for directory in DIRECTORIES_TO_SCAN:
        if not os.path.exists(directory):
            continue
            
        for filename in os.listdir(directory):
            if filename.endswith(('.pdf', '.jpg', '.png')):
                year, title, provider = parse_filename(filename)
                file_path = f"{directory}/{filename}"
                
                # إنشاء رابط للملف
                file_link = f"[View]({file_path})"
                
                # إذا كان الملف صورة للجوائز، نضيف كلمة Award للعنوان
                if directory == 'Awards':
                    title = "🏆 " + title
                    provider = "Ibb University"

                row = f"| {year} | {title} | {provider} | {file_link} |"
                table_rows.append(row)
                
    return "\n".join(table_rows)

def update_readme():
    """تحديث ملف README بالجدول الجديد والتاريخ"""
    if not os.path.exists(README_FILE):
        print(f"Error: {README_FILE} not found.")
        return

    with open(README_FILE, 'r', encoding='utf-8') as file:
        content = file.read()

    # 1. توليد الجدول الجديد
    new_table = generate_markdown_table()

    # 2. تحديث الجدول باستخدام العلامات المخفية (Markers)
    content = re.sub(
        r'<!-- START_TABLE -->.*?<!-- END_TABLE -->',
        f'<!-- START_TABLE -->\n{new_table}\n<!-- END_TABLE -->',
        content,
        flags=re.DOTALL
    )

    # 3. تحديث التاريخ
    current_date = datetime.now().strftime("%Y-%m-%d")
    content = re.sub(
        r'<!-- START_DATE -->.*?<!-- END_DATE -->',
        f'<!-- START_DATE -->{current_date}<!-- END_DATE -->',
        content
    )

    # 4. حفظ الملف
    with open(README_FILE, 'w', encoding='utf-8') as file:
        file.write(content)
        
    print(f"✅ README updated successfully on {current_date}!")

if __name__ == "__main__":
    update_readme()