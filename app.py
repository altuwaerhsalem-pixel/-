import streamlit as st

# إعدادات الصفحة لتكون متوافقة تماماً مع الجوال واللابتوب
st.set_page_config(
    page_title="متطلبات وشكاوى متدربين المعهد الصناعي",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="auto"
)

# قاعدة بيانات المستخدمين والإداريين (محمية ومخفية بالكامل خلف الكواليس)
USERS_DB = {
    # 1. مالك النظام (الأونر)
    "owner@admin.com": {"password": "asue175gk@$", "role": "مالك النظام"},
    
    # 2. مطورو / مسؤولو تطوير المشروع (5 إيميلات)
    "dev1@project.com": {"password": ";dejhsilsh", "role": "مشروع"},
    "dev2@project.com": {"password": "hsdg47hdgh", "role": "مشروع"},
    "dev3@project.com": {"password": "sgcgccxggc", "role": "مشروع"},
    "dev4@project.com": {"password": "hcghnvghvv", "role": "مشروع"},
    "dev5@project.com": {"password": "gdfjbfvhjn", "role": "مشروع"},
    
    # 3. إدارة القسم (4 إيميلات)
    "manager1@dept.com": {"password": "ghjbfddwbn", "role": "إدارة القسم"},
    "manager2@dept.com": {"password": "12sqbjvtcc3", "role": "إدارة القسم"},
    "manager3@dept.com": {"password": "ladghlj7h323", "role": "إدارة القسم"},
    "manager4@dept.com": {"password": "123dhkkhdfbidw", "role": "إدارة القسم"}
}

# تهيئة حالة الجلسة للتسجيل والشكاوى
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "complaints" not in st.session_state:
    st.session_state.complaints = []

# --- تصميم الواجهة العلوية (زر تسجيل الدخول على اليمين فوق + العنوان في المنتصف) ---
col_title, col_login = st.columns([4, 1])

with col_login:
    if not st.session_state.logged_in:
        with st.popover("🔐 تسجيل دخول الإداريين"):
            st.markdown("### تسجیل دخول الإدارة")
            login_email = st.text_input("البريد الإلكتروني", key="login_email_input")
            login_pass = st.text_input("كلمة المرور", type="password", key="login_pass_input")
            
            if st.button("دخول"):
                if login_email in USERS_DB and USERS_DB[login_email]["password"] == login_pass:
                    st.session_state.logged_in = True
                    st.session_state.user_role = USERS_DB[login_email]["role"]
                    st.session_state.user_email = login_email
                    st.success("تم تسجيل الدخول بنجاح!")
                    st.rerun()
                else:
                    st.error("البريد أو كلمة المرور غير صحيحة!")
    else:
        if st.button("🚪 خروج"):
            st.session_state.logged_in = False
            st.session_state.user_role = ""
            st.session_state.user_email = ""
            st.rerun()

with col_title:
    pass

# العنوان الرئيسي في المنتصف
st.markdown("<h1 style='text-align: center; color: #1E3A8A; font-size: 24px;'>متطلبات وشكاوى متدربين المعهد الصناعي</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- لوحة تحكم الإدارة (تظهر فقط عند تسجيل الدخول بصلاحية صحيحة) ---
if st.session_state.logged_in:
    st.info(f"👤 مرحباً بك [{st.session_state.user_role}] - مسجل عبر: {st.session_state.user_email}")
    st.markdown("## 📊 صفحة متابعة الشكاوى والطلبات (خاص بالإدارة)")
    
    if len(st.session_state.complaints) == 0:
        st.warning("لا توجد أي شكاوى أو طلبات مرسلة حتى الآن.")
    else:
        st.write(f"إجمالي الطلبات الواردة: **{len(st.session_state.complaints)}**")
        
        for idx, comp in enumerate(reversed(st.session_state.complaints)):
            with st.expander(f"الطلب #{len(st.session_state.complaints) - idx} | القسم: {comp['department']} | المكان: {comp['location']} | صاحب الطلب: {comp['name']}"):
                st.markdown(f"**📝 تفاصيل المشكلة / الطلب:**")
                st.info(comp['text'])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**👤 الاسم الثلاثي:** {comp['name']}")
                    st.write(f"**📍 مكان المشكلة:** {comp['location']}")
                with col2:
                    st.write(f"**🆔 رقم الهوية:** {comp['national_id']}")
                    st.write(f"**⚡ مستوى الأهمية:** {comp['importance']}")
                
                if comp['images']:
                    st.write(f"**📷 الصور المرفقة ({len(comp['images'])}):**")
                    img_cols = st.columns(min(len(comp['images']), 3))
                    for i, img in enumerate(comp['images']):
                        with img_cols[i % len(img_cols)]:
                            st.image(img, caption=f"صورة {i+1}", use_column_width=True)
                else:
                    st.write("📷 **الصور المرفقة:** لا توجد صور مرفقة مع هذا الطلب.")
                    
    st.markdown("---")

# --- نموذج تقديم الشكاوى والطلبات للمتدربين بالترتيب المطلوب ---
st.markdown("### 📝 نموذج تقديم شكوى أو متطلب جديد")
st.markdown("الرجاء تعبئة الحقول أدناه بدقة:")

with st.form("complaint_form", clear_on_submit=True):
    # 1. المشكلة أو الطلب
    complaint_text = st.text_area("1. اكتب المشكلة أو الطلب بالتفصيل:", placeholder="اكتب تفاصيل الطلب هنا...")
    
    # 2. القسم
    department = st.selectbox("2. القسم:", ["قسم الحاسب الآلي"])
    
    # 3. مكان المشكلة (تحت القسم مباشرة)
    location = st.text_input("3. مكان المشكلة (مثال: القاعة الفلانية، المعمل رقم...):")
    
    # 4. أهمية المشكلة أو الطلب
    importance = st.selectbox("4. أهمية المشكلة أو الطلب:", ["عادي", "متوسط", "مهم"])
    
    # 5. الاسم الثلاثي
    name = st.text_input("5. الاسم الثلاثي:")
    
    # 6. رقم الهوية
    national_id = st.text_input("6. رقم الهوية:")
    
    # 7. الصور (بحد أقصى 5 صور)
    uploaded_images = st.file_uploader(
        "7. إرفاق صور (اختياري - الحد الأقصى 5 صور):", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )
    
    # زر الإرسال
    submit_button = st.form_submit_button(label="إرسال الطلب أو الشكوى")
    
    if submit_button:
        # التحقق من المدخلات الأساسية
        if not complaint_text.strip() or not location.strip() or not name.strip() or not national_id.strip():
            st.error("الرجاء تعبئة الحقول الإجبارية (المشكلة، مكان المشكلة، الاسم الثلاثي، ورقم الهوية).")
        elif uploaded_images and len(uploaded_images) > 5:
            st.error("عذراً، الحد الأقصى المسموح به لمرفقات الصور هو 5 صور فقط!")
        else:
            # حفظ الطلب
            new_complaint = {
                "text": complaint_text,
                "department": department,
                "location": location,
                "importance": importance,
                "name": name,
                "national_id": national_id,
                "images": uploaded_images
            }
            st.session_state.complaints.append(new_complaint)
            st.success("تم إرسال شكواك أو طلبك بنجاح وسيتم متابعتها من قبل الإدارة المختصة!")
