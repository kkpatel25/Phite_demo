import streamlit as st
from streamlit_carousel import carousel


st.set_page_config(layout="wide")

st.write("# Welcome to the PHITE Trancriptome!")

st.markdown(
    """
    <div style="
        font-family: 'Source Sans Pro', sans-serif; 
        font-size: 18px; 
        padding: 15px; 
        margin-bottom: 20px; 
        border-radius: 6px;
        color: black;
    ">
      <p>
        This site is designed to help you explore and visualize data from the PHITE study, which stands for Precision High-Intensity Training Through Epigenetics. This longitudinal <strong>Human acute- and long-term exercise trial </strong>was granted under the IRB-160512012.  </p>  
        <p> Use the <strong>sidebar</strong> to navigate through different pages and tools.
      </p>
      <ul>
        <li><a href="https://github.com/kkpatel25/Phite_demo" target="_blank"><strong>View our GitHub Repository</strong></a></li>
        <li><strong>Cite Us!</strong> Patel et al., manuscript in preparation</li>
      </ul>
    </div>
    """,
    unsafe_allow_html=True
)


items = [
    dict(
        title="",
        text="",
        img="folddemo.png",
    ),
    dict(
        title="",
        text="",
        img="vo2demo.png",
    ),
]
carousel(items=items, controls=False, interval=5000)

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        <div style="
            font-family: 'Source Sans Pro', sans-serif; 
            font-size: 18px; 
            color: black;
        ">
          <p> <center>
            This PHITE study was funded by Office of Naval Research (ONR). 
          </center> </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    _, center, _ = st.columns([1, 3, 1])  # Creates three columns
    with center:
        st.image("onr_logo.png", width=800)
with col2:
    st.markdown(
        """
        <div style="
            font-family: 'Source Sans Pro', sans-serif; 
            font-size: 18px; 
            color: black;
            padding: 15px; 
        ">
        <center>
          <p> 
            <strong> Developers: </strong> 
          </p>
          <p> Krish Patel (kpate156@jh.edu) </p> 
          <p> Dr. Weiwei Fan (wfan@salk.edu) </p>
          <p> Dr. Ron Evans (evans@salk.edu) </p>
          <p> Dr. Tae Gyu Oh (taegyu-oh@ou.edu) </p>
          </center>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div style="
        font-family: 'Source Sans Pro', sans-serif; 
        font-size: 18px; 
        background-color: #f5f5f5; 
        padding: 12px; 
        margin-top: 30px; 
        border-radius: 6px;
        color: black;
    ">
      <p><strong>Disclaimer: Research Use Only</strong></p>
      <p>
        This application, utilizing the phite-baseRNA-predict-futureVO2 model, 
        is built exclusively for academic research and informational purposes. 
        The underlying data for model training and validation was sourced entirely from a single institutional dataset 
        PHITE. 
        As such, the predictive values are based solely on that cohort. 
        <strong>The predicted results are not clinical advice and should not be used to guide personal health decisions, 
        medical diagnoses, or treatment plans. </strong> 
        The developers and associated institutions assume <strong>no legal responsibility or liability for the consequences 
        of any reliance placed upon these predictions. </strong>
      </p>
      <p>
        For any inquiries, collaborations, or consultation regarding the model or its underlying research, 
        please contact the developers directly.
      </p>
    </div>
    """,
    unsafe_allow_html=True
)
