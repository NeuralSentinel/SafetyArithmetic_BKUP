pipeline {
    agent any
    environment {
        PATH = "/usr/local/bin:/usr/bin:/bin" // Your explicit PATH setup
        OPENAI_API_KEY = credentials('OPENAI_API_KEY') // API key for OpenAI
        GITHUB_TOKEN = credentials('GITHUB_TOKEN')     // GitHub token
    }
    stages {
        stage('Prepare Environment') {
            steps {
                sh '''
                # Ensure Docker is available
                which docker
                docker --version
                '''
            }
        }
        stage('Run Code Review in Docker') {
            steps {
                sh '''
                # Pull the Python 3.9 image (if not already pulled)
                docker pull python:3.9

                # Run a Docker container and execute the review script
                docker run --rm \
                    -e OPENAI_API_KEY=$OPENAI_API_KEY \
                    -e GITHUB_TOKEN=$GITHUB_TOKEN \
                    python:3.9 /bin/bash -c "
                        # Install dependencies
                        python -m pip install --upgrade pip
                        pip install openai PyGithub GitPython

                        # Run your Python script
                        python -c review_pr.py
                    "
                '''
            }
        }
    }
}








// pipeline {
//     agent any
//     environment {
//         // Explicitly define PATH, ensuring /bin and /usr/bin are included
//         PATH = "/usr/local/bin:/usr/bin:/bin"
//     }
//     stages {
//         stage('Run Docker') {
//             steps {
//                 sh 'which docker'
//                 sh 'docker run --rm hello-world'
//             }
//         }
//     }
// }


// pipeline {
//     agent {
//         docker {
//             image 'NeuralSentinel/jenkins-openai-prreview:latest'
//             args '-u root:root'
//         }
//     }
//     environment {
//         OPENAI_API_KEY = credentials('openai_api_key')
//         GITHUB_TOKEN   = credentials('github_token')
//         GITHUB_REPO    = "your-username/my-awesome-repo"
//     }
//     stages {
//         stage('Checkout') {
//             steps {
//                 checkout scm
//             }
//         }

//         stage('Prepare') {
//             steps {
//                 sh 'git fetch origin main'
//             }
//         }

//         stage('Run OpenAI Review') {
//             steps {
//                 sh 'python3 review_pr.py'
//             }
//         }

//         stage('Archive') {
//             steps {
//                 archiveArtifacts artifacts: 'review_output.txt', onlyIfSuccessful: false
//             }
//         }
//     }
// }

