# Setup

## Tutorials:
* [https://fshschool.org/](https://fshschool.org/)

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
    $ cd ScheduleOfActivityIG
    $ ./_updatePublisher.sh
    ```
4. Initial build (this will depend on where you have ruby installed)
    ```shell
    $ cd ScheduleOfActivityIG
    $ ./_genonce.sh
    ```

## Visual Studio Code Support
1. Install `vscode-language-fsh` and call the file with an extension `.fsh`

