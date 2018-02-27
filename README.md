# FlatKivyExtensions


Goal: facilitate rapid utility application development with reduced UI implementation effort

Components: requires using kivy 1.10

- Application abstraction based on FlatKivy with the NavigationDrawer from kivy garden ( https://github.com/Kovak/FlatKivy and https://github.com/kivy-garden/garden.navigationdrawer respectively)

    - Application consists of NavigationDrawer, header and ScreenManager
    
       - For each screen assigned to the ScreenManager there is an associated button used to navigate to that screen
    
    - Application components configured by specifying:
    
        - Application title
        - Application 'about' information
        - List used to configure navigation panel 


# This should all go into a separate repo - here for now to collect thoughts

Goal: provide configurable kivy launcher app for Android and iOS

- Avoid dependency on buildozer or ios toolchain to test applications on Android or iOS respectively.

    - Application can be updated just by copying raw python code and specifying launcher configuration 

        - Does not require any mobile devepment environments or specific hardware

     - However: 
        
         - Code used for testing does not go through cythonization process

         - iOS version would not pass application validation process

Components:

- Launcher application projects for Android and iOS built with kivy_1.10

    - Similar to Kivy launcher app for android:
    
        - Launcher source generated from one-time build process with trivial kivy example.  Steps applied:
        
            - Android: Run buildozer in ubuntu VM with 'simpleApp' as the target application
            
                - Patches: 
                    - Modify PythonActivity.java and PythonService.java to configure runtime application paths from /sdcard/launcher_config.txt
                
                - Android Sudio project can (will) be found at.... <android studio project>
            
            - iOS: use kivy-ios toolchain to build the environment, then use 'toolchain.py create ...' applied to the 'simpleApp' target applictation folder
            
                - Patches: 
                    - Modify main.py to configure runtime application paths from launcher_config.txt copied to applications shared documents folder
                    - Remove scripts run in Build Phaeses for synchronizing and cyntonizing python application code 
                    - Make all paths to required 'dist' directory relative (hand edited the project.pbxproj)
                    - Add a directory to applications resources that is copied to the application documents folder when the app starts (if it is not already there)
                
                - Xcode project can (will) be found at ... <xcode project>

    - Developer specifies application path and python path extensions via a launcher_config.txt file
    
        - Same launcher_config.txt applied to both Android and iOS launchers
        
        - Path specifications need to be relative to writable memory
        
            - On Android relative to /sdcard/  (or /storage/emulated/0/)
            
            - On iOS relative to launcher application's Document folder.  iOS launcher built with filesharing enabled

