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

#length = 150,
#width = 75,
#height = 60,
#angle = 45

def make_cradle_controls():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cradle_length = st.number_input(
            "length",
            key="cradle_length",
            min_value=1.0, 
            max_value=400.0, 
            value=150.0,
            step=1.0
        )
    with col2:
        cradle_width = st.number_input(
            "width",
            key="cradle_width",
            min_value=1.0, 
            max_value=400.0, 
            value=75.0,
            step=1.0
        )
    with col3:
        cradle_height = st.number_input(
            "height",
            key="cradle_height",
            min_value=1.0, 
            max_value=200.0, 
            value=63.0,
            step=1.0
        )
    with col4:
        cradle_angle = st.number_input(
            "angle",
            key="cradle_angle",
            min_value=-360.0, 
            max_value=360.0, 
            value=45.0,
            step=1.0
        )

    return {
        'cradle_length':cradle_length,
        'cradle_width':cradle_width,
        'cradle_height':cradle_height,
        'cradle_angle':cradle_angle
    }