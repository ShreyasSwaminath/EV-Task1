import streamlit as st
import pandas as pd
import altair as alt # Import Altair for powerful charting

# --- Configuration ---
st.set_page_config(
    page_title="EV Data Analysis (Tasks 2 & 3)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Loading and Analysis Function ---

@st.cache_data
def load_and_analyze_data(file_path):
    """
    Loads the EV dataset and performs Task 2 (Aggregation) 
    and Task 3 (Summarization) analysis.
    """
    try:
        # Load the dataset
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        # This error message is what you would have seen if the path was wrong
        st.error(f"Error: The file '{file_path}' was not found. Please ensure it is in the correct directory.")
        return None, None
    except Exception as e:
        st.error(f"An error occurred during file loading: {e}")
        return None, None

    # --- Task 2: Data Aggregation (Total EVs by Make and Model Year) ---
    # Group by 'Make' and 'Model Year' and count the total number of vehicles
    ev_counts_by_make_year = df.groupby(['Make', 'Model Year']).size().reset_index(name='Total EVs')
    
    # Sort by 'Total EVs' in descending order
    ev_counts_by_make_year = ev_counts_by_make_year.sort_values(by='Total EVs', ascending=False)
    
    # Get the top 10
    top_10_ev_counts = ev_counts_by_make_year.head(10)

    # --- Task 3: Data Transformation and Summarization (Average Electric Range) ---
    # Group by 'Electric Vehicle Type' and calculate the mean of 'Electric Range'
    avg_range_by_type = df.groupby('Electric Vehicle Type')['Electric Range'].mean().reset_index(name='Average Electric Range (Miles)')
    
    # Sort in descending order of 'Average Electric Range (Miles)'
    avg_range_by_type = avg_range_by_type.sort_values(by='Average Electric Range (Miles)', ascending=False)

    return top_10_ev_counts, avg_range_by_type

# --- Main App Execution ---

st.title("🔌 Electric Vehicle Population Dataset Analysis")
st.markdown("---")

# *** CORRECTED FILE PATH HERE ***
FILE_PATH = "EV Population Dataset.csv"

# Run the analysis
top_10_ev_counts, avg_range_by_type = load_and_analyze_data(FILE_PATH)

if top_10_ev_counts is not None and avg_range_by_type is not None:
    
    # --- Task 2 Display ---
    
    st.header("1️⃣ Task 2: Top 10 EV Counts by Make and Model Year")
    st.info("Aggregated total number of EVs for each Make and Model Year.")
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Top 10 Aggregated Data Table")
        # Display the result table
        st.dataframe(
            top_10_ev_counts, 
            use_container_width=True, 
            hide_index=True
        )

    with col2:
        st.subheader("Visualization: Top 10 Counts")
        
        # Create a combined 'Make - Year' column for the chart axis
        top_10_ev_counts['Make_Year'] = top_10_ev_counts['Make'] + ' (' + top_10_ev_counts['Model Year'].astype(str) + ')'
        
        # Create an Altair bar chart
        chart_t2 = alt.Chart(top_10_ev_counts).mark_bar().encode(
            x=alt.X('Total EVs', title='Total EVs (Count)'),
            y=alt.Y('Make_Year', sort='-x', title='Make and Model Year'),
            color=alt.Color('Model Year', scale=alt.Scale(range='ramp')),
            tooltip=['Make', 'Model Year', 'Total EVs']
        ).properties(
            height=300
        ).interactive() # Add interactive zooming/panning

        st.altair_chart(chart_t2, use_container_width=True)

    st.markdown("---")

    # --- Task 3 Display ---
    
    st.header("2️⃣ Task 3: Average Electric Range by EV Type")
    st.info("Calculated average Electric Range for each Electric Vehicle Type, sorted descending.")
    
    col3, col4 = st.columns([1, 1])

    with col3:
        st.subheader("Average Range Data Table")
        # Display the result table with formatting
        st.dataframe(
            avg_range_by_type,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Average Electric Range (Miles)": st.column_config.NumberColumn(
                    "Average Electric Range (Miles)",
                    format="%.1f 🚗" # Formatting to one decimal place with an emoji
                )
            }
        )
    
    with col4:
        st.subheader("Visualization: Average Range")
        
        # Create an Altair bar chart
        chart_t3 = alt.Chart(avg_range_by_type).mark_bar().encode(
            x=alt.X('Electric Vehicle Type', title='EV Type'),
            y=alt.Y('Average Electric Range (Miles)', title='Avg. Range (Miles)'),
            color=alt.Color('Electric Vehicle Type'),
            tooltip=['Electric Vehicle Type', alt.Tooltip('Average Electric Range (Miles)', format='.1f')]
        ).properties(
            height=300
        ).interactive()

        st.altair_chart(chart_t3, use_container_width=True)

    st.markdown("---")
    st.caption(f"Data Source: **{FILE_PATH}** | Analysis performed using pandas and displayed with Streamlit.")