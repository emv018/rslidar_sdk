from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import tempfile

WS_DIR = os.path.expanduser('~/Drivers/roboscenese_dev')

def launch_setup(context, *args, **kwargs):
    config_path = LaunchConfiguration('config').perform(context)
    rviz_config = get_package_share_directory('rslidar_sdk') + '/rviz/rviz2.rviz'

    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
    tmp.write('/**:\n  ros__parameters:\n    config_path: "{}"\n'.format(config_path))
    tmp.close()

    return [
        Node(
            package='rslidar_sdk',
            executable='rslidar_sdk_node',
            name='rslidar_sdk_node',
            output='screen',
            parameters=[tmp.name]
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config]
        )
    ]

def generate_launch_description():
    default_config = os.path.join(WS_DIR, 'config', 'multi_lidar.yaml')

    return LaunchDescription([
        DeclareLaunchArgument(
            'config',
            default_value=default_config,
            description='Path to lidar config yaml'
        ),
        OpaqueFunction(function=launch_setup)
    ])
