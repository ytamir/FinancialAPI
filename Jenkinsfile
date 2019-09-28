pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                checkout scm
                sh 'pip install -r requirements.txt'
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
            }
        }
    }
}