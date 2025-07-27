pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('sonar-token')
        ARTIFACTORY_URL = 'https:///artifactory/api/pypi/flask-app-pypi'
    }

    stages {
        stage('checkout') {
            steps {
                git 'https://github.com/jitendrasahu1803/flask-app.git'
            }
        }

        stage('build') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python -m py_compile app.py'
            }
        }

        stage('Unit Test') {
            steps {
                sh 'pytest tests/'
            }
        }

        stage('Artifact Upload') {
            steps {
                sh '''
                mkdir -p artifacts
                cp app.py artifacts
                curl -u $ARTIFACTORY_USER:$ARTIFACTORY_PASS -T artifacts/app.py "$ARTIFACTORY_URL/flask-app/app.py"
                '''
            }
        }

        stage('Deploy to Dev') {
            steps {
                ansiblePlaybook(
                    playbook: 'ansible/deploy.yml',
                    inventory: 'ansible/inventory/dev.ini'
                    )
            }
        }

        stage('Deploy to QA') {
            steps {
                ansiblePlaybook(
                    playbook: 'ansible/deploy.yml',
                    inventory: 'ansible/inventory/qa.ini'
                    )
            }
        }

        stage('Deploy to UAT') {
            steps {
                ansiblePlaybook(
                    playbook: 'ansible/deploy.yml',
                    inventory: 'ansible/inventory/uat.ini'
                    )
            }
        }

        stage('Deploy to prod') {
            steps {
                ansiblePlaybook(
                    playbook: 'ansible/deploy.yml',
                    inventory: 'ansible/inventory/prod.ini'
                    )
            }
        }
    }

    post {
        always {
            slackSend(channel: '#ci-cd-updates', message: "Pipeline finished for ${env.BUILD_TAG}")
        }
        failure {
            mail to: 'jitendra.sahu1803@gmail.com',
                subject: "Build Failed: ${env.JOB_NAME}",
                body: "Check Jenkins for details: ${env.BUILD_URL}"
        }
    }
}
