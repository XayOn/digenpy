#!/bin/bash - 
#===============================================================================
#
#          FILE:  Package_generator
# 
#         USAGE:  ./generate_debian_package.sh 
# 
#   DESCRIPTION:  Generates packages for debian and exes
# 
#       OPTIONS:  [deb] [exe] [apk]
#  REQUIREMENTS:  python-stdeb
#          BUGS:  None described
#         NOTES:  None
#        AUTHOR:  David Francos Cuartero (XayOn)
#       COMPANY: 
#       CREATED:  22/07/11 05:10:10 CEST
#      REVISION:  0.1
#===============================================================================
export ANDROID_SDK_HOME=/home/xayon 
ANDROID_SDK="/usr/share/android-sdk/"
ANDROID_SDK_TOOLS="${ANDROID_SDK}/tools"
Package="Digenpy"
package="Digenpy"
version=1.3.4
user=xayon
owner=XayOn
remote_host=192.168.1.10
path=`pwd`
#opts="-us -uc"  # Enable if you're not me 
export ANDROID_SDK 

mkdeb(){
    python setup.py sdist
    py2dsc dist/$package-${version}.tar.gz
    cd deb_dist/$package-${version}/
    dpkg-buildpackage ${opts}
    cd ../.. 
}

mktar(){ python setup.py bdist tar; }
launch_vm(){ VBoxHeadless --vrde off -s $1 & }
stop_vm(){ VBoxManage controlvm windows poweroff ; }
mkexe(){
    echo "Stopping previous virtual machines"
    stop_vm
    echo "Launching windows virtual machine"
    launch_vm windows
    sleep 30;
    echo "Copying data"
    scp -r * $remote_host:build
    echo "Executing setup.bat"
    ssh $remote_host "cd build && setup.bat"
    echo "Setup.bat has been executed"
}

mkapk(){
    echo "Making apk, generating android key if not exists.";
    [[ ! -e /home/$user/.android.keystore ]] && _gen_new_android_key
    echo "Checkout to git branch"
    git checkout android
    echo "Making ant release, signing and zipaligning it"
    ant release && jarsigner -verbose -keystore /home/$user/.android.keystore ./bin/$package-release-unsigned.apk $owner
    $ANDROID_SDK_TOOLS/zipalign -v 4 ./bin/$Package-release-unsigned.apk releases/$Package-$version.apk
    echo "Now installing into the virtual machine"
    $ANDROID_SDK/platform-tools/adb install -r releases/$Package-$version.apk
}

_gen_new_android_key(){
    keytool -genkey -v -keystore /home/$user/.android.keystore \
    -alias $owner -keyalg RSA -keysize 2048 -validity 10000
}

[[ "$1" == "" ]] && {
     source $(source_jabashit)
     load TUI screen_display
     mkmenu -t "Wich package do you want to do" -o "Debian" -f mkdeb -o "Windows installer" -f mkexe -o "Android APK" -f mkapk
} || { 
    [[ $1 ]] && mk$1; 
}
