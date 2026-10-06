import os
import io
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
if not os.path.exists(FONT_BOLD_PATH):
    FONT_BOLD_PATH = FONT_PATH

def get_font(size, bold=False):
    path = FONT_BOLD_PATH if bold else FONT_PATH
    try:
        return ImageFont.truetype(path, int(size))
    except Exception:
        return ImageFont.load_default()

def render_chart(fig, target_w, target_h):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", transparent=True, dpi=300)
    plt.close(fig)
    buf.seek(0)
    img = Image.open(buf).convert("RGBA")
    return img.resize((target_w, target_h), Image.Resampling.LANCZOS)

# ==============================================================================
# 1. RENDER SUMMARY DASHBOARD
# ==============================================================================
def render_summary():
    bg = Image.open("powerbi/assets/templates/Summary_template.png").convert("RGBA")
    draw = ImageDraw.Draw(bg)

    # 1.1 Top KPI Numbers
    draw.text((125, 128), "6,418", fill="#FFFFFF", font=get_font(42, bold=True), anchor="mm")
    draw.text((125, 172), "Total Customers", fill="#E2E4FF", font=get_font(13), anchor="mm")

    draw.text((370, 128), "411", fill="#FFFFFF", font=get_font(42, bold=True), anchor="mm")
    draw.text((370, 172), "New Joiners", fill="#E2E4FF", font=get_font(13), anchor="mm")

    draw.text((615, 128), "1,732", fill="#FFFFFF", font=get_font(42, bold=True), anchor="mm")
    draw.text((615, 172), "Total Churn", fill="#E2E4FF", font=get_font(13), anchor="mm")

    draw.text((855, 128), "27.0%", fill="#FFFFFF", font=get_font(42, bold=True), anchor="mm")
    draw.text((855, 172), "Churn Rate", fill="#E2E4FF", font=get_font(13), anchor="mm")

    # Header Dropdowns & Action Button
    draw.rounded_rectangle([720, 24, 830, 48], radius=4, outline="#D0D0D0", fill="#FFFFFF")
    draw.text((728, 27), "Monthly Charge...", fill="#888888", font=get_font(7))
    draw.text((728, 36), "All", fill="#222222", font=get_font(9))
    draw.text((818, 34), "▼", fill="#888888", font=get_font(7))

    draw.rounded_rectangle([845, 24, 945, 48], radius=4, outline="#D0D0D0", fill="#FFFFFF")
    draw.text((853, 27), "Married", fill="#888888", font=get_font(7))
    draw.text((853, 36), "All", fill="#222222", font=get_font(9))
    draw.text((933, 34), "▼", fill="#888888", font=get_font(7))

    draw.rounded_rectangle([960, 22, 1100, 50], radius=5, fill="#0F101E")
    draw.text((1030, 36), "Churn Prediction", fill="#FFFFFF", font=get_font(10, bold=True), anchor="mm")

    # 1.2 Demographic: Total Churn by Gender (Donut Chart)
    draw.text((45, 252), "Total Churn by Gender", fill="#2B2B36", font=get_font(10, bold=True))
    
    fig, ax = plt.subplots(figsize=(2.0, 2.0))
    fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    wedges, _ = ax.pie([621, 1111], colors=['#8A85FF', '#2B26D9'], startangle=140,
                       wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2))
    ax.axis('equal')
    donut_img = render_chart(fig, 130, 130)
    bg.paste(donut_img, (55, 278), donut_img)

    # Donut center icons
    ico_gender = Image.open("powerbi/assets/icons/Ico_Gender.png").convert("RGBA").resize((26, 26))
    bg.paste(ico_gender, (107, 330), ico_gender)

    # Labels around donut
    draw.text((50, 275), "621\n(35.85%)", fill="#555555", font=get_font(7.5))
    draw.text((115, 408), "1,111 (64.15%)", fill="#555555", font=get_font(7.5))

    # Legend
    draw.text((195, 310), "Gender", fill="#666666", font=get_font(8.5, bold=True))
    draw.ellipse([195, 330, 203, 338], fill="#8A85FF")
    draw.text((210, 328), "Female", fill="#333333", font=get_font(8.5))
    draw.ellipse([195, 350, 203, 358], fill="#2B26D9")
    draw.text((210, 348), "Male", fill="#333333", font=get_font(8.5))

    # 1.3 Demographic: Total Customers & Churn Rate by Age Group (Combo Chart)
    draw.text((315, 252), "Total Customers and Churn Rate by Age Group", fill="#2B2B36", font=get_font(10, bold=True))
    
    fig, ax1 = plt.subplots(figsize=(3.5, 1.45))
    fig.subplots_adjust(left=0.08, right=0.88, top=0.88, bottom=0.20)
    ages = ['<20', '20-35', '36-50', '>50']
    cust = [0.1, 1.6, 1.8, 2.8]
    rate = [23.5, 23.5, 24.0, 31.0]

    bars = ax1.bar(ages, cust, color='#2B26D9', width=0.42)
    ax1.set_ylim(0, 3.8)
    ax1.set_yticks([])
    ax1.tick_params(axis='x', labelsize=7.5, pad=2)
    for b in bars:
        ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 0.1, f"{b.get_height():.1f}K",
                 ha='center', va='bottom', fontsize=6.5, color='#444444')

    ax2 = ax1.twinx()
    ax2.plot(ages, rate, color='#0D0A54', marker='o', linewidth=1.8, markersize=3.5)
    ax2.set_ylim(10, 42)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ax2.tick_params(axis='y', labelsize=6.5, pad=1)
    for i, txt in enumerate(rate):
        y_offset = 2.2 if i == 0 else 1.3
        ax2.annotate(f"{txt:.1f}%", (ages[i], rate[i] + y_offset), fontsize=6.5, ha='center', color='#0D0A54')

    for s in ax1.spines.values(): s.set_visible(False)
    for s in ax2.spines.values(): s.set_visible(False)
    combo_age = render_chart(fig, 340, 140)
    bg.paste(combo_age, (315, 275), combo_age)

    # 1.4 Account Info: Churn Rate by Payment Method
    draw.text((45, 452), "Churn Rate by Payment Method", fill="#2B2B36", font=get_font(9.5, bold=True))
    fig, ax = plt.subplots(figsize=(2.6, 0.9))
    fig.subplots_adjust(left=0.38, right=0.82, top=0.95, bottom=0.1)
    p_names = ['Credit Card', 'Bank Withdr...', 'Mailed Check']
    p_vals = [14.8, 34.4, 37.8]
    bars = ax.barh(p_names, p_vals, color='#2B26D9', height=0.52)
    ax.set_xlim(0, 48)
    ax.tick_params(axis='y', labelsize=7, pad=2)
    ax.xaxis.set_visible(False)
    for s in ax.spines.values(): s.set_visible(False)
    for b in bars:
        ax.text(b.get_width() + 1.2, b.get_y() + b.get_height()/2, f"{b.get_width():.1f}%",
                ha='left', va='center', fontsize=6.5, color='#222222')
    p_img = render_chart(fig, 260, 90)
    bg.paste(p_img, (35, 470), p_img)

    # 1.5 Account Info: Churn Rate by Contract
    draw.text((45, 575), "Churn Rate by Contract", fill="#2B2B36", font=get_font(9.5, bold=True))
    fig, ax = plt.subplots(figsize=(2.6, 0.9))
    fig.subplots_adjust(left=0.38, right=0.82, top=0.95, bottom=0.1)
    c_names = ['Two Year', 'One Year', 'Month-to-M...']
    c_vals = [2.7, 11.0, 46.5]
    bars = ax.barh(c_names, c_vals, color='#2B26D9', height=0.52)
    ax.set_xlim(0, 58)
    ax.tick_params(axis='y', labelsize=7, pad=2)
    ax.xaxis.set_visible(False)
    for s in ax.spines.values(): s.set_visible(False)
    for b in bars:
        ax.text(b.get_width() + 1.2, b.get_y() + b.get_height()/2, f"{b.get_width():.1f}%",
                ha='left', va='center', fontsize=6.5, color='#222222')
    c_img = render_chart(fig, 260, 90)
    bg.paste(c_img, (35, 595), c_img)

    # 1.6 Account Info: Tenure Group Combo Chart
    draw.text((320, 452), "Total Customers and Churn Rate by Tenure Group", fill="#2B2B36", font=get_font(9.5, bold=True))
    fig, ax1 = plt.subplots(figsize=(3.4, 2.0))
    fig.subplots_adjust(left=0.08, right=0.88, top=0.90, bottom=0.22)
    t_names = ['< 6\nMonths', '6-12\nMonths', '12-18\nMonths', '18-24\nMonths', '>= 24\nMonths']
    t_c = [1058, 1296, 997, 980, 2087]
    t_r = [26.4, 27.2, 26.1, 27.2, 27.5]

    bars = ax1.bar(t_names, t_c, color='#2B26D9', width=0.5)
    ax1.set_ylim(0, 2600)
    ax1.set_yticks([])
    ax1.tick_params(axis='x', labelsize=6.5, pad=2)
    for b in bars:
        ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 40, f"{int(b.get_height()):,}",
                 ha='center', va='bottom', fontsize=6, color='#444444')

    ax2 = ax1.twinx()
    ax2.plot(t_names, t_r, color='#0D0A54', marker='o', linewidth=1.8, markersize=3.2)
    ax2.set_ylim(25.0, 28.5)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
    ax2.tick_params(axis='y', labelsize=6, pad=1)
    for i, txt in enumerate(t_r):
        ax2.annotate(f"{txt:.1f}%", (t_names[i], t_r[i] + 0.12), fontsize=6, ha='center', color='#0D0A54')

    for s in ax1.spines.values(): s.set_visible(False)
    for s in ax2.spines.values(): s.set_visible(False)
    tenure_img = render_chart(fig, 335, 220)
    bg.paste(tenure_img, (315, 475), tenure_img)

    # 1.7 Geographic: Churn Rate by State (Top 5)
    draw.text((688, 256), "Churn Rate by State (Top 5)", fill="#2B2B36", font=get_font(9.5, bold=True))
    fig, ax = plt.subplots(figsize=(2.4, 1.30))
    fig.subplots_adjust(left=0.38, right=0.82, top=0.95, bottom=0.08)
    s_names = ['Delhi', 'Chhattis...', 'Jharkhand', 'Assam', 'Jammu ...']
    s_vals = [29.9, 30.5, 34.5, 38.1, 57.2]
    bars = ax.barh(s_names, s_vals, color='#2B26D9', height=0.55)
    ax.set_xlim(0, 72)
    ax.tick_params(axis='y', labelsize=6.8, pad=2)
    ax.xaxis.set_visible(False)
    for s in ax.spines.values(): s.set_visible(False)
    for b in bars:
        ax.text(b.get_width() + 1.2, b.get_y() + b.get_height()/2, f"{b.get_width():.1f}%",
                ha='left', va='center', fontsize=6.8, color='#222222')
    state_img = render_chart(fig, 240, 135)
    bg.paste(state_img, (682, 280), state_img)

    # 1.8 Churn Distribution: Total Churn by Churn Category
    draw.text((688, 458), "Total Churn by Churn Category", fill="#2B2B36", font=get_font(9.5, bold=True))
    fig, ax = plt.subplots(figsize=(2.4, 1.85))
    fig.subplots_adjust(left=0.36, right=0.82, top=0.95, bottom=0.08)
    c_cats = ['Other', 'Price', 'Dissatisf...', 'Attitude', 'Compet...']
    c_nums = [174, 196, 300, 301, 761]
    bars = ax.barh(c_cats, c_nums, color='#2B26D9', height=0.55)
    ax.set_xlim(0, 950)
    ax.tick_params(axis='y', labelsize=6.8, pad=2)
    ax.xaxis.set_visible(False)
    for s in ax.spines.values(): s.set_visible(False)
    for b in bars:
        ax.text(b.get_width() + 15, b.get_y() + b.get_height()/2, f"{int(b.get_width()):,}",
                ha='left', va='center', fontsize=6.8, color='#222222')
    cat_img = render_chart(fig, 240, 210)
    bg.paste(cat_img, (682, 480), cat_img)

    # 1.9 Services Used: Churn Rate by Internet Type
    draw.text((958, 256), "Churn Rate by Internet Type", fill="#2B2B36", font=get_font(9.5, bold=True))
    fig, ax = plt.subplots(figsize=(2.9, 0.95))
    fig.subplots_adjust(left=0.32, right=0.84, top=0.95, bottom=0.08)
    i_names = ['None', 'DSL', 'Cable', 'Fiber Optic']
    i_vals = [7.8, 19.4, 25.7, 41.1]
    bars = ax.barh(i_names, i_vals, color='#2B26D9', height=0.52)
    ax.set_xlim(0, 52)
    ax.tick_params(axis='y', labelsize=7, pad=2)
    ax.xaxis.set_visible(False)
    for s in ax.spines.values(): s.set_visible(False)
    for b in bars:
        ax.text(b.get_width() + 1.2, b.get_y() + b.get_height()/2, f"{b.get_width():.1f}%",
                ha='left', va='center', fontsize=6.8, color='#222222')
    inet_img = render_chart(fig, 295, 95)
    bg.paste(inet_img, (955, 278), inet_img)

    # 1.10 Services Used: Churn by Services Table
    draw.text((958, 385), "Churn by Services", fill="#2B2B36", font=get_font(9.5, bold=True))

    draw.rectangle([955, 404, 1260, 422], fill="#2B26D9")
    draw.text((962, 408), "Services", fill="#FFFFFF", font=get_font(7.8, bold=True))
    draw.text((1165, 408), "No", fill="#FFFFFF", font=get_font(7.8, bold=True))
    draw.text((1220, 408), "Yes", fill="#FFFFFF", font=get_font(7.8, bold=True))

    services_data = [
        ("Device_Protection_Plan", "71.0%", "29.0%"),
        ("Internet_Service", "6.3%", "93.7%"),
        ("Multiple_Lines", "54.8%", "45.2%"),
        ("Online_Backup", "71.9%", "28.1%"),
        ("Online_Security", "84.6%", "15.4%"),
        ("Paperless_Billing", "25.4%", "74.6%"),
        ("Phone_Service", "9.4%", "90.6%"),
        ("Premium_Support", "83.5%", "16.5%"),
        ("Streaming_Movies", "56.0%", "44.0%"),
        ("Streaming_Music", "61.1%", "38.9%"),
        ("Streaming_TV", "56.8%", "43.2%"),
    ]

    y_pos = 423
    for i, (name, n_val, y_val) in enumerate(services_data):
        row_bg = "#F3F5FD" if i % 2 == 1 else "#FFFFFF"
        draw.rectangle([955, y_pos, 1260, y_pos + 17], fill=row_bg)
        draw.text((962, y_pos + 3), name, fill="#222222", font=get_font(7.5))
        draw.text((1165, y_pos + 3), n_val, fill="#444444", font=get_font(7.5))
        draw.text((1220, y_pos + 3), y_val, fill="#444444", font=get_font(7.5))
        y_pos += 18

    out_file = "powerbi/assets/Summary.png"
    bg.save(out_file, "PNG")
    print("Summary rendered:", out_file)


# ==============================================================================
# 2. RENDER PREDICTION DASHBOARD
# ==============================================================================
def render_prediction():
    bg = Image.open("powerbi/assets/templates/Prediction_template.png").convert("RGBA")
    draw = ImageDraw.Draw(bg)

    # 2.1 Top Banner KPI Callout
    draw.rounded_rectangle([400, 18, 880, 68], radius=8, fill="#0F101E")
    draw.text((640, 43), "COUNT OF PREDICTED CHURNERS : 381", fill="#FFFFFF", font=get_font(18, bold=True), anchor="mm")

    # 2.2 Left Area (Blue Background): PREDICTED CHURNER PROFILE
    # Card 1: Demographics
    draw.rounded_rectangle([25, 120, 695, 290], radius=8, fill="#FFFFFF")
    draw.text((38, 128), "DEMOGRAPHIC BREAKDOWN", fill="#2B26D9", font=get_font(10.5, bold=True))

    # Gender Bar
    fig, ax = plt.subplots(figsize=(1.6, 1.1))
    fig.subplots_adjust(left=0.25, right=0.9, top=0.88, bottom=0.22)
    genders = ['Male', 'Female']
    g_counts = [132, 249]
    bars = ax.bar(genders, g_counts, color=['#8A85FF', '#2B26D9'], width=0.48)
    ax.set_ylim(0, 310)
    ax.tick_params(axis='x', labelsize=7.5, pad=2)
    ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    for b in bars:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 10, f"{int(b.get_height())}",
                ha='center', fontsize=7.5, color='#333333', fontweight='bold')
    g_img = render_chart(fig, 150, 110)
    bg.paste(g_img, (35, 155), g_img)
    draw.text((85, 150), "Gender", fill="#555555", font=get_font(8.5, bold=True))

    # Marital Status Bar
    fig, ax = plt.subplots(figsize=(1.6, 1.1))
    fig.subplots_adjust(left=0.25, right=0.9, top=0.88, bottom=0.22)
    marital = ['Married', 'Single']
    m_counts = [188, 193]
    bars = ax.bar(marital, m_counts, color=['#5B56F6', '#2B26D9'], width=0.48)
    ax.set_ylim(0, 240)
    ax.tick_params(axis='x', labelsize=7.5, pad=2)
    ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    for b in bars:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 8, f"{int(b.get_height())}",
                ha='center', fontsize=7.5, color='#333333', fontweight='bold')
    m_img = render_chart(fig, 150, 110)
    bg.paste(m_img, (225, 155), m_img)
    draw.text((260, 150), "Marital Status", fill="#555555", font=get_font(8.5, bold=True))

    # Age Group Bar
    fig, ax = plt.subplots(figsize=(2.5, 1.1))
    fig.subplots_adjust(left=0.15, right=0.92, top=0.88, bottom=0.22)
    ages = ['< 20', '20-35', '36-50', '> 50']
    a_counts = [12, 112, 130, 127]
    bars = ax.bar(ages, a_counts, color='#2B26D9', width=0.48)
    ax.set_ylim(0, 160)
    ax.tick_params(axis='x', labelsize=7.5, pad=2)
    ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    for b in bars:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 5, f"{int(b.get_height())}",
                ha='center', fontsize=7.5, color='#333333', fontweight='bold')
    a_img = render_chart(fig, 240, 110)
    bg.paste(a_img, (430, 155), a_img)
    draw.text((505, 150), "Age Group", fill="#555555", font=get_font(8.5, bold=True))

    # Card 2: Account & Payment Profile
    draw.rounded_rectangle([25, 305, 695, 490], radius=8, fill="#FFFFFF")
    draw.text((38, 313), "ACCOUNT & PAYMENT PROFILE", fill="#2B26D9", font=get_font(10.5, bold=True))

    # Contract Horizontal Bar
    fig, ax = plt.subplots(figsize=(2.0, 1.25))
    fig.subplots_adjust(left=0.42, right=0.82, top=0.95, bottom=0.12)
    c_types = ['Two Year', 'One Year', 'Month-to-M.']
    c_vals = [6, 18, 357]
    bars = ax.barh(c_types, c_vals, color='#2B26D9', height=0.52)
    ax.set_xlim(0, 420)
    ax.tick_params(axis='y', labelsize=7.5, pad=2)
    ax.xaxis.set_visible(False)
    for s in ax.spines.values(): s.set_visible(False)
    for b in bars:
        ax.text(b.get_width() + 8, b.get_y() + b.get_height()/2, f"{int(b.get_width())}",
                ha='left', va='center', fontsize=7.5, color='#222222', fontweight='bold')
    ct_img = render_chart(fig, 190, 125)
    bg.paste(ct_img, (35, 345), ct_img)
    draw.text((70, 335), "Contract", fill="#555555", font=get_font(8.5, bold=True))

    # Payment Method Horizontal Bar
    fig, ax = plt.subplots(figsize=(2.1, 1.25))
    fig.subplots_adjust(left=0.42, right=0.82, top=0.95, bottom=0.12)
    pm_types = ['Mailed Check', 'Bank Withdr.', 'Credit Card']
    pm_vals = [37, 150, 194]
    bars = ax.barh(pm_types, pm_vals, color='#2B26D9', height=0.52)
    ax.set_xlim(0, 240)
    ax.tick_params(axis='y', labelsize=7.5, pad=2)
    ax.xaxis.set_visible(False)
    for s in ax.spines.values(): s.set_visible(False)
    for b in bars:
        ax.text(b.get_width() + 6, b.get_y() + b.get_height()/2, f"{int(b.get_width())}",
                ha='left', va='center', fontsize=7.5, color='#222222', fontweight='bold')
    pm_img = render_chart(fig, 205, 125)
    bg.paste(pm_img, (250, 345), pm_img)
    draw.text((285, 335), "Payment Method", fill="#555555", font=get_font(8.5, bold=True))

    # Tenure Group Column Bar
    fig, ax = plt.subplots(figsize=(2.0, 1.25))
    fig.subplots_adjust(left=0.15, right=0.92, top=0.88, bottom=0.22)
    t_grps = ['<6M', '6-12M', '12-18M', '18-24M', '>=24M']
    t_vals = [86, 83, 65, 60, 87]
    bars = ax.bar(t_grps, t_vals, color='#5B56F6', width=0.5)
    ax.set_ylim(0, 110)
    ax.tick_params(axis='x', labelsize=6.8, pad=2)
    ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    for b in bars:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 3, f"{int(b.get_height())}",
                ha='center', fontsize=7, color='#222222', fontweight='bold')
    tg_img = render_chart(fig, 200, 125)
    bg.paste(tg_img, (475, 345), tg_img)
    draw.text((515, 335), "Tenure Group", fill="#555555", font=get_font(8.5, bold=True))

    # Card 3: Top States Horizontal Bar
    draw.rounded_rectangle([25, 505, 695, 690], radius=8, fill="#FFFFFF")
    draw.text((38, 513), "GEOGRAPHIC BREAKDOWN - TOP 5 STATES", fill="#2B26D9", font=get_font(10.5, bold=True))

    fig, ax = plt.subplots(figsize=(5.8, 1.35))
    fig.subplots_adjust(left=0.25, right=0.85, top=0.95, bottom=0.10)
    top_states = ['Andhra Pradesh', 'Karnataka', 'Tamil Nadu', 'Maharashtra', 'Uttar Pradesh']
    s_vals = [24, 30, 37, 41, 45]
    bars = ax.barh(top_states, s_vals, color='#2B26D9', height=0.55)
    ax.set_xlim(0, 56)
    ax.tick_params(axis='y', labelsize=8, pad=3)
    ax.xaxis.set_visible(False)
    for s in ax.spines.values(): s.set_visible(False)
    for b in bars:
        ax.text(b.get_width() + 1.2, b.get_y() + b.get_height()/2, f"{int(b.get_width())} Churners",
                ha='left', va='center', fontsize=8, color='#333333', fontweight='bold')
    top_s_img = render_chart(fig, 580, 140)
    bg.paste(top_s_img, (60, 535), top_s_img)

    # 2.3 Right Area (White Container): CUSTOMERS AT RISK
    draw.text((740, 120), "PREDICTED HIGH-RISK JOINERS (TOP 18 OF 381)", fill="#1E202A", font=get_font(11, bold=True))

    # Table Header
    draw.rectangle([730, 142, 1255, 166], fill="#2B26D9")
    draw.text((742, 149), "Customer ID", fill="#FFFFFF", font=get_font(8.5, bold=True))
    draw.text((860, 149), "Monthly Charge", fill="#FFFFFF", font=get_font(8.5, bold=True))
    draw.text((980, 149), "Total Revenue", fill="#FFFFFF", font=get_font(8.5, bold=True))
    draw.text((1090, 149), "Refunds", fill="#FFFFFF", font=get_font(8.5, bold=True))
    draw.text((1180, 149), "Referrals", fill="#FFFFFF", font=get_font(8.5, bold=True))

    pred_df = pd.read_csv("data/processed/Predictions.csv")
    y_r = 170
    for idx, row in pred_df.head(19).iterrows():
        row_bg = "#F4F6FD" if idx % 2 == 1 else "#FFFFFF"
        draw.rectangle([730, y_r, 1255, y_r + 23], fill=row_bg)

        cid = str(row['Customer_ID'])
        mc = f"${float(row['Monthly_Charge']):,.2f}"
        tr = f"${float(row['Total_Revenue']):,.2f}"
        rf = f"${float(row['Total_Refunds']):,.2f}"
        nr = str(int(row['Number_of_Referrals']))

        draw.text((742, y_r + 5), cid, fill="#0F101E", font=get_font(8, bold=True))
        draw.text((860, y_r + 5), mc, fill="#333333", font=get_font(8))
        draw.text((980, y_r + 5), tr, fill="#333333", font=get_font(8))
        draw.text((1090, y_r + 5), rf, fill="#333333", font=get_font(8))
        draw.text((1188, y_r + 5), nr, fill="#2B26D9", font=get_font(8, bold=True))

        y_r += 24

    out_file = "powerbi/assets/Prediction.png"
    bg.save(out_file, "PNG")
    print("Prediction rendered:", out_file)

if __name__ == "__main__":
    render_summary()
    render_prediction()
