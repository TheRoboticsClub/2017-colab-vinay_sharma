// Copyright 2016 Open Source Robotics Foundation, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "common.hpp"

using std::placeholders::_1;

class MinimalSubscriber : public rclcpp::Node
{
public:
  MinimalSubscriber(std::string topic)
  : Node("CameraViewer")
  {
    subscription_ = this->create_subscription<sensor_msgs::msg::Image>(
      topic, std::bind(&MinimalSubscriber::topic_callback, this, _1), rmw_qos_profile_sensor_data);
  }

private:
  void topic_callback(const sensor_msgs::msg::Image::SharedPtr msg)
  {
    cv::Mat cv_mat(
    msg->height, msg->width,
    encoding2mat_type(msg->encoding),
    msg->data.data());
    RCLCPP_INFO(this->get_logger(), "I heard: '%s'", "Image");

    cv::Mat c_mat = cv_mat;

    std::cout << c_mat.rows << " " << c_mat.cols << std::endl;

    cv::imshow("CameraViewer", c_mat);
    char key = cv::waitKey(1);    // Look for key presses.
    if (key == 27 /* ESC */ || key == 'q') {
      rclcpp::shutdown();
    }

  }
  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  if (argc <= 1) {
      throw "No topic specified";
  }

  std::string topic = argv[1];
  rclcpp::spin(std::make_shared<MinimalSubscriber>(topic));
  rclcpp::shutdown();
  return 0;
}
