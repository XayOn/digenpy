#!/bin/bash

package=$1
package_dir=$(echo src/$package|sed 's/\./\//g')
mkdir -p $package_dir
mv src/com/wireless/digenpy/* $package_dir/
rmdir src/com/wireless/digenpy
rmdir src/com/wireless
rmdir src/com
source_files=$package_dir/*
for filename in $source_files AndroidManifest.xml build.properties;
do
	sed 's/com\.wireless\.digenpy/'$package'/g' $filename > tmp; mv tmp $filename;
done
