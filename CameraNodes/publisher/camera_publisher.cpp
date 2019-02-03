#include <chrono>
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "common.hpp"

using namespace std::chrono_literals;

/* This example creates a subclass of Node and uses std::bind() to register a
 * member function as a callback from the timer. */

class CameraServer : public rclcpp::Node
{
public:
  CameraServer(std::string topic, std::string cameraNum, int fps, std::string name)
  : Node(name), count_(0)
  {
    publisher_ = this->create_publisher<sensor_msgs::msg::Image>(topic, rmw_qos_profile_sensor_data);
    timer_ = this->create_wall_timer(
      10ms, std::bind(&CameraServer::timer_callback, this));
    cap = cv::VideoCapture(-1);
  }

private:
  void timer_callback()
  {

      cap >> frame;

      std::cout << frame.rows << " " << frame.cols << std::endl;


    sensor_msgs::msg::Image::UniquePtr msg(new sensor_msgs::msg::Image());

      // Pack the OpenCV image into the ROS image.
    set_now(msg->header.stamp);
    msg->header.frame_id = "camera_frame";
    msg->height = frame.rows;
    msg->width = frame.cols;
    msg->encoding = mat_type2encoding(frame.type());
    msg->is_bigendian = false;
    msg->step = static_cast<sensor_msgs::msg::Image::_step_type>(frame.step);
    msg->data.assign(frame.datastart, frame.dataend);
    RCLCPP_INFO(this->get_logger(), "Publishing: '%d'", this->count_);
    publisher_->publish(msg);  // Publish.

    this->count_++;

  }
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr publisher_;
  //rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  cv::VideoCapture cap;
  cv::Mat frame;
  size_t count_;
};

int main(int argc, char * argv[])
{

  /*if (argc == 0) {
      throw "No arguments passed, a config file is necessary";
  }

  YAML::Node config;

  try {
      config = YAML::LoadFile(argv[0]);
  } catch (...) {
      throw "Invalid Config Yaml file passed";
  }


  if (!config["camServer"]) {
      throw "Invalid Config Yaml file passed";
  }

  config = config["camServer"];
*/
  std::string topic = "camserver/rgb";
  std::string cameraNum = "/dev/video0";
  int fps = 30;
  std::string name = "Camera_Server";

  /*if (config["Topic"])
    topic = config["Topic"].as<std::string>();

  if (config["cameraNum"])
    cameraNum = config["Uri"].as<std::string>();

  if (config["FrameRate"])
    fps = config["FrameRate"].as<int>();

  if (config["FrameRate"])
    name = config["Name"].as<std::string>();

*/

  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<CameraServer>(topic, cameraNum, fps, name));
  rclcpp::shutdown();
  return 0;
}
