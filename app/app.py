# Copyright 2023 James Adams
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#--------------------  

import streamlit as st
from uuid import uuid4
import glob
from datetime import datetime
from pathlib import Path
import cadquery as cq
from cqspoolterrain import SpoolCladding, SpoolCladdingGreebled, SpoolCladdingGreebledUnique, PowerStation
from controls import (
    make_sidebar, 
    make_spool_controls,
    make_cradle_controls,
    make_cladding_controls,
    make_model_controls_cladding,
    make_model_controls_combined,
    make_model_controls_cradle,
    make_model_controls_spool,
    make_code_view
)

def __make_tabs():
    power_tab,spool_tab, cradle_tab, cladding_tab, tab_code = st.tabs([
        "Power Station",
        "Spool",
        "Cradle",
        "Cladding",
        "Code",
        ])
    with power_tab:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            generate_button = st.button(f'Generate Model')
        with col2:
            export_type = st.selectbox("File type",('stl','step'), key="export_type", label_visibility="collapsed")
        with col3:
            color1 = st.color_picker(f'Model Color', '#E06600', label_visibility="collapsed", key="model_color")
        with col4:
            render = st.selectbox(f"Render", ["material", "wireframe"], label_visibility="collapsed", key="model_render")

        make_model_controls_combined(
            color1,
            render,
            export_type
        )
    with spool_tab:
        spool_parameters = make_spool_controls()

        make_model_controls_spool(
            color1,
            render,
            export_type
        )
    with cradle_tab:
        cradle_parameters = make_cradle_controls()

        make_model_controls_cradle(
            color1,
            render,
            export_type
        )
    with cladding_tab:
        cladding_parameters = make_cladding_controls()

        make_model_controls_cladding(
            color1,
            render,
            export_type
        )


    #combine tab parameter into one dictionary
    parameters = spool_parameters | cradle_parameters | cladding_parameters
    parameters['export_type'] = export_type

    with tab_code:
        make_code_view(parameters)

    return parameters

def __initialize_session():
    if 'init' not in st.session_state:
        st.session_state['init'] = True

    if "session_id" not in st.session_state:
        st.session_state['session_id'] = uuid4()

def __generate_model(parameters):
    export_type = parameters['export_type']
    session_id = st.session_state['session_id']

    cladding_type_param = parameters["cladding_type"]
    cladding_type = SpoolCladding
    cladding_types = {
        "plain":SpoolCladding, 
        "Greebled":SpoolCladdingGreebled, 
        "Greebled Unique":SpoolCladdingGreebledUnique
    }

    if cladding_type_param in cladding_types:
        cladding_type = cladding_types[cladding_type_param]
    else:
        raise Exception(f"Uncrecognized cladding type {cladding_type_param}")

    bp_power = PowerStation()

    bp_power.bp_spool.height = parameters["spool_height"]
    bp_power.bp_spool.radius = parameters["spool_radius"]
    bp_power.bp_spool.cut_radius = parameters["spool_cut_radius"]
    bp_power.bp_spool.wall_width = parameters["spool_wall_width"]
    bp_power.bp_spool.internal_wall_width = parameters["spool_internal_wall_width"]
    bp_power.bp_spool.internal_z_translate = parameters["spool_internal_z_translate"]

    bp_power.bp_cladding = cladding_type()
    bp_power.bp_cladding.seed=parameters["cladding_seed"]

    bp_power.render_spool = True
    bp_power.render_cladding = True
    bp_power.bp_cladding.count = parameters["cladding_count"]
    bp_power.bp_cladding.clad_width = parameters["clading_width"]
    bp_power.bp_cladding.clad_height = parameters["cladding_height"]
    bp_power.bp_cladding.clad_inset = parameters["cladding_inset"]

    bp_power.render_cradle = True
    bp_power.bp_cradle.length = parameters["cradle_length"]
    bp_power.bp_cradle.width = parameters["cradle_width"]
    bp_power.bp_cradle.height = parameters["cradle_height"]
    bp_power.bp_cradle.angle = parameters["cradle_angle"]

    bp_power.render_stairs = False
    bp_power.render_control = False
    bp_power.render_walkway = False
    bp_power.render_ladder = False

    bp_power.bp_walk.render_rails = True
    bp_power.bp_walk.rail_width = 4
    bp_power.bp_walk.rail_height = 20
    bp_power.bp_walk.rail_chamfer = 10

    bp_power.bp_walk.render_rail_slots = True
    bp_power.bp_walk.rail_slot_length = 6
    bp_power.bp_walk.rail_slot_top_padding = 6
    bp_power.bp_walk.rail_slot_length_offset = 4
    bp_power.bp_walk.rail_slots_end_margin = 8
    bp_power.bp_walk.rail_slot_pointed_inner_height = 7
    bp_power.bp_walk.rail_slot_type = 'box'

    bp_power.make()
    power = bp_power.build()
    spool = bp_power.bp_spool.build()

    cradle_scene = bp_power.bp_cradle.build()
    cladding_scene = bp_power.build_cladding()

    #create the model file for downloading
    EXPORT_NAME_SPOOL = 'model_spool'
    cq.exporters.export(spool,f'{EXPORT_NAME_SPOOL}.{export_type}')
    cq.exporters.export(spool,'app/static/'+f'{EXPORT_NAME_SPOOL}_{session_id}.stl')

    EXPORT_NAME_CRADLE = 'model_cradle'
    cq.exporters.export(cradle_scene,f'{EXPORT_NAME_CRADLE}.{export_type}')
    cq.exporters.export(cradle_scene,'app/static/'+f'{EXPORT_NAME_CRADLE}_{session_id}.stl')

    EXPORT_NAME_CLADDING = 'model_cladding'
    cq.exporters.export(cladding_scene,f'{EXPORT_NAME_CLADDING}.{export_type}')
    cq.exporters.export(cladding_scene,'app/static/'+f'{EXPORT_NAME_CLADDING}_{session_id}.stl')

    EXPORT_NAME_COMBINED = 'model_combined'
    cq.exporters.export(power,f'{EXPORT_NAME_COMBINED}.{export_type}')
    cq.exporters.export(power,'app/static/'+f'{EXPORT_NAME_COMBINED}_{session_id}.stl')


def __make_app():
    #st.markdown("""
    #    <style>
    #           .block-container {
    ##                padding-top: 1rem;
    #            }
    #    </style>
    #    """, unsafe_allow_html=True)

    if st.session_state['init']:
        with st.spinner('Starting Application..'):
            model_parameters = {
                'spool_height': 60.0, 
                'spool_radius': 97.5, 
                'spool_cut_radius': 36.5, 
                'spool_wall_width': 4.0, 
                'spool_internal_wall_width': 3.0, 
                'spool_internal_z_translate': 0.0, 
                'cradle_length': 150.0, 
                'cradle_width': 75.0, 
                'cradle_height': 63.0, 
                'cradle_angle': 45.0, 
                'cladding_type':'plain',
                'cladding_seed':'power!',
                'cladding_count': 17, 
                'clading_width': 33.0, 
                'cladding_height': 5.0, 
                'cladding_inset': 5.0,
                'export_type':'stl'
            }

            __generate_model(model_parameters)
            model_parameters = __make_tabs()
            st.session_state['init'] = False
    else:
        with st.spinner('Generating Model..'):
            __generate_model(st.session_state)
            model_parameters = __make_tabs()
            
    #st.write(st.session_state)


def __clean_up_static_files():
    files = glob.glob("app/static/model_*.stl")
    today = datetime.today()
    #print(files)
    for file_name in files:
        file_path = Path(file_name)
        modified = file_path.stat().st_mtime
        modified_date = datetime.fromtimestamp(modified)
        delta = today - modified_date
        #print('total seconds '+str(delta.total_seconds()))
        if delta.total_seconds() > 1200: # 20 minutes
            #print('removing '+file_name)
            file_path.unlink()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Spool Power Generator",
        page_icon="🧊"
    )
    __initialize_session()
    __make_app()
    make_sidebar()
    __clean_up_static_files()