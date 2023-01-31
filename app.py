import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network


st.set_page_config(page_title='The Real-World Evidence Lab')
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)


# Read dataset (CSV)
df_interact = pd.read_csv("D:\\Study\\FDA_ADE\\app\\AE Counts.csv")

# Set header title
st.title('Serious Adverse Drug Events in Inflammatory bowel disease (IBD)')

genre = st.radio("Select Network View",('Drug Class', 'Drug','AdverseEvent'))
if genre == 'Drug Class':
    # Define list of selection options and sort alphabetically
    node_list = ['Anti-TNF','JAK-inhibitor','Anti-IL-12/23','Anti-integrin' ]
    node_list.sort()

    # Implement multiselect dropdown menu for option selection (returns a list)
    selected_nodes = st.multiselect('Select steroid-sparing drug class to visualize', node_list)

    # Set info message on initial site load
    if len(selected_nodes) == 0:
        st.text('Choose at least 1 steroid-sparing drug class to get started')

    # Create network graph when user selects >= 1 item
    else:
        df_select = df_interact.loc[df_interact['Source'].isin(selected_nodes) | \
                                df_interact['Drugclass'].isin(selected_nodes) | \
                                df_interact['Weight'].isin(selected_nodes)]
        df_select = df_select.reset_index(drop=True)

        # Create networkx graph object from pandas dataframe
        got_net = Network( height="1500px",width="100%",bgcolor="#ffffff")
        
        # set the physics layout of the network
        got_net.barnes_hut(central_gravity=0.3, spring_length=250, spring_strength=0.006, damping=0.09, overlap=0)
        sources = df_select['Source']
        targets = df_select['Drugclass']
        weights = df_select['Weight']

        edge_data = zip(sources, targets, weights)

        for e in edge_data:
                src = e[0]
                dst = e[1]
                w = e[2]

                got_net.add_node(src, src, title=src)
                if dst in (node_list):
                  got_net.add_node(dst, dst, title=dst,color='#FF5C5C')
                else:
                  got_net.add_node(dst, dst, title=dst)
                got_net.add_edge(src, dst, value=w)

        neighbor_map = got_net.get_adj_list()
        
        # add neighbor data to node hover data
        for node in got_net.nodes:
                node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
                node["value"] = len(neighbor_map[node["id"]])

    # Generate network with specific layout settings
        got_net.repulsion(node_distance=420, central_gravity=0.33,
                       spring_length=110, spring_strength=0.10,
                       damping=0.95)
        #got_net.show_buttons(filter_=['physics'])
        # Save and read graph as HTML file (on Streamlit Sharing)
        try:
            path = '/tmp'
            got_net.save_graph(f'{path}/IBD_ADE_interactions_network_subset_repulsion.html')
            HtmlFile = open(f'{path}/IBD_ADE_interactions_network_subset_repulsion.html', 'r', encoding='utf-8')

        # Save and read graph as HTML file (locally)
        except:
            path = 'html_files'
            got_net.save_graph(f'{path}/IBD_ADE_interactions_network_subset_repulsion.html')
            HtmlFile = open(f'{path}/IBD_ADE_interactions_network_subset_repulsion.html', 'r', encoding='utf-8')
 
        # Load HTML file in HTML component for display on Streamlit page
        components.html(HtmlFile.read(), height=1500, width=1028)
        
elif  genre == 'Drug':
    # Define list of selection options and sort alphabetically
    node_list = ['Infliximab' , 'Adalimumab' , 'Ustekinumab' , 'Vedolizumab' , 'Tofacitnib' , 'Certolizumab' , 'Golimumab' , 'Etanercept' ]
    node_list.sort()

    # Implement multiselect dropdown menu for option selection (returns a list)
    selected_nodes = st.multiselect('Select steroid-sparing immunosuppressant/s to visualize', node_list)

    # Set info message on initial site load
    if len(selected_nodes) == 0:
        st.text('Choose at least 1 steroid-sparing immunosuppressant to get started')

    # Create network graph when user selects >= 1 item
    else:
        df_select = df_interact.loc[df_interact['Source'].isin(selected_nodes) | \
                                df_interact['Target'].isin(selected_nodes) | \
                                df_interact['Weight'].isin(selected_nodes)]
        df_select = df_select.reset_index(drop=True)

        # Create networkx graph object from pandas dataframe
        got_net = Network( height="1500px",width="100%",bgcolor="#ffffff")

        # set the physics layout of the network
        got_net.barnes_hut(central_gravity=0.3, spring_length=250, spring_strength=0.006, damping=0.09, overlap=0)
        sources = df_select['Source']
        targets = df_select['Target']
        weights = df_select['Weight']

        edge_data = zip(sources, targets, weights)

        for e in edge_data:
                src = e[0]
                dst = e[1]
                w = e[2]

                got_net.add_node(src, src, title=src)
                if dst in (node_list):
                  got_net.add_node(dst, dst, title=dst,color='#FF5C5C')
                else:
                  got_net.add_node(dst, dst, title=dst)
                got_net.add_edge(src, dst, value=w)

        neighbor_map = got_net.get_adj_list()

        # add neighbor data to node hover data
        for node in got_net.nodes:
                node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
                node["value"] = len(neighbor_map[node["id"]])

    # Generate network with specific layout settings
        got_net.repulsion(node_distance=420, central_gravity=0.33,
                       spring_length=110, spring_strength=0.10,
                       damping=0.95)
        #got_net.show_buttons(filter_=['physics'])
        # Save and read graph as HTML file (on Streamlit Sharing)
        try:
            path = '/tmp'
            got_net.save_graph(f'{path}/IBD_ADE_interactions_network_subset_repulsion.html')
            HtmlFile = open(f'{path}/IBD_ADE_interactions_network_subset_repulsion.html', 'r', encoding='utf-8')

        # Save and read graph as HTML file (locally)
        except:
            path = 'html_files'
            got_net.save_graph(f'{path}/IBD_ADE_interactions_network_subset_repulsion.html')
            HtmlFile = open(f'{path}/IBD_ADE_interactions_network_subset_repulsion.html', 'r', encoding='utf-8')

        # Load HTML file in HTML component for display on Streamlit page
        components.html(HtmlFile.read(), height=1500, width=1028)
elif  genre == 'AdverseEvent':
    # Define list of selection options and sort alphabetically
    node_list = ['Abdominal abscess','Abdominal distension','Acute kidney injury','Adrenal insufficiency','Anastomotic leak','Appendicitis','Arrhythmia','Arterial injury','Arthralgia','Arthritis bacterial','Asthenia','Atypical pneumonia','Bile duct stone','Blood electrolytes abnormal','Bradycardia','Cardiomyopathy','Cellulitis','Cerebrovascular accident','Chest pain','Chills','Cholangitis','Clostridium difficile colitis','Confusional state','Constipation','Cough','Deep vein thrombosis','Dehydration','Diverticulitis','Dyspnoea','Encephalitis','Endocarditis','Fatigue','Gastroenteritis aeromonas','Gastroenteritis norovirus','Gastrointestinal bacterial overgrowth','Gastrointestinal haemorrhage','Hepatitis','Herpes virus infection','Herpes zoster','Hip fracture','HIV infection','Hyperthyroidism','Hypokalaemia','Hypotension','Infection','Inflammation','Internal hernia','Intestinal obstruction','Intestinal perforation','Intestinal resection','Intestinal stenosis','Intussusception','Klebsiella bacteraemia','Large intestine perforation','Leukocytosis','Lymphadenopathy','Malnutrition','Mass','Meningitis viral','Metabolic encephalopathy','Migraine','Muscle spasms','Myocarditis','Nausea','Nephrotic syndrome','Oedema','Pancreatitis','Perforation','Perineal pain','Peritonitis','Pharyngitis','Pleural effusion','Pneumonia','Pneumonia cytomegaloviral','Presyncope','Psychotic disorder','Pulmonary tuberculosis','Pyoderma gangrenosum','Pyrexia','Rash','Renal tubular necrosis','Rhabdomyolysis','Salmonellosis','Sarcoma','Septic shock','Shock haemorrhagic','Sinusitis','Small intestinal obstruction','Stridor','Systemic candida','Tachycardia','Tenosynovitis','Thrombocytopenia','Uveitis','Viraemia','Viral infection','Vomiting' ]
    node_list.sort()
    node_list1 = ['Infliximab' , 'Adalimumab' , 'Ustekinumab' , 'Vedolizumab' , 'Tofacitnib' , 'Certolizumab' , 'Golimumab' , 'Etanercept' ]
    # Implement multiselect dropdown menu for option selection (returns a list)
    selected_nodes = st.multiselect('Select Adverse event to visualize', node_list)

    # Set info message on initial site load
    if len(selected_nodes) == 0:
        st.text('Choose at least 1 Adverse event to get started')

    # Create network graph when user selects >= 1 item
    else:
        df_select = df_interact.loc[df_interact['Source'].isin(selected_nodes) | \
                                df_interact['Target'].isin(selected_nodes) | \
                                df_interact['Weight'].isin(selected_nodes)]
        df_select = df_select.reset_index(drop=True)

        # Create networkx graph object from pandas dataframe
        got_net = Network( height="1500px",width="100%",bgcolor="#ffffff")

        # set the physics layout of the network
        got_net.barnes_hut(spring_strength=0.006)
        sources = df_select['Source']
        targets = df_select['Target']
        weights = df_select['Weight']

        edge_data = zip(sources, targets, weights)

        for e in edge_data:
                src = e[0]
                dst = e[1]
                w = e[2]

                got_net.add_node(src, src, title=src)
                if dst in (node_list1):
                  got_net.add_node(dst, dst, title=dst,color='#FF5C5C')
                else:
                  got_net.add_node(dst, dst, title=dst)
                got_net.add_edge(src, dst, value=w)

        neighbor_map = got_net.get_adj_list()

        # add neighbor data to node hover data
        for node in got_net.nodes:
                node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
                node["value"] = len(neighbor_map[node["id"]])

    # Generate network with specific layout settings
        got_net.repulsion(node_distance=420, central_gravity=0.33,
                       spring_length=110, spring_strength=0.10,
                       damping=0.95)
        #got_net.show_buttons(filter_=['physics'])
        
        # Save and read graph as HTML file (on Streamlit Sharing)
        try:
            path = '/tmp'
            got_net.save_graph(f'{path}/IBD_ADE_interactions_network_subset_repulsion.html')
            HtmlFile = open(f'{path}/IBD_ADE_interactions_network_subset_repulsion.html', 'r', encoding='utf-8')

        # Save and read graph as HTML file (locally)
        except:
            path = 'html_files'
            got_net.save_graph(f'{path}/IBD_ADE_interactions_network_subset_repulsion.html')
            HtmlFile = open(f'{path}/IBD_ADE_interactions_network_subset_repulsion.html', 'r', encoding='utf-8')

        # Load HTML file in HTML component for display on Streamlit page
        components.html(HtmlFile.read(), height=1500, width=1028)