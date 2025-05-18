bl_info = {
	"name" : "ARKit Toolset",
	"author" : "Andy Hellgrim",
	"description" : "Toolset for helping you create manually all 52 expressions required by ARKit",
	"version" : (1, 0, 0),
	"blender" : (4, 4, 0),
	"location" : "View3D > Item",
	"doc_url" : "https://github.com/AndyLobjois/BLENDER-ARKitToolset",
	"category" : "Utility"
}

import os
from os import listdir
from os.path import isfile, join
import bpy
import bpy.utils.previews
from bpy.props import EnumProperty, PointerProperty, StringProperty, IntProperty, BoolProperty
from bpy.types import Operator, Panel
import webbrowser


# Pictures
list_raw = []
directory = os.path.join(bpy.utils.script_path_user(), "addons") + "\\ARKit Toolset\\img\\default"
onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
for f in onlyfiles:
	if f[-4:] == ".png":
		list_raw.append(f)

# Lists
ARKitList = [
'tongueOut',
'eyeBlinkLeft', 'eyeLookUpLeft', 'eyeLookDownLeft', 'eyeLookInLeft', 'eyeLookOutLeft', 'eyeSquintLeft', 'eyeWideLeft',
'browInnerUp', 'browDownLeft', 'browOuterUpLeft',
'mouthLeft', 'mouthUpperUpLeft', 'mouthLowerDownLeft', 'mouthSmileLeft', 'mouthFrownLeft', 'mouthDimpleLeft', 'mouthStretchLeft', 'mouthPressLeft',
'jawLeft', 'jawForward', 'jawOpen', 'cheekPuff', 'cheekSquintLeft', 'noseSneerLeft',
'mouthClose', 'mouthFunnel', 'mouthPucker', 'mouthRollLower', 'mouthRollUpper', 'mouthShrugLower', 'mouthShrugUpper',
#'↓ MIRRORED ↓',
]

ARKitListAll = [
'eyeBlinkLeft', 'eyeBlinkRight',
'eyeLookUpLeft', 'eyeLookUpRight', 'eyeLookDownLeft', 'eyeLookDownRight', 'eyeLookInLeft', 'eyeLookInRight', 'eyeLookOutLeft', 'eyeLookOutRight',
'eyeSquintLeft', 'eyeSquintRight', 'eyeWideLeft', 'eyeWideRight',
'browInnerUp', 'browDownLeft', 'browDownRight', 'browOuterUpLeft', 'browOuterUpRight',
'mouthLeft', 'mouthRight', 'mouthUpperUpLeft', 'mouthUpperUpRight', 'mouthLowerDownLeft', 'mouthLowerDownRight',
'mouthSmileLeft', 'mouthSmileRight', 'mouthFrownLeft', 'mouthFrownRight', 'mouthDimpleLeft', 'mouthDimpleRight',
'mouthStretchLeft', 'mouthStretchRight', 'mouthPressLeft', 'mouthPressRight',
'jawLeft', 'jawRight', 'jawForward', 'jawOpen',
'cheekPuff', 'cheekSquintLeft', 'cheekSquintRight',
'noseSneerLeft', 'noseSneerRight',
'mouthClose', 'mouthFunnel', 'mouthPucker', 'mouthRollLower', 'mouthRollUpper', 'mouthShrugLower', 'mouthShrugUpper',
'tongueOut',
]

def SetupBlenderFeatures():
	# Disable XYZ Mirror symmetry
	bpy.context.object.use_mesh_mirror_x = False
	bpy.context.object.use_mesh_mirror_y = False
	bpy.context.object.use_mesh_mirror_z = False
	
	# Disable Auto-merge
	bpy.context.scene.tool_settings.use_mesh_automerge = False
	
	# Disable UV Auto Correction
	bpy.context.scene.tool_settings.use_transform_correct_face_attributes = False
	
	# Disable Show Only Shapekey
	bpy.context.object.show_only_shape_key = False


# Classes ------------------------------------------------------------------------------------------------------------------------------------
class GenerateEssentials(Operator):
	"""Create 32 essential shapekeys, the rest can be duplicated and mirrored"""
	bl_idname = "arkittoolset.generate_essentials"
	bl_label = "Essentials"
	
	def execute(self, context):
		SetupBlenderFeatures()
		
		# Save EditMode State
		editmode = False
		if context.mode == "EDIT_MESH":
			editmode = True
			bpy.ops.object.editmode_toggle()
		
		# Create Basis Shapekey & Get "Blocks"
		bpy.ops.object.shape_key_add(from_mix=False)
		blocks = context.active_object.data.shape_keys.key_blocks

		# Create 
		for i in range(0, len(ARKitList)):
			bpy.ops.object.shape_key_add(from_mix=False)
			blocks[i+1].name = ARKitList[i]
		
		# Add "MIRRORED" separator
		bpy.ops.object.shape_key_add(from_mix=False)
		blocks[len(ARKitList)+1].name = '↓ MIRRORED ↓'
		blocks[len(ARKitList)+1].mute = True
		
		# Select the first shapekey
		bpy.context.object.active_shape_key_index = 1
		
		# Go Back to Edit Mode State
		if editmode:
			bpy.ops.object.editmode_toggle()
		
		return{'FINISHED'}
	

class GenerateAll(Operator):
	"""If your face isn't symmetrical, Create 52 empty shapekeys required by ARKit"""
	bl_idname = "arkittoolset.generate_full"
	bl_label = "All"
	
	def execute(self, context):
		SetupBlenderFeatures()
		
		# Save EditMode State
		editmode = False
		if context.mode == "EDIT_MESH":
			editmode = True
			bpy.ops.object.editmode_toggle()
		
		# Create Basis Shapekey & Get Key Blocks
		bpy.ops.object.shape_key_add(from_mix=False)
		blocks = context.active_object.data.shape_keys.key_blocks
		
		# Create 
		for i in range(0, len(ARKitListAll)):
			bpy.ops.object.shape_key_add(from_mix=False)
			blocks[i+1].name = ARKitListAll[i]
		
		# Select the first shapekey
		bpy.context.object.active_shape_key_index = 1
		
		# Go Back to Edit Mode State
		if editmode:
			bpy.ops.object.editmode_toggle()
			
		return{'FINISHED'}


class DeleteAllShapekeys(Operator):
	"""Delete all shapekeys"""
	bl_idname = "arkittoolset.delete_all"
	bl_label = "Delete All"
	
	def execute(self, context):
		# Save EditMode State
		editmode = False
		if context.mode == "EDIT_MESH":
			editmode = True
			bpy.ops.object.editmode_toggle()
		
		# Delete All
		bpy.ops.object.shape_key_add(from_mix=False) # Create 1 shapekey just in case the list is empty
		bpy.ops.object.shape_key_lock(action='UNLOCK')
		bpy.ops.object.shape_key_remove(all=True, apply_mix=False)
		
		# Go Back to Edit Mode State
		if editmode:
			bpy.ops.object.editmode_toggle()
		
		return{'FINISHED'}


class Mirrored(Operator):
	"""Create 20 mirrored shapekeys from the base shapekeys"""
	bl_idname = "arkittoolset.mirrored"
	bl_label = "Generate Mirrored"
	
	def execute(self, context):
		SetupBlenderFeatures()
		
		# Save EditMode State
		editmode = False
		if context.mode == "EDIT_MESH":
			editmode = True
			bpy.ops.object.editmode_toggle()
		
		# Get Key Blocks
		blocks = context.active_object.data.shape_keys.key_blocks
		
		# Save current index
		index = bpy.context.object.active_shape_key_index
		
		# Clean
		bpy.ops.object.shape_key_lock(action='UNLOCK')
		if len(blocks) > 54:
			for i in reversed(range(34, 54 + 1)):
				bpy.context.object.active_shape_key_index = i
				bpy.ops.object.shape_key_remove(all=False)
		
		# Select First Shapekey
		bpy.context.object.active_shape_key_index = 1
		
		# Duplicate & Mirror Shapekeys
		others = len(blocks) - 34
		self.report({'INFO'}, str(others))
		
		for i in range(0, len(ARKitList)):
			_name = blocks[i+1].name
			
			if "Left" in _name:
				# Duplicate
				blocks[i+1].value = 1
				bpy.ops.object.shape_key_add(from_mix=True)
				blocks[i+1].value = 0
				
				# Get Length
				length = len(blocks)
				
				# Select, Mirror, Rename and Lock
				bpy.context.object.active_shape_key_index = length-1
				bpy.ops.object.shape_key_mirror(use_topology=False)
				blocks[length-1].name = _name.replace("Left", "Right")
				blocks[length-1].lock_shape = True
				
				# Move
				for o in range(0, others):
					bpy.ops.object.shape_key_move(type='UP')
		
		# Add "OTHERS" separator
		bpy.ops.object.shape_key_add(from_mix=True)
		blocks[length].name = '↓ OTHERS ↓'
		blocks[length].mute = True
		
		# Move
		for o in range(0, others):
			bpy.ops.object.shape_key_move(type='UP')
		
		# Go back to current index
		bpy.context.object.active_shape_key_index = index
		
		# Go Back to Edit Mode State
		if editmode:
			bpy.ops.object.editmode_toggle()
		
		return{'FINISHED'}


class ToggleLock(Operator):
	"""Lock/Unlock every mirrored shapekeys"""
	bl_idname = "arkittoolset.toggle_lock"
	bl_label = "Lock/Unlock Mirrored"
	
	def execute(self, context):
		# Get Key Blocks
		blocks = context.active_object.data.shape_keys.key_blocks
		
		for i in range(34, 54):
			blocks[i].lock_shape = not blocks[i].lock_shape
		return{'FINISHED'}


# Tools -----------------------------------------------------------------------------------------------------------------------
class ResetShapekey(Operator):
	"""Reset current shapekey from Basis"""
	bl_idname = "arkittoolset.reset_shapekey"
	bl_label = "Reset Current Shapekey"
	
	def execute(self, context):
		blocks = context.active_object.data.shape_keys.key_blocks
		index = context.object.active_shape_key_index
		name = blocks[index].name
		length = len(blocks)
		editmode = False
		
		# Save EditMode State
		if context.mode == "EDIT_MESH":
			editmode = True
			bpy.ops.object.editmode_toggle()
		
		# Check Lock
		if blocks[index].lock_shape == True:
			self.report({'ERROR'}, 'Shapekey is locked !')
			return{'FINISHED'}
		
		# Delete current shapekey
		bpy.ops.object.shape_key_remove(all=False)
		
		# Create/Name a new shapekey
		bpy.ops.object.shape_key_add(from_mix=False)
		blocks[length - 1].name = name
		
		# Select & Move
		bpy.context.object.active_shape_key_index = length - 1
		for i in range(0, length - index - 1):
			bpy.ops.object.shape_key_move(type='UP')
		
		# Get Back to Edit Mode if necessary
		if editmode:
			bpy.ops.object.editmode_toggle()
		
		return{'FINISHED'}


class ApplyFromMix(Operator):
	"""Apply shapekey from mix onto the selected shapekey"""
	bl_idname = "arkittoolset.copy_shapekey"
	bl_label = "Apply from Mix"
	
	def execute(self, context):
		blocks = context.active_object.data.shape_keys.key_blocks
		index = context.object.active_shape_key_index
		name = blocks[index].name
		length = len(blocks)
		editmode = False
		
		# Save EditMode State
		if context.mode == "EDIT_MESH":
			editmode = True
			bpy.ops.object.editmode_toggle()
		
		# Delete
		bpy.ops.object.shape_key_remove(all=False)
		
		# New Shapekey from Mix & Rename
		bpy.ops.object.shape_key_add(from_mix=True)
		blocks[length - 1].name = name
		
		# Move
		bpy.context.object.active_shape_key_index = length - 1
		for i in range(0, length - index - 1):
			bpy.ops.object.shape_key_move(type='UP')
		
		# Go Back to Edit Mode State
		if editmode:
			bpy.ops.object.editmode_toggle()
		
		return{'FINISHED'}


class PreviousShapekey(Operator):
	"""Select previous shapekey"""
	bl_idname = "arkittoolset.previous_shapekey"
	bl_label = "Previous"
	
	def execute(self, context):
		bpy.context.object.active_shape_key_index = bpy.context.object.active_shape_key_index - 1
		return{'FINISHED'}


class NextShapekey(Operator):
	"""Select next shapekey"""
	bl_idname = "arkittoolset.next_shapekey"
	bl_label = "Next"
	
	def execute(self, context):
		bpy.context.object.active_shape_key_index = bpy.context.object.active_shape_key_index + 1
		return{'FINISHED'}


class AllShapekeysValueToZero(Operator):
	"""Put all shapekey values to zero"""
	bl_idname = "arkittoolset.all_shapekeys_to_zero"
	bl_label = "All Values To Zero"
	
	def execute(self, context):
		blocks = context.active_object.data.shape_keys.key_blocks
		for i in range(0, len(blocks)):
			blocks[i].value = 0
		
		return{'FINISHED'}


# UI ---------------------------------------------------------------------------------------------------------------------------
class UIMain(Panel):
	bl_idname = "arkittoolset.PT_panel"
	bl_label = "ARKit Toolset"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Item"

	def draw_header(self, context):
		header = self.layout.row(align=True)
		donation = header.operator(Donation.bl_idname, text="", icon_value=addon_icon['icon'].icon_id, emboss=True)
		
	def draw(self, context):
		layout = self.layout
		
		if len(context.selected_objects) == 0 or context.selected_objects[0].type != 'MESH':
			layout.label(text="No mesh selected.")
			return None
		
		# Essentials / All / Delete all
		GENERATE = layout.row(align=True)
		essentials = GENERATE.row(align=True)
		essentials.operator(GenerateEssentials.bl_idname, text=GenerateEssentials.bl_label, icon="SHAPEKEY_DATA")
		
		all = GENERATE.row(align=True)
		all.operator(GenerateAll.bl_idname, text=GenerateAll.bl_label, icon="SHAPEKEY_DATA")
		
		delete = GENERATE.row(align=True)
		delete.operator(DeleteAllShapekeys.bl_idname, text="", icon="X")
		
		# Generate Other Side
		MIRROR = layout.row(align=True)
		mirror = MIRROR.row(align=True)
		mirror.operator(Mirrored.bl_idname, text=Mirrored.bl_label, icon="MOD_MIRROR")
		lock = MIRROR.row(align=True)
		lock.operator(ToggleLock.bl_idname, text="", icon="LOCKED")
		
		layout.separator()
		
		# Tools
		TOOLS = layout.column()
		apply = TOOLS.column()
		apply.operator(ApplyFromMix.bl_idname, text=ApplyFromMix.bl_label, icon="IMPORT")
		reset = TOOLS.row(align=True)
		reset.operator(ResetShapekey.bl_idname, text=ResetShapekey.bl_label, icon="FILE_REFRESH")
		zero = reset.row(align=True)
		zero.operator(AllShapekeysValueToZero.bl_idname, text="0")
		zero.scale_x = 0.1
		
		# Enable/Disable features
		delete.enabled = False
		mirror.enabled = False
		lock.enabled = False
		apply.enabled = False
		reset.enabled = False
		
		if context.active_object.data.shape_keys:
			essentials.enabled = False
			all.enabled = False
			delete.enabled = True
			apply.enabled = True
			reset.enabled = True
			
			if context.active_object.data.shape_keys.key_blocks[33].name == "↓ MIRRORED ↓":
				mirror.enabled = True
			
			if len(context.active_object.data.shape_keys.key_blocks) >= 55:
				lock.enabled = True


class UIHead(Panel):
	bl_idname = "arkittoolset.PT_panel_head"
	bl_label = "Preview"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Item"
	bl_parent_id = UIMain.bl_idname
	#bl_options = {'DEFAULT_CLOSED'}
	
	@classmethod
	def poll(cls, context):
		if len(context.selected_objects) == 0:
			return None
		if context.selected_objects[0].type != 'MESH':
			return None
		return context.active_object.data.shape_keys
	
	def draw(self, context):
		index = bpy.context.object.active_shape_key_index
		name = bpy.context.active_object.data.shape_keys.key_blocks[index].name
		
		# Label & Previous/Next buttons
		line = self.layout.row()
		line.alignment = 'CENTER'
		col = line.column()
		
		previous = line.row()
		previous.operator(PreviousShapekey.bl_idname, text="", icon="TRIA_LEFT", emboss=True)
		
		line.label(text=name)
		
		next = line.row()
		next.operator(NextShapekey.bl_idname, text="", icon="TRIA_RIGHT", emboss=True)
		
		# Image & Subtexts
		for i in range(0, len(list_raw)):
			if name in list_raw[i]:
				self.layout.template_icon(icon_value=addon_images[list_raw[i][:-4]].icon_id, scale=10)
				
				if name == "mouthClose":
					detail = self.layout.row()
					detail.scale_y = 1
					detail.label(text="'mouthClose' is on top of 'jawOpen'.", icon="INFO")
					detail = self.layout.row()
					detail.scale_y = 0.6
					detail.label(text="1. Set 'jawOpen' to 1")
					detail = self.layout.row()
					detail.scale_y = 0.6
					detail.label(text="2. Enable 'Shape Key Edit Mode' (below the Shape Keys list)")
					detail = self.layout.row()
					detail.scale_y = 0.6
					detail.label(text="3. Edit only the mouth in 'close' state")
				
				if name == "mouthDimpleLeft":
					self.layout.label(text="Half of smile.", icon="INFO")
				if name == "mouthPressLeft":
					self.layout.label(text="Left corner scaled down.", icon="INFO")
				if name == "mouthPucker":
					self.layout.label(text="A little kiss ♥", icon="INFO")
				if name == "mouthRollLower":
					self.layout.label(text="Hide lower lip under upper lip.", icon="INFO")
				if name == "mouthRollUpper":
					self.layout.label(text="Hide upper lip under lower lip.", icon="INFO")
				if name == "mouthShrugLower":
					self.layout.label(text="Lift up the lower lip", icon="INFO")
				if name == "mouthShrugUpper":
					self.layout.label(text="Lift up the upper lip.", icon="INFO")
				
		# Previous / Next Check
		if bpy.context.object.active_shape_key_index > 0:
			previous.enabled = True
		else:
			previous.enabled = False
			
		if bpy.context.object.active_shape_key_index < len(context.active_object.data.shape_keys.key_blocks) - 1:
			next.enabled = True
		else:
			next.enabled = False


class Donation(Operator):
	"""If you appreciate this addon, please consider a donation ! Thanks a lot"""
	bl_idname = "arkittoolset.donation"
	bl_label = "Donation"
	
	def execute(self, context):
		webbrowser.open('https://www.paypal.com/paypalme/andylobjois')
		return{'FINISHED'}

	

# Registration -------------------------------------------------------------------------------------------------------------
addon_icon = None
addon_images = None

AllClasses = [UIMain, UIHead,
	GenerateEssentials, GenerateAll, DeleteAllShapekeys,
	Mirrored, ToggleLock,
	ApplyFromMix, ResetShapekey, AllShapekeysValueToZero,
	PreviousShapekey, NextShapekey,
	Donation,
	]

def register():
	for cls in AllClasses:
		bpy.utils.register_class(cls)
	
	# Icon
	global addon_icon
	addon_icon = bpy.utils.previews.new()
	addon_icon.load("icon", os.path.join(os.path.dirname(__file__), "icon.png"), 'IMAGE')
	
	# Images
	global addon_images
	addon_images = bpy.utils.previews.new()
	for z in list_raw:
		addon_images.load(z[:-4], os.path.join(directory, z), 'IMAGE')

def unregister():
	for cls in reversed(AllClasses):
		bpy.utils.unregister_class(cls)
	
	# Icon
	global addon_icon
	bpy.utils.previews.remove(addon_icon)
	
	# Images
	global addon_images
	bpy.utils.previews.remove(addon_images)

if __name__ == "__main__":
	register()