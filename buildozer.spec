[app]
title = Autotyper
package.name = autotyper
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json

version = 0.1
requirements = python3,kivy,requests

[buildozer]
log_level = 2

[android]
api = 33
minapi = 21
ndk = 25b
permissions = INTERNET

[android:meta-data]
android.app.uses_cleartext_traffic = true

[app]
orientation = portrait
fullscreen = 0
