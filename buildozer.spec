[app]
title = Autotyper
package.name = autotyper
package.domain = org.example

[buildozer]
log_level = 2

[app]
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

[app]
requirements = python3,kivy,requests,android

[app]
permissions = INTERNET, SYSTEM_ALERT_WINDOW

[app]
android.api = 33
android.minapi = 21