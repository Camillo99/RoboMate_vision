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

class PointCloud2Dto3D : public rclcpp::Node {
    
    public:
        ////////////////////////////////////
        //---Costructor---
        ////////////////////////////////////
        PointCloud2Dto3D();
        PointCloud2Dto3D(std::string node_name_);
        
        ////////////////////////////////////
        //---Get---
        ////////////////////////////////////
        bool isPointCloudReceived() const {
            return point_cloud_received;
        }
        pcl::PointCloud<PointT>::Ptr getRawCloud() const {
            return raw_cloud_;
        }

        ////////////////////////////////////
        //---Set---
        ////////////////////////////////////
        void setPointCloudReceived(bool received) {
            point_cloud_received = received;
        }
        void setRawCloud(const pcl::PointCloud<PointT>::Ptr& cloud) {
            raw_cloud_ = cloud;
        }

        //process the pointcloud
        void pc_processing();
        void hole_service_call();
 

    private:
        bool point_cloud_received;

        pcl::PointCloud<PointT>::Ptr raw_cloud_;
        pcl::PointCloud<pcl::Normal>::Ptr cloud_normals_;


        rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr subscription_;
        rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr publisher_;
        rclcpp::Publisher<geometry_msgs::msg::PoseStamped>::SharedPtr publisher_2_;
        rclcpp::Client<image_pros::srv::HoleCenter>::SharedPtr hole_client_;
        void callback(const sensor_msgs::msg::PointCloud2::SharedPtr cloud_msg);
};
