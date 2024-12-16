pipeline {
    agent any
    environment {
        PATH = "/usr/local/bin:/usr/bin:/bin"
        OPENAI_API_KEY = credentials('OPENAI_API_KEY')
        GITHUB_TOKEN   = credentials('GITHUB_TOKEN')
    }
    stages {
        stage('Prepare Environment') {
            steps {
                sh '''
                    echo "Verifying Docker availability..."
                    which docker
                    docker --version
                '''
            }
        }
        stage('Run Code Review in Docker') {
            steps {
                // Use triple-quoted string to easily quote the volume path
                sh """
                    # Pull Python 3.9 image if not already available
                    docker pull python:3.9
                    
                    # Make sure we quote the local path with spaces
                    docker run --rm \\
                        -v "/Users/somnbane/.jenkins/workspace/Automated PR Review:/workspace" \\
                        -w /workspace \\
                        -e OPENAI_API_KEY=\$OPENAI_API_KEY \\
                        -e GITHUB_TOKEN=\$GITHUB_TOKEN \\
                        -e GITHUB_REPO=\$GITHUB_REPO \\
                        -e CHANGE_ID=\$CHANGE_ID \\
                        python:3.9 /bin/bash -c "
                            python -m pip install --upgrade pip
                            pip install openai PyGithub GitPython
                            python review.py
                        "
                """
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

