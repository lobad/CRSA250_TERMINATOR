import numpy as np
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import matplotlib.pyplot as plt
import ikpy.utils.plot as plot_utils
from matplotlib import interactive
import time
import math
import serial

animation_speed = 1

robot_arm_chain = Chain.from_urdf_file("J:\\Documents\\CRS_Robot_Arm\\urdf-test.xml")
robot_arm_chain = Chain(name='5_dof_robot_arm', links=[
    
    OriginLink(),
    URDFLink(
        name="base_link",
        bounds=[-np.pi, np.pi],
        origin_translation=[0, 0, 0.1],
        origin_orientation=[0, 0, 0],
        rotation=[0, 0, 1],
    ),
    URDFLink(
        name="waist",
        bounds=[-np.pi, np.pi],
        origin_translation=[0, 0, 1],
        origin_orientation=[0, 0, 0],
        rotation=[0, 1, 0],
    ),
    URDFLink(
        name="shoulder",
        bounds=[-np.pi, np.pi],
        origin_translation=[0, 0, 1],
        origin_orientation=[0, 0, 0],
        rotation=[0, 1, 0],
    ),
    URDFLink(
        name="elbow",
        bounds=[-np.pi, np.pi],
        origin_translation=[0, 0, 1],
        origin_orientation=[0, 0, 0],
        rotation=[0, 1, 0],
    ),
    URDFLink(
        name="wrist_bend",
        bounds=[-np.pi, np.pi],
        origin_translation=[0, 0, 0.5],
        origin_orientation=[0, 0, 0],
        rotation=[0, 0, 1],
    ),
    URDFLink(
        name="tool_head",
        bounds=[-np.pi, np.pi],
        origin_translation=[0, 0, 0],
        origin_orientation=[0, 0, 0],
        rotation=[0, 0, 1],
    )
])




def sendCommand(a, b, c, d, e, f, move_time):
    # Replace this line with the appropriate command to send the command to your robot arm
    pass


def doIK():
    global ik
    old_position = ik.copy()
    ik = robot_arm_chain.inverse_kinematics(target_position, target_orientation, orientation_mode="Z", initial_position=old_position)


def update_plot(frame):
    # Clear the previous plot
    ax.clear()

    # Plot the robot arm
    lines = robot_arm_chain.plot(ik, ax)

    # Set the plot limits
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(0, 6)

    # Return the lines drawn by the plot
    return lines


def move(x, y, z):
    global target_position
    target_position = [x, y, z]
    doIK()
    animate_arm(0.05)

    sendCommand(ik[1].item(), ik[2].item(), ik[3].item(), ik[4].item(), ik[5].item(), ik[6].item(), 1)

    
   
target_position = [ 3, 0,0.58]
    
target_orientation = [-1, 20, 3]


joint_angles = robot_arm_chain.inverse_kinematics(target_position)
print("Joint angles for the target position are:", joint_angles)

calculated_position = robot_arm_chain.forward_kinematics(joint_angles)[:3, 3]
print("Calculated position for the given joint angles is:", calculated_position)

ik = robot_arm_chain.inverse_kinematics(target_position, target_orientation, orientation_mode="Y")
print("The angles of each joints are : ", list(map(lambda r:math.degrees(r),ik.tolist())))
computed_position = robot_arm_chain.forward_kinematics(ik)

print("Computed position: %s, original position : %s" % (computed_position[:3, 3], target_position))
print("Computed position (readable) : %s" % [ '%.2f' % elem for elem in computed_position[:3, 3] ])
target_position = [3, 1, 1]

def animate_arm(start_pos, stop_pos, animation_speed):
    # Calculate the distance between the start and stop positions
    dist = np.linalg.norm(np.array(stop_pos) - np.array(start_pos))
    
    # Calculate the direction of motion
    direction = (np.array(stop_pos) - np.array(start_pos)) / dist
    
    # Calculate the number of frames required to complete the animation
    num_frames = int(dist / 0.2)
    
    # Calculate a list of intermediate positions
    positions = [np.array(start_pos) + direction * (dist * i / num_frames) for i in range(num_frames)]
    
    for pos in positions:
        # Update the target_position based on the current position
        target_position = pos.tolist()
        doIK()

        # Clear the previous plot
        ax.clear()

        # Plot the robot arm
        robot_arm_chain.plot(ik, ax)

        # Set the plot limits
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_zlim(0, 6)

        # Redraw the plot and pause for the specified time
        plt.draw()
        plt.pause(animation_speed)


        
interactive(True)


fig, ax = plot_utils.init_3d_figure()
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(0, 6)
animate_arm([3, 3, 3], [1, 5, 6], 5)




robot_arm_chain.plot(joint_angles, ax)
plt.show()