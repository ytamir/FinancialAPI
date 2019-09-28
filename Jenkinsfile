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
                sh 'python application.py'
                sh 'curl http://127.0.0.1:8080/ > result'
                def output = readFile('result').trim()
                echo "output=$output";
            }
        }
    }
}