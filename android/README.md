# Lacuna Android

This is a lightweight Android WebView app for the Flask Lacuna web application.

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

Open the `android/` folder in Android Studio, let Gradle sync, then run the `app` configuration on an emulator or Android phone.

