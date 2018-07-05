#START FROM USER DIRECTORY

#Add to environment (.bashrc)
echo "source /opt/intel/computer_vision_sdk/bin/setupvars.sh" >> ~/.bashrc
echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/opencl" >> ~/.bashrc
echo "export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH" >> ~/.bashrc

#install NEO OpenCL driver
cd /opt/intel/computer_vision_sdk/install_dependencies
sudo ./install_NEO_OCL_driver.sh

#Build CVSDK extensions
cd /opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples
sudo mkdir build
cd build
sudo -E cmake ..
sudo make -j8

#Install protobuf dependencies
sudo apt-get install --yes autoconf automake libtool curl make g++ unzip

#Install protobuf v3
curr_user=$USER
cd $HOME/curr_user
git clone https://github.com/google/protobuf.git
cd protobuf
git reset --hard 513b35dc4e732a5649d50b2c56405109def40624
git submodule update --init --recursive
./autogen.sh
./configure --disable-shared --with-pic
make -j8
sudo make install

#Install Streamer
sudo apt-get install --yes --no-install-recommends cmake libglib2.0-dev libgoogle-glog-dev
sudo apt-get install --yes --no-install-recommends libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-good1.0-dev libgstreamer-plugins-bad1.0-dev
sudo apt-get install --yes --no-install-recommends gstreamer1.0:amd64
sudo apt-get remove --purge gstreamer1.0-vaapi
sudo apt-get install --yes libeigen3-dev
sudo apt-get install --yes libjemalloc-dev libzmq3-dev
sudo apt-get install --yes --no-install-recommends libboost-all-dev
sudo apt-get install --yes libcpprest-dev
sudo apt-get install --yes libjsoncpp-dev
sudo apt-get install --yes python-numpy python-scipy
sudo apt-get install --yes libopenblas-dev liblapack-dev
