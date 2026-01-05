import streamlit as st
import constantes as ct
from fonctions import *
import pandas as pd
import altair as alt

# LE CONTENU DU SIDEBAR
with st.sidebar:
    st.logo(image="logo/logo_DIT.png", size="large")

    st.sidebar.header("DATA COLLECTION")

    start = st.sidebar.selectbox(
        label="Selectionnez l'index de début",
        options=[index for index in range(1, 119)]
    )

    stop = st.sidebar.selectbox(
        label="Selectionnez l'index de fin",
        options=[stop for stop in range(1, 120)],
        index=118
    )

    option = st.sidebar.selectbox(
        label="Selectionnez une action",
        options=(ct.DASHBOARD, ct.SCRAP_DATA, ct.DOWNLOAD_DATA, ct.EVALUATE_APP)
    )

# VERIFICATION DE L'INDEX DE DEBUT ET DE FIN
if start == stop and option == ct.SCRAP_DATA:
    st.error(f"""
        Attention les deux champs sont égaux et donc seulement les données de la page {start} 
        sont retournées""", width="stretch")

############ STYLE GLOBALE A APPLIQUER SUR CERTAINS ELEMENTS DE L'APPLI ############
st.markdown(
    """
    <style>
        /* **** style pour la section principale de la page ****  */
        .stApp {
            background-color: #E0DEDE;
        }

        /* ****** pour les boutons **** */
        div.stButton > button {
            width: 100%;
            height: 50px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 12px;
            background-color: #2ebff0;
            color: white;
            border: 2px solid #2ebff0;
            margin: 5px 0;
            transition: all 0.4s ease;
        }
        div.stButton > button:hover {
            background-color: #111;
            color: #2ebff0;
            border: 2px solid #2ebff0;
        }

        /* ****** pour le side bar **** */
        section[data-testid="stSidebar"] {
            background-color: #1e1e2f;
            border-right: 2px solid #2ebff0;
            border-radius: 0 8px 8px 0;
            padding: 20px;
        }

        /* pour les textes */
        section[data-testid="stSidebar"] * {
            color: #2ebff0;
        }

        /* pour les titres */
        section[data-testid="stSidebar"] h2 {
            color: #fff;
        }

        /* pour les selectbox */
        section[data-testid="stSidebar"] .stSelectbox {
            background-color: #1e1e2f;
        }        
    </style>
    """,
    unsafe_allow_html=True
)

# LE CONTENU DE LA PAGE
if option == ct.DASHBOARD:
    st.markdown(write_title("Tableau de bord"), unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["Vêtements Hommes", "Chaussures Hommes", "Vêtements Enfants", "Chaussures Enfants"])
    list_options = ["From scrapping", "From webscrapper"]

    with tab1:        
        choix_tab1 = st.radio(label="-", options=list_options, horizontal=True, key="tab1")
        title = "vêtements pour hommes"
        if choix_tab1 == list_options[0]:
            dataframe = scrapping_url(url=ct.CLOTHES_MAN_URL, fin=1)
            show_chart(title=title, dataframe=dataframe)
        else:
            dataframe = pd.read_csv("./data/url_1.csv").head(n=20)
            show_chart_ws(dataframe=dataframe)
    
    with tab2:
        choix_tab2 = st.radio(label="-", options=list_options, horizontal=True, key="tab2")
        title = "chaussures pour hommes"
        if choix_tab2 == list_options[0]:
            dataframe = scrapping_url(url=ct.SHOES_MAN_URL, fin=1)
            show_chart(title=title, dataframe=dataframe)
        else:
            dataframe = pd.read_csv("./data/url_2.csv").head(n=20)
            show_chart_ws(dataframe=dataframe)

    with tab3:
        choix_tab3 = st.radio(label="-", options=list_options, horizontal=True, key="tab3")
        title = "vêtements pour enfants"
        if choix_tab3 == list_options[0]:
            dataframe = scrapping_url(url=ct.CLOTHES_CHILD_URL, fin=1)
            show_chart(title=title, dataframe=dataframe)
        else:
            dataframe = pd.read_csv("./data/url_3.csv").head(n=20)
            show_chart_ws(dataframe=dataframe)

    with tab4:
        choix_tab4 = st.radio(label="-", options=list_options, horizontal=True, key="tab4")
        title = "chaussures pour enfants"
        if choix_tab4 == list_options[0]:
            dataframe = scrapping_url(url=ct.SHOES_CHILD_URL, fin=1)
            show_chart(title=title, dataframe=dataframe)
        else:
            dataframe = pd.read_csv("./data/url_4.csv").head(n=40)
            show_chart_ws(dataframe=dataframe)
    
if option == ct.SCRAP_DATA:
    st.html(write_title("Scrapping de données avec BeautifulSoup"))
    st.html("""<p style='font-size:20px'>Cliquer sur l'un des boutons suivant pour avoir accès au dataframe correspondant</p>""")    
    
    # LIGNE 1 : POUR LES HOMMES
    col1, col2 = st.columns(2)
    with col1:
        btn1 = st.button("Vêtements hommes", use_container_width=True)
    with col2:
        btn2 = st.button("Chaussures hommes", use_container_width=True)

    # LIGNE 2 : POUR LES ENFANTS
    col3, col4 = st.columns(2)
    with col3:
        btn3 = st.button("Vêtements enfants", use_container_width=True)
    with col4:
        btn4 = st.button("Chaussures enfants", use_container_width=True)

    # AFFICHAGE DES DATAFRAMES
    if btn1:
        title = "Vêtements Hommes"
        with st.spinner(f"Scrapping {title} en cours ..."):
            df_1_sd = scrapping_url(url=ct.CLOTHES_MAN_URL, debut=start, fin=stop)
            if "Erreur" in df_1_sd:
                st.error(df_1_sd)
            else:
                st.html(show_info_df(df_1_sd, title))
                st.dataframe(df_1_sd)

    elif btn2:
        title = "Chaussures Hommes"
        with st.spinner(f"Scrapping {title} en cours ..."):
            df_2_sd = scrapping_url(url=ct.SHOES_MAN_URL, debut=start, fin=stop)
            if "Erreur" in df_2_sd:
                st.error(df_2_sd)
            else:
                st.html(show_info_df(df_2_sd, title))
                st.dataframe(df_2_sd)
    elif btn3:
        title = "Vêtements Enfants"
        with st.spinner(f"Scrapping {title} en cours ..."):
            df_3_sd = scrapping_url(url=ct.CLOTHES_CHILD_URL, debut=start, fin=stop)
            if "Erreur" in df_3_sd:
                st.error(df_3_sd)
            else:
                st.html(show_info_df(df_3_sd, title))
                st.dataframe(df_3_sd)
    elif btn4:
        title = "Chaussures Enfants"
        with st.spinner(f"Scrapping {title} en cours ..."):
            df_4_sd = scrapping_url(url=ct.SHOES_CHILD_URL, debut=start, fin=stop)
            if "Erreur" in df_4_sd:
                st.error(df_4_sd)
            else:
                st.html(show_info_df(df_4_sd, title))
                st.dataframe(df_4_sd)
if option == ct.DOWNLOAD_DATA:
    st.html(write_title("Téléchargement de données web scrappé"))
    st.html("""<p style='font-size:20px'>Cliquer sur l'un des boutons suivant pour avoir accès au dataframe correspondant</p>""")
    
    # LIGNE 2 : POUR LES HOMMES
    col1, col2 = st.columns(2)
    with col1:
        btn1 = st.button("Vêtements hommes", use_container_width=True)
    with col2:
        btn2 = st.button("Chaussures hommes", use_container_width=True)

    # LIGNE 2 : POUR LES ENFANTS
    col3, col4 = st.columns(2)
    with col3:
        btn3 = st.button("Vêtements enfants", use_container_width=True)
    with col4:
        btn4 = st.button("Chaussures enfants", use_container_width=True)

    # AFFICHAGE DES DATAFRAMES
    if btn1:
        with st.spinner("Display dataframe en cours ..."):
            df_1_wd = pd.read_csv("./data/url_1.csv")
            st.html(show_info_df(df_1_wd, "Vêtements Hommes"))
            st.dataframe(df_1_wd)

    elif btn2:
        with st.spinner("Display dataframe en cours ..."):
            df_2_wd = pd.read_csv("./data/url_2.csv")
            st.html(show_info_df(df_2_wd, "Chaussures Hommes"))
            st.dataframe(df_2_wd)

    elif btn3:
        with st.spinner("Display dataframe en cours ..."):
            df_3_wd = pd.read_csv("./data/url_3.csv")
            st.html(show_info_df(df_3_wd, "Vêtements Enfants"))
            st.dataframe(df_3_wd)

    elif btn4:
        with st.spinner("Display dataframe en cours ..."):
            df_4_wd = pd.read_csv("./data/url_4.csv")
            st.html(show_info_df(df_4_wd, "Chaussures Enfants"))
            st.dataframe(df_4_wd)

if option == ct.EVALUATE_APP:    
    st.html(write_title("Evaluation de l'application"))
    st.html(
        """
        <p style='font-size: 20px'>
            Veuillez utiliser l'un des formulaires suivants pour apprecier notre application, 
            merci d'avance pour votre temps
        </p>
        """
    )
    col1, col2 = st.columns(2)
    with col1:
        btn1 = st.link_button("Kobo forms", ct.KOBO_FORMS_URL, use_container_width=True)
    with col2:
        btn2 = st.link_button("Google forms", ct.GOOGLE_FORMS_URL, use_container_width=True)