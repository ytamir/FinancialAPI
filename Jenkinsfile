pipeline {
    agent any
    stages {
        stage('Build') {
            environment {
                PYTHONPATH = '/var/lib/jenkins/workspace/FinancialAnalysis_master/:/usr/lib/python2.7/site-packages/'
            }
            steps {
                echo 'Building..'
                checkout scm
                sh 'pip install -r requirements.txt --user'
                sh 'python application.py &'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Run') {

            steps {
                echo 'Running....'
                sleep 10
                sh 'curl --verbose http://127.0.0.1:1025/'
            }
        }
    }
}