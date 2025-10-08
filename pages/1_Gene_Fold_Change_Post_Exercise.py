import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(layout="wide")

timepoint_labels = {
    "w0pre": "Week 0 Pre",
    "w0h3": "Week 0 hour 3",
    "w0h24": "Week 0 hour 24",
    "w12pre": "Week 12 Pre",
    "w12h3": "Week 12 hour 3",
    "w12h24": "Week 12 hour 24",
    "w16rest": "Week 16 Rest",
}

@st.cache_data
def load_data():
    return pd.read_csv(st.secrets["data_url"])


def app():
    df = load_data()

    tabs_font_css = """
    <style>
    div[class*="stTextInput"] label p {
        font: Source Sans;
        font-size: 18px;
    }
    </style>
    """

    st.write(tabs_font_css, unsafe_allow_html=True)

    gene_input = st.text_input("Type a gene name and enter:")


    if "downloads_ready" not in st.session_state:
        st.session_state.downloads_ready = False

    if gene_input:
        gene_input = gene_input.strip().upper()

        if gene_input not in df["genesymbol"].values:
            st.error(f"{gene_input} is not a valid gene name. Please try again.")
        else:
            st.success(f"Gene {gene_input} found!")

            plot_df = process_df(gene_input, df)

            if "current_gene" not in st.session_state:
                st.session_state.current_gene = gene_input

            cols_to_plot = st.multiselect(
                "**Select columns to display:**",
                options=plot_df["comparison"].values,  # exclude 'Gene' column
                default=plot_df["comparison"].values,
            )

            if "cols_to_plot" not in st.session_state:
                st.session_state.cols_to_plot = cols_to_plot

            plot_df = plot_df[plot_df["comparison"].isin(cols_to_plot)]

            fig = generateBar(plot_df, gene_input)
            st.plotly_chart(fig, use_container_width=True)

            _, center, _ = st.columns([1, 2, 1])

            if st.session_state.cols_to_plot != cols_to_plot or st.session_state.current_gene != gene_input:
                st.session_state.downloads_ready = False
                st.session_state.cols_to_plot = cols_to_plot
                st.session_state.current_gene = gene_input

            with center:
                if not st.session_state.downloads_ready:
                    if st.button("Generate Download"):
                        st.session_state.downloads_ready = True
                        st.session_state.figure_png = fig.to_image(format="png", engine="kaleido")
                        st.session_state.figure_pdf = fig.to_image(format="pdf", engine="kaleido")
                        st.rerun()
                else:
                    # its already cached
                    pdf_image = st.session_state.figure_pdf
                    png_image = st.session_state.figure_png

                    col1, col2 = st.columns(2)

                    with col1:
                        st.download_button(
                            label="Download PNG",
                            data=png_image,
                            file_name=f"{gene_input}.png",
                            mime="image/png",
                            use_container_width=True
                        )

                    with col2:
                        st.download_button(
                            label="Download PDF",
                            data=pdf_image,
                            file_name=f"{gene_input}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

            # for spacing
            st.write("##")

            fig_table = generateTable(plot_df, gene_input)
            st.plotly_chart(fig_table, use_container_width=True)

def process_df(gene, df):
    g = df[df["genesymbol"] == gene].squeeze()
    fc_cols = [c for c in df.columns if c.startswith("log2FC_")]
    padj_cols = [c for c in df.columns if c.startswith("padj_")]

    plot_df = pd.DataFrame({
        "comparison": [c.replace("log2FC_", "") for c in fc_cols],
        "log2FC": [g[c] for c in fc_cols],
        "padj": [g[p] for p in padj_cols],
    })
    return plot_df

def format_comparison_label(comp):
    # Split into parts like "w0h3" and "w0pre"
    parts = comp.split("_vs_")
    if len(parts) != 2:
        return comp  # fallback for unexpected cases

    left, right = parts
    global timepoint_labels
    left_label = timepoint_labels.get(left, left)
    right_label = timepoint_labels.get(right, right)

    return f"{left_label} vs {right_label}"


comparison_label_map = {
    comp: format_comparison_label(comp)
    for comp in [
        'w0h3_vs_w0pre', 'w0h24_vs_w0pre', 'w12pre_vs_w0pre',
        'w12h3_vs_w0pre', 'w12h24_vs_w0pre', 'w16rest_vs_w0pre',
        'w12h3_vs_w12pre', 'w12h24_vs_w12pre', 'w16rest_vs_w12pre',
        'w0h24_vs_w0h3', 'w12h24_vs_w12h3', 'w16rest_vs_w12h24'
    ]
}

# Create base bar plot
def generateBar(plot_df, gene):

    colors = ["#d62728" if fc > 0 else "#1f77b4" for fc in plot_df["log2FC"]]

    significance = []
    for i, row in plot_df.iterrows():
        # [0.05 - 0.01) *
        # [0.01 - 0.001) **
        # [0.001 - 0 ***)
        if row["padj"] < 0.05:
            if row["padj"] <= 0.001:
                significance.append("***")
            elif row["padj"] <= 0.01:
                significance.append("**")
            else:
                significance.append("*")
        else:
            significance.append(" ")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=plot_df["comparison"],
        y=plot_df["log2FC"],
        name="",
        showlegend=False,
        hovertemplate="<b>%{x}</b><br>log2FC = %{y:.2f}<br>padj = %{customdata:.5f}",
        customdata=plot_df["padj"],
        marker_color=colors,
        text=significance,
        textfont=dict(
            size=18,  # Set the desired font size
            color='black',
            family="Arial Black"
        ),
        textposition="outside"
    ))

    ymin, ymax = plot_df["log2FC"].min(), plot_df["log2FC"].max()
    yrange = ymax - ymin
    fig.update_yaxes(range=[ymin - 0.15 * yrange, ymax + 0.15 * yrange])

    fig.update_layout(
        title=f"Fold Change Across Time Points for {gene}",
        xaxis_title="Timepoints",
        yaxis_title="log2FC",
        template="plotly_white",
        showlegend=False
    )

    fig.update_xaxes(
        ticktext=plot_df["comparison"],
        tickvals=plot_df["comparison"],
        tickfont=dict(size=12)
    )
    fig.update_xaxes(linewidth=2, linecolor='rgb(231, 234, 240)', mirror=True,
                     showline=True)

    fig.update_yaxes(linewidth=2, linecolor='rgb(231, 234, 240)', mirror=True,
                     showline=True)

    return fig

def generateTable(plot_df, gene):
    fig_table = go.Figure(
        data=[go.Table(
            header=dict(
                values=["Time Points", "Fold Change (log2FC)", "Adjusted P-value"],
                fill_color="#1f77b4",
                align="center",  # horizontal center
                font=dict(color="white", size=15)
            ),
            cells=dict(
                values=[
                    #[comparison_label_map.get(x, x) for x in plot_df["comparison"]],
                    plot_df["comparison"],
                    [f"{x:.2f}" for x in plot_df["log2FC"]],
                    [f"{x:.2e}" for x in plot_df["padj"]]
                ],
                fill_color=[
                    ["#f9f9f9" if i % 2 == 0 else "#ffffff" for i in range(len(plot_df))]
                    for _ in range(3)  # one list per column
                ],
                align="center",  # horizontal center
                font=dict(size=15),
                height=30  # set row height for all cells
            )
        )]
    )

    fig_table.update_layout(
        title=f"Fold Change and Adjusted P-values for {gene}",
        template="plotly_white",
        margin=dict(t=40, l=20, r=20, b=20)
    )
    return fig_table

app()
