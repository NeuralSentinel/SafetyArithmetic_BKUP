pipeline {
    agent {
        docker {
            image 'NeuralSentinel/jenkins-openai-prreview:latest'
            args '-u root:root'
        }
    }
    environment {
        OPENAI_API_KEY = credentials('openai_api_key')
        GITHUB_TOKEN   = credentials('github_token')
        GITHUB_REPO    = "your-username/my-awesome-repo"
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare') {
            steps {
                sh 'git fetch origin main'
            }
        }

        stage('Run OpenAI Review') {
            steps {
                sh 'python3 review_pr.py'
            }
        }

        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'review_output.txt', onlyIfSuccessful: false
            }
        }
    }
}

