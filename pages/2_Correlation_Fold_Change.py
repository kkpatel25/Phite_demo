import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_carousel import carousel


st.set_page_config(layout="wide")

@st.cache_data
def load_stats():
    return pd.read_csv(st.secrets["corr_url"])


def app():
    df = load_stats()
    df = df.set_index("Unnamed: 0")

    tabs_font_css = """
    <style>
    div[class*="stTextInput"] label p {
        font: Source Sans;
        font-size: 18px;
    }
    </style>
    """

    items = [
        dict(
            title="",
            text="",
            img="images/average_csa_top100_corr_heatmap_noGray.png",
        ),
        dict(
            title="",
            text="",
            img="images/avg_peak_torque_away_top100_corr_heatmap_noGray.png",
        ),
        dict(
            title="",
            text="",
            img="images/ss_cx4_top100_corr_heatmap_noGray.png",
        ),
        dict(
            title="",
            text="",
            img="images/total_contacts_top100_corr_heatmap_noGray.png",
        ),
        dict(
            title="",
            text="",
            img="images/vo2_peak_relative_top100_corr_heatmap_noGray.png",
        )
    ]
    carousel(items=items, controls=True, interval=10000, width = 0.75)

    st.write(tabs_font_css, unsafe_allow_html=True)

    gene_input = st.text_input("Type a gene name and enter:", value = "PPARD")

    if "downloads_ready" not in st.session_state:
        st.session_state.downloads_ready = False

    if gene_input:
        gene_input = gene_input.strip().upper()
        if gene_input not in df.index.values:
            st.error(f"{gene_input} expression not detected. Please try again.")
        else:
            st.success(f"Gene {gene_input} found!")

            plot_df = process_df(gene_input, df)

            if "current_gene" not in st.session_state:
                st.session_state.current_gene = gene_input

            fig_table = generateTable(plot_df, gene_input)
            st.plotly_chart(fig_table, use_container_width=True)


def process_df(gene, df):
    return df.loc[gene]

def generateTable(df, gene):
    metrics = {
        "csa": "Myofibrils Size",
        "torque": "Strength (Peak Torque)",
        "contacts": "Vascular (contacts) Changes",
        "vo2": "Vo2peak"
    }

    corr_values = [f"{df[f'{m}_corr']:+.2f}" for m in metrics]
    p_values = [f"{df[f'{m}_p_val']:.3f}" for m in metrics]
    corr_labels = [f"Correlation with {name}" for name in metrics.values()]

    fig_table = go.Figure(
        data=[go.Table(
            header=dict(
                values=["Statistic", "Correlation", "P-vals"],
                fill_color="#1f77b4",
                align="center",
                font=dict(color="white", size=15)
            ),
            cells=dict(
                values=[corr_labels, corr_values, p_values],
                fill_color=[
                    ["#f9f9f9" if i % 2 == 0 else "#ffffff" for i in range(len(corr_labels))],
                    ["#f9f9f9" if i % 2 == 0 else "#ffffff" for i in range(len(corr_values))],
                    ["#f9f9f9" if i % 2 == 0 else "#ffffff" for i in range(len(p_values))]
                ],
                align="center",
                font=dict(size=15),
                height=30
            )
        )]
    )

    fig_table.update_layout(
        title=f"Various Correlations for {gene}",
        template="plotly_white",
        margin=dict(t=40, l=20, r=20, b=20)
    )
    return fig_table

app()
