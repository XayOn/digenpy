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
#opts="-us -uc"  # Enable if you're not me 


mkdeb(){
    python setup.py sdist
    py2dsc dist/$Package-${version}.tar.gz
    cd deb_dist/$package-${version}/
    dpkg-buildpackage ${opts}
    cd ../.. 
}

mkexe(){
    echo ""
}

mkapk(){
    echo "";
    [[ ! -e /home/xayon/.android.keystore ]] && _gen_new_android_key
    git checkout android
    ant release && jarsigner -verbose -keystore /home/xayon/.android.keystore $package.apk XayOn
    zipalign -v 4 $package.apk $package-1.apk
    mv $package-1.apk $package.apk
    echo "Now installing into the virtual machine"
    $ANDROID_SDK/adb install bin/$package.apk
}

_gen_new_android_key(){
    keytool -genkey -v -keystore /home/xayon/.android.keystore \
    -alias XayOn -keyalg RSA -keysize 2048 -validity 10000
}

[[ "$1" == "" ]] && {
     source $(source_jabashit)
     load TUI screen_display
     mkmenu -t "Wich package do you want to do" -o "Debian" -f mkdeb -o "Windows installer" -f mkexe -o "Android APK" -f mkapk
} || { 
    [[ $1 ]] && mk$1; 
}
