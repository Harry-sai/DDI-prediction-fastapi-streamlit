import streamlit as st
import requests

# Base URL of FastAPI backend
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Drug Interaction App", page_icon="💊", layout="centered")

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["Home", "About", "Drug Interaction"])

# ---------------- Home Page ----------------
if page == "Home":
    st.title("🏠 Welcome to the Drug Interaction App")
    try:
        response = requests.get(f"{BASE_URL}/home")
        if response.status_code == 200:
            st.success("✅ Connected to backend successfully!")
            st.write(response.text)
        else:
            st.error(f"❌ Error {response.status_code}")
    except Exception as e:
        st.error(f"⚠️ Could not connect to backend: {e}")

# ---------------- About Page ----------------
elif page == "About":
    st.title("ℹ️ About this App")
    try:
        response = requests.get(f"{BASE_URL}/about")
        if response.status_code == 200:
            st.info(response.text)
        else:
            st.error(f"❌ Error {response.status_code}")
    except Exception as e:
        st.error(f"⚠️ Could not connect to backend: {e}")

# ---------------- Drug Interaction Page ----------------
elif page == "Drug Interaction":
    st.title("💊 Drug Interaction Prediction")
    st.write("Enter two drug names to check their possible interaction.")

    drug1 = st.text_input("Drug 1", placeholder="e.g., Bivalirudin")
    drug2 = st.text_input("Drug 2", placeholder="e.g., Edoxaban")

    if st.button("Check Interaction"):
        if not drug1 or not drug2:
            st.warning("⚠️ Please enter both drug names.")
        else:
            try:
                response = requests.post(
                    f"{BASE_URL}/Drug_interaction",
                    params={"drug1": drug1, "drug2": drug2}
                )

                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Prediction successful!")
                    st.write(f"**Interaction Type Index:** {data['interaction_type_index']}")
                    st.write(f"**Interaction Type Label:** {data['interaction_type_label']}")
                else:
                    err = response.json()
                    st.error(f"❌ Error {response.status_code}: {err.get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"⚠️ Could not connect to API: {e}")

