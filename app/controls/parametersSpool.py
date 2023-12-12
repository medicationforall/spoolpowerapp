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

def make_spool_controls():
    col1, col2, col3 = st.columns(3)
    with col1:
        spool_height = st.number_input(
            "height",
            key="spool_height",
            help='"height" of the spool turned on its side',
            min_value=10.0, 
            max_value=200.0, 
            value=60.0 ,
            step=1.0
        )
    with col2:
        spool_radius = st.number_input(
            "radius",
            key="spool_radius",
            help='Outside of the spool radius',
            min_value=10.0, 
            max_value=400.0, 
            value=97.5, 
            step=1.0
        )
    with col3:
        spool_cut_radius = st.number_input(
            "cut radius",
            key="spool_cut_radius",
            help='Inside of the spool radius',
            min_value=5.0, 
            max_value=390.0,  
            value=36.5, 
            step=1.0
        )

    col1, col2, col3 = st.columns(3)    
    with col1:
        spool_wall_width = st.number_input(
            "wall width",
            key="spool_wall_width",
            min_value=1.0, 
            max_value=100.0, 
            value=4.0 ,
            step=1.0
        )
    with col2:
        spool_internal_wall_width = st.number_input(
            "internal width",
            key="spool_internal_wall_width",
            min_value=1.0, 
            max_value=100.0, 
            value=3.0,
            step=1.0
        )
    with col3:
        spool_internal_z_translate = st.number_input(
            "z translate",
            key="spool_internal_z_translate",
            min_value=-100.0, 
            max_value=100.0, 
            value=0.0,
            step=1.0
        )


    return {
        'spool_height':spool_height,
        'spool_radius':spool_radius,
        'spool_cut_radius':spool_cut_radius,
        'spool_wall_width':spool_wall_width,
        'spool_internal_wall_width':spool_internal_wall_width,
        'spool_internal_z_translate':spool_internal_z_translate
    }