***Step 1***:Clone our github repository into your desired location using the below link: https://github.com/kuluruvineeth/Agrosahakar 

***Step 2***: create a VM instance on any cloud platform such as aws, azure, GCP, heroku. 

***Step 3***: Deploy RASAX server on VM instance created in step1 as mentioned in the phase 2. For detailed information please refer to the official RASA documentation:[RASA documentation](https://cdn2.hubspot.net/hubfs/6711345/ebook-v3.pdf?__hstc=123545108.89abd9a4f81cca58a8242833f77146c9.1618572135666.1618572135666.1618572135666.1&__hssc=123545108.1.1618572135666&__hsfp=1177053440&hsCtaTracking=2cf912f3-4137-4338-829e-08bb4713f0f6%7Cda22eae5-512d-48fe-b46a-c74517f3d870)

***Step 4***: Now your RASAX server will be up and running.

***Step 5***: Connect your repository to the RASAX server:

**1.Generate SSH keys:**
* Navigate back to your terminal. If you’ve closed the connection to your VM instance, log back in.
* Run the following command to generate a public and private SSH key
  * ssh-keygen -t rsa -b 4096 -f git-deploy-key

* After the key has finished generating, you can run the ls command in the /rasa/etc directory to see the newly created keys: git-deploy-key (the private key) and git-deploy-key.pub (the public key).

**2.Save the public key in GitHub:**
* We’ll print the public key to the terminal so we can copy and save it in our GitHub settings.Run the following command to view the public key:
  * cat git-deploy-key.pub
* Copy the entire contents.
In your GitHub repository, navigate to Settings>Deploy keys. Click the Add deploy key button and paste your public key into the Key box. Give the key a title to identify it, like medicare-rasax, and be sure to check the box to allow Write permissions. Click Add key.

**3.We’ll establish the connection between the Rasa X instance and GitHub repository by making a POST request to this Rasa X API endpoint.**

**4.The JSON request body contains three pieces of information:**
  * repository_url - The SSH URL for your GitHub repository, e.g. kuluruvineeth/Agrosahakar.git
  * To get the URL for your repo, click the Clone or download button on your GitHub repository and select the Use SSH link.
  * target_branch - The GitHub repository branch where Rasa X should push and pull changes, e.g. master
  * ssh_key - The private SSH key generated on your server.
To copy the private key, run the following command in the /etc/rasa folder on your server:
    * cat git-deploy-key
    * Copy the entire contents of the key, including the lines
 -----BEGIN RSA PRIVATE KEY----- 
                        And
 -----END RSA PRIVATE KEY-----
Once you’ve assembled the JSON object, you’ll have something like this:
{ "repository_url":"kuluruvineeth/Agrosahakar.git", "target_branch": "master", 
"ssh_key": "-----BEGIN RSA PRIVATE KEY-----b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAACFwAAAAdzc2gtcnNhAAAAAwEAAQAAAgEAu/Giin7t8DFMxsaTbyy1To2EQpLIAhpAIgpyC/e45NYVTwKRGCB1mxHzt5IWoh7GSWry3pKFBM74UpXxrRPBdCmFeUIiJoslAukNkRSckAUj0VEfOIZLf2SSPg...CDHniFksE1SjkAAAEBANJacZeM2Qdk/vditmBQV97Ac2VJL/Btt8Rks2Vb3CORyXQn3Bpb+5ZONhmPEoCg4FcZbAm02gYw3dSoBBWz2i8mmAv71mVsNoddWKpDngRFv4PUaITnYYxrZ4-----END RSA PRIVATE KEY-----"}
We’ll save this JSON object in a file called repository.json, in the /rasa/etc folder on the server

**5.First, let’s create that file touch repository.json**
   * Open the file to edit it:nano repository.json
Paste the JSON object into the file. Press Control + X to exit the editor, and confirm Y to save your changes when prompted.
   * Head back to the terminal. Still in the /etc/rasa directory, run the following cURL command which you will get clicking on upload model button in RASAX interface, replacing the Rasa X server URL and API key values with your own:
    * curl --request POST 
    *  --url http://<Rasa X server host>/api/projects/default/git_repositories?api_token=<your api token> 
    *  --header 'content-type: application/json' \ --data-binary @repository.json
   * Check the connection by navigating back to the Rasa X dashboard in your browser and checking the Integrated Version Control icon in the bottom left corner. If the connection was successful, you’ll see either a green indicator, meaning Rasa X is up to date with the GitHub repository, or a yellow indicator, meaning Rasa X has changes that need to be pushed to GitHub.
   
***Step 6***: Set up the Actions Server:
* We have one more thing to configure: the assistant’s custom action server. To do this, we’ll place the assistant’s custom action code within an actions directory on the server.
* Connect to your server and make sure you’re in the /etc/rasa directory. In your terminal, run the following commands to create the actions directory and two files inside it: __init__.py and actions.py:
* Run nano actions/actions.py to edit the newly-created actions.py file. 
* Paste the code from your assistant’s actions.py file into the blank file, save, and close the editor. 
* Then, we need to create a docker-compose.override.yml file. This file instructs docker-compose to spin up a custom action server when the Rasa X server starts up.
* Let’s create that file:
    **touch docker-compose.override.yml**


    Open the file editor:**nano docker-compose.override.yml**

    And add the following contents:


     **version: '3.4'**
     **services:**
     **app:** 
     **image: 'rasa/rasa-sdk:latest'**
     **volumes: - './actions:/app/actions' expose: - '5055'**
     **depends_on: - rasa-production**
* Here, we’re using the rasa-sdk image to run our custom actions, and we’re specifying that the actions server will listen on port 5055. The actions server depends on the rasa-production service, which is responsible for running the trained model, parsing intent messages, and predicting actions.
* Once you’ve saved the file, you can restart the Rasa X docker container and the assistant will be fully functional on Rasa X.
   **sudo docker-compose up -d**
***Step 7***: Eureka!!! You have done the complete set up and are ready to use our chatbot. Feel free to share your comments in github.


