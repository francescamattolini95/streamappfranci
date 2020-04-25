import streamlit as st
import spacy
from spacy import displacy
import pandas as pd
from spacy.pipeline import EntityRuler
from spacy.matcher import PhraseMatcher
import base64

SPACY_MODEL_NAMES = ["jobtitles"]
#SPACY_MODEL_NAMES = ["ergonomy_spacy_model"]
DEFAULT_TEXT = "I'm a management engineer!"
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; 
                margin-bottom: 2.5rem">{}</div>"""

#@st.cache(ignore_hash=True)
#@st.cache(allow_output_mutation=TRUE)
def load_model(name):
    return spacy.load(name)

#@st.cache(ignore_hash=True)
#@st.cache(allow_output_mutation=TRUE)
def process_text(model_name, text):
    nlp = load_model(model_name)
    return nlp(text)

# Sidebar Title
from PIL import Image
img= Image.open("imm.jpeg")
st.sidebar.image(img, width=300)

# Description
st.sidebar.markdown(
"""This interactive web application uses [spaCy](https://spacy.io) models to visualize Job Titles within a given text.
It uses spaCy's built-in [displaCy](http://spacy.io/usage/visualizers) visualizer under the hood.
"""
)
st.sidebar.title("")

# Spacy
spacy_model = "jobtitles"
model_load_state = st.info(f"Loading model '{spacy_model}'...")
nlp = load_model(spacy_model)
model_load_state.empty()
#nlp.to_disk("./jobtitles")

# Page Title
st.title("Try the visualizer")

# Text_Area
text = st.text_area("Please, paste your text below!", DEFAULT_TEXT)

# Code
if "ner" in nlp.pipe_names:
    st.subheader("Job Titles sorting")
    st.sidebar.header("Base Job Titles")
    default_labels = ["ENGINEER"]
    labels = st.sidebar.multiselect("""By selecting one or several Base Job Titles from the dropdown menu below, 
        the text on the right will automatically highlight the correspondent Compound Job Titles. """,
    	("ENGINEER", "SPECIALIST", "MANAGER", "OPERATOR", "AGENT", "SCIENTIST"), default_labels)
    ruler = EntityRuler(nlp)
    patterns = [{"label": "ENGINEER", "pattern": [{'DEP': 'compound'},{'LOWER': 'engineer'}]},
            {"label": "ENGINEER", "pattern": [{'LOWER': 'engineer'},{'DEP': 'prep'},{'DEP': 'amod'},{'POS': 'NOUN'},
                                              {'DEP': 'prep'},{'DEP': 'amod'},{'POS': 'NOUN'}]},
            {"label": "ENGINEER", "pattern": [{'LOWER': 'engineer'},{'DEP': 'prep'},{'POS': 'NOUN'},
                                              {'DEP': 'prep'},{'DEP': 'amod'},{'POS': 'NOUN'}]},
            {"label": "ENGINEER", "pattern": [{'LOWER': 'engineer'},{'DEP': 'prep'},{'POS': 'NOUN'},
                                              {'DEP': 'prep'},{'POS': 'NOUN'}]},
            {"label": "ENGINEER", "pattern": [{'DEP': 'amod'},{'DEP': 'compound'},{'LOWER': 'engineer'}]},
            {"label": "ENGINEER", "pattern": [{'LOWER': 'engineer'},{'DEP': 'prep'},{'DEP': 'det'},
                                              {'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "ENGINEER", "pattern":  [{'DEP': 'amod'},{'LOWER': 'engineer'}]},
            {"label": "ENGINEER", "pattern": [{'DEP': 'compound'},{'LOWER': 'engineers'}]},
            {"label": "ENGINEER", "pattern": [{'LOWER': 'engineers'},{'DEP': 'prep'},{'DEP': 'amod'},{'POS': 'NOUN'},
                                              {'DEP': 'prep'},{'DEP': 'amod'},{'POS': 'NOUN'}]},
            {"label": "ENGINEER", "pattern": [{'LOWER': 'engineers'},{'DEP': 'prep'},{'POS': 'NOUN'},
                                              {'DEP': 'prep'},{'DEP': 'amod'},{'POS': 'NOUN'}]},
            {"label": "ENGINEER", "pattern": [{'LOWER': 'engineers'},{'DEP': 'prep'},{'POS': 'NOUN'},
                                              {'DEP': 'prep'},{'POS': 'NOUN'}]},
            {"label": "ENGINEER", "pattern": [{'DEP': 'amod'},{'DEP': 'compound'},{'LOWER': 'engineers'}]},
            {"label": "ENGINEER", "pattern": [{'LOWER': 'engineers'},{'DEP': 'prep'},{'DEP': 'det'},
                                              {'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "ENGINEER", "pattern": [{'DEP': 'amod'},{'LOWER': 'engineers'}]},
            {"label": "SPECIALIST", "pattern": [{'DEP': 'compound'},{'LOWER': 'specialist'}]},
            {"label": "SPECIALIST", "pattern": [{'DEP': 'amod'},{'LOWER': 'specialist'}]},
            {"label": "SPECIALIST", "pattern": [{'DEP': 'advmod'},{'DEP': 'amod'},{'LOWER': 'specialist'}]},
            {"label": "SPECIALIST", "pattern": [{'LOWER': 'specialist'},{'POS': 'ADP'},{'POS': 'VERB'},
                                                {'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "SPECIALIST", "pattern": [{'LOWER': 'specialist'},{'POS': 'ADP'},{'POS': 'VERB'},
                                                {'POS': 'CCONJ'},{'POS': 'VERB'},{'DEP': 'compound'},
                                                {'POS': 'NOUN'},{'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "SPECIALIST", "pattern": [{'LOWER': 'specialist'},{'POS': 'ADP'},{'POS': 'NOUN'},
                                                {'POS': 'ADP'},{'POS': 'ADJ'},{'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "SPECIALIST", "pattern": [{'LOWER': 'specialist'},{'POS': 'ADP'},{'POS': 'ADJ'},{'POS': 'NOUN'},
                                                {'POS': 'CCONJ'},{'POS': 'NOUN'},{'POS': 'ADP'},{'POS': 'ADJ'},
                                                {'POS': 'CCONJ'},{'POS': 'ADJ'},{'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "SPECIALIST", "pattern": [{'DEP': 'amod'},{'DEP': 'compound'},{'LOWER': 'specialist'}]},
            {"label": "SPECIALIST", "pattern": [{'LOWER': 'specialist'},{'DEP': 'prep'},{'DEP': 'det'},{'POS': 'NOUN'},
                                                {'DEP': 'prep'},{'POS': 'ADJ'},{'POS': 'NOUN'}]},
            {"label": "SPECIALIST", "pattern": [{'LOWER': 'specialist'},{'DEP': 'prep'},{'DEP': 'det'},
                                                {'DEP': 'amod'},{'POS': 'NOUN'}]},
            {"label": "SPECIALIST", "pattern": [{'DEP': 'compound'},{'LOWER': 'specialists'}]},
            {"label": "SPECIALIST", "pattern": [{'DEP': 'amod'},{'LOWER': 'specialists'}]},
            {"label": "SPECIALIST", "pattern": [{'DEP': 'advmod'},{'DEP': 'amod'},{'LOWER': 'specialists'}]},
            {"label": "SPECIALIST", "pattern": [{'LOWER': 'specialists'},{'POS': 'ADP'},{'POS': 'VERB'},
                                                {'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "SPECIALIST", "pattern": [{'LOWER': 'specialists'},{'POS': 'ADP'},{'POS': 'VERB'},
                                                {'POS': 'CCONJ'},{'POS': 'VERB'},{'DEP': 'compound'},
                                                {'POS': 'NOUN'},{'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "SPECIALIST", "pattern": [{'LOWER': 'specialists'},{'POS': 'ADP'},{'POS': 'NOUN'},
                                                {'POS': 'ADP'},{'POS': 'ADJ'},{'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "SPECIALIST", "pattern": [{'LOWER': 'specialists'},{'POS': 'ADP'},{'POS': 'ADJ'},{'POS': 'NOUN'},
                                                {'POS': 'CCONJ'},{'POS': 'NOUN'},{'POS': 'ADP'},{'POS': 'ADJ'},
                                                {'POS': 'CCONJ'},{'POS': 'ADJ'},{'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "SPECIALIST", "pattern": [{'DEP': 'amod'},{'DEP': 'compound'},{'LOWER': 'specialists'}]},
            {"label": "SPECIALIST", "pattern": [{'LOWER': 'specialists'},{'DEP': 'prep'},{'DEP': 'det'},{'POS': 'NOUN'},
                                                {'DEP': 'prep'},{'POS': 'ADJ'},{'POS': 'NOUN'}]},
            {"label": "SPECIALIST", "pattern": [{'LOWER': 'specialists'},{'DEP': 'prep'},{'DEP': 'det'},
                                                {'DEP': 'amod'},{'POS': 'NOUN'}]},
            {"label": "MANAGER", "pattern": [{'DEP': 'amod'},{'LOWER': 'manager'}]},
            {"label": "MANAGER", "pattern": [{'DEP': 'compound'},{'LOWER': 'manager'}]},
            {"label": "MANAGER", "pattern": [{'DEP': 'amod'},{'DEP': 'compound'},{'LOWER': 'manager'}]},
            {"label": "MANAGER", "pattern": [{'LOWER': 'manager'},{'DEP': 'acl'},{'DEP': 'prep'},{'POS': 'NOUN'}]},
            {"label": "MANAGER", "pattern": [{'LOWER': 'manager'},{'DEP': 'prep'},{'DEP': 'amod'},
                                             {'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "MANAGER", "pattern": [{'LOWER': 'manager'},{'DEP': 'prep'},{'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "MANAGER", "pattern": [{'LOWER': 'manager'},{'DEP': 'prep'},{'DEP': 'det'},
                                             {'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "MANAGER", "pattern": [{'LOWER': 'manager'},{'DEP': 'prep'},{'DEP': 'amod'},{'POS': 'NOUN'}]},
            {"label": "MANAGER", "pattern": [{'DEP': 'compound'},{'DEP': 'compound'},{'LOWER': 'manager'}]},
            {"label": "MANAGER", "pattern": [{'DEP': 'amod'},{'LOWER': 'managers'}]},
            {"label": "MANAGER", "pattern": [{'DEP': 'compound'},{'LOWER': 'managers'}]},
            {"label": "MANAGER", "pattern": [{'DEP': 'amod'},{'DEP': 'compound'},{'LOWER': 'managers'}]},
            {"label": "MANAGER", "pattern": [{'LOWER': 'managers'},{'DEP': 'acl'},{'DEP': 'prep'},{'POS': 'NOUN'}]},
            {"label": "MANAGER", "pattern": [{'LOWER': 'managers'},{'DEP': 'prep'},{'DEP': 'amod'},
                                             {'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "MANAGER", "pattern": [{'LOWER': 'managers'},{'DEP': 'prep'},{'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "MANAGER", "pattern": [{'LOWER': 'managers'},{'DEP': 'prep'},{'DEP': 'det'},
                                             {'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "MANAGER", "pattern": [{'LOWER': 'managers'},{'DEP': 'prep'},{'DEP': 'amod'},{'POS': 'NOUN'}]},
            {"label": "MANAGER", "pattern": [{'DEP': 'compound'},{'DEP': 'compound'},{'LOWER': 'managers'}]},
            {"label": "OPERATOR", "pattern": [{'DEP': 'amod'},{'LOWER': 'operator'}]},
            {"label": "OPERATOR", "pattern": [{'DEP': 'compound'},{'LOWER': 'operator'}]},
            {"label": "OPERATOR", "pattern": [{'DEP': 'amod'},{'DEP': 'compound'},{'LOWER': 'operator'}]},
            {"label": "OPERATOR", "pattern": [{'DEP': 'compound'},{'DEP': 'compound'},{'LOWER': 'operator'}]},
            {"label": "OPERATOR", "pattern": [{'LOWER': 'operator'},{'DEP': 'prep'},{'DEP': 'amod'},
                                              {'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "OPERATOR", "pattern": [{'LOWER': 'operator'},{'DEP': 'prep'},{'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "OPERATOR", "pattern": [{'LOWER': 'operator'},{'DEP': 'prep'},{'POS': 'NOUN'}]},
            {"label": "OPERATOR", "pattern": [{'DEP': 'amod'},{'LOWER': 'operators'}]},
            {"label": "OPERATOR", "pattern": [{'DEP': 'compound'},{'LOWER': 'operators'}]},
            {"label": "OPERATOR", "pattern": [{'DEP': 'amod'},{'DEP': 'compound'},{'LOWER': 'operators'}]},
            {"label": "OPERATOR", "pattern": [{'DEP': 'compound'},{'DEP': 'compound'},{'LOWER': 'operators'}]},
            {"label": "OPERATOR", "pattern": [{'LOWER': 'operators'},{'DEP': 'prep'},{'DEP': 'amod'},
                                              {'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "OPERATOR", "pattern": [{'LOWER': 'operators'},{'DEP': 'prep'},{'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "OPERATOR", "pattern": [{'LOWER': 'operators'},{'DEP': 'prep'},{'POS': 'NOUN'}]},
            {"label": "AGENT", "pattern": [{'DEP': 'compound'},{'LOWER': 'agent'}]},
            {"label": "AGENT", "pattern": [{'DEP': 'amod'},{'LOWER': 'agent'}]},
            {"label": "AGENT", "pattern": [{'DEP': 'compound'},{'DEP': 'amod'},{'LOWER': 'agent'}]},
            {"label": "AGENT", "pattern": [{'DEP': 'amod'},{'DEP': 'compound'},{'LOWER': 'agent'}]},
            {"label": "AGENT", "pattern": [{'LOWER': 'agent'},{'DEP': 'prep'},{'POS': 'NOUN'}]},
            {"label": "AGENT", "pattern": [{'LOWER': 'agent'},{'DEP': 'prep'},{'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "AGENT", "pattern": [{'LOWER': 'agent'},{'DEP': 'prep'},{'DEP': 'amod'},
                                           {'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "AGENT", "pattern": [{'DEP': 'compound'},{'LOWER': 'agents'}]},
            {"label": "AGENT", "pattern": [{'DEP': 'amod'},{'LOWER': 'agents'}]},
            {"label": "AGENT", "pattern": [{'DEP': 'compound'},{'DEP': 'amod'},{'LOWER': 'agents'}]},
            {"label": "AGENT", "pattern": [{'DEP': 'amod'},{'DEP': 'compound'},{'LOWER': 'agents'}]},
            {"label": "AGENT", "pattern": [{'LOWER': 'agents'},{'DEP': 'prep'},{'POS': 'NOUN'}]},
            {"label": "AGENT", "pattern": [{'LOWER': 'agents'},{'DEP': 'prep'},{'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "AGENT", "pattern": [{'LOWER': 'agents'},{'DEP': 'prep'},{'DEP': 'amod'},
                                           {'DEP': 'compound'},{'POS': 'NOUN'}]},
            {"label": "SCIENTIST", "pattern": [{'DEP': 'compound'},{'LOWER': 'scientist'}]},
            {"label": "SCIENTIST", "pattern": [{'DEP': 'amod'},{'LOWER': 'scientist'}]},
            {"label": "SCIENTIST", "pattern": [{'LOWER': 'scientist'},{'DEP': 'amod'},{'DEP': 'prep'},{'POS': 'NOUN'}]},
            {"label": "SCIENTIST", "pattern": [{'LOWER': 'scientist'},{'DEP': 'cc'},{'DEP': 'conj'},
                                               {'DEP': 'amod'},{'DEP': 'prep'},{'POS': 'NOUN'}]},
            {"label": "SCIENTIST", "pattern": [{'LOWER': 'scientist'},{'DEP': 'prep'},{'DEP': 'det'},
                                               {'POS': 'NOUN'},{'DEP': 'prep'},{'DEP': 'amod'},{'POS': 'NOUN'}]},
            {"label": "SCIENTIST", "pattern": [{'LOWER': 'scientist'},{'DEP': 'prep'},{'DEP': 'det'},
                                               {'POS': 'NOUN'},{'DEP': 'prep'},{'POS': 'NOUN'}]},
            {"label": "SCIENTIST", "pattern": [{'LOWER': 'scientist'},{'DEP': 'prep'},{'DEP': 'det'},
                                               {'POS': 'NOUN'},{'DEP': 'prep'},{'POS': 'NOUN'},
                                               {'DEP': 'cc'},{'DEP': 'amod'},{'POS': 'NOUN'}]},
            {"label": "SCIENTIST", "pattern": [{'LOWER': 'scientist'},{'DEP': 'prep'},{'DEP': 'pobj'}]},
            {"label": "SCIENTIST", "pattern": [{'DEP': 'amod'},{'DEP': 'amod'},{'LOWER': 'scientist'}]},
            {"label": "SCIENTIST", "pattern": [{'DEP': 'compound'},{'LOWER': 'scientists'}]},
            {"label": "SCIENTIST", "pattern": [{'DEP': 'amod'},{'LOWER': 'scientists'}]},
            {"label": "SCIENTIST", "pattern": [{'LOWER': 'scientists'},{'DEP': 'amod'},{'DEP': 'prep'},{'POS': 'NOUN'}]},
            {"label": "SCIENTIST", "pattern": [{'LOWER': 'scientists'},{'DEP': 'cc'},{'DEP': 'conj'},
                                               {'DEP': 'amod'},{'DEP': 'prep'},{'POS': 'NOUN'}]},
            {"label": "SCIENTIST", "pattern": [{'LOWER': 'scientists'},{'DEP': 'prep'},{'DEP': 'det'},
                                               {'POS': 'NOUN'},{'DEP': 'prep'},{'DEP': 'amod'},{'POS': 'NOUN'}]},
            {"label": "SCIENTIST", "pattern": [{'LOWER': 'scientists'},{'DEP': 'prep'},{'DEP': 'det'},
                                               {'POS': 'NOUN'},{'DEP': 'prep'},{'POS': 'NOUN'}]},
            {"label": "SCIENTIST", "pattern": [{'LOWER': 'scientists'},{'DEP': 'prep'},{'DEP': 'det'},
                                               {'POS': 'NOUN'},{'DEP': 'prep'},{'POS': 'NOUN'},
                                               {'DEP': 'cc'},{'DEP': 'amod'},{'POS': 'NOUN'}]},
            {"label": "SCIENTIST", "pattern": [{'LOWER': 'scientists'},{'DEP': 'prep'},{'DEP': 'pobj'}]},
            {"label": "SCIENTIST", "pattern": [{'DEP': 'amod'},{'DEP': 'amod'},{'LOWER': 'scientists'}]}]
    ruler.add_patterns(patterns)
    nlp.add_pipe(ruler)
    doc = nlp(text)
    colors = {"ENGINEER": "linear-gradient(90deg, #94d5e2, #94d5e2)",
          "SPECIALIST": "linear-gradient(90deg, #fba8f4, #fba8f4)",
          "MANAGER":"linear-gradient(90deg, #c29ee8, #c29ee8)",
          "OPERATOR":"linear-gradient(90deg, #9ee8a8, #9ee8a8)",
          "AGENT":"linear-gradient(90deg, #ebe596, #ebe596)",
          "SCIENTIST":"linear-gradient(90deg, #eec68d, #eec68d)"}
    options = {"ents": ["ENGINEER", "SPECIALIST", "MANAGER", "OPERATOR", "AGENT", "SCIENTIST"], "colors": colors}
    html = displacy.render(doc, style="ent", options={"ents": labels, "colors": colors})

    # Newlines seem to mess with the rendering
    html = html.replace("\n", " ")
    st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)

    # Download csv file
    st.sidebar.subheader("Compound Job Titles Table")
    entity = []
    label = []
    lista = labels
    for ent in doc.ents:
    	if ent.label_ in lista: 
    		entity.append(ent.text)
    		label.append(ent.label_)
    dataframe = pd.DataFrame({'entity' : entity, 'label' : label})
    csv = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="prova.csv">Download CSV File</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)