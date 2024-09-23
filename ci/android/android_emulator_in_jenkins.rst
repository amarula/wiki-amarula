Android emulator in docker/jenkins pipeline
*******************************************

Create android emulator
=======================

To create an emulator, use the following steps in DockerFile.

    1. Define Android version **e.g. android-25**
    2. Define emulator architecture **e.g. arm, x86 etc**
    3. Complete emulator package.
    4. Make **.android** directory in **$JENKINS_HOME**. This path will be used by android emulator to store data. If we don't provide our path it will use **~/.android** to store data and this path cannot be accessed without root access.
    5. Add **ANDROID_AVD_HOME** environment variable. Point variable to the directory created in **point 4**.
    6. Define unique emulator name and set it to **EMULATOR_NAME** environment variable.
    7. Create emulator using avdmanager command. Use **EMULATOR_NAME** defined in **point 6** and **ANDROID_EMULATOR_PACKAGE** defined in **point 3**.

Example:

::

            ARG ANDROID_VERSION="android-25"
            ARG EMULATOR_ARCH="armeabi-v7a"
            ARG ANDROID_EMULATOR_PACKAGE="system-images;${ANDROID_VERSION};google_apis;${EMULATOR_ARCH}"
            
            RUN mkdir $JENKINS_HOME/.android
            ENV ANDROID_AVD_HOME="/home/jenkins/.android/avd"
            ENV EMULATOR_NAME="android_emulator"
            RUN echo "no" | avdmanager --verbose create avd --force --name "${EMULATOR_NAME}" --device "pixel" -k "${ANDROID_EMULATOR_PACKAGE}"


Add Emulator start script
=========================

Create a shell script and add the following lines in it.

Use **emulator** command to start emulator. Use **EMULATOR_NAME** environment variable(defined in step **Create android emulator**), to start the emulator. 

Since emulator can take some time to boot, so we have to check if emulator is fully booted and ready to run app. For that we can use **adb shell getprop sys.boot_completed** command to check status of emulator in **while loop**.

Example Script:

::

            adb devices | grep emulator | cut -f1 | while read line; do adb -s $line emu kill; done
            emulator -avd "${EMULATOR_NAME}" -verbose -wipe-data -no-snapshot -no-window -no-audio &
            while [ "$(adb shell getprop sys.boot_completed | tr -d '\r')" != "1" ]; do
                echo "Still waiting for boot.."
                sleep 1
            done

We have to add this script in our **Dockerfile**, so that we can run it from **Jenkins pipeline**.

Example:

::

            ADD script.sh /

Start Emulator from Jenkins pipeline
====================================

We can use the **shell script** created above to start the emulator from **jenkins pipeline**.

Example pipeline:

::

            #!groovy
        
            import com.amarula.build.Build
            
            node('android-build') {
                def build = new Build(this, env, 'abc123')
                def repoUrl = "https://github.com/yourRepo"
            
                final def dockerImage = 'android-with-emulator:1.0'
            
                build.build(repoUrl, {
                    
                    sh 'chmod +x gradlew'
            
                    sh '. /start_emulator.sh'
                    sh './gradlew connectedAndroidTest'
            
                }, [branch: "master", history: true, dockerImage: dockerImage, gerritRemoteUrl: env.GERRIT_HTTPS_URL])
            }
