import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import sklearn

@st.cache_data
def load_model():
    return joblib.load("vo2_predict.joblib")

def predict(gene_dict):
    loaded_model = load_model()
    df = pd.DataFrame([gene_dict], index=[0])
    return (loaded_model.predict(df))[-1]


def render_result(col2, gene_dict):
    with col2:
        value = predict(gene_dict)
        st.markdown(
            f"""
                    <div style="margin-top: 130px; font-size:18px; font-weight:bold; color:black; padding:10px; border-radius:8px;">
                        Predicted VO2Peak change (ml/kg/min) after 12 weeks of training: {value:+.2f}
                    </div>
                    """,
            unsafe_allow_html=True
        )

st.set_page_config(layout="wide")

predict_vals = [
    0.3271350723, 0.5140979903, 0.9784933069, 5.146365909, -0.4403633775,
    -1.774901452, 2.185483432, 2.281083054, 4.891635604, 4.006383688,
    -0.2511161867, 6.115860855, 4.504438631, 9.11876205, 6.827807641,
    6.918630304, 10.73728057
]

target_vals = [
    -1.5, -1, -0.9, -0.5, 1.5,
    1.6, 1.8, 1.8, 2, 3.3,
    6.5, 6.7, 7.7, 7.8, 8,
    9.4, 12.3
]

genes = ["ADK","CD248","CD68","CHAD","CLIP3","CNIH3","COL6A1","CPO","CRAMP1","DNAJC25-GNG10","ECM1","ENSG00000253671","ENSG00000279662","ENSG00000279838","ENSG00000283228","ENSG00000287627","HOXB-AS1","IFFO1","LINC01996","MAGEF1","MOCOS","MPDZ","NCF4","P2RX5-TAX1BP3","RNF139-DT","SEC11C","SRRM4","STRBP","TMEM202-AS1","TTC7A","ZBTB39","ZSCAN26"]

df = pd.DataFrame({
    "Person": [f"Person {i+1}" for i in range(len(predict_vals))],
    "Predicted": predict_vals,
    "Ground Truth": target_vals
})

df_melted = df.melt(
    id_vars="Person",
    value_vars=["Predicted", "Ground Truth"],
    var_name="Type",
    value_name="VO2Peak change (ml/kg/min)"
)

fig = px.scatter(
    df_melted,
    x="Person",
    y="VO2Peak change (ml/kg/min)",
    color="Type",
    color_discrete_map={"Predicted": "blue", "Ground Truth": "red"},
)

fig.update_layout(
    xaxis=dict(
        title="",
        showticklabels=False
    ),
    legend_title="",
    legend=dict(
        font=dict(size=15,
            color='black',
            family="Source Sans"
        )
    ),
    margin=dict(l=20, r=20, t=30, b=20),
    height=600,
    annotations=[
        dict(
            x=1,  # far right
            y=0,  # bottom
            xref="paper",
            yref="paper",
            text="R² = 0.526",
            showarrow=False,
            font=dict(
                family="Source Sans",
                size=20,
                color="black"
            ),
            align="center",
            xanchor="right",
            yanchor="bottom",
            bordercolor="black",
            borderwidth=1,
            borderpad=4,
            bgcolor="rgba(217,217,214,0.8)",  # semi-transparent white
            opacity=0.9
        )
    ],
)

fig.update_traces(marker=dict(size=10))

st.plotly_chart(fig, use_container_width=True)
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        "<p style='font-family: Source Sans; font-size: 18px;'>Insert normalized basal expression of each gene:</p>",
        unsafe_allow_html = True )
    st.markdown(
        """
        <style>
        /* Target the scroll-box container specifically */
        div[data-testid="stForm"] > div:nth-child(1) {
            height: 300px;      /* match plot height */
            overflow-y: auto;   /* enable vertical scroll */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.form("gene_input_form", clear_on_submit=False):
        # All text inputs go here
        gene_inputs = {}
        for g in genes:
            gene_inputs[g] = st.text_input(g, value="")

        submitted = st.form_submit_button("Submit")

        if submitted:
            if any(v.strip() == "" for v in gene_inputs.values()):
                st.error("Please fill in all gene values.")
            else:
                st.success("Values successfully submitted!")
                gene_dict_float = {k: float(v) for k, v in gene_inputs.items()}
                render_result(col2, gene_dict_float)
