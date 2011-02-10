;--------------------------------
;Include Modern UI

  !include "MUI.nsh"

;--------------------------------
;General

  ;Name and file
  Name "Digenpy"
  OutFile "Digenpy.exe"

  ;Default installation folder
  InstallDir "$PROGRAMFILES\Digenpy"
 
  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\Digenpy" ""

;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING

;--------------------------------
;Pages

  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_LICENSE "License.txt"
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
 
  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH
;--------------------------------
;Languages
 
  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

Section "Package" SecDummy

  SetOutPath "$INSTDIR"
 
   File "dist\*.*"
   
  ;Store installation folder
  WriteRegStr HKCU "Software\Digenpy" "" $INSTDIR
 
  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  CreateShortCut "$INSTDIR\Digenpy.lnk" "$INSTDIR\Digenpy.exe"
  SetOutPath "$SMPROGRAMS\Digenpy\"
  CopyFiles "$INSTDIR\Digenpy.lnk" "$SMPROGRAMS\MegSoft Solutions\"
  CopyFiles "$INSTDIR\Digenpy.lnk" "$DESKTOP\"
  Delete "$INSTDIR\Digenpy.lnk" 
  CreateShortCut "$SMPROGRAMS\GemSoft Solutions\Uninstall.lnk" "$INSTDIR\Uninstall.exe"

SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_SecDummy ${LANG_ENGLISH} "Main Package"

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDummy} $(DESC_SecDummy)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall" 

  Delete "$INSTDIR\*.*"

  Delete "$DESKTOP\Digenpy.lnk"
  Delete "$SMPROGRAMS\Digenpy\Digenpy.lnk"
  Delete "$SMPROGRAMS\Digenpy\Uninstall.lnk"

  RMDir  "$SMPROGRAMS\Digenpy\"

  RMDir /r "$INSTDIR\etc\"   
  RMDir /r "$INSTDIR\lib\"
  RMDir /r "$INSTDIR\share\"

  RMDir "$INSTDIR"

  DeleteRegKey /ifempty HKCU "Software\Digenpy"

SectionEnd

