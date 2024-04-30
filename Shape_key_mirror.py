import bpy
#keys has to end with Left,Right or L R
active_obj = bpy.context.object
active_sk = active_obj.active_shape_key_index
shape_keys = active_obj.data.shape_keys.key_blocks

#creates list with sk names
sk_list = shape_keys.keys()
sk_index = len(sk_list)

last_mode = active_obj.mode
bpy.ops.object.mode_set(mode = 'OBJECT')

#looks for active direction in sk name
direction = ["Left", "L", "Right", "R"]
if sk_list[active_sk].endswith(direction[0]) or sk_list[active_sk].endswith(direction[1]):
    print("Copying from Left")
    
elif sk_list[active_sk].endswith(direction[2]) or sk_list[active_sk].endswith(direction[3]):
    
    direction[0], direction[2] = direction[2], direction[0]
    direction[1], direction[3] = direction[3], direction[1]
    print("Copying from Right") 
    
else:
    raise Exception('Please select a shape key to copy the direction from. Shape key name has to end with "Left" or "R')

i = 1
mrr_list = []
del_list = []
#change range here, 0 is Basis
for i in range(1,sk_index) :
    
    shape_keys[i].value = 0
    #sets sk at 0 to create from mix later, adds keys to be mirrored in a list
    if sk_list[i].endswith(direction[0]) or sk_list[i].endswith(direction[1]):
        mrr_list.append(shape_keys[i])
        
    #if ends with unwanted direction, select, delete, update list
    if sk_list[i].endswith(direction[2]) or sk_list[i].endswith(direction[3]):
        del_list.append(shape_keys[i])

for i in del_list:
    active_obj.shape_key_remove(i)
   
print("Keys reset and cleared")
print(mrr_list)
print(del_list)

i = 0
for i in range(0, len(mrr_list)):
    
    mrr_list[i].value = 1

    #store name change
    sk_name = str(mrr_list[i].name)
    if sk_name.endswith(direction[0]):
        #Longname
        sk_name = sk_name.replace(direction[0], direction[2])
    else:
        #Shortname
        sk_name = sk_name.replace(direction[1], direction[3])
        
    #active_obj.shape_key_add(name, from mix) would not let mirror directly
    bpy.ops.object.shape_key_add(from_mix=True)
    bpy.ops.object.shape_key_mirror(use_topology=False)
    #renames last key
    shape_keys[len(shape_keys)-1].name = sk_name
    
    mrr_list[i].value = 0
    
print("Keys mirrored.")
bpy.ops.object.mode_set(mode = last_mode)
#yipee i dont like lists i am scared of them, hope its not too much of a mush to read
#script from PopatoChisp