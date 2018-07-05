#Build Streamer
cd streamer
mkdir cvsdk
cd cvsdk
cmake -DCMAKE_BUILD_TYPE=Release -DUSE_CVSDK=ON -DBACKEND=cpu -DTEST_ON=ON -DUSE_SSD=ON -DUSE_WEBSOCKET=ON -DUSE_KAFKA=ON -DUSE_MQTT=ON -DUSE_PYTHON=ON ..
make -j8 && make apps -j8
sudo make install_python

#Copy config files
cd ./config
cp cameras.toml.example cameras.toml
cp models.toml.example models.toml
cp config.toml.example config.toml 
cd ../
