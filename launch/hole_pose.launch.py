import launch
import launch_ros.actions
import os

def generate_launch_description():
    # Define nodes
    node1 = launch_ros.actions.Node(
        package='image_pros',
        executable='circle_2D_topic.py',
        name='circle_2D_topic',
        output='screen',
        emulate_tty=True
    )

    node2 = launch_ros.actions.Node(
        package='image_pros',
        executable='pc_topic',
        name='pc_topic',
        output='screen',
        emulate_tty=True
    )

    node3 = launch_ros.actions.Node(
        package='image_pros',
        executable='call_capture.py',
        name='call_capture',
        output='screen',
        emulate_tty=True
    )
    # Create launch description
    ld = launch.LaunchDescription()

    # Add nodes to the launch description
    ld.add_action(node1)
    ld.add_action(node2)
    #ld.add_action(node3)

    return ld