scp -i ~/.ssh/jondy_ubuntu_svr_id_rsa \
    jondy@192.168.121.103:/home/jondy/workspace/pyarmor/src/platforms/linux_x86_64/_pytransform.so \
    ./linux_x86_64

scp -i ~/.ssh/jondy_ubuntu_svr_id_rsa \
    jondy@192.168.121.103:/home/jondy/workspace/pyarmor/src/platforms/macosx_intel/_pytransform.dylib \
    ./macosx_intel

scp -i ~/.ssh/jondy_ubuntu_svr_id_rsa \
    jondy@192.168.121.103:/home/jondy/workspace/pytransform/cross-platform/raspberrypi/build/.libs/_pytransform.so \
    ../extra-platforms/raspberrypi

scp -i ~/.ssh/jondy_ubuntu_svr_id_rsa \
    jondy@192.168.121.103:/home/jondy/workspace/pytransform/cross-platform/bananapi/build/.libs/_pytransform.so \
    ../extra-platforms/ts-4600

scp jondy@192.168.121.106:/home/jondy/workspace/pytransform/cross-platform/ts-4600/build/.libs/_pytransform.so \
    ../extra-platforms/bananapi
    
scp jondy@192.168.121.106:/home/jondy/workspace/pyarmor/src/platforms/linux_i386/_pytransform.so \
    ./linux_i386
