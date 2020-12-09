# Setup

## Installation Instructions (Mac OSX)
1. Install Sushi
    ```
    $ brew install node
    $ npm install -g fsh-sushi 
    ```
2. Install jekyll
    ```
    $ brew install rbenv
    $ rbenv install 2.5.8
    $ rbenv local 2.5.8
    $ gem install --user-install bundler jekyll
    ```
3. Update the publisher
    ```
    $ cd ScheduleOfActivityIG
    $ ./_updatePublisher.sh
    ```
4. Initial build (this will depend on where you have ruby installed)
    ```
    $ cd ScheduleOfActivityIG
    $ ./_genonce.sh
    ```

## Visual Studio Code Support
1. Install `vscode-language-fsh` and call the file with an extension `.fsh`

