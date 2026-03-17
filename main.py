import streamlit as st
import json
import pandas as pd

def get_table(json_data, frame=st):
    df = pd.DataFrame(json_data)
    if df.empty:
        frame.text("No data found!")
        return
    def make_pretty(styler):
        styler.map(lambda x: 'font-weight: bold', subset=['class'])
        styler.map(lambda x: "font-size: 18px;", subset=['class'])
        # styler.set_properties(**{'text-align': 'center'})
        return styler
    frame.dataframe(
        df.style.pipe(make_pretty),
        # df.style.apply(operacao_color, axis=0),
        width="stretch",
        # For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.
        hide_index=True,
        column_order=["class", "skill", "lv", "effect"],
        column_config={
            "class": st.column_config.TextColumn(
                "Class",
                width="small"
            ),

            "skill": st.column_config.TextColumn(
                "Skill",
                width="medium"
            ),
            "lv": st.column_config.TextColumn(
                "lv",
                width="small"
            ),
            "effect": st.column_config.TextColumn(
                "Effect",
                width="large"
            )
        }
    )

def get_all_from_file():
    file = f"ieh2/ieh2_dados.json"
    all_data = []
    with open(file, mode="r", encoding="utf-8") as f:
        json_data = json.load(f)
        for hero_info in json_data:
            for skill in hero_info["skills"]:
                for passive in skill["passives"]:
                    all_data.append({
                        "class": hero_info["name"],
                        "skill": skill["name"],
                        "lv": passive["lv"],
                        "effect": passive["effect"]
                    })
    return all_data

def find_effect(hero_class, effect):
    all_data = st.session_state.all_data
    filtered_data = []
    for hero_info in all_data:
        print(hero_info)
        if hero_class.lower() == hero_info["class"] or hero_class == "All":
            if effect in hero_info["effect"]:
                filtered_data.append(hero_info)
    return filtered_data

st.session_state.all_data = get_all_from_file()

st.title("Idle Epic Hero 2")
all_data = st.session_state.all_data
hero_class = st.selectbox("Class", ["All","Warrior","Wizard","Angel","Thief","Archer","Tamer"])
input = st.text_input('Filtro')
retorno = find_effect(hero_class, input)
get_table(retorno)
