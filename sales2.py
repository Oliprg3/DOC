import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report, confusion_matrix
from sklearn.decomposition import PCA
import xgboost as xgb
import plotly.express as px
from sklearn.cluster import KMeans

st.set_page_config(page_title="Pro Data Analytics Dashboard", layout="wide", initial_sidebar_state="expanded")

if "page" not in st.session_state:
    st.session_state["page"] = "Home"
pages = ["Home","Data Upload","EDA & Cleaning","Visualization Dashboard","ML Training","Prediction Simulator","PCA & Dimensionality Reduction","Clustering","KPI Dashboard","Reports","About"]
choice = st.sidebar.radio("Navigation", pages, index=pages.index(st.session_state["page"]))
st.session_state["page"] = choice

for k in ['df','df_clean','model','scaler','features','train_columns','label_encoder','target','problem_type','feature_options']:
    if k not in st.session_state:
        st.session_state[k] = None

def go(page):
    st.session_state["page"] = page
    st.experimental_rerun()

if choice == "Home":
    st.markdown("""
    <style>
    .hero {
      border-radius:16px;
      padding:40px;
      color: white;
      background: linear-gradient(135deg, #0f62fe 0%, #3db2ff 100%);
      box-shadow: 0 10px 30px rgba(13, 71, 161, 0.18);
    }
    .title {font-size:42px; font-weight:800; margin-bottom:6px;}
    .subtitle {font-size:18px; opacity:0.95; margin-bottom:18px;}
    .tiles {display:flex; gap:14px; flex-wrap:wrap; justify-content:center; margin-top:18px;}
    .tile {
      width:230px;
      background: rgba(255,255,255,0.06);
      border-radius:12px;
      padding:14px;
      color: #fff;
      box-shadow: 0 6px 18px rgba(12, 61, 139, 0.12);
      transition: transform .18s ease, box-shadow .18s ease;
      cursor: pointer;
      text-align:left;
    }
    .tile:hover { transform: translateY(-8px); box-shadow: 0 18px 40px rgba(12,61,139,0.18); }
    .tile h4{margin:0 0 6px 0}
    .cta {margin-top:18px; display:inline-block; padding:12px 22px; background:white; color:#0f62fe; font-weight:700; border-radius:10px}
    </style>
    <div class="hero">
      <div class="title">Pro Data Analytics & ML Dashboard</div>
      <div class="subtitle">Upload data, explore with interactive EDA, train models, simulate predictions, and export reports — all in one polished app.</div>
      <div style="display:flex;gap:10px;justify-content:center">
        <button onclick="document.location='#upload'" style="border:none;padding:10px 18px;border-radius:10px;background:#ffffff;color:#0f62fe;font-weight:700;cursor:pointer">Get Started</button>
        <button id="demo-btn" style="border:none;padding:10px 18px;border-radius:10px;background:transparent;color:#fff;border:1px solid rgba(255,255,255,0.25);cursor:pointer">Take Tour</button>
      </div>
      <div class="tiles" style="margin-top:24px">
        <div class="tile" onclick="">
          <h4>Upload</h4>
          <div>Load CSV / Excel and preview data with one click.</div>
        </div>
        <div class="tile">
          <h4>EDA & Cleaning</h4>
          <div>Missing value handlers, filters, outlier detection.</div>
        </div>
        <div class="tile">
          <h4>Visualization</h4>
          <div>Interactive Plotly charts and correlation analytics.</div>
        </div>
        <div class="tile">
          <h4>Modeling</h4>
          <div>Train RandomForest, XGBoost, Logistic or Linear models.</div>
        </div>
        <div class="tile">
          <h4>Prediction</h4>
          <div>Simulate scenarios using the trained model.</div>
        </div>
        <div class="tile">
          <h4>Export</h4>
          <div>Download cleaned data and generate reports.</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("### Quick actions")
        if st.button("Go to Upload"):
            go("Data Upload")
        if st.button("Go to EDA & Cleaning"):
            go("EDA & Cleaning")
        if st.button("Go to Visualization"):
            go("Visualization Dashboard")
        st.markdown("### Status")
        df = st.session_state.get('df')
        if df is not None:
            st.success(f"Dataset loaded ({df.shape[0]} rows × {df.shape[1]} cols)")
        else:
            st.info("No dataset loaded")

elif choice == "Data Upload":
    st.title("Upload Dataset")
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv","xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.lower().endswith(".csv"):
                try:
                    df = pd.read_csv(uploaded_file, encoding='utf-8')
                except Exception:
                    df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
            else:
                df = pd.read_excel(uploaded_file)
            st.session_state['df'] = df.copy()
            st.session_state['df_clean'] = df.copy()
            feature_options = {}
            for c in df.columns:
                try:
                    vals = df[c].dropna().unique()
                    if len(vals) > 200:
                        vals = list(vals[:200])
                    feature_options[c] = vals.tolist() if hasattr(vals, "tolist") else list(vals)
                except Exception:
                    feature_options[c] = []
            st.session_state['feature_options'] = feature_options
            st.success(f"Loaded {uploaded_file.name}")
            st.dataframe(df.head(200), use_container_width=True)
            st.write("Shape:", df.shape)
            if st.button("Clear stored model & preprocessing"):
                for k in ['model','scaler','features','train_columns','label_encoder','target','problem_type']:
                    st.session_state[k] = None
                st.success("Session cleared")
        except Exception as e:
            st.error(f"Failed to load file: {e}")

elif choice == "EDA & Cleaning":
    df = st.session_state.get('df_clean') if st.session_state.get('df_clean') is not None else st.session_state.get('df')
    if df is None:
        st.warning("Upload dataset first")
    else:
        st.title("EDA & Cleaning")
        st.subheader("Preview (first 100 rows)")
        st.dataframe(df.head(100), use_container_width=True)
        buf = BytesIO()
        try:
            df.info(buf=buf)
            st.text(buf.getvalue().decode())
        except Exception:
            st.text("Dataset info not available")
        st.subheader("Summary statistics")
        try:
            st.dataframe(df.describe(include='all').T, use_container_width=True)
        except Exception:
            st.dataframe(df.describe().T, use_container_width=True)
        st.subheader("Missing values & simple fixes")
        miss = df.isnull().sum()
        miss = miss[miss > 0].sort_values(ascending=False)
        if not miss.empty:
            st.table(miss)
        else:
            st.info("No missing values detected")
        with st.expander("Handle missing values (safe, non-destructive)"):
            cols_missing = [c for c in df.columns if df[c].isnull().any()]
            if cols_missing:
                col = st.selectbox("Select column", cols_missing)
                method = st.selectbox("Method", ["Fill mean/mode","Fill constant","Drop rows with nulls","Drop column"])
                if method == "Fill constant":
                    const = st.text_input("Value to fill with")
                if st.button("Apply missing-value action"):
                    try:
                        df2 = st.session_state['df_clean'].copy()
                        if method == "Fill mean/mode":
                            if pd.api.types.is_numeric_dtype(df2[col]):
                                df2[col].fillna(df2[col].mean(), inplace=True)
                            else:
                                df2[col].fillna(df2[col].mode().iloc[0], inplace=True)
                        elif method == "Fill constant":
                            if const == "":
                                st.error("Provide a constant value")
                            else:
                                df2[col].fillna(const, inplace=True)
                        elif method == "Drop rows with nulls":
                            df2 = df2.dropna(subset=[col])
                        elif method == "Drop column":
                            df2 = df2.drop(columns=[col])
                        st.session_state['df_clean'] = df2
                        st.success("Missing-value action applied (df_clean updated)")
                    except Exception as e:
                        st.error(f"Action failed: {e}")
            else:
                st.info("No columns with missing values")
        st.subheader("Interactive filtering (apply to working dataset)")
        with st.form("filters"):
            filter_cols = st.multiselect("Select columns to filter", options=df.columns.tolist())
            conditions = []
            for c in filter_cols:
                if pd.api.types.is_numeric_dtype(df[c]):
                    rmin, rmax = float(df[c].min()), float(df[c].max())
                    lo, hi = st.slider(f"Range for {c}", min_value=rmin, max_value=rmax, value=(rmin, rmax))
                    conditions.append(("range", c, lo, hi))
                else:
                    opts = st.session_state.get('feature_options', {}).get(c, list(df[c].dropna().unique()))
                    sel = st.multiselect(f"Values for {c}", options=opts, default=opts[:6])
                    conditions.append(("in", c, sel))
            apply_filters = st.form_submit_button("Apply filters")
        if apply_filters:
            try:
                df2 = st.session_state['df_clean'].copy()
                for cond in conditions:
                    if cond[0] == "range":
                        _, c, lo, hi = cond
                        df2 = df2[(df2[c] >= lo) & (df2[c] <= hi)]
                    else:
                        _, c, vals = cond
                        if vals:
                            df2 = df2[df2[c].isin(vals)]
                st.session_state['df_clean'] = df2
                st.success(f"Filters applied; new shape: {df2.shape}")
            except Exception as e:
                st.error(f"Failed to apply filters: {e}")
        st.subheader("Outlier detection (IQR)")
        numeric = df.select_dtypes(include=np.number).columns.tolist()
        if numeric:
            col_out = st.selectbox("Choose numeric column for outliers", numeric)
            if st.button("Detect outliers"):
                try:
                    q1 = df[col_out].quantile(0.25)
                    q3 = df[col_out].quantile(0.75)
                    iqr = q3 - q1
                    outs = df[(df[col_out] < q1 - 1.5 * iqr) | (df[col_out] > q3 + 1.5 * iqr)]
                    st.write("Outliers:", len(outs))
                    fig, ax = plt.subplots(figsize=(8,3))
                    sns.boxplot(x=df[col_out], ax=ax)
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Outlier detection failed: {e}")
        else:
            st.info("No numeric columns available for outlier detection")
        st.subheader("Categorical distributions")
        cat_cols = df.select_dtypes(include=['object','category']).columns.tolist()
        if cat_cols:
            cat = st.selectbox("Choose categorical column", cat_cols)
            vc = df[cat].value_counts().reset_index().rename(columns={'index':cat, cat:'count'})
            fig = px.bar(vc, x=cat, y='count', height=350)
            st.plotly_chart(fig, use_container_width=True)

elif choice == "Visualization Dashboard":
    df = st.session_state.get('df_clean') if st.session_state.get('df_clean') is not None else st.session_state.get('df')
    if df is None:
        st.warning("Clean dataset first")
    else:
        st.title("Interactive Visualization Dashboard")
        cols = df.columns.tolist()
        x_axis = st.selectbox("X axis", cols, index=0)
        y_axis = st.selectbox("Y axis", cols, index=min(1, len(cols)-1))
        color_by = st.selectbox("Color by (optional)", [None] + cols)
        agg = st.selectbox("Aggregation (for categorical X)", ["None","mean","sum","count","median"])
        plot_type = st.selectbox("Plot type", ["Auto","Scatter","Line","Bar","Box","Histogram","Pie"])
        if st.button("Generate plot"):
            try:
                x_is_num = pd.api.types.is_numeric_dtype(df[x_axis])
                y_is_num = pd.api.types.is_numeric_dtype(df[y_axis])
                color_arg = color_by if color_by is not None else None
                fig = None
                if plot_type == "Auto":
                    if x_is_num and y_is_num:
                        fig = px.scatter(df, x=x_axis, y=y_axis, color=color_arg)
                    elif not x_is_num and y_is_num:
                        if agg == "None":
                            fig = px.box(df, x=x_axis, y=y_axis, color=color_arg)
                        else:
                            grouped = df.groupby(x_axis)[y_axis].agg(agg).reset_index().rename(columns={y_axis:f"{agg}_{y_axis}"})
                            fig = px.bar(grouped, x=x_axis, y=f"{agg}_{y_axis}")
                    elif x_is_num and not y_is_num:
                        fig = px.histogram(df, x=x_axis, color=y_axis)
                    else:
                        fig = px.histogram(df, x=x_axis, color=color_arg)
                elif plot_type == "Scatter":
                    fig = px.scatter(df, x=x_axis, y=y_axis, color=color_arg)
                elif plot_type == "Line":
                    fig = px.line(df, x=x_axis, y=y_axis, color=color_arg)
                elif plot_type == "Bar":
                    fig = px.bar(df, x=x_axis, y=y_axis, color=color_arg)
                elif plot_type == "Box":
                    fig = px.box(df, x=x_axis, y=y_axis, color=color_arg)
                elif plot_type == "Histogram":
                    fig = px.histogram(df, x=x_axis, color=color_arg)
                elif plot_type == "Pie":
                    if not pd.api.types.is_numeric_dtype(df[y_axis]):
                        fig = px.pie(df, names=x_axis)
                    else:
                        fig = px.pie(df, names=x_axis, values=y_axis)
                if fig is not None:
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Plot failed: {e}")
        st.subheader("Scatter matrix (numeric features)")
        num = df.select_dtypes(np.number)
        if 0 < num.shape[1] <= 12:
            st.plotly_chart(px.scatter_matrix(num.sample(min(500, len(num)))), use_container_width=True)
        st.subheader("Top correlations")
        if num.shape[1] >= 2:
            corr = num.corr().abs().unstack().sort_values(kind="quicksort", ascending=False)
            corr = corr[corr != 1].drop_duplicates().head(20)
            st.table(corr.reset_index().rename(columns={'level_0':'var1','level_1':'var2',0:'corr'}))

elif choice == "ML Training":
    df = st.session_state.get('df_clean') if st.session_state.get('df_clean') is not None else st.session_state.get('df')
    if df is None:
        st.warning("Clean dataset first")
    else:
        st.title("Machine Learning Training")
        cols = df.columns.tolist()
        target = st.selectbox("Target column", cols)
        features = st.multiselect("Feature columns", [c for c in cols if c != target])
        model_choice = st.selectbox("Model", ["Random Forest","XGBoost","Logistic Regression","Linear Regression"])
        problem_type = st.radio("Problem Type", ["Classification","Regression"])
        test_size = st.slider("Test set proportion (%)", 5, 50, 20) / 100.0
        if model_choice == "Random Forest":
            n_est = st.slider("Trees", 50, 500, 100, step=50)
            max_d = st.slider("Max depth", 1, 30, 6)
        if model_choice == "XGBoost":
            n_est = st.slider("Trees (XGBoost)", 50, 500, 100, step=50)
            max_d = st.slider("Max depth (XGBoost)", 1, 30, 6)
            lr = st.slider("Learning rate", 0.01, 0.5, 0.1)
        if st.button("Train model"):
            if not features:
                st.error("Select features before training")
            else:
                try:
                    X_raw = df[features].copy()
                    y_raw = df[target].copy()
                    X = pd.get_dummies(X_raw, drop_first=False)
                    train_columns = X.columns.tolist()
                    le = None
                    if problem_type == "Classification":
                        if y_raw.dtype == 'object' or y_raw.dtype.name == 'category':
                            le = LabelEncoder().fit(y_raw.astype(str))
                            y = le.transform(y_raw.astype(str))
                        else:
                            y = y_raw.values
                    else:
                        y = y_raw.values
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
                    scaler = StandardScaler()
                    X_train_scaled = scaler.fit_transform(X_train)
                    X_test_scaled = scaler.transform(X_test)
                    model = None
                    if model_choice == "Random Forest":
                        model = RandomForestClassifier(n_estimators=n_est, max_depth=max_d, random_state=42) if problem_type == "Classification" else RandomForestRegressor(n_estimators=n_est, max_depth=max_d, random_state=42)
                    elif model_choice == "XGBoost":
                        model = xgb.XGBClassifier(n_estimators=n_est, max_depth=max_d, learning_rate=lr, use_label_encoder=False, eval_metric='logloss') if problem_type == "Classification" else xgb.XGBRegressor(n_estimators=n_est, max_depth=max_d, learning_rate=lr)
                    elif model_choice == "Logistic Regression":
                        model = LogisticRegression(max_iter=2000)
                    elif model_choice == "Linear Regression":
                        model = LinearRegression()
                    model.fit(X_train_scaled, y_train)
                    preds = model.predict(X_test_scaled)
                    if problem_type == "Classification":
                        acc = accuracy_score(y_test, preds)
                        st.write("Accuracy:", round(acc, 4))
                        st.text(classification_report(y_test, preds))
                        cm = confusion_matrix(y_test, preds)
                        fig, ax = plt.subplots()
                        sns.heatmap(cm, annot=True, fmt='d', ax=ax)
                        st.pyplot(fig)
                    else:
                        mse = mean_squared_error(y_test, preds)
                        st.write("MSE:", round(mse, 4))
                        fig, ax = plt.subplots()
                        plt.scatter(y_test, preds, alpha=0.6)
                        plt.xlabel("Actual")
                        plt.ylabel("Predicted")
                        st.pyplot(fig)
                    imp = None
                    if hasattr(model, "feature_importances_"):
                        imp = model.feature_importances_
                    elif hasattr(model, "coef_"):
                        imp = np.abs(model.coef_).ravel()
                    if imp is not None:
                        fi_df = pd.DataFrame({"Feature": train_columns, "Importance": imp})
                        fi_df = fi_df.sort_values("Importance", ascending=False).head(30)
                        st.subheader("Feature importance")
                        st.plotly_chart(px.bar(fi_df, x="Feature", y="Importance"), use_container_width=True)
                    st.session_state['model'] = model
                    st.session_state['scaler'] = scaler
                    st.session_state['features'] = features
                    st.session_state['train_columns'] = train_columns
                    st.session_state['label_encoder'] = le
                    st.session_state['target'] = target
                    st.session_state['problem_type'] = problem_type
                    st.success("Model trained and saved to session. Data remains intact.")
                except Exception as e:
                    st.error(f"Training failed: {e}")

elif choice == "Prediction Simulator":
    model = st.session_state.get('model')
    scaler = st.session_state.get('scaler')
    features = st.session_state.get('features')
    train_cols = st.session_state.get('train_columns')
    le = st.session_state.get('label_encoder')
    problem_type = st.session_state.get('problem_type')
    df_work = st.session_state.get('df_clean') if st.session_state.get('df_clean') is not None else st.session_state.get('df')
    if model is None or scaler is None or features is None:
        st.warning("Train a model first")
    else:
        st.title("Prediction Simulator")
        user_vals = {}
        feature_options = st.session_state.get('feature_options', {})
        for f in features:
            try:
                if pd.api.types.is_numeric_dtype(df_work[f]):
                    mn = float(df_work[f].min()); mx = float(df_work[f].max()); mean = float(df_work[f].mean())
                    user_vals[f] = st.number_input(f, value=mean, min_value=mn, max_value=mx, format="%.6f")
                else:
                    opts = feature_options.get(f, list(df_work[f].dropna().unique()) if f in df_work.columns else [])
                    if opts:
                        user_vals[f] = st.selectbox(f, opts)
                    else:
                        user_vals[f] = st.text_input(f, value="")
            except Exception:
                opts = feature_options.get(f, [])
                if opts:
                    user_vals[f] = st.selectbox(f, opts)
                else:
                    user_vals[f] = st.text_input(f, value="")
        if st.button("Predict"):
            try:
                X_new_raw = pd.DataFrame([user_vals])
                X_new = pd.get_dummies(X_new_raw, drop_first=False)
                for c in train_cols:
                    if c not in X_new.columns:
                        X_new[c] = 0
                X_new = X_new[train_cols]
                X_new_scaled = scaler.transform(X_new)
                pred = model.predict(X_new_scaled)
                if problem_type == "Classification" and le is not None:
                    try:
                        out = le.inverse_transform(pred.astype(int))
                    except Exception:
                        out = pred
                else:
                    out = pred
                st.success(f"Prediction: {out[0]}")
            except Exception as e:
                st.error(f"Prediction failed: {e}")

elif choice == "PCA & Dimensionality Reduction":
    df = st.session_state.get('df_clean') if st.session_state.get('df_clean') is not None else st.session_state.get('df')
    if df is None:
        st.warning("Clean dataset first")
    else:
        st.title("PCA & Dimensionality Reduction")
        num = df.select_dtypes(np.number)
        if num.shape[1] < 2:
            st.info("Need at least 2 numeric columns for PCA")
        else:
            n_comp = st.slider("Components", 2, min(10, num.shape[1]), min(2, num.shape[1]))
            try:
                pca = PCA(n_components=n_comp)
                comps = pca.fit_transform(num.fillna(num.mean()))
                comp_df = pd.DataFrame(comps, columns=[f"PC{i+1}" for i in range(n_comp)])
                st.dataframe(comp_df.head(), use_container_width=True)
                st.plotly_chart(px.scatter_matrix(comp_df.sample(min(500, comp_df.shape[0]))), use_container_width=True)
                explain = pd.DataFrame({"PC": [f"PC{i+1}" for i in range(n_comp)], "Explained": pca.explained_variance_ratio_})
                st.table(explain)
            except Exception as e:
                st.error(f"PCA failed: {e}")

elif choice == "Clustering":
    df = st.session_state.get('df_clean') if st.session_state.get('df_clean') is not None else st.session_state.get('df')
    if df is None:
        st.warning("Clean dataset first")
    else:
        st.title("Clustering (KMeans)")
        num = df.select_dtypes(np.number)
        if num.empty:
            st.info("No numeric columns to cluster")
        else:
            k = st.slider("Number of clusters", 2, 12, 3)
            sample = num.fillna(num.mean())
            try:
                km = KMeans(n_clusters=k, random_state=42)
                labels = km.fit_predict(sample)
                df_cluster = df.copy()
                df_cluster['_cluster'] = labels
                st.dataframe(df_cluster.head(), use_container_width=True)
                st.write(df_cluster.groupby('_cluster').mean().T)
                if num.shape[1] >= 2:
                    cols = list(num.columns[:3])
                    fig = px.scatter(df_cluster, x=cols[0], y=cols[1], color=df_cluster['_cluster'].astype(str), hover_data=cols)
                    st.plotly_chart(fig, use_container_width=True)
                st.session_state['df_clean'] = df_cluster
            except Exception as e:
                st.error(f"Clustering failed: {e}")

elif choice == "KPI Dashboard":
    df = st.session_state.get('df_clean') if st.session_state.get('df_clean') is not None else st.session_state.get('df')
    if df is None:
        st.warning("Clean dataset first")
    else:
        st.title("KPIs & Metrics")
        num_cols = df.select_dtypes(np.number).columns.tolist()
        c1, c2, c3 = st.columns(3)
        c1.metric("Rows", df.shape[0])
        c2.metric("Columns", df.shape[1])
        c3.metric("Numeric cols", len(num_cols))
        if num_cols:
            sel = st.selectbox("Choose numeric column for trend & stats", num_cols)
            st.metric("Mean", round(df[sel].mean(), 6))
            st.metric("Median", round(df[sel].median(), 6))
            st.metric("Std", round(df[sel].std(), 6))
            try:
                st.line_chart(df[sel].fillna(method='ffill').sample(min(500, len(df))))
            except Exception:
                st.line_chart(df[sel].fillna(method='ffill'))
        if st.button("Download cleaned dataset"):
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", data=csv, file_name="cleaned_data.csv")

elif choice == "Reports":
    df = st.session_state.get('df_clean') if st.session_state.get('df_clean') is not None else st.session_state.get('df')
    if df is None:
        st.warning("No data available")
    else:
        st.title("Reports & Export")
        st.write("Dataset shape:", df.shape)
        if st.button("Generate summary report (xlsx)"):
            try:
                buf = BytesIO()
                df.describe(include='all').to_excel(buf, sheet_name="summary")
                buf.seek(0)
                st.download_button("Download report (xlsx)", data=buf, file_name="report.xlsx")
            except Exception as e:
                st.error(f"Report failed: {e}")
        st.markdown("Download dataset:")
        st.download_button("CSV", data=df.to_csv(index=False).encode('utf-8'), file_name="dataset.csv")
        excel_io = BytesIO()
        df.to_excel(excel_io, index=False)
        st.download_button("Excel", data=excel_io.getvalue(), file_name="dataset.xlsx")

elif choice == "About":
    st.title("About Pro Analytics Dashboard")
    st.markdown("""
    - Interactive Streamlit app for EDA, visualization, ML training, prediction, PCA, clustering, and reporting.
    - Session persists dataset and trained model; operations update df_clean (working copy) only when you apply them.
    - Use the Home quick-action buttons to jump straight to Upload / EDA / Visualization.
    """)
