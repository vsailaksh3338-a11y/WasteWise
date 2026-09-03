import streamlit as st
from PIL import Image

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="WasteWise ♻️",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f6faf7;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #e9f5ec;
    }

    /* Main title */
    .main-title {
        font-size: 48px;
        font-weight: 800;
        color: #174d2c;
        margin-bottom: 0px;
    }

    .tagline {
        font-size: 20px;
        color: #558064;
        margin-top: 0px;
        margin-bottom: 30px;
    }

    /* Cards */
    .card {
        background-color: white;
        padding: 22px;
        border-radius: 18px;
        margin-bottom: 18px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.06);
        border: 1px solid #e3eee5;
    }

    .card h3 {
        color: #174d2c;
        margin-bottom: 8px;
    }

    /* Waste result */
    .result-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 20px;
        border-left: 7px solid #35a853;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.07);
    }

    .bin {
        font-size: 55px;
        text-align: center;
    }

    .points {
        background-color: #e5f6e9;
        padding: 12px 18px;
        border-radius: 12px;
        color: #1b6e35;
        font-weight: bold;
    }

    /* Section headings */
    .section-title {
        color: #174d2c;
        font-size: 30px;
        font-weight: 700;
        margin-top: 20px;
    }

    /* Small text */
    .muted {
        color: #6c7c70;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "eco_points" not in st.session_state:
    st.session_state.eco_points = 120

if "scanned_items" not in st.session_state:
    st.session_state.scanned_items = []

if "saved_items" not in st.session_state:
    st.session_state.saved_items = []


# ============================================================
# WASTE DATABASE
# ============================================================

waste_data = {

    "banana": {
        "category": "Organic Waste",
        "bin": "Green Bin",
        "icon": "🟢",
        "why": "Banana peels are biodegradable and can naturally decompose.",
        "instructions": [
            "Remove any non-organic material.",
            "Place the banana peel in the organic waste bin.",
            "Use it for composting where available."
        ],
        "dont": "Do not mix it with plastic packaging.",
        "points": 10
    },

    "apple": {
        "category": "Organic Waste",
        "bin": "Green Bin",
        "icon": "🟢",
        "why": "Apple cores are biodegradable organic material.",
        "instructions": [
            "Remove stickers or packaging.",
            "Place the apple core in the organic waste bin.",
            "Compost it if a composting facility is available."
        ],
        "dont": "Do not place it inside a plastic bag.",
        "points": 10
    },

    "food": {
        "category": "Organic Waste",
        "bin": "Green Bin",
        "icon": "🟢",
        "why": "Food waste can decompose and may be converted into compost.",
        "instructions": [
            "Separate food from packaging.",
            "Drain excess liquid where possible.",
            "Place food waste into the organic bin."
        ],
        "dont": "Do not mix food waste with batteries or chemicals.",
        "points": 10
    },

    "paper": {
        "category": "Recyclable Waste",
        "bin": "Blue Bin",
        "icon": "🔵",
        "why": "Clean and dry paper can be processed and recycled.",
        "instructions": [
            "Keep paper dry.",
            "Remove plastic covers and non-paper materials.",
            "Place it in the recyclable waste bin."
        ],
        "dont": "Do not recycle heavily contaminated or food-soaked paper.",
        "points": 10
    },

    "newspaper": {
        "category": "Recyclable Waste",
        "bin": "Blue Bin",
        "icon": "🔵",
        "why": "Newspapers are commonly recyclable paper products.",
        "instructions": [
            "Keep newspapers dry.",
            "Remove plastic wrapping.",
            "Place them in the recycling bin."
        ],
        "dont": "Do not throw wet newspapers into recycling.",
        "points": 10
    },

    "plastic bottle": {
        "category": "Recyclable Waste",
        "bin": "Blue Bin",
        "icon": "🔵",
        "why": "Many clean plastic bottles can be collected and recycled.",
        "instructions": [
            "Empty the bottle.",
            "Rinse it if necessary.",
            "Place it in the appropriate recycling bin."
        ],
        "dont": "Do not put bottles containing liquid into recycling.",
        "points": 10
    },

    "glass bottle": {
        "category": "Recyclable Waste",
        "bin": "Blue Bin",
        "icon": "🔵",
        "why": "Glass can often be processed repeatedly without losing its basic properties.",
        "instructions": [
            "Empty the bottle.",
            "Rinse if required.",
            "Place it in a glass/recycling collection container."
        ],
        "dont": "Do not mix broken glass with loose household waste.",
        "points": 10
    },

    "metal can": {
        "category": "Recyclable Waste",
        "bin": "Blue Bin",
        "icon": "🔵",
        "why": "Metal containers can often be recovered and recycled.",
        "instructions": [
            "Empty the can.",
            "Rinse away remaining contents.",
            "Place it in the recyclable waste bin."
        ],
        "dont": "Do not place cans containing hazardous chemicals in normal recycling.",
        "points": 10
    },

    "wrapper": {
        "category": "Non-Recyclable Waste",
        "bin": "Black/Grey Bin",
        "icon": "⚫",
        "why": "Many multilayer food wrappers are difficult to recycle through standard systems.",
        "instructions": [
            "Make sure no food remains inside.",
            "Separate it from recyclable materials.",
            "Place it in the general waste bin."
        ],
        "dont": "Do not put multilayer wrappers into recycling unless your local program accepts them.",
        "points": 5
    },

    "battery": {
        "category": "Hazardous / Special Waste",
        "bin": "Special E-Waste Collection",
        "icon": "🔴",
        "why": "Batteries can contain chemicals and metals that require specialized handling.",
        "instructions": [
            "Do not put batteries into normal household bins.",
            "Store damaged batteries safely away from heat.",
            "Take them to an authorized battery or e-waste collection point."
        ],
        "dont": "Never burn, crush, puncture, or throw batteries into normal waste.",
        "points": 20
    },

    "phone": {
        "category": "E-Waste",
        "bin": "E-Waste Collection",
        "icon": "🔴",
        "why": "Electronic devices contain valuable materials as well as components that require specialized processing.",
        "instructions": [
            "Back up and remove personal data.",
            "Remove the battery if designed to be removable.",
            "Take the device to an authorized e-waste recycler."
        ],
        "dont": "Do not place electronics in regular household waste.",
        "points": 20
    },

    "medicine": {
        "category": "Hazardous / Special Waste",
        "bin": "Medicine Collection",
        "icon": "🔴",
        "why": "Unused medicines should be handled separately to reduce environmental and safety risks.",
        "instructions": [
            "Keep medicines in their original packaging where possible.",
            "Check for a pharmacy or authorized medicine take-back service.",
            "Follow local disposal instructions."
        ],
        "dont": "Do not flush medicines down drains unless specifically instructed by local authorities.",
        "points": 20
    },

    "bulb": {
        "category": "Hazardous / Special Waste",
        "bin": "Special Waste Collection",
        "icon": "🔴",
        "why": "Some bulbs contain materials that require specialized disposal.",
        "instructions": [
            "Handle bulbs carefully.",
            "Keep broken bulbs contained.",
            "Take them to an appropriate collection point."
        ],
        "dont": "Do not crush bulbs or put special-waste bulbs into regular bins.",
        "points": 20
    }
}


# ============================================================
# HELPER FUNCTION
# ============================================================

def identify_waste(item):

    item = item.lower().strip()

    # Exact match
    if item in waste_data:
        return waste_data[item]

    # Partial match
    for key in waste_data:
        if key in item or item in key:
            return waste_data[key]

    return None


def show_waste_result(item_name, data):

    st.markdown('<div class="result-card">', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])

    with col1:
        st.markdown(
            f"<div class='bin'>{data['icon']}</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.subheader(item_name.title())
        st.success(f"Correct Category: {data['category']}")
        st.markdown(f"### Put it in: **{data['bin']}**")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## 📝 Disposal Instructions")

    for i, instruction in enumerate(data["instructions"], 1):
        st.write(f"**{i}.** {instruction}")

    st.warning(f"⚠️ **What not to do:** {data['dont']}")

    st.markdown("## 💡 Why This Bin?")
    st.info(data["why"])

    st.markdown(
        f"<div class='points'>🏆 You can earn {data['points']} Eco Points for correct segregation.</div>",
        unsafe_allow_html=True
    )

    if st.button("✅ I disposed of it correctly"):
        st.session_state.eco_points += data["points"]

        if item_name not in st.session_state.scanned_items:
            st.session_state.scanned_items.append(item_name)

        st.success(
            f"Great job! +{data['points']} Eco Points 🌱"
        )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("# ♻️ WasteWise")
st.sidebar.caption("Start today. A greater tomorrow.")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "📷 Waste Scanner",
        "♻️ Correct Bin",
        "📚 Waste Guide",
        "⚠️ Special Waste",
        "📅 Collection Schedule",
        "📍 Recycling Centres",
        "🏆 Eco Points",
        "🌱 Tips & Learning",
        "⚙️ Profile"
    ]
)

st.sidebar.markdown("---")

st.sidebar.metric(
    "🏆 Eco Points",
    st.session_state.eco_points
)

st.sidebar.caption(
    f"Items correctly identified: {len(st.session_state.scanned_items)}"
)


# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":

    st.markdown(
        "<div class='main-title'>♻️ WasteWise</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='tagline'>Start today. A greater tomorrow.</div>",
        unsafe_allow_html=True
    )

    st.success(
        "🌱 Make the right waste decision in seconds. Search or scan an item to discover how to dispose of it responsibly."
    )

    st.markdown("## 🔎 Search Waste")

    search = st.text_input(
        "What do you want to dispose of?",
        placeholder="Example: plastic bottle, banana, battery..."
    )

    if search:

        result = identify_waste(search)

        if result:
            show_waste_result(search, result)
        else:
            st.warning(
                "We couldn't identify this item yet. Try another name or use the Waste Guide."
            )

    st.markdown("## 🚀 Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        <h3>📷 Scan Waste</h3>
        <p>Take or upload a photo and identify the waste.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Scanner"):
            st.switch_page("app.py")

    with col2:
        st.markdown("""
        <div class="card">
        <h3>📚 Waste Guide</h3>
        <p>Learn how common waste items should be segregated.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        <h3>🏆 Eco Points</h3>
        <p>Track your sustainable actions and progress.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## 🗑️ Common Waste Items")

    common_items = [
        ("🍌", "Banana", "Organic"),
        ("📄", "Paper", "Recyclable"),
        ("🥤", "Plastic Bottle", "Recyclable"),
        ("🍾", "Glass Bottle", "Recyclable"),
        ("🔋", "Battery", "Special Waste"),
        ("📱", "Phone", "E-Waste")
    ]

    cols = st.columns(3)

    for i, (icon, name, category) in enumerate(common_items):

        with cols[i % 3]:

            st.markdown(
                f"""
                <div class="card">
                <h2>{icon}</h2>
                <h3>{name}</h3>
                <p class="muted">{category}</p>
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# WASTE SCANNER
# ============================================================

elif page == "📷 Waste Scanner":

    st.markdown("## 📷 Waste Scanner")

    st.write(
        "Upload a photo of a waste item. For this prototype, the image upload is provided and the user can confirm the item using manual search."
    )

    uploaded_file = st.file_uploader(
        "Upload a photo",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:

        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Uploaded waste item",
            width=400
        )

        st.info(
            "🤖 AI image classification can be connected here using a computer-vision model or API."
        )

        scanner_search = st.text_input(
            "Confirm / search the item",
            placeholder="Example: bottle"
        )

        if scanner_search:

            result = identify_waste(scanner_search)

            if result:
                show_waste_result(scanner_search, result)
            else:
                st.error(
                    "Item not found in the current WasteWise database."
                )


# ============================================================
# CORRECT BIN
# ============================================================

elif page == "♻️ Correct Bin":

    st.markdown("## ♻️ Find the Correct Bin")

    item = st.selectbox(
        "Select a waste item",
        sorted(waste_data.keys())
    )

    result = waste_data[item]

    st.markdown(
        f"""
        <div class="result-card">
            <h1>{result['icon']}</h1>
            <h2>{result['bin']}</h2>
            <p><strong>Category:</strong> {result['category']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 💡 Why?")
    st.info(result["why"])


# ============================================================
# WASTE GUIDE
# ============================================================

elif page == "📚 Waste Guide":

    st.markdown("## 📚 Waste Guide")

    st.write(
        "Learn how common household materials should be segregated."
    )

    category_filter = st.selectbox(
        "Filter by category",
        [
            "All",
            "Organic Waste",
            "Recyclable Waste",
            "Non-Recyclable Waste",
            "Hazardous / Special Waste",
            "E-Waste"
        ]
    )

    filtered_items = waste_data.items()

    for item, data in filtered_items:

        if category_filter != "All" and data["category"] != category_filter:
            continue

        with st.expander(
            f"{data['icon']} {item.title()} — {data['category']}"
        ):

            st.write(
                f"**Correct bin:** {data['bin']}"
            )

            st.write(
                f"**Why:** {data['why']}"
            )

            st.write("**Disposal:**")

            for instruction in data["instructions"]:
                st.write(f"• {instruction}")


# ============================================================
# SPECIAL WASTE
# ============================================================

elif page == "⚠️ Special Waste":

    st.markdown("## ⚠️ Special Waste")

    st.warning(
        "Special waste should not normally be mixed with household waste. Follow local collection guidance."
    )

    special_items = {
        "🔋 Batteries": "Take batteries to an authorized battery/e-waste collection point.",
        "📱 E-Waste": "Take electronics to an authorized e-waste recycler.",
        "💊 Medicines": "Use an appropriate medicine take-back or disposal service.",
        "💡 Bulbs": "Handle carefully and use a suitable collection facility.",
        "🧪 Chemicals": "Follow local hazardous-waste collection instructions."
    }

    for name, description in special_items.items():

        st.markdown(
            f"""
            <div class="card">
                <h3>{name}</h3>
                <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# COLLECTION SCHEDULE
# ============================================================

elif page == "📅 Collection Schedule":

    st.markdown("## 📅 Collection Schedule")

    st.write(
        "View upcoming waste collection dates."
    )

    schedule = [
        ("Organic Waste", "Friday", "7:00 AM – 10:00 AM"),
        ("Recyclable Waste", "Saturday", "7:00 AM – 11:00 AM"),
        ("General Waste", "Monday", "7:00 AM – 10:00 AM"),
        ("E-Waste", "1st Sunday of Month", "9:00 AM – 1:00 PM")
    ]

    for waste_type, day, time in schedule:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(f"**♻️ {waste_type}**")

        with col2:
            st.write(day)

        with col3:
            st.write(time)

    st.markdown("---")

    if st.button("🔔 Enable Collection Reminder"):
        st.success(
            "Collection reminder enabled for this demo."
        )


# ============================================================
# RECYCLING CENTRES
# ============================================================

elif page == "📍 Recycling Centres":

    st.markdown("## 📍 Nearby Recycling Centres")

    st.info(
        "📍 Location services can be connected to Google Maps or another maps API in the production version."
    )

    centres = [
        ("Green Earth Recycling Centre", "Recyclables • Plastic • Paper • Metal"),
        ("EcoTech E-Waste Centre", "Phones • Computers • Batteries • Electronics"),
        ("Community Recycling Hub", "Paper • Glass • Plastic • Metal")
    ]

    for name, accepted in centres:

        st.markdown(
            f"""
            <div class="card">
                <h3>📍 {name}</h3>
                <p><strong>Accepted:</strong> {accepted}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.button(
            "🧭 Get Directions",
            key=name
        )


# ============================================================
# ECO POINTS
# ============================================================

elif page == "🏆 Eco Points":

    st.markdown("## 🏆 Eco Points")

    points = st.session_state.eco_points

    st.metric(
        "Total Eco Points",
        points
    )

    st.progress(
        min(points / 500, 1.0)
    )

    st.write(
        f"You need **{max(500 - points, 0)} more points** to reach the next major milestone."
    )

    st.markdown("## 🥇 Your Badges")

    badges = []

    if points >= 50:
        badges.append("🌱 First Steps")

    if points >= 100:
        badges.append("♻️ Waste Warrior")

    if points >= 250:
        badges.append("🌍 Eco Champion")

    if points >= 500:
        badges.append("🏆 Planet Protector")

    if badges:

        for badge in badges:
            st.success(badge)

    else:
        st.info(
            "Start correctly segregating waste to unlock your first badge!"
        )

    st.markdown("## 📊 Activity")

    st.write(
        f"Items identified: **{len(st.session_state.scanned_items)}**"
    )


# ============================================================
# TIPS & LEARNING
# ============================================================

elif page == "🌱 Tips & Learning":

    st.markdown("## 🌱 Tips & Learning")

    tips = [
        "♻️ Separate waste at the source instead of mixing everything together.",
        "🥬 Compost food and garden waste where possible.",
        "💧 Keep recyclable materials reasonably clean and dry.",
        "🔋 Never place batteries in normal household waste.",
        "📱 Take electronic devices to authorized e-waste recyclers.",
        "🛍️ Reduce the use of unnecessary single-use plastics.",
        "🍶 Reuse containers whenever practical.",
        "🌎 Small segregation habits can make recycling more effective."
    ]

    for tip in tips:

        st.markdown(
            f"""
            <div class="card">
                <h3>{tip}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("## 💡 Daily Challenge")

    st.info(
        "Today's challenge: Correctly separate your kitchen waste into organic and recyclable/general categories."
    )


# ============================================================
# PROFILE
# ============================================================

elif page == "⚙️ Profile":

    st.markdown("## ⚙️ Profile")

    st.markdown(
        f"""
        <div class="card">
            <h2>🌱 Eco User</h2>
            <p>Keep making small changes for a cleaner future.</p>
            <h3>🏆 {st.session_state.eco_points} Eco Points</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ⭐ Your Activity")

    st.write(
        f"Correctly identified items: **{len(st.session_state.scanned_items)}**"
    )

    st.markdown("### 💾 Saved Items")

    if st.session_state.saved_items:

        for item in st.session_state.saved_items:
            st.write(f"♻️ {item}")

    else:
        st.info(
            "You haven't saved any items yet."
        )

    st.markdown("### 🔔 Notifications")

    st.checkbox(
        "Collection reminders",
        value=True
    )

    st.checkbox(
        "Daily sustainability tips",
        value=True
    )

    st.checkbox(
        "Eco Point updates",
        value=True
    )

    st.markdown("### 💬 Feedback")

    feedback = st.text_area(
        "Tell us how we can improve WasteWise"
    )

    if st.button("Submit Feedback"):

        if feedback.strip():
            st.success(
                "Thank you for helping us improve WasteWise! 🌱"
            )
        else:
            st.warning(
                "Please enter some feedback first."
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#6c7c70;">
        <p>♻️ <strong>WasteWise</strong></p>
        <p>Start today. A greater tomorrow.</p>
        <p>Making responsible waste management simple.</p>
    </div>
    """,
    unsafe_allow_html=True
)