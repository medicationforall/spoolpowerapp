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

import streamlit as st

#start_angle = 0,
#end_angle = 360,
#rotate_solid = True,

#count = 17,
#clad_width = 33,
#clad_height = 5,
#clad_inset = 5

def make_cladding_controls():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        cladding_count = st.number_input(
            "count",
            key="cladding_count",
            help="Number of panels around the spool radius",
            min_value=1, 
            max_value=100, 
            value=17,
            step=1
        )
    with col2:
        clading_width = st.number_input(
            "Clad Width",
            key="clading_width",
            help="Width of each panel",
            min_value=1.0, 
            max_value=400.0, 
            value=33.0,
            step=1.0
        )
    with col3:
        cladding_height = st.number_input(
            "Clad Height",
            key="cladding_height",
            help="Height of each panel",
            min_value=1.0, 
            max_value=100.0, 
            value=5.0,
            step=1.0
        )
    with col4:
        cladding_inset = st.number_input(
            "Clad Inset",
            key="cladding_inset",
            help="Inset into the spool",
            min_value=1.0, 
            max_value=400.0, 
            value=5.0,
            step=1.0
        )

    col1, col2, col3 = st.columns(3)
    with col1:
        cladding_seed = st.text_input(
            "Seed",
            key="cladding_seed",
            help="Determines the random pattern",
            value="power!"
        )
    with col2:
        st.warning('Cladding Type is a performance drain, set this last!', icon="⚠️")
    with col3:
        cladding_type = st.selectbox(
            "Cladding Type", 
            ["plain", "Greebled","Greebled Unique"], 
            key="cladding_type",
            help="This is a performance drain, set this last!"
        )


    

    return {
        'cladding_count':cladding_count,
        'clading_width':clading_width,
        'cladding_height':cladding_height,
        'cladding_inset':cladding_inset,
        'cladding_type':cladding_type,
        'cladding_seed':cladding_seed
    }