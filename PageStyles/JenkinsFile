pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                python application.py
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                curl -i http://127.0.0.1:8080/
                echo $'\cc' | application.py
            }
        }
    }
}