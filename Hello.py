# streamlit_app.py
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import hydralit_components as hc
import datetime
from streamlit_image_coordinates import streamlit_image_coordinates
from streamlit_elements import nivo, elements, mui, html

# Make it look nice from the start
st.set_page_config(layout='wide', initial_sidebar_state='collapsed')
custom_html = """
<div class="banner">
    <img src="https://github.com/ArthurSrz/forge-data-position-final/blob/main/resource/logo_forge.png?raw=true" alt="Banner Image">
</div>
<style>
    .banner {
        width: 100%;
        height: 150px;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
        padding: 10px;
        
    }
    .banner img {
        max-width: 100%;
        max-height: 100%;
    }
</style>
"""
# Display the custom HTML
st.components.v1.html(custom_html)
# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

# Specify the primary menu definition
menu_data = [
    {'icon': "far fa-copy", 'label': "Qualification"},
    {'icon': "far fa-copy", 'label': "Recrutement"},
    {'icon': "far fa-copy", 'label': "Position"},
]

# Initialize session state
if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = "Qualification"

def colorizer_tab():
    st.title("Table de qualification des profils data")
    st.markdown("Vous envisagez de classer une population en différents profils _data_.")
    st.markdown("Chaque **profil data** correspond à un ensemble de compétences auxquelles sont associées un certain niveau de maitrise. ") 
    st.markdown("Pour évaluer le niveau de maitrise, vous poserez à la population des **questions** ")
    st.markdown("A chaque question est associé un ensemble de 4 **réponses** possibles.")
    st.markdown("Chaque réponse correspond à un certain **niveau de maîtrise**")
    
    st.markdown("This is where I will add the two options for the user to choose from")


    col1, col2 = st.columns(2)

    if 'data' not in st.session_state:
        st.session_state.data = {
            'profile_type':[],
            'question': [],
            'answer': [],
            'score': []
        }

    with col1:
        st.header('Ma :blue[table] :sunglasses:')
        profile_type = st.text_input("Le profil")
        question = st.text_input("La question")
        answer = st.text_input("Une réponse possible")
        score = st.selectbox("Le niveau de maitrise associé", [1, 2, 3, 4])

        if st.button("Ajouter", key=8):
            st.session_state.data['profile_type'].append(profile_type)
            st.session_state.data['question'].append(question)
            st.session_state.data['answer'].append(answer)
            st.session_state.data['score'].append(score)
            # Combine the existing data from Google Sheets and new data
            existing_data = conn.read(worksheet="Colorizer", usecols=["question","answer","score","profile_type"],ttl=0, nrows=10)
            existing_df = pd.DataFrame(existing_data)
            #st.write("Existing Data:")
            #st.dataframe(existing_df)
            new_df = pd.DataFrame(st.session_state.data)
            #st.write("New Data:")
            #st.dataframe(new_df)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            #st.write("Combined Data:")
            #st.dataframe(combined_df)
            conn.update(worksheet="Colorizer", data=combined_df)
            st.success("Data added to Google Sheets")
            st.session_state.data = {
                'profile_type': [],
                'question': [],
                'answer': [],
                'score': []
            }

    
    with col2:
        st.header(':blue[Inspiration] :star-struck:')
        st.image("resource/skills_framework.png")
         
                    

def gatherizer_tab():
    #st.image('resource/logo_forge.png', width=400, use_column_width=True)
    st.title("Recrutement des profils data")
    st.markdown("Bienvenue sur le formulaire de recrutement. Répondez aux questions pour valider votre candidature. Nous reviendrons vers vous très vite.")
    #create an empty dataframe
    df_answers = pd.DataFrame(columns=['nom', 'prenom', 'mail', 'question', 'answer', 'score','profile_type'])
    # Add content for the form
    question_data = conn.read(worksheet="Colorizer", usecols=["question","answer","score","profile_type"],ttl=0, nrows=10)
    question_df = pd.DataFrame(question_data)
    #st.write(question_df.profile_type.values)
    unique_questions = question_df.question.unique()
    st.header("Qui êtes-vous ? :disguised_face:")
    nom = st.text_input("Nom", key='nom')
    prenom = st.text_input("Prenom", key='prenom')
    mail = st.text_input("Mail", key='mail')
    #append the values of the inputs to the df_answers
    df_answers = df_answers.append({'nom': nom, 'prenom': prenom, 'mail': mail}, ignore_index=True)
    st.header("Parlons de vous (et de data) :floppy_disk: ")


    for question_people in unique_questions:
        st.write(question_people)
        answer_people = st.selectbox("Answers", question_df[question_df.question == question_people].answer, index=None)
        score = question_df[question_df.answer == answer_people].score.values
        profile_type_val = question_df[question_df.answer == answer_people].profile_type.values
        df = pd.DataFrame({'nom': [nom], 'prenom': [prenom], 'mail': [mail],'question': [question_people], 'answer': [answer_people],'score': [score],'profile_type':[profile_type_val]})
        # Append the data to the df_answers DataFrame
        df_answers = df_answers.append(df, ignore_index=True)

        #st.dataframe(df)
    if st.button("Je valide"):
        conn.update(worksheet="Gatherizer", data=df_answers)
        st.success("Bien reçu ! A bientôt <3")
    
    # Now, outside the loop, you can display the complete df_answers DataFrame
    #st.dataframe(df_answers)
    

def dispenser_tab():
    st.header("Position des profils")
    st.markdown("Grâce au _radar graph_, analysez la distribution des profils au sein de votre population")
    with elements("nivo_charts"):
        form_data = conn.read(worksheet="Gatherizer", usecols=["nom","prenom","mail","question","answer","score","profile_type"],ttl=0, nrows=10) 
        # Obtenez les valeurs uniques de la colonne "nom"
        unique_noms = form_data['nom'].unique()

        # Créez la structure de données DATA
        DATA = []

        # Pour chaque profil unique, créez un dictionnaire
        for profile_type in form_data['profile_type'].unique():
            profile_data = {"profile": profile_type}

            # Parcourez les noms uniques
            for nom in unique_noms:
                # Filtrer le DataFrame pour obtenir les lignes correspondant au nom et profil
                filtered_data = form_data[(form_data['nom'] == nom) & (form_data['profile_type'] == profile_type)]
        
                # Vérifiez s'il y a des données pour le nom et le profil actuels
                if not filtered_data.empty:
                    score = int(filtered_data['score'].str.strip('[]').values[0])
                    profile_data[nom] = score

            DATA.append(profile_data)

        # Affichez la liste DATA
        #st.write(DATA)

        with mui.Box(sx={"height": 500}):
            nivo.Radar(
                data=DATA,
                keys=unique_noms,
                indexBy="profile",
                maxValue = 4,
                valueFormat=">-.2f",
                curve="linearClosed",
                margin={ "top": 70, "right": 80, "bottom": 40, "left": 80 },
                borderColor={ "theme": "grid.line.stroke" },
                gridLabelOffset=36,
                dotSize=8,
                dotColor={ "theme": "background" },
                dotBorderWidth=2,
                motionConfig="wobbly",
                legends=[
                    {
                        "anchor": "top-left",
                        "direction": "column",
                        "translateX": -50,
                        "translateY": -40,
                        "itemWidth": 80,
                        "itemHeight": 20,
                        "itemTextColor": "#999",
                        "symbolSize": 12,
                        "symbolShape": "circle",
                        "effects": [
                            {
                                "on": "hover",
                                "style": {
                                    "itemTextColor": "#000"
                                }
                            }
                        ]
                    }
                ],
                theme={
                    "background": "#FFFFFF",
                    "textColor": "#31333F",
                    "tooltip": {
                        "container": {
                            "background": "#FFFFFF",
                            "color": "#31333F",
                        }
                    }
                }
            )
    
    #create a df that is form_data df but group by name
    form_data = form_data[form_data['score'].notna()]
    form_data['score'] = form_data['score'].str.strip('[]').astype(int)
    form_data_grouped = form_data.groupby(['nom', 'prenom'])['score'].mean().reset_index()
    form_data_grouped['groupe'] = pd.NA
    st.header("Constitution des groupes")
    st.markdown("Répartissez les profils au sein de groupes")
    groups = st.data_editor(
        form_data_grouped,
        column_config={
            "group": st.column_config.NumberColumn(
                "Group",
                help="What group",
                min_value=1,
                max_value=10,
                step=1,
                format="%d 👭",
        )
        }
    )
    #st.dataframe(groups)
    #st.write(st.session_state)
    if st.button("Assigner", key=8):
        conn.update(worksheet="Dispenser", data=groups)
        st.success("C'est fait !")
        



# Create a function to display the selected tab content
def display_tab_content(tab_label):
    if tab_label == "Qualification":
        colorizer_tab()
    elif tab_label == "Recrutement":
        gatherizer_tab()
    elif tab_label == "Position":
        dispenser_tab()
#
over_theme = {'txc_inactive': 'white','menu_background':'#1c3f4b','txc_active':'#e95459','option_active':''}
# Create the navigation bar
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    #home_name='Home',
    #login_name='Logout',
    hide_streamlit_markers=False,
    sticky_nav=True,
    sticky_mode='pinned'
)

# Get the selected tab label from the menu
selected_tab_label = menu_id

# Display the selected tab content
display_tab_content(selected_tab_label)


# Store the selected tab in the session state
if selected_tab_label != st.session_state.selected_tab:
    st.session_state.selected_tab = selected_tab_label

# Get the id of the menu item clicked
#st.info(f"Selected tab: {selected_tab_label}")
#st.info(f"Menu {menu_id}")