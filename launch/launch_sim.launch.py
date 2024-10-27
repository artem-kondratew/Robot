import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():

    package_name = 'robot'

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(get_package_share_directory(package_name), 'launch', 'rsp.launch.py')]
        ),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    world = os.path.join(get_package_share_directory(package_name), 'worlds', 'maze.world')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
            launch_arguments={'use_sim_time': 'true',
                              'world': world}.items()
    )

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'robot',
                                   '-x', '0.50',
                                   '-y', '0.50',
                                   '-z', '0.23',
                                   '-Y', '1.57'],
                        output='screen',
                        namespace='robot',
                        )

    return LaunchDescription([
        rsp,
        spawn_entity,
        gazebo,
    ])
