pipeline {
    agent {
        docker {
            image 'python:3.9' // Use Python 3.9 Docker image
            args '-u root'     // Run as root to allow package installations
        }
    }
    environment {
        OPENAI_API_KEY = credentials('OPENAI_API_KEY') // Securely fetch API key from Jenkins credentials
        GITHUB_TOKEN = credentials('GITHUB_TOKEN')     // Securely fetch GitHub token from Jenkins credentials
    }
    stages {
        stage('Checkout repository') {
            steps {
                // Use a plugin or script to check out the repository
                checkout scm
            }
        }
        stage('Install dependencies') {
            steps {
                sh '''
                # Upgrade pip
                python -m pip install --upgrade pip

                # Install required Python packages
                pip install openai PyGithub GitPython
                '''
            }
        }
        stage('Run Code Review') {
            steps {
                sh '''
                # Execute the code review script
                python .github/actions/code_review.py
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

