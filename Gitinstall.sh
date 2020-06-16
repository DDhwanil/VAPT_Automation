cd ./git
cd droopescan
pip install -r requirements.txt
cd ../
cd gobuster
make
cd ../
cd ike-scan
autoreconf --install
./configure
make
make install
cd ../
cd masscan
make
cd ../
cd nmap
./configure
make
make install
cd ../
cd Reconnoitre
python3 setup.py install
cd ../
cd sslscan
sudo apt-get install build-essential git zlib1g-dev
sudo apt-get build-dep openssl
make static
cd ../
cd wfuzz
python setup.py install
cd ../
cd smbmap
python3 -m pip install -r requirements.txt
cd ../
cd zap-cli
python setup.py install
pip install --upgrade zapcli
cd ../
