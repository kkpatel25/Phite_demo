import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import sklearn

@st.cache_data
def load_model():
    return joblib.load("power_predict.joblib")

def predict(gene_dict):
    loaded_model = load_model()
    df = pd.DataFrame([gene_dict], index=[0])
    return (loaded_model.predict(df))[-1]


def render_result(col2, gene_dict):
    with col2:
        value = predict(gene_dict)
        st.markdown(
            f"""
                    <div style="margin-top: 130px; font-size:20px; font-weight:bold; color:black; padding:10px; border-radius:8px;">
                        Predicted Power delta after 12 weeks of training: {value:+.2f}
                    </div>
                    """,
            unsafe_allow_html=True
        )

st.set_page_config(layout="wide")

predict_vals = [
    0.005599743186, 1.298266617, 1.891041318, 0.7535308592, 1.16681347,
    0.3959297206, 1.815427717, 1.882253625, 1.839312917, 3.049305107,
    1.506710053, 1.780577201, 3.42148162, 3.23387687, 3.832846885, 3.417289455
]

target_vals = [
    -2.607897982, 0.269361509, 0.503708835, 1.186004643, 1.195350356,
    2.224511249, 2.435519798, 2.656927711, 2.700224126, 2.812167434,
    3.045725237, 3.604506253, 4.125, 4.817310275, 4.916382253, 7.202941176
]

genes = ['CCDC32', 'CDIN1', 'CHURC1', 'CYP4X1', 'ENSG00000235296', 'ENSG00000275202', 'ENSG00000284773', 'ENSG00000286970', 'EP400', 'FAM102A', 'GASK1A', 'GOLGA8J', 'HOMER1', 'IFT27', 'ITM2B', 'KCNIP3', 'KRBOX1', 'LARGE1', 'LINC00924', 'LRRC4B', 'LRRK1', 'MANEAL', 'NDUFB1', 'NECAP1', 'NOP2', 'PRKCH-AS1', 'PRKCSH', 'PRPF40A', 'PTPRC', 'PUM3', 'PXDNL', 'RFTN1', 'SCGB1D2', 'SLC38A7', 'SLC6A16', 'SNX7', 'VPS35L', 'ZNF570']

df = pd.DataFrame({
    "Person": [f"Person {i+1}" for i in range(len(predict_vals))],
    "Predicted": predict_vals,
    "True": target_vals
})

df_melted = df.melt(
    id_vars="Person",
    value_vars=["Predicted", "True"],
    var_name="Type",
    value_name="Power Delta"
)

fig = px.scatter(
    df_melted,
    x="Person",
    y="Power Delta",
    color="Type",
    color_discrete_map={"Predicted": "blue", "True": "red"},
)

fig.update_layout(
    xaxis=dict(
        title="",
        showticklabels=False  # hides Person names
    ),
    legend_title="",
    margin=dict(l=20, r=20, t=30, b=20),
    height=600,
    annotations=[
        dict(
            x=1,  # far right
            y=0,  # bottom
            xref="paper",
            yref="paper",
            text="R² = 0.483",
            showarrow=False,
            font=dict(
                family="Arial",
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
    ]

)

st.plotly_chart(fig, use_container_width=True)
col1, col2 = st.columns([2, 1])

with col1:
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
