# Lacuna Android

This is a standalone Android Studio project for the Lacuna mobile app. It wraps the Lacuna Flask web application in a native Android WebView.

## Upload To GitHub

Upload the contents of this `lacuna-android/` folder as its own GitHub repository.

Keep these files and folders:

```text
app/
gradle/
build.gradle
gradlew
gradlew.bat
settings.gradle
README.md
.gitignore
```

Do not upload generated local files such as `.gradle/`, `.idea/`, `build/`, `app/build/`, or `local.properties`.

## Run With Local Flask Server

Start the Flask app on your computer:

```bash
flask --app news run --host 0.0.0.0 --port 5001
```

The Android emulator can reach your computer at:

```text
http://10.0.2.2:5001
```

That is the default value in:

```text
app/src/main/res/values/strings.xml
```

## Use Hosted App

After deploying Lacuna to Render, Railway, or another host, replace `lacuna_url` with your public HTTPS URL:

```xml
<string name="lacuna_url">https://your-app-url.onrender.com</string>
```

## Open In Android Studio

Open this folder in Android Studio, let Gradle sync, then run the `app` configuration on an emulator or Android phone.
