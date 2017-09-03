''' This script will generate twist joints between the selected joint and its parent

'''

import maya.cmds as cmds


def create_joints():
      
    # This is to get the input values, and store them into 2 var. 
    
    # joint_name will be a string as text=True grabs the input as a string
    joint_name=cmds.textField('name_textField',q=True,text=True)  
    # cmds_num will be an int as value=True grabs the input as a integer 
    joint_num=cmds.intField('joint_num_intField',q=True,value=True)
    
    # to check if the user has checked checkbox
    axisStatus=cmds.checkBox('local_axis',q=True,value=True)
    orientStatus=cmds.checkBox('clear_orient',q=True,value=True)
    
    # to check if the name contains any numbers
    for char in joint_name:
        if char.isdigit():
            cmds.warning('The input should not contain numbers. Please give another name.')
            return
    

    # to store the selected joint
    sel=cmds.ls(sl=True,type='joint')   
    # to clear the joint orient, o is the orient
    if orientStatus==True:
        cmds.joint(sel[0],e=True,o=[0,0,0])
    
    # to get the parent joint
    parentJnt=cmds.listRelatives(sel[0],p=True) 
           
    # to check if the input is valid
    if joint_num==0:
        cmds.warning('Value must be greater than 0.')
        return 
    # to terminate if the input name conflicts with any existing joints in the scene
    if joint_name:
        if joint_name in sel[0] or joint_name in parentJnt[0]:
            cmds.warning('The name may already exist in the scene. Please give another name.')
            return
    # to terminate if the input number is too big
    if joint_num>=20:
        cmds.warning('The maximum amount of joints generated should be less than 20.')
        return
           
    # to query the position of the selected joint, q is to query, p is the position, r is the relative position. Store the position value as sel_Pos
    sel_Pos=cmds.joint(sel,q=True,p=True,r=True)
    
    
    floCounter=1.0
    intCounter=1
    
    # to check whether joint_num+1 > counter        
    while intCounter-joint_num<1:        
        
        
        # if no name is given, create a joint with default name
        if not joint_name:
            newJnt=cmds.joint()
        # if a name is given, create a joint with the specific name
        else:
            newJnt=cmds.joint(n=joint_name+str(intCounter))
            
        # parent the new generated joint to the parentJnt
        cmds.parent(newJnt,parentJnt)     
            
        # Turn on the local rotation axis. .dla = '.displayLocalAxis' if user has checked it
        if axisStatus==True:
            cmds.setAttr(newJnt+'.dla',True)    
        
        
        
        # to determine where to put it, ratio 1: Position ([x/(n+1)]) * childjoint.translate X  
        # sel_Pos[0] is select joint's translate X
        x_pos=sel_Pos[0]*floCounter/(joint_num+1)        
        # ratio 2: the amount of twist x/n * childjoint.rotate X
        x_rot=floCounter/joint_num 
        
        # to move and orient it to the right place, enter edit mode. p is position, o is orientation, set the radius smaller            
        cmds.joint(newJnt,edit=True,p=[x_pos,0,0],o=[0,0,0],rad=0.2,r=True)
                

        # create a multiply divide node 
        divide=cmds.shadingNode('multiplyDivide',name=(newJnt+'_MD'),asUtility=True)
        # set the multiply divide node input 2X as the rotation factor
        cmds.setAttr(divide+'.input2X',x_rot)            
        # connect the selected joint rotation X to the divide node's input X
        cmds.connectAttr(sel[0]+'.rotateX',divide+'.input1X',f=True)         
        # connect the output of the divide node to the new generated joint's rotation X
        cmds.connectAttr(divide+'.outputX',newJnt+'.rotateX',f=True)
      
        # increment 
        floCounter=floCounter+1.0
        intCounter=intCounter+1
        
    # to keep the current selection and turn off the window    
    cmds.select(sel)    
    cmds.deleteUI('joint_twist_UI')   
     

# 1. To check whether a user has selected a joint        
if cmds.ls(sl=True,type='joint'):
    
    # cmds.ls(sl=True,type='joint') to prevent the case that joints and non joints are both selected
    sel=cmds.ls(sl=True)
    
    if len(sel)!=1:
        cmds.warning('Please select only 1 joint.') 
    
    else:   
      
        # 2. To check the selected joint has a parent joint
        if not cmds.listRelatives(sel[0],p=True):
            cmds.warning('The joint selected has no parent. Please select another one')  
                        
        else:
 
            # 3. Generate a UI that asks the name and number of twist joints
            if cmds.window('joint_twist_UI', exists = True):
                cmds.deleteUI('joint_twist_UI')
            else:  
                cmds.window('joint_twist_UI')
                cmds.window('joint_twist_UI',e=True,w=350,h=100)
                cmds.showWindow('joint_twist_UI')
                
                cmds.columnLayout('main_cl')
                cmds.rowColumnLayout('text_rcl',nc=2)
                cmds.text(label='Name:')   # This prints out a label
                cmds.textField('name_textField')  # This is to create a typing field
                cmds.text(label='# of Joints')
                cmds.intField('joint_num_intField',value = 1,minValue=1)
            
 
                # When the Create Joints is pressed, the create_joints def will be called. 
                cmds.checkBox('local_axis',label='Display Local Rotation Axis')
                cmds.checkBox('clear_orient',label='Zero Out Current Joint Orient')
                cmds.button('create_button',label='Create Joints',command='create_joints()')  
                cmds.button('cancel_button',label='Cancel',command='cmds.deleteUI("joint_twist_UI")')
             
else:
    cmds.warning('You need to select a joint.')      

             

