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
import time
from datetime import datetime, date
from pathlib import Path
import cadquery as cq
from cqspoolterrain import Spool, Cradle, SpoolCladding, SpoolCladdingGreebled, SpoolCladdingGreebledUnique, PowerStation
from controls import (
    make_sidebar, 
    make_parameter_controls, 
    make_parameter_controls_layers,
    make_parameter_point,
    make_model_controls_cladding,
    make_model_controls_combined,
    make_model_controls_cradle,
    make_model_controls_spool,
    make_file_controls,
    make_code_view
)

def __make_tabs():
    tab_parameters, tab_base, tab_inset, tab_middle, tab_top, tab_layer, tab_file, tab_code = st.tabs([
        "Model",
        "Base",
        "Inset",
        "Middle",
        "Top", 
        "Layers",
        "File",
        "Code",
        ])
    with tab_parameters:
        model_parameters = make_parameter_controls()
    with tab_base:
        base = make_parameter_point('base', 3.0, 30.0)
    with tab_inset:
        inset = make_parameter_point('inset', 5.0, 15.0)
    with tab_middle:
        middle = make_parameter_point('middle', 15.0, 30.0)
    with tab_top:
        top = make_parameter_point('top', 70.0, 15.0)
    with tab_layer:
        add_button, dupe = make_parameter_controls_layers()
    with tab_file:
        file_controls = make_file_controls()
 
    #combine tab parameter into one dictionary
    parameters = model_parameters | base | inset | middle | top | dupe

    with tab_code:
        make_code_view(parameters, st.session_state['models'])

    return add_button, parameters, file_controls

def __make_model_tabs(model_parameters, file_controls):
    spool_tab, cradle_tab, cladding_tab, combined_tab = st.tabs([
    "Spool",
    "Cradle",
    "Cladding",
    "Combined"
    ])

    with spool_tab:
        __model_controls(model_parameters, file_controls, "Spool", make_model_controls_spool)
    with cradle_tab:
        __model_controls(model_parameters, file_controls, "Cradle", make_model_controls_cradle)
    with cladding_tab:
        __model_controls(model_parameters, file_controls, "Cladding", make_model_controls_cladding)
    with combined_tab:
        __model_controls(model_parameters, file_controls, "Combined", make_model_controls_combined)

def __initialize_session():
    if 'models' not in st.session_state:
        st.session_state['models'] = []

    if "session_id" not in st.session_state:
        st.session_state['session_id'] = uuid4()


def __model_controls(model_parameters, file_controls, key, callback):
    col1, col2, col3 = st.columns(3)
    with col1:
        generate_button = st.button(f'Generate {key} Model')
    with col2:
        color1 = st.color_picker(f'{key} Model Color', '#E06600', label_visibility="collapsed")
    with col3:
        render = st.selectbox(f"{key} Render", ["material", "wireframe"], label_visibility="collapsed")

    callback(
        model_parameters,
        color1,
        render,
        file_controls
    )

def __handle_add_button_click(add_model_layer_button, model_parameters):
    if add_model_layer_button:
        # fix layer name dupes
        if len(st.session_state['models']) > 0:
            for model in st.session_state['models']:
                if model_parameters['layer_name']==model['layer_name']:
                    model_parameters['layer_name'] += " copy"

        st.session_state['models'].append(model_parameters)
        st.experimental_rerun()

def __generate_model(parameters, file_controls):
    bp_power = PowerStation()

    #bp_power.bp_cladding = SpoolCladdingGreebledUnique()
    bp_power.bp_cladding.seed="uniquePanels"

    bp_power.render_spool = True
    bp_power.render_cladding = True
    bp_power.render_cradle = True
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

    export_type = file_controls['type']
    session_id = st.session_state['session_id']

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
    # main tabs
    add_model_layer_button, model_parameters, file_controls = __make_tabs()
    st.divider()
    with st.spinner('Generating Model..'):
        __generate_model(model_parameters, file_controls)
        __make_model_tabs(model_parameters, file_controls)
        #__model_controls(model_parameters, file_controls)
        __handle_add_button_click(add_model_layer_button, model_parameters)


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
        page_title="CadQuery Obelisk Generator",
        page_icon="🧊"
    )
    __initialize_session()
    __make_app()
    make_sidebar()
    __clean_up_static_files()