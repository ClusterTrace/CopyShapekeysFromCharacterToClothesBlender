# Programmer: ClusterTrace
# Date: April 11, 2023
# Purpose: Creates a rough copy of shapekeys for clothes by coping the new shape they are in from a surface deform modifier

# Notes: 
#-Requires two objects be selected, with the second/active one being the "clothing" and first the "character"
#-To function correctly the "clothing" needs a surface deform modifer that is bound to the "character"
#-Remember to unbind or remove the surface deform operator later

import bpy

context = bpy.context
scene = context.scene

clothes = context.active_object # gets the clothes, aka the active selected object
#character = bpy.context.selected_objects[0] # DOESN'T WORK: selected objects is in alphabetical order, so number doesn't represent order selected
for i in bpy.context.selected_objects: # grabs character by grabbing whatever isn't the clothes
    if i != clothes:
        character = i

#character.shape_key_clear() # doesn't work, as this version is apprently used as a duplicate shape_key_remove command, but would work if used in bpy.ops version
# As a result, I made my own function for resetting shape key wieghts for an object
def resetShapeKeyWeights(obj):
    if (None != obj.data.shape_keys): # prevents fault from no shapekey data
        shapeKeys = obj.data.shape_keys.key_blocks.keys() # gets shapeKeys
        for i in shapeKeys: # loop through each shapekey on character
            obj.data.shape_keys.key_blocks[i].value = 0

# cannot apparently apply as a shape key without use bpy.ops or operators, so I made a function that uses context overrides to prevent weird selection management       
def saveSurfaceDeformAsShapeKey(obj):
    override = bpy.context.copy()
    override["selected_objects"] = context.scene.objects[obj.name]
    with bpy.context.temp_override(**override):
        bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=True, modifier="SurfaceDeform")




if (clothes.data.shape_keys == None): # adds Basis shapekey if it doesn't have one
    clothes.shape_key_add(name = "Basis")

resetShapeKeyWeights(clothes)

shapeKeys = character.data.shape_keys.key_blocks.keys() # gets shapeKeys
for i in shapeKeys: # loop through each shapekey on character
    # save new shape as a shapekey for clothes named the same as it is on character
    if i != "Basis":
        resetShapeKeyWeights(character)
        character.data.shape_keys.key_blocks[i].value = 1
        saveSurfaceDeformAsShapeKey(clothes)
        clothes.data.shape_keys.key_blocks['SurfaceDeform'].name = i

resetShapeKeyWeights(character)