from bs4 import BeautifulSoup
import requests as rq
import pandas as pd

# FONCTION POUR ECRIRE LE TITRE LA PAGE
def write_title(title):
    return f"""
        <h1 
            style='text-transform:uppercase; text-align:center; letter-spacing:10px; 
            text-decoration:underline; color: #2ebff0';
        >
            {title}
        </h1>
    """

def show_info_df(dataframe, title):
    return f"""
        <h1 style='text-align:center'>Dimension du dataframe : <span style='color:#2ebff0'>{title}</span></h1>
        <p style='text-align:center'>
            Le dataframe a : 
            <span style='color:#2ebff0'>{dataframe.shape[0]}</span> ligne(s) et 
            <span style='color:#2ebff0'>{dataframe.shape[1]}</span> colonne(s)
        </p>
    """

# FONCTION POUR NETTOYER UN DATAFRAME
def cleaning_df(df):
    if df is None or df.empty:
        return pd.DataFrame()

    df_clean = df.copy()
    for col in ["type", "adresse", "Image"]:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna(pd.NA)
    
    if "type" in df_clean.columns:
        df_clean['type'] = df_clean['type'].astype(str)
    
    if "prix" in df_clean.columns:
        df_clean['prix'] = pd.to_numeric(df_clean['prix'], errors="coerce")
        df_clean["prix"] = df_clean['prix'].fillna(df_clean['prix'].mean())
    
    df_clean.drop_duplicates(inplace=True)
    
    return df_clean


def scrapping_url(url, debut=1, fin=119):
    df = pd.DataFrame()    
    for page in range(debut, fin+1):        
        list_data = []
        try:
            url_page = f"{url}?page={page}"
            response = rq.get(url_page)
            soup = BeautifulSoup(response.content, "html.parser")
            articles = soup.find_all("div", "col s6 m4 l3")
            for article in articles:
                type_habit = article.find("p", "ad__card-description").a.text.strip()                
                prix = article.find("p", "ad__card-price").a.text.strip()
                if "FCFA" in prix:
                    prix = prix.replace("FCFA", "").replace(" ", "")
                if "CFA" in prix:
                    prix = prix.replace("CFA", "").replace(" ", "")
                adresse = article.find("p", "ad__card-location").span.text.strip()
                image = article.find("img", "ad__card-img")["src"]

                element = {
                    "type": type_habit,
                    "prix": prix,
                    "adresse":adresse,
                    "Image": image
                }

                list_data.append(element)
        except Exception as e:
            return f"Erreur sur la page : {url_page} - {e}"

        DF_PAGE = pd.DataFrame(list_data)
        df = pd.concat([df, DF_PAGE], axis=0).reset_index(drop=True)
    
    dataframe = cleaning_df(df)
    return dataframe

# FFICHAGE DES GRAPHIQUES
def show_chart(title, dataframe):
    import streamlit as st
    import altair as alt
    st.subheader(f"Grphique sur les {title} (quelques données)", text_alignment="center")
    if "Erreur" in dataframe:
        st.error(dataframe)
    else:
        col1, col2 = st.columns(2)

        # Graphe lié au type de vêtement
        with col1:
            chart_type = (
                alt.Chart(dataframe)
                .mark_line(point=True)
                .encode(
                    x=alt.X("type:N", title="Type de vêtement"),
                    y=alt.Y("count():Q", title="Nombre", axis=alt.Axis(tickMinStep=1))
                ).properties(width=300,height=500)
            )
            st.altair_chart(chart_type)
        
        # Graphe lié au prix
        with col2:
            chart_price = (
                alt.Chart(dataframe)
                .mark_bar()
                .encode(
                    x=alt.X("prix:Q", bin=True, title="Prix"),
                    y=alt.Y("count():Q", title="Nombre")
                ).properties(width=300, height=500)
            )
            st.altair_chart(chart_price)

        # Graphe lié au prix par type de vêtement
        st.markdown("### Prix par type de vêtement")
        chart_type_price = (
            alt.Chart(dataframe)
            .mark_bar()
            .encode(
                x=alt.X("type:N", title="Type"),
                y=alt.Y("prix:Q", title="Prix"),
                tooltip=["type", "prix"]
            )
            .properties(width=650, height=700)
        )
        st.altair_chart(chart_type_price)

def show_chart_ws(dataframe):
    import streamlit as st

    # Nettoyage minimal
    df = dataframe.copy()

    df['type'] = df['type'].astype(str)
    df['prix'] = (
        df['prix']
        .astype(str)
        .str.replace("FCFA", "", regex=False)
        .str.replace("CFA", "", regex=False)
        .str.replace(" ", "", regex=False)
    )
    df['prix'] = pd.to_numeric(df['prix'], errors='coerce')

    # Calculs
    count_by_type = df['type'].value_counts()
    count_by_prix = df['prix'].value_counts().sort_index()
    grouped_by_type_prix = df.groupby('type')['prix'].mean()

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Vêtements par type")
        st.bar_chart(count_by_type)

    with col2:
        st.subheader("Prix moyen par type")
        st.bar_chart(count_by_prix)

    st.subheader("Distribution des prix")
    st.line_chart(grouped_by_type_prix)