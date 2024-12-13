import streamlit as st
import pandas as pd
import bar_chart_race as bcr

def user_guide_show():
    st.write("""
             This application creates racing charts consisting of bar graphs by calculating the cumulative totals of the data based on the time column.

             Points to consider:
                1. The dataset must include a date column.
                2. It is recommended that the date column be in a structured format.
                3. Accepted formats for the date column:
                    -> ISO 8601 Format
                    -> US Date Format
                    -> European Date Format
                    -> Unix Timestamp
                    -> Abbreviated Month Names
                4. It is recommended that the dataset be pre-processed (missing values may hinder achieving the desired outcome).
                5. Below is an example of a dataset:
             """)
    data = pd.read_csv('corona.csv')
    st.dataframe(data)


def create_graph(data: pd.DataFrame, title):
    data['date'] = pd.to_datetime(data['date'])
    data = data.set_index('date')
    cumulative = data.cumsum()

    try:
        bcr.bar_chart_race(cumulative,
                   n_bars = min(10, len(data.columns)),
                   filename = 'racing_graph.mp4',
                   figsize = (10, 8),
                   interpolate_period=True,
                   cmap='tab20',
                   period_length = 500,
                   steps_per_period = min(5, max(1, int(len(data) / 500))),
                   period_label = False,
                   title = title)
    
    except Exception as e:
        st.error(f"Racing graph could not be generated: {e}")


def download_graph():
    try:
        with open('racing_graph.mp4', 'rb') as f:
            st.download_button(
                        label="Download",
                        data=f,
                        file_name='racing_graph.mp4',
                        mime='video/mp4'
                    )
    
    except Exception as e:
        st.error(f"Racing graph could not be downloaded: {e}")


st.title("RACING GRAPHS")

user_guide = st.button("User Guide")

if user_guide:
    user_guide_show()

title = st.text_input("Enter the title of the graph")

dataset = st.file_uploader("Upload the dataset", type= ["csv", "xlsx", "json", "txt", "pkl"])

generate = st.button("Generate")
if generate and dataset is not None:
    try:
        name = str(dataset.name)
        if name.endswith(".csv"):
            data = pd.read_csv(dataset)
        elif name.endswith(".xlsx"):
            data = pd.read_excel(dataset)
        elif name.endswith(".json"):
            data = pd.read_json(dataset)
        elif name.endswith(".txt"):
            data = pd.read_csv(dataset)
        elif name.endswith(".pkl"):
            data = pd.read_pickle(dataset)
        else:
            st.error("Unsupported file type.")
            data = None

    except Exception as e:
        st.error(f"An error occurred while uploading the file: {e}")


    create_graph(data, title)

    download_graph()
