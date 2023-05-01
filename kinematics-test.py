import numpy as np
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import matplotlib.pyplot as plt
import ikpy.utils.plot as plot_utils
import matplotlib.widgets as widgets


robot_arm_chain = Chain.from_urdf_file("J:\\Documents\\CRS_Robot_Arm\\urdf-test.xml")


# Define the robot arm kinematic chain
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
], active_links_mask=[False, True, True, True, True, True, True])


def move_to_position(target_position):
    # Calculate the inverse kinematics
    joint_angles = robot_arm_chain.inverse_kinematics(target_position)
    print("Joint angles for the target position are:", joint_angles)

    # Compute the forward kinematics to verify the result
    calculated_position = robot_arm_chain.forward_kinematics(joint_angles)[:3, 3]
    print("Calculated position for the given joint angles is:", calculated_position)

    fig, ax = plot_utils.init_3d_figure()
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(0, 6)
    robot_arm_chain.plot(joint_angles, ax)
    plt.show()

def on_slider_change(val):
    joint_angles = np.array([s_joint.value for s_joint in sliders])
    ax_3d.clear()
    robot_arm_chain.plot(joint_angles, ax_3d)
    fig_3d.canvas.draw_idle()


# Initialize the figure and create sliders for each joint
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.3)
sliders = []

for i in range(len(robot_arm_chain.links) - 1):
    ax_slider = plt.axes([0.15, 0.1 + 0.05 * i, 0.7, 0.03])
    min_angle, max_angle = robot_arm_chain.links[i + 1].bounds
    slider = widgets.Slider(ax_slider, f"Joint {i+1}", min_angle, max_angle, valinit=0, valstep=0.01)
    slider.on_changed(on_slider_change)
    sliders.append(slider)

fig_3d, ax_3d = plot_utils.init_3d_figure()
ax_3d.set_xlim(-3, 3)
ax_3d.set_ylim(-3, 3)
ax_3d.set_zlim(0, 6)
initial_joint_angles = np.zeros(sum(robot_arm_chain.active_links_mask))
robot_arm_chain.plot(robot_arm_chain.active_to_full(initial_joint_angles, initial_position=np.zeros(3)), ax_3d)


plt.show()
# Example usage:
target_position = [3, 1, 1]
move_to_position(target_position)

# Define the target position for the end effector
target_position = [3, 1, 1]

# Calculate the inverse kinematics
joint_angles = robot_arm_chain.inverse_kinematics(target_position)
print("Joint angles for the target position are:", joint_angles)

# Compute the forward kinematics to verify the result
calculated_position = robot_arm_chain.forward_kinematics(joint_angles)[:3, 3]
print("Calculated position for the given joint angles is:", calculated_position)

fig, ax = plot_utils.init_3d_figure()
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(0, 6)
robot_arm_chain.plot(joint_angles, ax)
plt.show()
