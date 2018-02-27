# FlatKivyExtensions


Goal: rapid utility application development

- Minimal UI development effort

- Avoid dependency on buildozer or ios toolchain to test applications on Android or iOS respectively.

    - Application can be updated just by copying raw python code 

        - Application can be updated without required devepment environments or specific hardware

     - However: 
        
         - Code used for testing does not go through cythonization process

         - iOS version would not pass application validation process


Components:

- Application abstraction based on Flat Kivy assuming kivy_1.10

    - Application consists of NavigationDrawer, header and ScreenManager
    
       - For each screen assigned to the ScreenManager there is an associated button used to navigate to that screen
    
    - Application components configured by specifying:
    
        - Application title
        - Application 'about' information
        - List used to configure navigation panel 

- Launcher applications for Android and iOS built with kivy_1.10

    - Similar to Kivy launcher app for android:
    
        - Launcher source generated from one-time build process with trivial kivy example:
        
            - buildozer for android in ubuntu VM 
            
                - Patches: Modify PythonActivity.java and PythonService.java to configure application paths at runtime
                
                - Android Sudio project can (will) be found at.... <android studio project>
            
            - kivy-ios toolchain build and app generation with toolchain.py create ...
            
                - Patches: Modify main.py to configure application paths at runtime
                
                - Xcode project can (will) be found at ... <xcode project>

    - Developer specifies application path and python path extensions via a launcher_config.txt file
    
        - Path specifications need to be relative to writable memory
        
            - On Android relative to /sdcard/  (or /storage/emulated/0/)
            
            - On iOS relative to launcher application's Document folder.  iOS launcher built with filesharing enabled

