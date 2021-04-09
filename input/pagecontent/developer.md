# Setup

**NOTE** This is a temporary page - it will not be included in the final IG

## Tutorials:
* [https://fshschool.org/](https://fshschool.org/)

## Repository
* The repository for this project is currently [fhir-schedule-of-activities-ig](https://github.com/phuse-org/fhir-schedule-of-activities-ig) (it will be migrated to the HL7 org at some point)
* The documentation is being automatically built and is available [here](https://phuse-org.github.io/fhir-schedule-of-activities-ig/)


## Recommended Editor 
* We **strongly** recommend the [Visual Studio Code](https://code.visualstudio.com/) editor for this!

## Installation Instructions (Mac OSX)
1. Install Sushi
    ```shell
    $ brew install node
    $ npm install -g fsh-sushi 
    ```
2. Install jekyll
    ```shell
    $ brew install rbenv
    $ rbenv install 2.5.8
    $ rbenv local 2.5.8
    $ gem install --user-install bundler jekyll
    ```
3. Update the publisher
    ```shell
    $ ./_updatePublisher.sh
    ```
4. Initial build (this will depend on where you have ruby installed)
    ```shell
    $ PATH=$PATH:~/.gem/ruby/2.5.8/bin ./_genonce.sh
    ```

## Installation Instructions (Windows)
1. Install Node
    * https://nodejs.org/en/download/ - download and install the Windows Installer 
2. Install Visual Studio Code 
    * https://code.visualstudio.com/download - download and install the Windows Installer
3. Install Jekyll 
    * Follow the instructions on https://jekyllrb.com/docs/installation/windows/
4. Install the VS Code extension for FSH
    * https://marketplace.visualstudio.com/items?itemName=kmahalingam.vscode-language-fsh 
5. Start VS Code and open a terminal (CTRL + `) and in the terminal run the following
    ```shell
    $ npm install -g fsh-sushi 
    ```
6. Update the publisher
    ```shell
    $ ./_updatePublisher.sh
    ```
7. Build
    ```shell
    $ ./_genonce.sh
    ```



