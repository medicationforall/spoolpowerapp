import streamlit as st

def __make_scene(models):
    unions = ''

    scene_begin = f'''
scene = (
    cq.Workplane("XY")
    .union(model)
'''

    for index, params in enumerate(models):
        if params["layer_display"]:
            scene_begin = scene_begin + f'''    .union(model_{index})
'''
    return scene_begin +unions+ ')'

def __make_layer_code(index, parameters):
    base_width = parameters['base_width']
    base_height = parameters['base_height']
    inset_width = parameters['inset_width']
    inset_height = parameters['inset_height']
    middle_width = parameters['middle_width']
    middle_height = parameters['middle_height']
    top_width = parameters['top_width']
    top_height = parameters['top_height']
    height = parameters['height']
    faces = parameters['faces']
    intersect = parameters['intersect']
    layer_rotate = parameters['layer_rotate']
    layer_name = parameters['layer_name']

    layer_string = f'''
# {layer_name}
model_{index} = obelisk(
        base_width={base_width},
        base_height={base_height},
        inset_width={inset_width},
        inset_height={inset_height},
        mid_width={middle_width},
        mid_height={middle_height},
        top_width={top_width},
        top_height={top_height},
        height={height},
        faces={faces},
        intersect={intersect}
    ).rotate((0,0,1),(0,0,0),{layer_rotate})

'''
    return layer_string

def make_code_view(parameters):
    cladding_type = parameters['cladding_type']
    cladding_types = cladding_types = {
        "plain":"SpoolCladding", 
        "Greebled":"SpoolCladdingGreebled", 
        "Greebled Unique":"SpoolCladdingGreebledUnique"
    }
    cladding_types_class= cladding_types[cladding_type]

    cladding_seed = parameters["cladding_seed"]
    export_type = parameters['export_type']
    spool_height = parameters["spool_height"]
    spool_radius = parameters["spool_radius"]
    spool_cut_radius = parameters["spool_cut_radius"]
    spool_wall_width = parameters["spool_wall_width"]
    spool_internal_wall_width = parameters["spool_internal_wall_width"]
    spool_internal_z_translate = parameters["spool_internal_z_translate"]
    cladding_count = parameters["cladding_count"]
    clading_width = parameters["clading_width"]
    cladding_height = parameters["cladding_height"]
    cladding_inset = parameters["cladding_inset"]

    cradle_length = parameters["cradle_length"]
    cradle_width = parameters["cradle_width"]
    cradle_height = parameters["cradle_height"]
    cradle_angle = parameters["cradle_angle"]

    code_string = f'''
import cadquery as cq
from cqspoolterrain import {cladding_types_class}, PowerStation

bp_power = PowerStation()

bp_power.bp_spool.height = {spool_height}
bp_power.bp_spool.radius = {spool_radius}
bp_power.bp_spool.cut_radius = {spool_cut_radius}
bp_power.bp_spool.wall_width = {spool_wall_width}
bp_power.bp_spool.internal_wall_width = {spool_internal_wall_width}
bp_power.bp_spool.internal_z_translate = {spool_internal_z_translate}

bp_power.bp_cladding = {cladding_types_class}()
bp_power.bp_cladding.seed = '{cladding_seed}'

bp_power.render_spool = True
bp_power.render_cladding = True
bp_power.bp_cladding.count = {cladding_count}
bp_power.bp_cladding.clad_width = {clading_width}
bp_power.bp_cladding.clad_height = {cladding_height}
bp_power.bp_cladding.clad_inset = {cladding_inset}

bp_power.render_cradle = True
bp_power.bp_cradle.length = {cradle_length}
bp_power.bp_cradle.width = {cradle_width}
bp_power.bp_cradle.height = {cradle_height}
bp_power.bp_cradle.angle = {cradle_angle}

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

show_object(power)
#cq.exporters.export(spool,'model_spool.{export_type}')
#cq.exporters.export(cradle_scene,'model_cradle.{export_type}')
#cq.exporters.export(cladding_scene,'model_cladding.{export_type}')
#cq.exporters.export(power,'model_combined.{export_type}')
'''
    
    st.code(
    f'{code_string}',
    language="python", 
    line_numbers=True
)