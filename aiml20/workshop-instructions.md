# Workshop 1: 
# Using Pre-Built AI to Solve Business Challenges

## Workshop Abstract

TAs a data-driven company, Tailwind Traders understands the importance of using Artificial Intelligence to improve business processes and delight customers. Before investing in an AI team, their existing developers were able to demonstrate some quick wins using pre-built AI technologies. In this session, we will show how you can use Azure Cognitive Services to extract insights from retail data. We’ll go into the neural networks behind computer vision, and show how you can augment the pre-built AI with your own images for custom image recognition applications.

## Pre-reading

* **Azure Basics**
    * I would recommend getting a basic understanding of cloud technologies and Azure (storage, VMs and networking) from [Azure Fundamentals](https://docs.microsoft.com/en-us/learn/paths/azure-fundamentals/?WT.mc_id=aimlworkshop-github-amynic) 
* **Azure AI introduction**
    * (Prebuilt AI) [Classify images](https:/docs.microsoft.com/en-us/learn/paths/classify-images-with-vision-services/?WT.mc_id=aimlworkshop-github-amynic) 
    * (Prebuilt AI) [Evaluate Text](https://docs.microsoft.com/en-us/learn/paths/evaluate-text-with-language-services/?WT.mc_id=aimlworkshop-github-amynic) 
    * (Data Science) [Using Python and Azure Notebooks](https:/docs.microsoft.com/en-us/learn/paths/intro-to-ml-with-python/?WT.mc_id=aimlworkshop-github-amynic)
    * (Bespoke Machine Learning) [Introduction to Azure Machine Learning](https://docs.microsoft.com/en-us/learn/paths/build-ai-solutions-with-azure-ml-service/?WT.mc_id=aimlworkshop-github-amynic)
* **General other interesting learning:**
    * (Theory/approaches) [Machine Learning Crash Course](https://docs.microsoft.com/en-us/learn/paths/ml-crash-course/?WT.mc_id=aimlworkshop-github-amynic)
    * [Principles for Responsible AI](https:/docs.microsoft.com/en-us/learn/modules/responsible-ai-principles/?WT.mc_id=aimlworkshop-github-amynic)

## Pre-requisites

* Laptop with a modern web browser (Edge, Chrome etc)
* Access to a [Azure Subscription](https:/azure.microsoft.com/en-us/free/students/?WT.mc_id=aimlworkshop-github-amynic)
* [Visual Studio Code](https:/code.visualstudio.com/?WT.mc_id=aimlworkshop-github-amynic)
* Basic understanding of how to access code and instructions from [GitHub](https://guides.github.com/)

## Deploy the Workshop Environment:

## Clone the repository to your local machine

You will need the contents of https://github.com/microsoft/ignite-learning-paths-training-aiml/tree/master/aiml20 on your local machine. The easiest way to do this is to visit the [Developer's Guide to AI Learning Paths repository](https://github.com/microsoft/ignite-learning-paths-training-aiml) and click the "Clone or download" button. We will refer to files relative to the `aiml20` folder.

## Find your Azure Subscription ID

In the [Azure Portal](https://portal.azure.com), sign in and click on
"Subscriptions" in the left menu bar. Click on the Subscription Name you will be
using, and copy the "Subscription ID" shown there. You'll need it later when you
create resources.

Alternatively, run `az account show` in the Azure CLI and copy the `id` value
shown.

## Deploy the Tailwind Traders website.

Click the button below. This will deploy
[TailwindTraders-Website](https://github.com/Microsoft/TailwindTraders-Website)
from Github, using an ARM template to enable the Personalizer integration and ONNX-based Shop by Photo feature. ([More details about this deployment](https://github.com/microsoft/TailwindTraders-Website/blob/master/Source/Tailwind.Traders.Web/Standalone/README.md).)

[![Deploy to Azure](https://azuredeploy.net/deploybutton.svg)](https://portal.azure.com/?feature.customportal=false#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FMicrosoft%2FTailwindTraders-Website%2Fmaster%2Fazuredeploy.json)

In the form that appears, select the following options:

* Subscription: Select the subscription in which to deploy the resources

* Resource Group: resources will be created in the resource group you specify.
  We recommend choosing "New" and entering the name `aiml20-demo`. When
  you're done, you can delete this resource group to shut down the site and
  delete all associated resources.

* Location: The Azure region where the resources will be deployed. You must
  be able to deploy SQL Database and App Services in that region. 

  Note: Since Personalizer is currently only available in WestUS2 and WestEurope, it will be deployed there regardless of what you choose.

* Site Name: This will be used in the site's URL and visible publicly, and must
  be globally unique. To avoid clashes, choose `aiml20-xy` replacing `xy` with your initials, but we will refer to this name as just `aiml20` in these scripts. (If you
  choose a name that is in use, you will get "Conflict" errors during the
  deployment.)

* Site Location: Enter the short version of "Location" above, e.g. `westus2`.
  (You can get a list of short names in the Azure CLI with: `az account
  list-locations -o table`).

* Deployment mode: Choose `standalone`

* SQL Login: Enter `twt`

* SQL Password: generate and use a secure password (it must include punctuation
  and mixed case, but do not use `;`). You won't need it for our demos, so no
  need to write it down.

* Enable Personalizer: choose `true`

* Repo URL: accept the default, `https://github.com/microsoft/TailwindTraders-Website`

* Branch: accept the default, `master`

(As a backup, you can also use the Repo URL
`https://github.com/revodavid/TailwindTraders-Website` with the branch `aiml20`.
This was forked on 2019-10-25 and is known to work.)

Check "I agree to the terms and condtions" and click "Purchase".

>*This could take around 15 minutes to deploy, continue the task and check back* 

The deployed website URL will be of the form SITENAME.azurewebsites.net (using the Site Name you provided above), or you can find it as follows:

* click "Go To Resource" under "Next Steps"

* Click the "App Service" resource

* Look at the "URL" value displayed in the right pane

The website URL will be displayed after the "Setting up Source Control" step, or you can inspect the "App Service" resource.

### Install the "Simple" ONNX model

Follow the instructions in [DEMO ONNX deployment.md](DEMO%20ONNX%20deployment.md#load-the-simple-onnx-model) under the heading "Load the Simple ONNX model". This will degrade the "Shop by Photo" tool in the app to only recognize hammers and drills.

## Configure Visual Studio Code

Install the extension [Azure
Account](https://marketplace.visualstudio.com/items?itemName=ms-vscode.azure-account).
(On Windows, you will also need to [install node.js](https://nodejs.org/).) In VS Code, log
into Azure with the "Azure: Sign In" command (use Control-Shift-P to open the
Command Palette). To run Azure CLI commands from a script in VS Code, use
"Terminal: Run Selected Text in Azure Terminal" to copy commands.)

Alternatively you can [install the Azure
CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest&WT.mc_id=https://docs.microsoft.com/cli/azure/install-azure-cli?view=azure-cli-latest&WT.mc_id=msignitethetour2019-github-aiml20)
on your local Windows, MacOS or Linux machine. If you don't have it installed,
you can also launch the [Azure Cloud
Shell](https://docs.microsoft.com/en-us/azure/cloud-shell/overview?WT.mc_id=msignitethetour2019-github-aiml20)
and run these commands from a browser window. 

## Prepare Visual Studio for demo

- Open `vision_demo.sh`
- launch a Cloud Shell with "Azure: Open Bash In Cloud Shell". (If you prefer, you can use the Azure CLI locally.)   

## Open browser pages ready to demo.

* The deployed Tailwind Trader app 
* https://portal.azure.com/?feature.customportal=false#home (browse to resources - note this link shows the public portal, not the preview version for those with access)  
* https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/
* https://customvision.ai
* https://lutzroeder.github.io/netron/

## Find the image files on your local machine

Once you have cloned the repository, you can find the training images in the `aiml20/CV Training Images` folder. You will
use these images to train the Custom Vision model. The folder contains the following subfolders:

* drills
* hammers
* hard hats
* pliers
* screwdrivers

These images will be used to test the Computer Vision service and create a model
with the Custom Vision service.

These images were sourced from Wikimedia Commons and used under their respective
Creative Commons licenses. See the file [ATTRIBUTIONS.md](https://github.com/microsoft/ignite-learning-paths-training-aiml/blob/master/aiml20/CV%20training%20images/ATTRIBUTIONS.md) for
details.

Additional test images can be found in the `test images` folder. These images will not be used in
training, but will be used to test that our models are working.

## Task 1: Azure Cognitive Services, Computer Vision


## Task 2: Azure Custom Vision


## Task 3: ONNX deployment


## Task 4: Azure Cognitive Services, Personalizer


## Resources and Continued Learning

### Cognitive Services information

* Cognitive Services pricing: https://aka.ms/cs-pricing 
* Cognitive Services compliance and privacy: https://aka.ms/az-compliance
* Microsoft's approach to ethical AI: [https://microsoft.com/AI/our-approach-to-ai](https://www.microsoft.com/AI/our-approach-to-ai?rtc=1&WT.mc_id=msignitethetour2019-github-aiml20)
* Cognitive Services training courses in Microsoft Learn: https://aka.ms/AIML20MSLearnCollection
* Microsoft Certified Azure Data Scientist Associate: https://aka.ms/DataScientistCert 
* Microsoft Certified Azure AI Engineer Associate https://aka.ms/AIEngineerCert

### Azure Cognitive Services docs and apps
* Cognitive Services Computer Vision: [https://aka.ms/try-computervision](https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/?WT.mc_id=ignitetour-talk-davidsmi)  
* Cognitive Services Custom Vision: [Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/?WT.mc_id=ignitethetour-github-davidsmi) and application at [https://customvision.ai](https://www.customvision.ai/?WT.mc_id=ignitethetour-github-davidsmi)
* ONNX Runtime: https://github.com/microsoft/onnxruntime
* Cognitive Services Personalizer: [https://aka.ms/personalizer-intro](https://docs.microsoft.com/en-us/azure/cognitive-services/personalizer/?WT.mc_id=msignitethetour2019-github-aiml20)
* Reinforcement Learning with Personalizer: https://aka.ms/personalizerdemo
* Cognitive Services in containers: https://aka.ms/cs-containers


