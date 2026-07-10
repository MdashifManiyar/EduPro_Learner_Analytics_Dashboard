import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── CUSTOM CSS — Professional Styling ──────────────────────────────
st.markdown("""
<style>
    /* Overall page padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Main title styling */
    h1 {
        font-weight: 700 !important;
        letter-spacing: -0.5px;
        padding-bottom: 0.3rem;
        border-bottom: 3px solid #1D9E75;
        margin-bottom: 1rem !important;
    }

    h2, h3 {
        font-weight: 600 !important;
        letter-spacing: -0.2px;
    }

    /* Tabs — bigger, cleaner, clear active indicator */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 46px;
        padding: 0 20px;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
        font-size: 0.95rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(29, 158, 117, 0.12);
        border-bottom: 3px solid #1D9E75 !important;
    }

    /* Metric cards — subtle border + shadow, no harsh colors */
    [data-testid="stMetric"] {
        background: rgba(135, 135, 135, 0.06);
        border: 1px solid rgba(135, 135, 135, 0.15);
        border-radius: 10px;
        padding: 14px 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    [data-testid="stMetricLabel"] {
        font-weight: 600 !important;
        font-size: 0.8rem !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #1D9E75;
    }

    /* Sidebar — light, clean separation from main content */
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(135, 135, 135, 0.15);
    }
    [data-testid="stSidebar"] h1 {
        border-bottom: none;
        font-size: 1.4rem !important;
    }

    /* Buttons — rounded, consistent accent color */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid rgba(29, 158, 117, 0.4);
    }
    .stButton > button:hover {
        border-color: #1D9E75;
        color: #1D9E75;
    }

    /* Dataframe / table corners */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
    }

    /* Captions — slightly muted, smaller */
    .stCaption, [data-testid="stCaptionContainer"] {
        opacity: 0.75;
    }

    /* Hide Streamlit's default footer/menu for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="EduPro Analytics Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── COLOUR PALETTE ─────────────────────────────────────────────────
TEAL   = ["#9FE1CB", "#5DCAA5", "#1D9E75", "#0f6e56"]
PURPLE = ["#CECBF6", "#AFA9EC", "#7F77DD", "#534AB7"]
AMBER  = ["#FAC775", "#EF9F27", "#BA7517"]
CORAL  = ["#F5C4B3", "#F0997B", "#D85A30"]

AGE_ORDER   = ['Teen (15–17)', 'Young Adult (18–25)', 'Adult (26–35)']
LEVEL_ORDER = ['Beginner', 'Intermediate', 'Advanced']

# ── LOAD DATA ──────────────────────────────────────────────────────
@st.cache_data
def load_data():
    xl = pd.ExcelFile("EduPro Online Platform.xlsx")
    users        = pd.read_excel(xl, "Users")
    courses      = pd.read_excel(xl, "Courses")
    transactions = pd.read_excel(xl, "Transactions")

    def age_group(a):
        if a <= 17:   return 'Teen (15–17)'
        elif a <= 25: return 'Young Adult (18–25)'
        else:         return 'Adult (26–35)'

    users_c = users[['UserID', 'Age', 'Gender']].copy()
    users_c['AgeGroup'] = users_c['Age'].apply(age_group)

    courses_c = courses[['CourseID', 'CourseName', 'CourseCategory',
                          'CourseType', 'CourseLevel',
                          'CoursePrice', 'CourseRating']].copy()

    tx = transactions[['TransactionID', 'UserID', 'CourseID',
                        'TransactionDate', 'Amount', 'PaymentMethod']].copy()
    tx['Year']  = tx['TransactionDate'].dt.year
    tx['Month'] = tx['TransactionDate'].dt.month

    master = (tx
              .merge(users_c,   on='UserID',  how='inner')
              .merge(courses_c, on='CourseID', how='inner'))

    return users_c, courses_c, tx, master

users_df, courses_df, tx_df, master = load_data()

# ── FILTER OPTIONS ─────────────────────────────────────────────────
AGE_OPTIONS      = ['Teen (15–17)', 'Young Adult (18–25)', 'Adult (26–35)']
GENDER_OPTIONS   = ['Female', 'Male']
CATEGORY_OPTIONS = sorted(master['CourseCategory'].dropna().unique().tolist())
LEVEL_OPTIONS    = ['Beginner', 'Intermediate', 'Advanced']
TYPE_OPTIONS     = ['Free', 'Paid']

# ── RESET CALLBACK ───────────────────────────────────────────────
def reset_filters():
    st.session_state["widget_age"]      = AGE_OPTIONS
    st.session_state["widget_gender"]   = GENDER_OPTIONS
    st.session_state["widget_category"] = CATEGORY_OPTIONS
    st.session_state["widget_level"]    = LEVEL_OPTIONS
    st.session_state["widget_type"]     = TYPE_OPTIONS

# ── SIDEBAR ────────────────────────────────────────────────────────
with st.sidebar:
    st.sidebar.image("Unified_logo.png", use_container_width=True)
    #st.title("📚 EduPro") # for normal title without allignment
    st.markdown(
    "<h2 style='text-align:center;'>📚 EduPro</h2>",
    unsafe_allow_html=True,
    )
    #st.caption("Learner Analytics Dashboard")
    #st.divider()

    sel_age = st.multiselect(
        "Age Group",
        options=AGE_OPTIONS,
        default=AGE_OPTIONS,
        key="widget_age",
    )
    sel_gender = st.multiselect(
        "Gender",
        options=GENDER_OPTIONS,
        default=GENDER_OPTIONS,
        key="widget_gender",
    )
    sel_category = st.multiselect(
        "Course Category",
        options=CATEGORY_OPTIONS,
        default=CATEGORY_OPTIONS,
        key="widget_category",
    )
    sel_level = st.multiselect(
        "Course Level",
        options=LEVEL_OPTIONS,
        default=LEVEL_OPTIONS,
        key="widget_level",
    )
    sel_type = st.multiselect(
        "Course Type",
        options=TYPE_OPTIONS,
        default=TYPE_OPTIONS,
        key="widget_type",
    )

    #st.divider()
    st.button("🔄 Reset Filters", use_container_width=True, on_click=reset_filters)

    #st.divider()
    st.caption(f"🔍 Active filters: {len(sel_category)}/{len(CATEGORY_OPTIONS)} categories, "
               f"{len(sel_age)}/{len(AGE_OPTIONS)} age groups, {len(sel_level)}/{len(LEVEL_OPTIONS)} levels")

# ── APPLY FILTERS ──────────────────────────────────────────────────
# Use full data if any filter is cleared to empty
_age      = sel_age      if sel_age      else AGE_OPTIONS
_gender   = sel_gender   if sel_gender   else GENDER_OPTIONS
_category = sel_category if sel_category else CATEGORY_OPTIONS
_level    = sel_level    if sel_level    else LEVEL_OPTIONS
_type     = sel_type     if sel_type     else TYPE_OPTIONS

filtered = master[
    master['AgeGroup'].isin(_age)           &
    master['Gender'].isin(_gender)          &
    master['CourseCategory'].isin(_category) &
    master['CourseLevel'].isin(_level)      &
    master['CourseType'].isin(_type)
].copy()

# Demographics tab uses only age + gender filter (not course filters)
filtered_users = users_df[
    users_df['AgeGroup'].isin(_age)    &
    users_df['Gender'].isin(_gender)
].copy()

# ── HELPERS ────────────────────────────────────────────────────────
def kpi(col, value, label):
    col.metric(label=label, value=value)

def hdr(text):
    st.markdown(f"**{text}**")

def insight(text):
    # st.info() already understands markdown bold (**text**), so no HTML needed.
    st.info(text)

def clean_fig(fig, h=320):
    fig.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=30, b=10, l=10, r=10), height=h,
        font=dict(family="sans-serif", size=12),
        legend=dict(bgcolor='rgba(0,0,0,0)', borderwidth=0),
    )
    fig.update_xaxes(showgrid=False, linecolor='#e0e0e0')
    fig.update_yaxes(gridcolor='#f0f0f0', linecolor='#e0e0e0')
    return fig

def classify_segment(row):
    """Classify a user as Beginner-only, Advanced-only, or Mixed-level
    based on which course levels they have enrolled in."""
    has_beg = row['Beginner'] > 0
    has_adv = row['Advanced'] > 0
    has_int = row['Intermediate'] > 0
    if has_beg and not has_adv and not has_int:
        return 'Beginner-only'
    elif has_adv and not has_beg and not has_int:
        return 'Advanced-only'
    else:
        return 'Mixed-level'

# Enrollments per user, computed once and reused across Tabs 1, 5, and 6
# instead of recalculating the same groupby in each tab.
user_enroll = (filtered.groupby('UserID').size().reset_index(name='CourseCount')
               .merge(users_df[['UserID', 'AgeGroup', 'Gender']], on='UserID', how='left'))

# ── MAIN HEADER ────────────────────────────────────────────────────
st.title("📚 EduPro Learner Analytics Dashboard")
st.markdown(
    f"Showing **{len(filtered):,}** of **{len(master):,}** enrollments "
    f"({len(filtered)/len(master)*100:.1f}% of data based on current filters)"
)

if len(filtered) == 0:
    st.error("No data matches the current filter selection. Please adjust your filters.")
    st.stop()

st.divider()

# ── TABS ───────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🏠 Overview",
    "👥 Demographics",
    "📊 Enrollments",
    "🔥 Cross Analysis",
    "💡 Behavior",
    "📈 KPIs",
    "🎯 Problem, Solution & Insights",
])

# ══════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Platform Overview")
    st.caption("High-level summary based on current filter selection.")

    c1, c2, c3, c4, c5 = st.columns(5)
    kpi(c1, f"{len(filtered_users):,}",                                   "Users (filtered)")
    kpi(c2, f"{len(filtered):,}",                                         "Enrollments (filtered)")
    kpi(c3, f"{len(master):,}",                                           "Total Enrollments")
    kpi(c4, f"{filtered.groupby('UserID').size().mean():.2f}",            "Avg Courses / User")
    kpi(c5, f"{filtered['CourseCategory'].nunique()}",                    "Categories Selected")

    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
        hdr("Enrollments by age group")
        d = (filtered.groupby('AgeGroup').size()
             .reindex(AGE_ORDER, fill_value=0).reset_index(name='Enrollments'))
        fig = px.bar(d, x='AgeGroup', y='Enrollments',
                     color='AgeGroup', color_discrete_sequence=TEAL,
                     text='Enrollments')
        fig.update_traces(textposition='outside', textfont_size=13)
        fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Enrollments")
        st.plotly_chart(clean_fig(fig), use_container_width=True)

        # "Most active" has two valid readings — total volume vs per-user engagement
        if len(filtered) > 0 and d['Enrollments'].sum() > 0:
            avg_by_age = (user_enroll.groupby('AgeGroup')['CourseCount']
                          .mean().reindex(AGE_ORDER).dropna())

            if len(avg_by_age) > 0:
                most_volume_age  = d.loc[d['Enrollments'].idxmax(), 'AgeGroup']
                most_volume_n    = int(d['Enrollments'].max())
                most_engaged_age = avg_by_age.idxmax()
                most_engaged_val = avg_by_age.max()

                ac1, ac2 = st.columns(2)
                with ac1:
                    st.info(f"📊 **By total volume:** {most_volume_age} "
                            f"— {most_volume_n:,} enrollments")
                with ac2:
                    st.info(f"🔥 **By per-user engagement:** {most_engaged_age} "
                            f"— {most_engaged_val:.2f} avg courses/user")

    with col_b:
        hdr("Enrollments by gender")
        d = filtered.groupby('Gender').size().reset_index(name='Enrollments')
        fig = px.pie(d, names='Gender', values='Enrollments',
                     color='Gender',
                     color_discrete_map={'Female': PURPLE[2], 'Male': PURPLE[1]},
                     hole=0.48)
        fig.update_traces(textinfo='label+percent+value', textfont_size=13,
                          pull=[0.03, 0.03])
        fig.update_layout(showlegend=False)
        st.plotly_chart(clean_fig(fig), use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        hdr("Enrollments by course category")
        d = (filtered.groupby('CourseCategory').size()
             .sort_values(ascending=True).reset_index(name='Enrollments'))
        fig = px.bar(d, x='Enrollments', y='CourseCategory',
                     orientation='h',
                     color='Enrollments',
                     color_continuous_scale=['#9FE1CB', '#085041'],
                     text='Enrollments')
        fig.update_traces(textposition='outside', textfont_size=10)
        fig.update_layout(showlegend=False, coloraxis_showscale=False,
                          xaxis_title="", yaxis_title="")
        st.plotly_chart(clean_fig(fig, h=380), use_container_width=True)

    with col_d:
        hdr("Course level distribution")
        d = (filtered.groupby('CourseLevel').size()
             .reindex(LEVEL_ORDER, fill_value=0).reset_index(name='Enrollments'))
        fig = px.pie(d, names='CourseLevel', values='Enrollments',
                     color='CourseLevel',
                     color_discrete_map={
                         'Beginner': PURPLE[0],
                         'Intermediate': AMBER[1],
                         'Advanced': TEAL[2]},
                     hole=0.48)
        fig.update_traces(textinfo='label+percent', textfont_size=13,
                          pull=[0.03, 0.03, 0.03])
        fig.update_layout(showlegend=True)
        st.plotly_chart(clean_fig(fig, h=380), use_container_width=True)

    insight("\"Most active\" can mean two different things: Adults generate the most total enrollments "
            "simply because they're the largest group, while Teens average the highest enrollments per "
            "user — the platform's most engaged individual learners, group size aside. "
            "Use the sidebar filters to slice by Age Group, Gender, Course Category, "
            "Level, and Type — every chart across all tabs updates instantly.")


# ══════════════════════════════════════════════════════════════════
# TAB 2 — DEMOGRAPHICS
# ══════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Learner Demographics")
    st.caption("Responds to Age Group and Gender filters only.")

    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, f"{len(filtered_users):,}",                                        "Total Users")
    kpi(c2, f"{len(filtered_users[filtered_users['Gender']=='Female']):,}",    "Female Users")
    kpi(c3, f"{len(filtered_users[filtered_users['Gender']=='Male']):,}",      "Male Users")
    kpi(c4, f"{filtered_users['Age'].mean():.1f}" if len(filtered_users) > 0 else "—", "Avg Age")

    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
        hdr("Age distribution (individual ages)")
        d = filtered_users.groupby('Age').size().reset_index(name='Users')
        d['Color'] = d['Age'].apply(
            lambda a: TEAL[0] if a <= 17 else TEAL[1] if a <= 25 else TEAL[2])
        fig = px.bar(d, x='Age', y='Users',
                     color='Color', color_discrete_map='identity')
        fig.update_layout(showlegend=False, xaxis_title="Age", yaxis_title="Users")
        fig.update_xaxes(dtick=1)
        st.plotly_chart(clean_fig(fig), use_container_width=True)

    with col_b:
        hdr("Users by age group")
        d = (filtered_users.groupby('AgeGroup').size()
             .reindex(AGE_ORDER, fill_value=0).reset_index(name='Users'))
        total_u = d['Users'].sum()
        d['Pct'] = (d['Users'] / total_u * 100).round(1) if total_u > 0 else 0
        fig = px.bar(d, x='AgeGroup', y='Users',
                     color='AgeGroup', color_discrete_sequence=TEAL,
                     text=d['Pct'].apply(lambda x: f"{x}%"))
        fig.update_traces(textposition='outside', textfont_size=14)
        fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Users")
        st.plotly_chart(clean_fig(fig), use_container_width=True)

    st.divider()
    col_c, col_d = st.columns(2)

    with col_c:
        hdr("Gender distribution")
        d = filtered_users['Gender'].value_counts().reset_index()
        d.columns = ['Gender', 'Users']
        fig = px.pie(d, names='Gender', values='Users',
                     color='Gender',
                     color_discrete_map={'Female': PURPLE[2], 'Male': PURPLE[1]},
                     hole=0.5)
        fig.update_traces(textinfo='label+percent+value', textfont_size=14,
                          pull=[0.04, 0.04])
        fig.update_layout(showlegend=False)
        st.plotly_chart(clean_fig(fig), use_container_width=True)

    with col_d:
        hdr("Gender split across age groups")
        d = (filtered_users.groupby(['AgeGroup', 'Gender']).size()
             .reset_index(name='Users'))
        d['AgeGroup'] = pd.Categorical(d['AgeGroup'], AGE_ORDER, ordered=True)
        d = d.sort_values('AgeGroup')
        fig = px.bar(d, x='AgeGroup', y='Users', color='Gender',
                     barmode='group',
                     color_discrete_map={'Female': PURPLE[2], 'Male': PURPLE[1]},
                     text='Users')
        fig.update_traces(textposition='outside', textfont_size=11)
        fig.update_layout(xaxis_title="", yaxis_title="Users", legend_title="Gender")
        st.plotly_chart(clean_fig(fig), use_container_width=True)

    insight("Gender parity is near-perfect at 50.7% Female / 49.3% Male across all age groups. "
            "This makes gender comparisons statistically valid throughout the analysis.")


# ══════════════════════════════════════════════════════════════════
# TAB 3 — ENROLLMENT DISTRIBUTION
# ══════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Enrollment Distribution")
    st.caption("Responds to all sidebar filters.")

    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, f"{len(filtered):,}",                                        "Total Enrollments")
    kpi(c2, f"{len(filtered[filtered['CourseType']=='Free']):,}",        "Free Enrollments")
    kpi(c3, f"{len(filtered[filtered['CourseType']=='Paid']):,}",        "Paid Enrollments")
    top_cat = filtered['CourseCategory'].value_counts()
    kpi(c4, top_cat.index[0] if len(top_cat) > 0 else "—",              "Top Category")

    st.divider()
    hdr("Enrollments by course category")
    d = (filtered.groupby('CourseCategory').size()
         .sort_values(ascending=False).reset_index(name='Enrollments'))

    # Highlight the most and least popular category with distinct colors
    if len(d) > 0:
        most_pop  = d.iloc[0]
        least_pop = d.iloc[-1]
        bar_colors = []
        for cat in d['CourseCategory']:
            if cat == most_pop['CourseCategory']:
                bar_colors.append('#0f6e56')       # dark teal — most popular
            elif cat == least_pop['CourseCategory']:
                bar_colors.append('#D85A30')       # coral — least popular
            else:
                bar_colors.append('#9FE1CB')       # neutral teal
        fig = px.bar(d, x='CourseCategory', y='Enrollments',
                     text='Enrollments')
        fig.update_traces(marker_color=bar_colors,
                          textposition='outside', textfont_size=11)
        fig.update_layout(showlegend=False,
                          xaxis_title="", yaxis_title="Enrollments",
                          xaxis_tickangle=-30)
        st.plotly_chart(clean_fig(fig, h=360), use_container_width=True)

        mc1, mc2 = st.columns(2)
        with mc1:
            st.success(f"🏆 **Most popular:** {most_pop['CourseCategory']} "
                       f"— {int(most_pop['Enrollments']):,} enrollments")
        with mc2:
            st.error(f"📉 **Least popular:** {least_pop['CourseCategory']} "
                     f"— {int(least_pop['Enrollments']):,} enrollments")
    else:
        st.info("No data for selected filters.")

    st.divider()
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        hdr("Course level preference")
        d = (filtered.groupby('CourseLevel').size()
             .reindex(LEVEL_ORDER, fill_value=0).reset_index(name='Enrollments'))
        fig = px.pie(d, names='CourseLevel', values='Enrollments',
                     color='CourseLevel',
                     color_discrete_map={
                         'Beginner': PURPLE[0],
                         'Intermediate': AMBER[1],
                         'Advanced': TEAL[2]},
                     hole=0.46)
        fig.update_traces(textinfo='label+percent', textfont_size=12,
                          pull=[0.03, 0.03, 0.03])
        fig.update_layout(showlegend=False)
        st.plotly_chart(clean_fig(fig, h=280), use_container_width=True)

    with col_b:
        hdr("Free vs Paid enrollments")
        d = filtered.groupby('CourseType').size().reset_index(name='Enrollments')
        fig = px.pie(d, names='CourseType', values='Enrollments',
                     color='CourseType',
                     color_discrete_map={'Free': TEAL[2], 'Paid': AMBER[1]},
                     hole=0.46)
        fig.update_traces(textinfo='label+percent+value', textfont_size=12,
                          pull=[0.04, 0.04])
        fig.update_layout(showlegend=False)
        st.plotly_chart(clean_fig(fig, h=280), use_container_width=True)

    with col_c:
        hdr("Payment method (paid only)")
        paid = filtered[filtered['CourseType'] == 'Paid']
        if len(paid) > 0:
            d = paid.groupby('PaymentMethod').size().reset_index(name='Count')
            fig = px.pie(d, names='PaymentMethod', values='Count',
                         color_discrete_sequence=CORAL, hole=0.46)
            fig.update_traces(textinfo='label+percent', textfont_size=12,
                              pull=[0.03, 0.03, 0.03])
            fig.update_layout(showlegend=False)
            st.plotly_chart(clean_fig(fig, h=280), use_container_width=True)
        else:
            st.info("No paid enrollments in current filter selection.")

    st.divider()
    hdr("Do beginners prefer certain course types or categories?")
    st.caption("Direct comparison of Beginner-level enrollments vs Intermediate/Advanced")

    beg_data    = filtered[filtered['CourseLevel'] == 'Beginner']
    nonbeg_data = filtered[filtered['CourseLevel'] != 'Beginner']

    if len(beg_data) == 0:
        st.info("No Beginner-level enrollments in current filter selection.")
    else:
        bq1, bq2 = st.columns(2)

        with bq1:
            st.caption("Free vs Paid — Beginner vs other levels")
            beg_type   = beg_data['CourseType'].value_counts(normalize=True).mul(100).round(1)
            other_type = (nonbeg_data['CourseType'].value_counts(normalize=True).mul(100).round(1)
                          if len(nonbeg_data) > 0 else pd.Series(dtype=float))

            comp_df = pd.DataFrame({
                'CourseType': ['Free', 'Paid'],
                'Beginner':   [beg_type.get('Free', 0), beg_type.get('Paid', 0)],
                'Other Levels': [other_type.get('Free', 0), other_type.get('Paid', 0)],
            }).melt(id_vars='CourseType', var_name='Group', value_name='Pct')

            fig = px.bar(comp_df, x='CourseType', y='Pct', color='Group',
                         barmode='group',
                         color_discrete_map={'Beginner': PURPLE[0], 'Other Levels': TEAL[2]},
                         text=comp_df['Pct'].apply(lambda x: f"{x:.1f}%"))
            fig.update_traces(textposition='outside', textfont_size=12)
            fig.update_layout(xaxis_title="", yaxis_title="% of enrollments",
                              legend_title="", yaxis_range=[0, 100])
            st.plotly_chart(clean_fig(fig, h=300), use_container_width=True)

        with bq2:
            st.caption("Top categories among Beginner-level enrollments")
            beg_cat = (beg_data.groupby('CourseCategory').size()
                      .sort_values(ascending=False).head(6).reset_index(name='Enrollments'))
            fig = px.bar(beg_cat, x='Enrollments', y='CourseCategory',
                         orientation='h',
                         color_discrete_sequence=[PURPLE[0]],
                         text='Enrollments')
            fig.update_traces(textposition='outside', textfont_size=11)
            fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="",
                              yaxis=dict(autorange="reversed"))
            st.plotly_chart(clean_fig(fig, h=300), use_container_width=True)

        beg_free_pct = beg_type.get('Free', 0)
        other_free_pct = other_type.get('Free', 0) if len(other_type) > 0 else 0
        top_beg_cat = beg_cat.iloc[0]['CourseCategory'] if len(beg_cat) > 0 else "N/A"

        insight(f"Beginner-level enrollments are **{beg_free_pct:.1f}% Free**, compared to "
                f"**{other_free_pct:.1f}% Free** for Intermediate/Advanced enrollments — "
                f"beginners lean more heavily toward no-cost content, likely to explore before "
                f"committing financially. By category, **{top_beg_cat}** is the most common "
                f"entry point for Beginner-level learners, suggesting it functions as a key on-ramp "
                f"category for EduPro's newest learners.")

    st.divider()
    hdr("Monthly enrollment trend")
    d = (filtered.groupby(['Year', 'Month']).size().reset_index(name='Enrollments'))
    d['Period'] = d['Year'].astype(str) + '-' + d['Month'].astype(str).str.zfill(2)
    d = d.sort_values('Period')
    fig = px.line(d, x='Period', y='Enrollments',
                  markers=True, line_shape='spline',
                  color_discrete_sequence=[TEAL[2]])
    fig.update_traces(line_width=2.5, marker_size=7,
                      fill='tozeroy', fillcolor='rgba(29,158,117,0.08)')
    fig.update_layout(xaxis_title="Month", yaxis_title="Enrollments")
    fig.update_xaxes(tickangle=-30)
    st.plotly_chart(clean_fig(fig, h=280), use_container_width=True)

    free_share = (len(filtered[filtered['CourseType']=='Free']) / len(filtered) * 100) if len(filtered)>0 else 0
    if len(d) > 0:
        insight(f"Free courses account for **{free_share:.1f}%** of enrollments — learners strongly "
                f"prefer no-cost options. Beginner and Advanced levels are nearly tied, showing the "
                f"platform serves both new and experienced learners.")


# ══════════════════════════════════════════════════════════════════
# TAB 4 — CROSS ANALYSIS
# ══════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Demographics × Course Preference")
    st.caption("Responds to all sidebar filters.")

    hdr("Age group × course category heatmap")
    pivot = (filtered.groupby(['AgeGroup', 'CourseCategory']).size()
             .unstack(fill_value=0)
             .reindex([a for a in AGE_ORDER if a in filtered['AgeGroup'].unique()]))

    if pivot.empty or pivot.shape[1] == 0:
        st.info("No data for selected filters.")
    else:
        fig = go.Figure(go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            colorscale=[[0, '#E8F7F1'], [0.5, '#1D9E75'], [1, '#085041']],
            text=pivot.values,
            texttemplate="%{text}",
            textfont={"size": 13, "color": "black"},
            hoverongaps=False,
            colorbar=dict(title="Enrollments"),
        ))
        fig.update_layout(
            xaxis_tickangle=-30, xaxis_title="", yaxis_title="",
            height=300, margin=dict(t=20, b=80, l=10, r=10),
            plot_bgcolor='white', paper_bgcolor='white',
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
        hdr("Gender × course level")
        d = (filtered.groupby(['Gender', 'CourseLevel']).size()
             .reset_index(name='Enrollments'))
        d['CourseLevel'] = pd.Categorical(d['CourseLevel'], LEVEL_ORDER, ordered=True)
        d = d.sort_values('CourseLevel')
        fig = px.bar(d, x='CourseLevel', y='Enrollments', color='Gender',
                     barmode='group',
                     color_discrete_map={'Female': PURPLE[2], 'Male': PURPLE[1]},
                     text='Enrollments')
        fig.update_traces(textposition='outside', textfont_size=11)
        fig.update_layout(xaxis_title="", yaxis_title="Enrollments", legend_title="Gender")
        st.plotly_chart(clean_fig(fig), use_container_width=True)

    with col_b:
        hdr("Gender × course category")
        d = (filtered.groupby(['Gender', 'CourseCategory']).size()
             .reset_index(name='Enrollments'))
        fig = px.bar(d, x='CourseCategory', y='Enrollments', color='Gender',
                     barmode='stack',
                     color_discrete_map={'Female': PURPLE[2], 'Male': PURPLE[1]})
        fig.update_layout(xaxis_title="", xaxis_tickangle=-30,
                          yaxis_title="Enrollments", legend_title="Gender")
        st.plotly_chart(clean_fig(fig, h=320), use_container_width=True)

    st.divider()
    hdr("Age group × course level — are Beginner, Intermediate, or Advanced more popular in specific age groups?")

    d = (filtered.groupby(['AgeGroup', 'CourseLevel']).size()
         .reset_index(name='Enrollments'))
    d['AgeGroup']   = pd.Categorical(d['AgeGroup'],   AGE_ORDER,   ordered=True)
    d['CourseLevel'] = pd.Categorical(d['CourseLevel'], LEVEL_ORDER, ordered=True)
    d = d.sort_values(['AgeGroup', 'CourseLevel'])

    lvl_pivot = (filtered.groupby(['AgeGroup', 'CourseLevel']).size()
                .unstack(fill_value=0).reindex(AGE_ORDER).dropna(how='all'))
    for lvl in LEVEL_ORDER:
        if lvl not in lvl_pivot.columns:
            lvl_pivot[lvl] = 0
    lvl_pct = (lvl_pivot.div(lvl_pivot.sum(axis=1), axis=0) * 100).round(1)
    lvl_pct_long = lvl_pct.reset_index().melt(id_vars='AgeGroup', var_name='CourseLevel', value_name='Pct')
    lvl_pct_long['CourseLevel'] = pd.Categorical(lvl_pct_long['CourseLevel'], LEVEL_ORDER, ordered=True)
    lvl_pct_long = lvl_pct_long.sort_values(['AgeGroup', 'CourseLevel'])

    lc1, lc2 = st.columns(2)

    with lc1:
        st.caption("Raw enrollment counts (affected by group size)")
        fig = px.bar(d, x='AgeGroup', y='Enrollments', color='CourseLevel',
                     barmode='group',
                     color_discrete_map={
                         'Beginner': PURPLE[0],
                         'Intermediate': AMBER[1],
                         'Advanced': TEAL[2]},
                     text='Enrollments')
        fig.update_traces(textposition='outside', textfont_size=10)
        fig.update_layout(xaxis_title="", yaxis_title="Enrollments", legend_title="Level")
        st.plotly_chart(clean_fig(fig, h=340), use_container_width=True)

    with lc2:
        st.caption("Within-group % — the true preference signal, independent of group size")
        fig = px.bar(lvl_pct_long, x='AgeGroup', y='Pct', color='CourseLevel',
                     barmode='group',
                     color_discrete_map={
                         'Beginner': PURPLE[0],
                         'Intermediate': AMBER[1],
                         'Advanced': TEAL[2]},
                     text=lvl_pct_long['Pct'].apply(lambda x: f"{x:.1f}%"))
        fig.update_traces(textposition='outside', textfont_size=10)
        fig.update_layout(xaxis_title="", yaxis_title="% within age group",
                          legend_title="Level", yaxis_range=[0, 50])
        st.plotly_chart(clean_fig(fig, h=340), use_container_width=True)

    # Determine the top level per age group dynamically (the real answer to this question)
    top_level_per_age = {}
    for age in lvl_pct.index:
        top_level_per_age[age] = (lvl_pct.loc[age].idxmax(), lvl_pct.loc[age].max())

    lines = "; ".join([f"{age} → {lvl} ({pct:.1f}%)" for age, (lvl, pct) in top_level_per_age.items()])

    distinct_top_levels = set(v[0] for v in top_level_per_age.values())
    if len(distinct_top_levels) > 1:
        age_pref_summary = (f"Level preference does vary by age group, when measured as a share of each "
                            f"group's own enrollments: {lines}. This is a genuine, non-obvious pattern — "
                            f"it is not simply explained by group size.")
    else:
        only_level = list(distinct_top_levels)[0]
        age_pref_summary = (f"Every age group shares the same top level preference ({only_level}), with "
                            f"shares of: {lines}. Age alone does not strongly differentiate level preference "
                            f"in the current selection.")

    insight(f"**Direct answer:** {age_pref_summary} The heatmap above shows Data Science and "
            f"Finance attract high engagement across all age groups, while Teens show relatively stronger "
            f"interest in Programming as a category.")


# ══════════════════════════════════════════════════════════════════
# TAB 5 — BEHAVIORAL INSIGHTS
# ══════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("Behavioral Insights")
    st.caption("Responds to all sidebar filters.")

    if len(user_enroll) == 0:
        st.warning("No users match the current filter selection.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        kpi(c1, f"{user_enroll['CourseCount'].mean():.2f}",            "Avg Courses / User")
        kpi(c2, f"{int(user_enroll['CourseCount'].max())}",             "Max (one user)")
        kpi(c3, f"{int((user_enroll['CourseCount'] == 1).sum())}",      "Users — 1 course only")
        kpi(c4, f"{int((user_enroll['CourseCount'] >= 5).sum())}",      "Users — 5+ courses")

        st.divider()
        col_a, col_b = st.columns(2)

        with col_a:
            hdr("Enrollment count distribution per user")
            d = user_enroll['CourseCount'].value_counts().sort_index().reset_index()
            d.columns = ['Courses Enrolled', 'Users']
            fig = px.bar(d, x='Courses Enrolled', y='Users',
                         color='Users',
                         color_continuous_scale=['#9FE1CB', '#085041'],
                         text='Users')
            fig.update_traces(textposition='outside', textfont_size=10)
            fig.update_layout(showlegend=False, coloraxis_showscale=False,
                              xaxis_title="Number of courses", yaxis_title="Users")
            st.plotly_chart(clean_fig(fig), use_container_width=True)

        with col_b:
            hdr("Avg courses per user — by age group")
            d = (user_enroll.groupby('AgeGroup')['CourseCount']
                 .mean().reindex(AGE_ORDER).dropna().reset_index())
            d.columns = ['AgeGroup', 'AvgCourses']
            if len(d) > 0:
                fig = px.bar(d, x='AgeGroup', y='AvgCourses',
                             color='AgeGroup', color_discrete_sequence=TEAL,
                             text=d['AvgCourses'].apply(lambda x: f"{x:.2f}"))
                fig.update_traces(textposition='outside', textfont_size=14)
                fig.update_layout(showlegend=False, xaxis_title="",
                                  yaxis_title="Avg courses / user",
                                  yaxis_range=[0, d['AvgCourses'].max() + 0.5])
                st.plotly_chart(clean_fig(fig), use_container_width=True)

        st.divider()
        col_c, col_d = st.columns(2)

        with col_c:
            hdr("Avg courses per user — by gender")
            d = user_enroll.groupby('Gender')['CourseCount'].mean().reset_index()
            d.columns = ['Gender', 'AvgCourses']
            if len(d) > 0:
                fig = px.bar(d, x='Gender', y='AvgCourses',
                             color='Gender',
                             color_discrete_map={'Female': PURPLE[2], 'Male': PURPLE[1]},
                             text=d['AvgCourses'].apply(lambda x: f"{x:.2f}"))
                fig.update_traces(textposition='outside', textfont_size=14)
                fig.update_layout(showlegend=False, xaxis_title="",
                                  yaxis_title="Avg courses / user",
                                  yaxis_range=[0, d['AvgCourses'].max() + 0.5])
                st.plotly_chart(clean_fig(fig), use_container_width=True)

        with col_d:
            hdr("Top 10 most active learners")
            top10 = (user_enroll.nlargest(10, 'CourseCount')
                     [['UserID', 'CourseCount', 'AgeGroup', 'Gender']]
                     .reset_index(drop=True))
            top10.index += 1
            top10.columns = ['User ID', 'Courses Taken', 'Age Group', 'Gender']
            st.dataframe(top10, use_container_width=True, height=300)

        # ── ENROLLMENT CONCENTRATION (Pareto-style) ──────────────────
        st.divider()
        hdr("Enrollment concentration among active users")

        sorted_users = user_enroll.sort_values('CourseCount', ascending=False).reset_index(drop=True)
        n_users = len(sorted_users)
        total_enroll_filtered = sorted_users['CourseCount'].sum()

        top10pct_n = max(1, int(n_users * 0.10))
        top20pct_n = max(1, int(n_users * 0.20))
        top10pct_share = sorted_users.head(top10pct_n)['CourseCount'].sum() / total_enroll_filtered * 100
        top20pct_share = sorted_users.head(top20pct_n)['CourseCount'].sum() / total_enroll_filtered * 100

        cc1, cc2, cc3 = st.columns(3)
        kpi(cc1, f"{top10pct_share:.1f}%", "Enrollments from Top 10% of Users")
        kpi(cc2, f"{top20pct_share:.1f}%", "Enrollments from Top 20% of Users")
        kpi(cc3, f"{n_users:,}",            "Total Active Users (filtered)")

        # Cumulative share curve (Lorenz-style)
        sorted_users['CumulativeEnrollments'] = sorted_users['CourseCount'].cumsum()
        sorted_users['CumulativeSharePct'] = (sorted_users['CumulativeEnrollments'] / total_enroll_filtered * 100)
        sorted_users['UserPercentile'] = ((sorted_users.index + 1) / n_users * 100)

        fig = px.line(sorted_users, x='UserPercentile', y='CumulativeSharePct',
                      color_discrete_sequence=[TEAL[2]])
        fig.update_traces(line_width=3, fill='tozeroy', fillcolor='rgba(29,158,117,0.10)')
        fig.add_shape(type='line', x0=0, y0=0, x1=100, y1=100,
                     line=dict(color='#bbbbbb', dash='dash', width=1.5))
        fig.update_layout(
            xaxis_title="Cumulative % of users (ranked by activity)",
            yaxis_title="Cumulative % of enrollments",
            xaxis_range=[0,100], yaxis_range=[0,100],
        )
        st.plotly_chart(clean_fig(fig, h=300), use_container_width=True)

        insight(f"The top 10% most active users generate **{top10pct_share:.1f}%** of all "
                f"enrollments, and the top 20% generate **{top20pct_share:.1f}%**. "
                f"This shows a meaningful concentration of engagement — a relatively small group of "
                f"power users drives a disproportionate share of platform activity, which is valuable "
                f"for retention and loyalty-targeting strategies.")

        # ── BEGINNER VS ADVANCED LEARNER BEHAVIOR ─────────────────────
        st.divider()
        hdr("Beginner vs Advanced learner behavior patterns")

        # Build per-user level pivot from filtered data
        user_level_pivot = (filtered.groupby(['UserID', 'CourseLevel']).size()
                            .unstack(fill_value=0))
        for lvl in LEVEL_ORDER:
            if lvl not in user_level_pivot.columns:
                user_level_pivot[lvl] = 0

        user_level_pivot['Segment'] = user_level_pivot.apply(classify_segment, axis=1)
        user_level_pivot = user_level_pivot.reset_index()

        # Total courses per user + course type preference
        user_totals = filtered.groupby('UserID').size().reset_index(name='TotalCourses')
        seg_df = user_level_pivot.merge(user_totals, on='UserID')

        seg_summary = (seg_df.groupby('Segment')['TotalCourses']
                       .agg(['mean', 'count']).reset_index())
        seg_summary.columns = ['Segment', 'AvgCourses', 'UserCount']
        seg_order = ['Beginner-only', 'Mixed-level', 'Advanced-only']
        seg_summary['Segment'] = pd.Categorical(seg_summary['Segment'], seg_order, ordered=True)
        seg_summary = seg_summary.sort_values('Segment')

        # Free vs Paid preference by segment
        type_by_seg = filtered.merge(user_level_pivot[['UserID', 'Segment']], on='UserID')
        type_pct = (pd.crosstab(type_by_seg['Segment'], type_by_seg['CourseType'], normalize='index') * 100).reset_index()

        bcol1, bcol2 = st.columns(2)
        with bcol1:
            st.caption("Average total courses taken, by learner segment")
            fig = px.bar(seg_summary, x='Segment', y='AvgCourses',
                         color='Segment',
                         color_discrete_map={
                             'Beginner-only': PURPLE[0],
                             'Mixed-level': AMBER[1],
                             'Advanced-only': TEAL[2]},
                         text=seg_summary['AvgCourses'].apply(lambda x: f"{x:.2f}"))
            fig.update_traces(textposition='outside', textfont_size=13)
            fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Avg total courses")
            st.plotly_chart(clean_fig(fig, h=300), use_container_width=True)

        with bcol2:
            st.caption("Free vs Paid course preference, by learner segment")
            # Some filter combinations may only have Free or only Paid courses present
            available_types = [t for t in ['Free', 'Paid'] if t in type_pct.columns]
            fig = px.bar(type_pct, x='Segment', y=available_types,
                         barmode='stack',
                         color_discrete_map={'Free': TEAL[2], 'Paid': AMBER[1]})
            fig.update_layout(xaxis_title="", yaxis_title="% of enrollments", legend_title="Type")
            st.plotly_chart(clean_fig(fig, h=300), use_container_width=True)

        st.dataframe(
            seg_summary.rename(columns={
                'Segment': 'Learner Segment',
                'AvgCourses': 'Avg Total Courses',
                'UserCount': 'Number of Users'
            }).assign(**{'Avg Total Courses': lambda x: x['Avg Total Courses'].round(2)}),
            use_container_width=True, hide_index=True
        )

        beg_only_avg = seg_summary[seg_summary['Segment']=='Beginner-only']['AvgCourses'].values
        adv_only_avg = seg_summary[seg_summary['Segment']=='Advanced-only']['AvgCourses'].values
        mixed_avg    = seg_summary[seg_summary['Segment']=='Mixed-level']['AvgCourses'].values

        beg_txt = f"{beg_only_avg[0]:.2f}" if len(beg_only_avg) else "N/A"
        adv_txt = f"{adv_only_avg[0]:.2f}" if len(adv_only_avg) else "N/A"
        mix_txt = f"{mixed_avg[0]:.2f}" if len(mixed_avg) else "N/A"

        insight(f"Learners are classified into three behavioral segments: **Beginner-only** "
                f"(avg {beg_txt} courses), **Advanced-only** (avg {adv_txt} courses), and "
                f"**Mixed-level** learners who explore multiple levels (avg {mix_txt} courses). "
                f"Mixed-level learners take substantially more courses overall, suggesting that learners "
                f"who progress across levels — rather than staying purely Beginner or purely Advanced — "
                f"are EduPro's most engaged segment. Beginner-only learners show a stronger preference "
                f"for Free courses compared to Advanced-only learners, who are more willing to pay.")

        # Compute the actual spread of engagement across age groups from current filter,
        # instead of asserting a fixed claim regardless of what's selected.
        age_avg = user_enroll.groupby('AgeGroup')['CourseCount'].mean()
        if len(age_avg) > 1:
            spread = age_avg.max() - age_avg.min()
            insight(f"Across the current filter selection, average courses per user ranges from "
                    f"**{age_avg.min():.2f}** to **{age_avg.max():.2f}** between age groups "
                    f"(a spread of {spread:.2f}) — engagement depth is broadly similar across "
                    f"demographics, with most learners taking 2–4 courses and a small group of "
                    f"power users taking 10+.")


# ══════════════════════════════════════════════════════════════════
# TAB 6 — KPI SUMMARY
# ══════════════════════════════════════════════════════════════════
with tab6:
    st.subheader("KPI Summary")
    st.caption("Based on current filter selection. Reset filters to see full platform KPIs.")

    total      = len(filtered)
    f_teen     = len(filtered[filtered['AgeGroup'] == 'Teen (15–17)'])
    f_ya       = len(filtered[filtered['AgeGroup'] == 'Young Adult (18–25)'])
    f_adult    = len(filtered[filtered['AgeGroup'] == 'Adult (26–35)'])
    f_female   = len(filtered[filtered['Gender'] == 'Female'])
    f_male     = len(filtered[filtered['Gender'] == 'Male'])
    top_cat    = filtered.groupby('CourseCategory').size().idxmax()
    top_cat_n  = int(filtered.groupby('CourseCategory').size().max())
    free_pct   = round(len(filtered[filtered['CourseType'] == 'Free'])    / total * 100, 1)
    beg_pct    = round(len(filtered[filtered['CourseLevel'] == 'Beginner'])    / total * 100, 1)
    int_pct    = round(len(filtered[filtered['CourseLevel'] == 'Intermediate']) / total * 100, 1)
    adv_pct    = round(len(filtered[filtered['CourseLevel'] == 'Advanced'])     / total * 100, 1)
    avg_crs    = round(user_enroll['CourseCount'].mean(), 2)
    unique_usr = user_enroll['UserID'].nunique()

    kpi_rows = [
        ("Filtered Users",             f"{len(filtered_users):,}",                       "Based on age + gender filters"),
        ("Filtered Enrollments",       f"{total:,}",                                     "Based on all filters"),
        ("Unique Active Users",        f"{unique_usr:,}",                                "Users with ≥1 enrollment"),
        ("Avg Courses / User",         str(avg_crs),                                     "Engagement depth"),
        ("Teen Enrollments (15–17)",   f"{f_teen:,} ({f_teen/total*100:.1f}%)",          "Age segment share"),
        ("Young Adult Enrollments",    f"{f_ya:,} ({f_ya/total*100:.1f}%)",              "Age segment share"),
        ("Adult Enrollments (26–35)",  f"{f_adult:,} ({f_adult/total*100:.1f}%)",        "Age segment share"),
        ("Female Enrollments",         f"{f_female:,} ({f_female/total*100:.1f}%)",      "Gender split"),
        ("Male Enrollments",           f"{f_male:,} ({f_male/total*100:.1f}%)",          "Gender split"),
        ("Top Course Category",        f"{top_cat} ({top_cat_n})",                       "Highest enrollment"),
        ("Free Course Uptake",         f"{free_pct}%",                                   "Learner cost preference"),
        ("Beginner Level Share",       f"{beg_pct}%",                                    "Skill level insight"),
        ("Intermediate Level Share",   f"{int_pct}%",                                    "Skill level insight"),
        ("Advanced Level Share",       f"{adv_pct}%",                                    "Skill level insight"),
        ("Course Categories Active",   f"{filtered['CourseCategory'].nunique()}",         "Categories in selection"),
    ]

    cols = st.columns(3)
    for i, (name, value, desc) in enumerate(kpi_rows):
        with cols[i % 3]:
            st.metric(label=name, value=value, help=desc)

    st.divider()
    hdr("Full KPI table — downloadable")
    kpi_df = pd.DataFrame(kpi_rows, columns=['KPI', 'Value', 'Description'])
    st.dataframe(kpi_df, use_container_width=True, hide_index=True, height=460)

    csv = kpi_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download KPI table as CSV",
        data=csv,
        file_name="edupro_kpis.csv",
        mime="text/csv",
        use_container_width=True,
    )

    insight("KPI Summary now reflects your current filter selection. "
            "Use Reset Filters in the sidebar to restore all data and see full platform KPIs.")

# ══════════════════════════════════════════════════════════════════
# TAB 7 — PROBLEM, SOLUTION & INSIGHTS
# ══════════════════════════════════════════════════════════════════
with tab7:
    st.subheader("Problem, Solution & Insights")
    st.markdown(
        "EduPro lacked clear, data-driven answers to four core business questions. "
        "This tab answers each one directly using the current filter selection."
    )
    st.divider()

    # ── QUESTION 1 — Which age groups are most active? ─────────────
    hdr("1️⃣ Which age groups are most active on the platform?")
    st.markdown(
        "**Problem:** Leadership had no clear view of which age groups drive the most activity.\n\n"
        "**Solution:** Measured activity two ways — total enrollment volume, and average "
        "courses per user (engagement depth) — by age group."
    )

    age_volume = (filtered.groupby('AgeGroup').size()
                  .reindex(AGE_ORDER, fill_value=0))
    age_engagement = (user_enroll.groupby('AgeGroup')['CourseCount']
                       .mean().reindex(AGE_ORDER).dropna())

    if age_volume.sum() > 0 and len(age_engagement) > 0:
        top_volume_age = age_volume.idxmax()
        top_engagement_age = age_engagement.idxmax()

        q1c1, q1c2 = st.columns(2)
        kpi(q1c1, top_volume_age, f"Most active by volume ({int(age_volume.max()):,} enrollments)")
        kpi(q1c2, top_engagement_age, f"Most active by engagement ({age_engagement.max():.2f} courses/user)")

        fig = px.bar(age_volume.reset_index(name='Enrollments'),
                     x='AgeGroup', y='Enrollments', color='AgeGroup',
                     color_discrete_sequence=TEAL, text='Enrollments')
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Enrollments")
        st.plotly_chart(clean_fig(fig, h=300), use_container_width=True)

        insight(f"**{top_volume_age}** leads by total volume, while **{top_engagement_age}** "
                f"leads by individual engagement. Both are valid answers depending on whether "
                f"the question is about scale or depth of engagement.")
    else:
        st.info("No data available for the current filter selection.")

    st.divider()

    # ── QUESTION 2 — How do enrollment patterns differ by gender? ──
    hdr("2️⃣ How do enrollment patterns differ by gender?")
    st.markdown(
        "**Problem:** Gender-based enrollment differences were never measured.\n\n"
        "**Solution:** Compared enrollment share and average engagement by gender."
    )

    gender_volume = filtered.groupby('Gender').size()
    gender_engagement = user_enroll.groupby('Gender')['CourseCount'].mean()

    if gender_volume.sum() > 0:
        female_pct = gender_volume.get('Female', 0) / gender_volume.sum() * 100
        male_pct = gender_volume.get('Male', 0) / gender_volume.sum() * 100

        q2c1, q2c2 = st.columns(2)
        with q2c1:
            fig = px.pie(names=gender_volume.index, values=gender_volume.values,
                         color=gender_volume.index,
                         color_discrete_map={'Female': PURPLE[2], 'Male': PURPLE[1]}, hole=0.5)
            fig.update_traces(textinfo='label+percent')
            fig.update_layout(showlegend=False)
            st.plotly_chart(clean_fig(fig, h=280), use_container_width=True)
        with q2c2:
            fig = px.bar(gender_engagement.reset_index(name='AvgCourses'),
                         x='Gender', y='AvgCourses', color='Gender',
                         color_discrete_map={'Female': PURPLE[2], 'Male': PURPLE[1]},
                         text=gender_engagement.reset_index(name='AvgCourses')['AvgCourses'].apply(lambda x: f"{x:.2f}"))
            fig.update_traces(textposition='outside')
            fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Avg courses/user")
            st.plotly_chart(clean_fig(fig, h=280), use_container_width=True)

        insight(f"Enrollment share is **{female_pct:.1f}% Female / {male_pct:.1f}% Male** — "
                f"close to parity, meaning gender does not strongly differentiate platform "
                f"activity in the current selection.")
    else:
        st.info("No data available for the current filter selection.")

    st.divider()

    # ── QUESTION 3 — Which categories do different segments prefer? ─
    hdr("3️⃣ What course categories are preferred by different learner segments?")
    st.markdown(
        "**Problem:** It was unclear whether different age or gender segments prefer "
        "different course categories.\n\n"
        "**Solution:** Ranked categories overall, and identified each age group's top category."
    )

    cat_overall = filtered.groupby('CourseCategory').size().sort_values(ascending=False)

    if len(cat_overall) > 0:
        top_overall_cat = cat_overall.index[0]

        fig = px.bar(cat_overall.head(6).reset_index(name='Enrollments'),
                     x='Enrollments', y='CourseCategory', orientation='h',
                     color='Enrollments', color_continuous_scale=['#9FE1CB', '#085041'],
                     text='Enrollments')
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False, coloraxis_showscale=False,
                          xaxis_title="", yaxis_title="",
                          yaxis=dict(autorange="reversed"))
        st.plotly_chart(clean_fig(fig, h=320), use_container_width=True)

        age_cat = filtered.groupby(['AgeGroup', 'CourseCategory']).size()
        top_per_age = []
        for age in AGE_ORDER:
            if age in age_cat.index.get_level_values(0):
                top_per_age.append(f"{age} → {age_cat[age].idxmax()}")

        insight(f"**{top_overall_cat}** is the most preferred category platform-wide. "
                f"By age group: {'; '.join(top_per_age)}. See the Cross Analysis tab for the "
                f"full age × category heatmap.")
    else:
        st.info("No data available for the current filter selection.")

    st.divider()

    # ── QUESTION 4 — Are levels more popular in specific age groups? ─
    hdr("4️⃣ Are beginner, intermediate, or advanced courses more popular among specific age groups?")
    st.markdown(
        "**Problem:** It was assumed level preference might vary by age, but this was "
        "never measured.\n\n"
        "**Solution:** Calculated each level's share *within* each age group's own "
        "enrollments, removing the bias of group size."
    )

    lvl_pivot_q4 = (filtered.groupby(['AgeGroup', 'CourseLevel']).size()
                    .unstack(fill_value=0).reindex(AGE_ORDER).dropna(how='all'))
    for lvl in LEVEL_ORDER:
        if lvl not in lvl_pivot_q4.columns:
            lvl_pivot_q4[lvl] = 0

    if len(lvl_pivot_q4) > 0 and lvl_pivot_q4.sum().sum() > 0:
        lvl_pct_q4 = (lvl_pivot_q4.div(lvl_pivot_q4.sum(axis=1), axis=0) * 100).round(1)
        lvl_pct_long_q4 = lvl_pct_q4.reset_index().melt(
            id_vars='AgeGroup', var_name='CourseLevel', value_name='Pct')

        fig = px.bar(lvl_pct_long_q4, x='AgeGroup', y='Pct', color='CourseLevel',
                     barmode='group',
                     color_discrete_map={'Beginner': PURPLE[0], 'Intermediate': AMBER[1], 'Advanced': TEAL[2]},
                     text=lvl_pct_long_q4['Pct'].apply(lambda x: f"{x:.1f}%"))
        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis_title="", yaxis_title="% within age group", legend_title="Level")
        st.plotly_chart(clean_fig(fig, h=320), use_container_width=True)

        top_level_summary = "; ".join(
            f"{age} → {lvl_pct_q4.loc[age].idxmax()} ({lvl_pct_q4.loc[age].max():.1f}%)"
            for age in lvl_pct_q4.index
        )
        insight(f"**Direct answer:** {top_level_summary}. Comparing these shares (not raw counts) "
                f"removes the bias of larger age groups simply having more enrollments overall.")
    else:
        st.info("No data available for the current filter selection.")