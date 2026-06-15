import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
from datetime import datetime, date, timedelta

# ─────────────────────────────────────────────
#  ثنائي اللغة — قاموس الترجمة
# ─────────────────────────────────────────────
TRANSLATIONS = {
    "ar": {
        "page_title": "StockPro v2 Demo | إدارة المخزون",
        "app_title": "📦 StockPro v2 — إدارة المخزون (نسخة تجريبية)",
        "app_subtitle": "نظام متكامل لإدارة المخزون والمبيعات بشكل احترافي — نسخة عرض",
        "lang_label": "🌐 English",
        "dir": "rtl",
        "demo_badge": "🧪 نسخة تجريبية",
        "demo_msg": "هذه نسخة تجريبية للعرض فقط — البيانات وهمية",
        "full_version": "✨ متوفر في النسخة الكاملة",
        "role_label": "الصلاحية: مدير (تجريبي)",
        "total_products": "إجمالي المنتجات",
        "stock_value": "قيمة المخزون",
        "total_sales": "إجمالي المبيعات",
        "net_profit": "صافي الربح",
        "low_stock_items": "منتجات منخفضة",
        "low_stock_title": "### ⚠️ تنبيهات المخزون المنخفض",
        "low_stock_msg": "🔴 <strong>{name}</strong> — الكمية المتبقية: <strong>{qty}</strong> قطعة (الحد الأدنى: {thresh})",
        "tab_inventory": "📋 المخزون",
        "tab_sales": "📈 المبيعات",
        "tab_analytics": "📊 التحليلات",
        "tab_reports": "📥 التقارير",
        "products_list": "📋 قائمة المنتجات",
        "filter_category": "تصفية حسب القسم",
        "filter_all": "الكل",
        "search_placeholder": "ابحث...",
        "search_label": "🔍 بحث بالاسم أو SKU",
        "status_low": "⚠️ منخفض",
        "status_good": "✅ جيد",
        "col_sku": "SKU",
        "col_product": "المنتج",
        "col_category": "القسم",
        "col_cost": "التكلفة ($)",
        "col_price": "السعر ($)",
        "col_discount": "الخصم (%)",
        "col_after_discount": "بعد الخصم ($)",
        "col_margin": "هامش الربح (%)",
        "col_quantity": "الكمية",
        "col_stock_value": "قيمة المخزون ($)",
        "col_status": "الحالة",
        "export_disabled": "📥 تصدير Excel — متوفر في النسخة الكاملة",
        "sales_log_title": "📜 سجل المبيعات",
        "col_qty_sold": "الكمية",
        "col_sale_price": "سعر البيع ($)",
        "col_total": "الإجمالي ($)",
        "col_profit": "الربح ($)",
        "col_date": "التاريخ",
        "period_summary": "**ملخص الفترة:** المبيعات: **${sales:,.2f}** | الربح: **${profit:,.2f}** | عدد العمليات: **{count}**",
        "analytics_title": "📊 لوحة التحليلات",
        "chart_pie_title": "توزيع قيمة المخزون حسب القسم",
        "chart_top_value": "أعلى 8 منتجات بقيمة المخزون",
        "chart_margin_title": "💵 هامش الربح لكل منتج",
        "chart_qty_by_cat": "📦 الكميات حسب القسم",
        "sales_analytics_title": "### 📈 تحليلات المبيعات",
        "chart_daily_sales": "📈 المبيعات والأرباح اليومية",
        "chart_top_sold": "🏆 أكثر المنتجات مبيعاً (حسب الإيراد)",
        "chart_qty_level": "📦 مستوى الكمية لكل منتج",
        "xaxis_stock_value": "قيمة المخزون ($)",
        "xaxis_margin": "هامش الربح (%)",
        "yaxis_quantity": "الكمية",
        "xaxis_revenue": "الإيراد ($)",
        "label_amount": "المبلغ ($)",
        "label_date": "التاريخ",
        "pieces": "قطعة",
        "reports_title": "📥 التقارير",
        "report_disabled": "📄 تصدير التقارير متوفر في النسخة الكاملة",
        "features_disabled": "الميزات التالية متوفرة في النسخة الكاملة:",
        "feature_list": [
            "تصدير Excel و CSV",
            "استيراد منتجات من CSV",
            "إضافة / تعديل / حذف منتجات",
            "تسجيل مبيعات",
            "نسخ احتياطي واستعادة",
            "إدارة المستخدمين",
            "تقارير HTML قابلة للطباعة",
        ],
    },
    "en": {
        "page_title": "StockPro v2 Demo | Inventory Management",
        "app_title": "📦 StockPro v2 — Inventory Management (Demo)",
        "app_subtitle": "Professional inventory & sales management system — Demo version",
        "lang_label": "🌐 عربي",
        "dir": "ltr",
        "demo_badge": "🧪 Demo Version",
        "demo_msg": "This is a demo version — Data is sample only",
        "full_version": "✨ Available in full version",
        "role_label": "Role: Admin (Demo)",
        "total_products": "Total Products",
        "stock_value": "Stock Value",
        "total_sales": "Total Sales",
        "net_profit": "Net Profit",
        "low_stock_items": "Low Stock Items",
        "low_stock_title": "### ⚠️ Low Stock Alerts",
        "low_stock_msg": "🔴 <strong>{name}</strong> — Remaining: <strong>{qty}</strong> pcs (Threshold: {thresh})",
        "tab_inventory": "📋 Inventory",
        "tab_sales": "📈 Sales",
        "tab_analytics": "📊 Analytics",
        "tab_reports": "📥 Reports",
        "products_list": "📋 Products List",
        "filter_category": "Filter by Category",
        "filter_all": "All",
        "search_placeholder": "Search...",
        "search_label": "🔍 Search by name or SKU",
        "status_low": "⚠️ Low",
        "status_good": "✅ Good",
        "col_sku": "SKU",
        "col_product": "Product",
        "col_category": "Category",
        "col_cost": "Cost ($)",
        "col_price": "Price ($)",
        "col_discount": "Discount (%)",
        "col_after_discount": "After Discount ($)",
        "col_margin": "Profit Margin (%)",
        "col_quantity": "Quantity",
        "col_stock_value": "Stock Value ($)",
        "col_status": "Status",
        "export_disabled": "📥 Export Excel — Available in full version",
        "sales_log_title": "📜 Sales Log",
        "col_qty_sold": "Qty Sold",
        "col_sale_price": "Sale Price ($)",
        "col_total": "Total ($)",
        "col_profit": "Profit ($)",
        "col_date": "Date",
        "period_summary": "**Period Summary:** Sales: **${sales:,.2f}** | Profit: **${profit:,.2f}** | Transactions: **{count}**",
        "analytics_title": "📊 Analytics Dashboard",
        "chart_pie_title": "Stock Value Distribution by Category",
        "chart_top_value": "Top 8 Products by Stock Value",
        "chart_margin_title": "💵 Profit Margin per Product",
        "chart_qty_by_cat": "📦 Quantities by Category",
        "sales_analytics_title": "### 📈 Sales Analytics",
        "chart_daily_sales": "📈 Daily Sales & Profits",
        "chart_top_sold": "🏆 Top Products by Revenue",
        "chart_qty_level": "📦 Quantity Level per Product",
        "xaxis_stock_value": "Stock Value ($)",
        "xaxis_margin": "Profit Margin (%)",
        "yaxis_quantity": "Quantity",
        "xaxis_revenue": "Revenue ($)",
        "label_amount": "Amount ($)",
        "label_date": "Date",
        "pieces": "pcs",
        "reports_title": "📥 Reports",
        "report_disabled": "📄 Report export available in full version",
        "features_disabled": "The following features are available in the full version:",
        "feature_list": [
            "Export to Excel & CSV",
            "Import products from CSV",
            "Add / Edit / Delete products",
            "Record sales",
            "Backup & Restore",
            "User management",
            "Printable HTML reports",
        ],
    }
}


def t(key, **kwargs):
    lang = st.session_state.get("lang", "ar")
    text = TRANSLATIONS.get(lang, TRANSLATIONS["ar"]).get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text


# ─────────────────────────────────────────────
#  بيانات تجريبية Hardcoded
# ─────────────────────────────────────────────
def get_demo_products() -> pd.DataFrame:
    data = [
        {"id":1,"sku":"ELC-0001","product_name":"لابتوب HP ProBook 450","category":"إلكترونيات","cost_price":600.0,"price":850.0,"discount_pct":10.0,"quantity":25,"low_stock_threshold":5},
        {"id":2,"sku":"ELC-0002","product_name":"شاشة Samsung 27 بوصة","category":"إلكترونيات","cost_price":200.0,"price":320.0,"discount_pct":5.0,"quantity":40,"low_stock_threshold":8},
        {"id":3,"sku":"ELC-0003","product_name":"كيبورد ميكانيكي Keychron","category":"إلكترونيات","cost_price":45.0,"price":75.0,"discount_pct":0.0,"quantity":3,"low_stock_threshold":10},
        {"id":4,"sku":"ELC-0004","product_name":"ماوس لاسلكي Logitech MX","category":"إلكترونيات","cost_price":25.0,"price":45.0,"discount_pct":15.0,"quantity":60,"low_stock_threshold":10},
        {"id":5,"sku":"ELC-0005","product_name":"سماعات بلوتوث JBL Tune","category":"إلكترونيات","cost_price":70.0,"price":120.0,"discount_pct":12.0,"quantity":18,"low_stock_threshold":5},
        {"id":6,"sku":"ELC-0006","product_name":"طابعة HP LaserJet Pro","category":"إلكترونيات","cost_price":180.0,"price":280.0,"discount_pct":8.0,"quantity":7,"low_stock_threshold":3},
        {"id":7,"sku":"ELC-0007","product_name":"فلاش ميموري USB 64GB","category":"إلكترونيات","cost_price":5.0,"price":12.0,"discount_pct":0.0,"quantity":120,"low_stock_threshold":20},
        {"id":8,"sku":"ELC-0008","product_name":"كابل HDMI 2M","category":"إلكترونيات","cost_price":3.0,"price":8.0,"discount_pct":0.0,"quantity":2,"low_stock_threshold":15},
        {"id":9,"sku":"FD-0009","product_name":"أرز بسمتي 5 كيلو","category":"مواد غذائية","cost_price":8.0,"price":12.0,"discount_pct":0.0,"quantity":200,"low_stock_threshold":30},
        {"id":10,"sku":"FD-0010","product_name":"زيت زيتون بكر 1 لتر","category":"مواد غذائية","cost_price":12.0,"price":18.5,"discount_pct":5.0,"quantity":80,"low_stock_threshold":15},
        {"id":11,"sku":"FD-0011","product_name":"تمر مجدول 1 كيلو","category":"مواد غذائية","cost_price":15.0,"price":25.0,"discount_pct":0.0,"quantity":45,"low_stock_threshold":10},
        {"id":12,"sku":"FD-0012","product_name":"عسل طبيعي 500 مل","category":"مواد غذائية","cost_price":18.0,"price":32.0,"discount_pct":10.0,"quantity":30,"low_stock_threshold":8},
        {"id":13,"sku":"FD-0013","product_name":"حليب كامل الدسم 1 لتر","category":"مواد غذائية","cost_price":0.8,"price":1.5,"discount_pct":0.0,"quantity":150,"low_stock_threshold":25},
        {"id":14,"sku":"BV-0014","product_name":"عصير برتقال طبيعي 1 لتر","category":"مشروبات","cost_price":2.0,"price":3.5,"discount_pct":0.0,"quantity":2,"low_stock_threshold":20},
        {"id":15,"sku":"BV-0015","product_name":"ماء معدني 12 عبوة","category":"مشروبات","cost_price":3.5,"price":6.0,"discount_pct":10.0,"quantity":150,"low_stock_threshold":25},
        {"id":16,"sku":"BV-0016","product_name":"قهوة نسكافيه 200 غرام","category":"مشروبات","cost_price":8.0,"price":14.0,"discount_pct":0.0,"quantity":55,"low_stock_threshold":10},
        {"id":17,"sku":"BV-0017","product_name":"شاي أخضر 100 كيس","category":"مشروبات","cost_price":5.0,"price":9.0,"discount_pct":5.0,"quantity":40,"low_stock_threshold":10},
        {"id":18,"sku":"CLN-0018","product_name":"صابون غسيل سائل 3 لتر","category":"منظفات","cost_price":4.5,"price":8.0,"discount_pct":0.0,"quantity":45,"low_stock_threshold":10},
        {"id":19,"sku":"CLN-0019","product_name":"معقم أسطح 750 مل","category":"منظفات","cost_price":2.5,"price":5.5,"discount_pct":20.0,"quantity":4,"low_stock_threshold":12},
        {"id":20,"sku":"CLN-0020","product_name":"مسحوق غسيل 3 كيلو","category":"منظفات","cost_price":7.0,"price":12.0,"discount_pct":0.0,"quantity":35,"low_stock_threshold":8},
        {"id":21,"sku":"HM-0021","product_name":"مكنسة كهربائية Philips","category":"أجهزة منزلية","cost_price":80.0,"price":130.0,"discount_pct":15.0,"quantity":12,"low_stock_threshold":3},
        {"id":22,"sku":"HM-0022","product_name":"غلاية كهربائية 1.7 لتر","category":"أجهزة منزلية","cost_price":20.0,"price":38.0,"discount_pct":0.0,"quantity":20,"low_stock_threshold":5},
        {"id":23,"sku":"HM-0023","product_name":"مروحة طاولة 40 سم","category":"أجهزة منزلية","cost_price":15.0,"price":28.0,"discount_pct":10.0,"quantity":8,"low_stock_threshold":4},
        {"id":24,"sku":"HM-0024","product_name":"ميزان رقمي للمطبخ","category":"أجهزة منزلية","cost_price":8.0,"price":18.0,"discount_pct":0.0,"quantity":25,"low_stock_threshold":5},
    ]
    df = pd.DataFrame(data)
    df['price_after_discount'] = (df['price'] * (1 - df['discount_pct'] / 100)).round(2)
    df['profit_margin'] = ((df['price_after_discount'] - df['cost_price']) / df['price_after_discount'] * 100).round(1)
    df['total_stock_value'] = (df['price_after_discount'] * df['quantity']).round(2)
    return df


def get_demo_sales() -> pd.DataFrame:
    today = date.today()
    sales = [
        {"product_name":"لابتوب HP ProBook 450","sku":"ELC-0001","quantity_sold":3,"cost_price":600.0,"sale_price":765.0,"sale_date":(today - timedelta(days=1)).isoformat()},
        {"product_name":"شاشة Samsung 27 بوصة","sku":"ELC-0002","quantity_sold":5,"cost_price":200.0,"sale_price":304.0,"sale_date":(today - timedelta(days=1)).isoformat()},
        {"product_name":"ماوس لاسلكي Logitech MX","sku":"ELC-0004","quantity_sold":10,"cost_price":25.0,"sale_price":38.25,"sale_date":(today - timedelta(days=2)).isoformat()},
        {"product_name":"سماعات بلوتوث JBL Tune","sku":"ELC-0005","quantity_sold":4,"cost_price":70.0,"sale_price":105.6,"sale_date":(today - timedelta(days=2)).isoformat()},
        {"product_name":"أرز بسمتي 5 كيلو","sku":"FD-0009","quantity_sold":20,"cost_price":8.0,"sale_price":12.0,"sale_date":(today - timedelta(days=3)).isoformat()},
        {"product_name":"زيت زيتون بكر 1 لتر","sku":"FD-0010","quantity_sold":8,"cost_price":12.0,"sale_price":17.58,"sale_date":(today - timedelta(days=3)).isoformat()},
        {"product_name":"تمر مجدول 1 كيلو","sku":"FD-0011","quantity_sold":6,"cost_price":15.0,"sale_price":25.0,"sale_date":(today - timedelta(days=4)).isoformat()},
        {"product_name":"عسل طبيعي 500 مل","sku":"FD-0012","quantity_sold":3,"cost_price":18.0,"sale_price":28.8,"sale_date":(today - timedelta(days=4)).isoformat()},
        {"product_name":"قهوة نسكافيه 200 غرام","sku":"BV-0016","quantity_sold":7,"cost_price":8.0,"sale_price":14.0,"sale_date":(today - timedelta(days=5)).isoformat()},
        {"product_name":"ماء معدني 12 عبوة","sku":"BV-0015","quantity_sold":15,"cost_price":3.5,"sale_price":5.4,"sale_date":(today - timedelta(days=5)).isoformat()},
        {"product_name":"مكنسة كهربائية Philips","sku":"HM-0021","quantity_sold":2,"cost_price":80.0,"sale_price":110.5,"sale_date":(today - timedelta(days=6)).isoformat()},
        {"product_name":"غلاية كهربائية 1.7 لتر","sku":"HM-0022","quantity_sold":4,"cost_price":20.0,"sale_price":38.0,"sale_date":(today - timedelta(days=7)).isoformat()},
        {"product_name":"صابون غسيل سائل 3 لتر","sku":"CLN-0018","quantity_sold":10,"cost_price":4.5,"sale_price":8.0,"sale_date":(today - timedelta(days=8)).isoformat()},
        {"product_name":"فلاش ميموري USB 64GB","sku":"ELC-0007","quantity_sold":25,"cost_price":5.0,"sale_price":12.0,"sale_date":(today - timedelta(days=9)).isoformat()},
        {"product_name":"لابتوب HP ProBook 450","sku":"ELC-0001","quantity_sold":2,"cost_price":600.0,"sale_price":765.0,"sale_date":(today - timedelta(days=10)).isoformat()},
        {"product_name":"حليب كامل الدسم 1 لتر","sku":"FD-0013","quantity_sold":30,"cost_price":0.8,"sale_price":1.5,"sale_date":(today - timedelta(days=10)).isoformat()},
        {"product_name":"شاي أخضر 100 كيس","sku":"BV-0017","quantity_sold":5,"cost_price":5.0,"sale_price":8.55,"sale_date":(today - timedelta(days=12)).isoformat()},
        {"product_name":"مسحوق غسيل 3 كيلو","sku":"CLN-0020","quantity_sold":8,"cost_price":7.0,"sale_price":12.0,"sale_date":(today - timedelta(days=14)).isoformat()},
        {"product_name":"مروحة طاولة 40 سم","sku":"HM-0023","quantity_sold":3,"cost_price":15.0,"sale_price":25.2,"sale_date":(today - timedelta(days=15)).isoformat()},
        {"product_name":"ميزان رقمي للمطبخ","sku":"HM-0024","quantity_sold":5,"cost_price":8.0,"sale_price":18.0,"sale_date":(today - timedelta(days=18)).isoformat()},
    ]
    df = pd.DataFrame(sales)
    df['total_amount'] = (df['quantity_sold'] * df['sale_price']).round(2)
    df['profit'] = ((df['sale_price'] - df['cost_price']) * df['quantity_sold']).round(2)
    return df


# ─────────────────────────────────────────────
#  إعدادات الصفحة
# ─────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state["lang"] = "ar"

st.set_page_config(
    page_title=TRANSLATIONS[st.session_state["lang"]]["page_title"],
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

_dir = t("dir")
_text_align = "right" if _dir == "rtl" else "left"
_border_side = "right" if _dir == "rtl" else "left"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');

html, body, [class="css"] {{ font-family: 'Cairo' !important; }}
.main .block-container {{ direction: {_dir}; padding-top: 2rem; }}
[data-testid="stSidebar"] > div {{ direction: {_dir}; }}

[data-testid="stAppDeployButton"] {{ display: none !important; }}
#MainMenu {{ visibility: hidden !important; }}
footer {{ visibility: hidden !important; }}
header {{ background-color: transparent !important; }}

[data-testid="collapsedControl"] {{
    position: fixed !important;
    top: 15px !important;
    left: 15px !important;
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    z-index: 999999 !important;
    background-color: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
}}

.stApp {{
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}}

section[data-testid="stSidebar"] {{
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(20px);
    border-{_border_side}: 1px solid rgba(255,255,255,0.1);
}}
section[data-testid="stSidebar"] * {{ color: #fff !important; }}

.stMarkdown, p, span, label, div {{ color: #e2e8f0; }}

.metric-card {{
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 20px 24px;
    backdrop-filter: blur(10px);
    transition: transform 0.2s, box-shadow 0.2s;
    text-align: center;
}}
.metric-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}}
.metric-value {{
    font-size: 2rem;
    font-weight: 900;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.metric-label {{
    font-size: 0.85rem;
    color: #94a3b8;
    margin-top: 4px;
}}

.low-stock-alert {{
    background: linear-gradient(135deg, rgba(239,68,68,0.2), rgba(239,68,68,0.05));
    border: 1px solid rgba(239,68,68,0.4);
    border-radius: 12px;
    padding: 12px 16px;
    margin: 8px 0;
    color: #fca5a5 !important;
    font-weight: 600;
}}

.app-title {{
    font-size: 2.2rem;
    font-weight: 900;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: {_text_align};
    direction: {_dir};
    margin-bottom: 0;
}}
.app-subtitle {{
    color: #64748b;
    font-size: 0.95rem;
    text-align: {_text_align};
    direction: {_dir};
    margin-top: 4px;
}}

.stButton > button {{
    background: linear-gradient(135deg, #7c3aed, #3b82f6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 700 !important;
    padding: 10px 20px !important;
    transition: all 0.3s !important;
    width: 100% !important;
}}
.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 25px rgba(124,58,237,0.4) !important;
}}

input, textarea,
.stTextInput input, .stNumberInput input,
[data-baseweb="input"] input, [data-baseweb="input"] div,
[data-baseweb="select"] div, [data-baseweb="select"] input,
div[data-testid="stTextInput"] input,
.stSelectbox div[data-baseweb="select"] div,
[role="listbox"], [role="option"] {{
    background: rgba(20,20,50,0.95) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    direction: {_dir} !important;
    caret-color: #a78bfa !important;
}}
[data-baseweb="popover"] li,
[data-baseweb="menu"] li,
[data-baseweb="menu"] ul {{
    background: #1e1b4b !important;
    color: #ffffff !important;
}}
[data-baseweb="menu"] li:hover {{
    background: #3b82f6 !important;
    color: #ffffff !important;
}}
input::placeholder, textarea::placeholder {{
    color: rgba(255,255,255,0.4) !important;
}}
input:focus, textarea:focus {{
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.3) !important;
    outline: none !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 4px;
    direction: {_dir};
}}
.stTabs [data-baseweb="tab"] {{
    color: #94a3b8 !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, #7c3aed, #3b82f6) !important;
    color: white !important;
}}

.stDataFrame {{ border-radius: 12px; overflow: hidden; }}
hr {{ border-color: rgba(255,255,255,0.1) !important; }}

.demo-badge {{
    background: linear-gradient(135deg, #f59e0b, #ef4444);
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.85rem;
    display: inline-block;
    margin: 5px 0;
}}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  الواجهة الرئيسية — Demo
# ─────────────────────────────────────────────
df = get_demo_products()
sales_df = get_demo_sales()
low_stock_df = df[df['quantity'] <= df['low_stock_threshold']]

# ── الشريط الجانبي ──
with st.sidebar:
    if st.button(t("lang_label"), key="lang_sidebar"):
        st.session_state["lang"] = "en" if st.session_state["lang"] == "ar" else "ar"
        st.rerun()

    st.markdown("---")
    st.markdown(f'<div class="demo-badge">{t("demo_badge")}</div>', unsafe_allow_html=True)
    st.markdown(f"### 👤 Admin")
    st.caption(t("role_label"))
    st.markdown("---")
    st.info(t("demo_msg"))

    st.markdown("---")
    st.markdown(f"### {t('full_version')}")
    features = t("feature_list")
    st.markdown(t("features_disabled"))
    for feat in features:
        st.markdown(f"- ✅ {feat}")

# ── المحتوى الرئيسي ──
st.markdown(f'<div class="app-title">{t("app_title")}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="app-subtitle">{t("app_subtitle")}</div>', unsafe_allow_html=True)
st.markdown("---")

# ── بطاقات الإحصاء ──
total_products = len(df)
total_value = df['total_stock_value'].sum()
total_sales_val = sales_df['total_amount'].sum()
total_profit = sales_df['profit'].sum()
low_stock_count = len(low_stock_df)

c1, c2, c3, c4, c5 = st.columns(5)
cards = [
    (c1, "📦", f"{total_products}", t("total_products")),
    (c2, "💰", f"${total_value:,.0f}", t("stock_value")),
    (c3, "📈", f"${total_sales_val:,.0f}", t("total_sales")),
    (c4, "💵", f"${total_profit:,.0f}", t("net_profit")),
    (c5, "⚠️", f"{low_stock_count}", t("low_stock_items")),
]
for col, icon, val, label in cards:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size:1.8rem">{icon}</div>
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ── تنبيهات المخزون المنخفض ──
if not low_stock_df.empty:
    st.markdown(t("low_stock_title"))
    for _, row in low_stock_df.iterrows():
        st.markdown(f"""
        <div class="low-stock-alert">
            {t('low_stock_msg', name=row['product_name'], qty=row['quantity'], thresh=row['low_stock_threshold'])}
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")

# ── التبويبات ──
tab1, tab2, tab3, tab4 = st.tabs([
    t("tab_inventory"), t("tab_sales"), t("tab_analytics"), t("tab_reports")
])

# ═══════════════════════════════════════════
#  تبويب 1: المخزون
# ═══════════════════════════════════════════
with tab1:
    st.subheader(t("products_list"))

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        categories = sorted(df['category'].unique().tolist())
        cats_filter = [t("filter_all")] + categories
        sel_filter = st.selectbox(t("filter_category"), cats_filter, key="filter_cat")
    with col_f2:
        search = st.text_input(t("search_label"), placeholder=t("search_placeholder"))

    df_show = df.copy()
    if sel_filter != t("filter_all"):
        df_show = df_show[df_show['category'] == sel_filter]
    if search:
        mask = (
            df_show['product_name'].str.contains(search, case=False, na=False) |
            df_show['sku'].astype(str).str.contains(search, case=False, na=False)
        )
        df_show = df_show[mask]

    status_col = t('col_status')
    df_show = df_show.copy()
    df_show[status_col] = df_show.apply(
        lambda r: t("status_low") if r['quantity'] <= r['low_stock_threshold'] else t("status_good"), axis=1)

    display_cols = {
        'sku': t('col_sku'),
        'product_name': t('col_product'),
        'category': t('col_category'),
        'cost_price': t('col_cost'),
        'price': t('col_price'),
        'discount_pct': t('col_discount'),
        'price_after_discount': t('col_after_discount'),
        'profit_margin': t('col_margin'),
        'quantity': t('col_quantity'),
        'total_stock_value': t('col_stock_value'),
        status_col: t('col_status'),
    }
    available = [c for c in display_cols if c in df_show.columns]
    st.dataframe(
        df_show[available].rename(columns=display_cols),
        use_container_width=True,
        hide_index=True,
    )

    st.button(t("export_disabled"), disabled=True, use_container_width=True)

# ═══════════════════════════════════════════
#  تبويب 2: المبيعات
# ═══════════════════════════════════════════
with tab2:
    st.subheader(t("sales_log_title"))

    sales_display_cols = ['product_name', 'sku', 'quantity_sold', 'sale_price', 'total_amount', 'profit', 'sale_date']
    col_names = {
        'product_name': t('col_product'), 'sku': t('col_sku'),
        'quantity_sold': t('col_qty_sold'), 'sale_price': t('col_sale_price'),
        'total_amount': t('col_total'), 'profit': t('col_profit'),
        'sale_date': t('col_date'),
    }
    st.dataframe(
        sales_df[sales_display_cols].rename(columns=col_names),
        use_container_width=True, hide_index=True
    )

    st.markdown(t("period_summary",
                 sales=sales_df['total_amount'].sum(),
                 profit=sales_df['profit'].sum(),
                 count=len(sales_df)))

    st.button(t("export_disabled"), disabled=True, use_container_width=True, key="export_sales_disabled")

# ═══════════════════════════════════════════
#  تبويب 3: التحليلات
# ═══════════════════════════════════════════
with tab3:
    st.subheader(t("analytics_title"))

    col_ch1, col_ch2 = st.columns(2)

    with col_ch1:
        cat_data = df.groupby('category')['total_stock_value'].sum().reset_index()
        fig_pie = px.pie(
            cat_data, values='total_stock_value', names='category',
            hole=0.5, title=t("chart_pie_title"),
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0', title_font_size=16, showlegend=True,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_ch2:
        top_products = df.nlargest(8, 'total_stock_value')
        fig_bar = px.bar(
            top_products, x='total_stock_value', y='product_name',
            orientation='h', title=t("chart_top_value"),
            color='total_stock_value', color_continuous_scale='Viridis'
        )
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0', title_font_size=16, showlegend=False,
            yaxis_title="", xaxis_title=t("xaxis_stock_value")
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        margin_df = df[df['profit_margin'] != 0].sort_values('profit_margin')
        colors = ['#ef4444' if m < 0 else '#22c55e' if m > 20 else '#f59e0b'
                  for m in margin_df['profit_margin']]
        fig_margin = go.Figure(go.Bar(
            x=margin_df['profit_margin'],
            y=margin_df['product_name'],
            orientation='h',
            marker_color=colors,
            text=[f"{m:.1f}%" for m in margin_df['profit_margin']],
            textposition='auto',
        ))
        fig_margin.update_layout(
            title=t("chart_margin_title"),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0', title_font_size=16,
            yaxis_title="", xaxis_title=t("xaxis_margin"),
        )
        fig_margin.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
        fig_margin.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
        st.plotly_chart(fig_margin, use_container_width=True)

    with col_m2:
        cat_qty = df.groupby('category')['quantity'].sum().reset_index()
        fig_cat_qty = px.bar(
            cat_qty, x='category', y='quantity',
            title=t("chart_qty_by_cat"),
            color='quantity', color_continuous_scale='Blues'
        )
        fig_cat_qty.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0', title_font_size=16,
            xaxis_title="", yaxis_title=t("yaxis_quantity"),
        )
        fig_cat_qty.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
        fig_cat_qty.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
        st.plotly_chart(fig_cat_qty, use_container_width=True)

    # تحليلات المبيعات
    st.markdown("---")
    st.markdown(t("sales_analytics_title"))

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        daily_sales = sales_df.groupby('sale_date').agg(
            total=('total_amount', 'sum'),
            profit=('profit', 'sum')
        ).reset_index()
        fig_line = px.line(
            daily_sales, x='sale_date', y=['total', 'profit'],
            title=t("chart_daily_sales"),
            markers=True,
            labels={'value': t('label_amount'), 'sale_date': t('label_date'), 'variable': ''},
            color_discrete_map={'total': '#a78bfa', 'profit': '#34d399'},
        )
        fig_line.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0', title_font_size=16,
        )
        fig_line.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
        fig_line.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
        st.plotly_chart(fig_line, use_container_width=True)

    with col_s2:
        top_sold = sales_df.groupby('product_name').agg(
            total_qty=('quantity_sold', 'sum'),
            total_revenue=('total_amount', 'sum')
        ).nlargest(8, 'total_revenue').reset_index()
        fig_top = px.bar(
            top_sold, x='total_revenue', y='product_name',
            orientation='h', title=t("chart_top_sold"),
            color='total_revenue', color_continuous_scale='Purples',
            text='total_qty',
        )
        fig_top.update_traces(texttemplate=f'%{{text}} {t("pieces")}', textposition='auto')
        fig_top.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0', title_font_size=16, showlegend=False,
            yaxis_title="", xaxis_title=t("xaxis_revenue"),
        )
        st.plotly_chart(fig_top, use_container_width=True)

    fig_qty = px.bar(
        df.sort_values('quantity'), x='product_name', y='quantity',
        title=t("chart_qty_level"),
        color='quantity', color_continuous_scale=['#ef4444', '#f59e0b', '#22c55e']
    )
    fig_qty.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e2e8f0', title_font_size=16,
        xaxis_title="", yaxis_title=t("yaxis_quantity")
    )
    fig_qty.update_xaxes(gridcolor='rgba(255,255,255,0.1)', tickangle=-30)
    fig_qty.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
    st.plotly_chart(fig_qty, use_container_width=True)

# ═══════════════════════════════════════════
#  تبويب 4: التقارير
# ═══════════════════════════════════════════
with tab4:
    st.subheader(t("reports_title"))
    st.info(t("report_disabled"))
    st.button(t("export_disabled"), disabled=True, use_container_width=True, key="report_disabled_btn")
