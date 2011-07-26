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

ANDROID_SDK="/usr/share/android-sdk/"
Package="Digenpy"
package="digenpy"
version=1.3.4
user=xayon
owner=XayOn
remote_host=192.168.1.13
#opts="-us -uc"  # Enable if you're not me 

mkdeb(){
    python setup.py sdist
    py2dsc dist/$Package-${version}.tar.gz
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
    sleep 90;
    echo "Executing setup.bat"
    ssh $remote_host devel/$package/setup.bat
    echo "Setup.bat has been executed"
}

mkapk(){
    echo "Making apk, generating android key if not exists.";
    [[ ! -e /home/$user/.android.keystore ]] && _gen_new_android_key
    echo "Checkout to git branch"
    git checkout android
    echo "Making ant release, signing and zipaligning it"
    ant release && jarsigner -verbose -keystore /home/$user/.android.keystore $package.apk $owner
    zipalign -v 4 $package.apk $package-1.apk
    mv $package-1.apk $package.apk
    echo "Now installing into the virtual machine"
    $ANDROID_SDK/adb install bin/$package.apk
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
