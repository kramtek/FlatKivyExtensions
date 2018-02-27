# FlatKivyExtensions


Goal: rapid utility application development

    - Minimal UI development effort

    - Avoid dependency on buildozer or ios toolchain to test applications on Android or iOS respectively.

        - Application can be updated just by copying raw python code 

            - Application can be updated without required devepment environments or specific hardware

        - However: Code used for testing does not go through cythonization process


Components:

    - Application abstraction based on Flat Kivy

    - Launcher applications for Android and iOS

        - Similar to Kivy launcher app for android

        - Developer specifies application path and python path extensions via a launcher_config.txt file

