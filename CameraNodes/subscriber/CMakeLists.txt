cmake_minimum_required(VERSION 3.5)
project(camera_subscriber)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(OpenCV REQUIRED)

add_executable(camera_subscriber camera_subscriber.cpp)
ament_target_dependencies(camera_subscriber rclcpp sensor_msgs OpenCV)

install(TARGETS
  camera_subscriber
  DESTINATION lib/${PROJECT_NAME})

ament_package()
