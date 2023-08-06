[Read complete documentation](http://django-for-android.readthedocs.io/en/latest/index.html)

---

# Installation #

Install using **pip**.
```
#!bash

pip install djangoforandroid
```

Add **djangoforandroid.builder** to your **INSTALLED_APPS** setting.
```
#!python
INSTALLED_APPS = (
    ...
    'djangoforandroid.builder',
    'djangoforandroid.mdl', #optional
)
```

There are some additional settings that you can override. Here are all the available defaults.

Basic configuration:
```
#!python

ANDROID = {

    'APK': {
        'name': "App Name",
        'version': '0.1',
        'numericversion': 10,
        'package': 'com.djangoforandroid.appname',
        'icon': os.path.join(BASE_DIR, 'static', 'images', 'icon.png'),
    },

    'ANDROID': {
        'ARCH': 'armeabi-v7a',
        'SDK': '/absolute/path/to/android-sdk-linux',
        'API': '21',
        'CRYSTAX_NDK': '/absolute/path/to/crystax-ndk-10.3.2',
        'CRYSTAX_NDK_VERSION': '10.3.2',
    },
}
```

All configuration options with default values:

```
#!python

ANDROID = {

    'APK': {
        'name': "App Name",
        'version': '0.1',  #https://developer.android.com/studio/publish/versioning.html
        'numericversion': 10,
        'package': 'com.djangoforandroid.appname',
        'icon': os.path.join(BASE_DIR, 'static', 'images', 'icon.png'),
        'statusbarcolor': '#7c962b',
        'navigationbarcolor': '#000000',
        'orientation': 'sensor', #other options: 'portrait' and 'landscape'
        'intent_filters': None,

    },

    'ANDROID': {
        'ARCH': 'armeabi-v7a',
        'SDK': '/absolute/path/to/android-sdk-linux', #https://developer.android.com/studio/index.html
        'API': '21',
        'CRYSTAX_NDK': '/absolute/path/to/crystax-ndk-10.3.2', #https://www.crystax.net/en/download
        'CRYSTAX_NDK_VERSION': '10.3.2',
    },


    'APP': {
        'multithread': False,
    },


    #Extra configurations

    #for sign and release packages
    'KEY': {
        'RELEASE_KEYSTORE': os.path.join(BASE_DIR, 'djangoforandroid.keystore'),
        'RELEASE_KEYALIAS': 'djangoforandroid',
        'RELEASE_KEYSTORE_PASSWD': 'djangoforandroid', #use your own password
        'RELEASE_KEYALIAS_PASSWD': 'djangoforandroid',
    },

    #splash screen for your app, this is static html, NOT a Django view
    'SPLASH': {
        'static_html': False, #path to .html, resources must be added with ony name, i.e background-image: url("splash.png");
        'resources': [], #list of files used in the static html, i.e ['static/images/splash.png']
    },

    #for localserver
    'PORT': '8888',

    #extra permissions for app https://developer.android.com/reference/android/Manifest.permission.html
    'PERMISSIONS': [], #list of permissions, i.e ['BLUETOOTH', 'BLUETOOTH_ADMIN', 'CAMERA']

    #sandbox for python-for-andoid operations
    'BUILD': {
        'build': os.path.expanduser('~/.django-for-android'), #where the magic happens
        'recipes': None, #path for user recipes parent directory, check http://python-for-android.readthedocs.io/en/latest/recipes/
        'whitelist': None, #for python-for-android users
        'requirements': [], #extra python packages to install, differents to ['python3crystax', 'pyjnius', 'django', 'sqlite3', 'djangoforandroid']
        'exclude_dirs': [], #list of RELATIVE paths, this directories will not be included in the final .apk
        'include_exts': [], #list of extensions to include in final .apk, i.e ['py', 'png', 'sqlite3', 'html', 'css', 'js'], if empty then add all files
        },
}
```