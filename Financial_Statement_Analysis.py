import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

st.title('Financial Statement Analysis')

frame = pd.read_csv('dataframe.csv')

colonna_da_scegliere = st.selectbox(
     'Seleziona una colonna ',
     tuple(frame.columns)[2:])

source = frame[frame['Ragione_sociale'] != 'Orbita Verticale S.R.L.']


nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['Anno'], empty='none')

selectors = alt.Chart(source).mark_point().encode(
    x='Anno:T',
    opacity=alt.value(0),
).add_selection(
    nearest
)

line = alt.Chart(source).mark_line().encode(
    x='Anno:T',
    y=f'{colonna_da_scegliere}:Q',
    color='Ragione_sociale',
)

points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

text = line.mark_text(align='left', dx=5, dy=-10).encode(
    text=alt.condition(nearest, f'{colonna_da_scegliere}:Q', alt.value(' '))
)

rules = alt.Chart(source).mark_rule(color='gray').encode(
    x='Anno:T',
).transform_filter(
    nearest
)

partecipate = alt.layer(
    line, selectors, points, rules, text
)#.properties(width=620, height=375)

source_orbita = frame[frame['Ragione_sociale'] == 'Orbita Verticale S.R.L.']


nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['Anno'], empty='none')

selectors_o = alt.Chart(source_orbita).mark_point().encode(
    x='Anno:T',
    opacity=alt.value(0),
).add_selection(
    nearest
)

orbita_verticale_line = alt.Chart(source_orbita).mark_line().encode(
    x='Anno:T',
    y=f'{colonna_da_scegliere}:Q',
    color='Ragione_sociale',
)#.properties(width=400)


points_o = orbita_verticale_line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

text_o = orbita_verticale_line.mark_text(align='left', dx=5, dy=-10).encode(
    text=alt.condition(nearest, f'{colonna_da_scegliere}:Q', alt.value(' '))
)

rules_o = alt.Chart(source_orbita).mark_rule(color='gray').encode(
    x='Anno:T',
).transform_filter(
    nearest
)

orbita_verticale = alt.layer(
    orbita_verticale_line, selectors_o, points_o, rules_o, text_o
)

c = alt.hconcat(
    orbita_verticale,
    partecipate
).resolve_scale(
    y='shared'
)

st.altair_chart(c, use_container_width=False)
