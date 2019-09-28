pipeline {
    agent any
    environment {
        PYTHONPATH=$PYTHONPATH:'ConfigFiles':'PageCallbacks':'PageLayouts':'PageStyles':'PyhonRequestFiles'
    }
    stages {
        stage('Build') {
            steps {
                echo 'Building..'

                echo "Database engine is ${PYTHONPATH}"
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
                sh 'curl http://127.0.0.1:8080/'
            }
        }
    }
}