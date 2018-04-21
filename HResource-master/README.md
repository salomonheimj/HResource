# [Fast Medical Solutions](http://hresource-imperative-manslayer.mybluemix.net/)

## Run the app locally
```
pip install -r requirements.txt
```
You can optionally use a virtual environment to avoid having these dependencies clash with those of other Python projects or your operating system.

Run the app.
```
python fms.py
```

 View the app at: http://localhost:8000

## Deploy the app

Choose your API endpoint
   ```
cf api https://api.ng.bluemix.net
   ```
Login to your Bluemix account
  ```
cf login
  ```
From within the HResource directory push your app to Bluemix
  ```
cf push
  ```

This can take a minute. If there is an error in the deployment process you can use the command `cf logs <Your-App-Name> --recent` to troubleshoot.

When deployment completes you should see a message indicating that your app is running.  View your app at the URL listed in the output of the push command.  You can also issue the
```
cf apps
```
command to view your apps status and see the URL.

```

View the app at http://hresource-imperative-manslayer.mybluemix.net/
