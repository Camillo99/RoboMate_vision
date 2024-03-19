//class definition


#include <algorithm>
#include <memory>
#include <stdexcept>
#include <utility>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "image_pros/srv/hole_center.hpp"

#include "pcl_conversions/pcl_conversions.h"
#include "pcl/point_cloud.h"
#include <pcl/point_types.h>

typedef pcl::PointXYZ PointT;

class PcThread : public rclcpp::Node {

    public:
        ////////////////////////////////////
        //---Costructor---
        ////////////////////////////////////
        PcThread();



    
    private:
        rclcpp::CallbackGroup::SharedPtr topic_cb_group_;
        rclcpp::CallbackGroup::SharedPtr client_cb_group_;
        rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr subscription_;
        rclcpp::Client<image_pros::srv::HoleCenter>::SharedPtr hole_client_ptr_;
        void sub_callback(const sensor_msgs::msg::PointCloud2::SharedPtr cloud_msg);

};