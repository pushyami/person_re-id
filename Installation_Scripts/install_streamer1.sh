#START FROM USER DIRECTORY

#Install common toolchain tools
sudo apt-get install --yes cmake git
sudo apt-get install --yes gcc-multilib

curr_user=$USER
cd $HOME/curr_user

#clean OpenCV if previously installed
sudo apt-get remove libopencv-*
sudo apt-get autoremove opencv-data
 
#Install CVSDK
wget -e use_proxy=yes http://registrationcenter-download.intel.com/akdlm/irc_nas/13131/l_openvino_toolkit_p_2018.1.265.tgz
tar zxvf l_openvino_toolkit_p_2018.1.265.tgz
cd l_openvino_toolkit_p_2018.1.265.tgz
./install_cv_sdk_dependencies.sh
./install.sh
