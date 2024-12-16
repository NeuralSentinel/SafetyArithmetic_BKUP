pipeline {
    agent any
    environment {
        PATH = "/usr/local/bin:/usr/bin:/bin" // Explicitly define PATH as in your original pipeline
        OPENAI_API_KEY = credentials('OPENAI_API_KEY') // Securely fetch API key from Jenkins credentials
        GITHUB_TOKEN = credentials('GITHUB_TOKEN')     // Securely fetch GitHub token from Jenkins credentials
    }
    stages {
        stage('Prepare Environment') {
            steps {
                sh '''
                # Verify Docker is available
                which docker
                docker --version
                '''
            }
        }
        stage('Run Code Review in Docker') {
            steps {
                sh '''
                # Pull Python 3.9 Docker image
                docker pull python:3.9

                # Run the Docker container to execute the script
                docker run --rm \
                    -v $PWD:/workspace \  # Mount workspace to container
                    -w /workspace \       # Set working directory inside the container
                    -e OPENAI_API_KEY=$OPENAI_API_KEY \ # Pass environment variables
                    -e GITHUB_TOKEN=$GITHUB_TOKEN \
                    python:3.9 /bin/bash -c "
                        # Install dependencies
                        python -m pip install --upgrade pip
                        pip install openai PyGithub GitPython

                        # Execute the script
                        python .github/actions/code_review.py
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

