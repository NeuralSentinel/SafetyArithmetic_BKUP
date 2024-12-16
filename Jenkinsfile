pipeline {
    agent any
    
    environment {
        // Your explicit PATH setup
        PATH = "/usr/local/bin:/usr/bin:/bin"
        
        // Jenkins credentials
        OPENAI_API_KEY = credentials('OPENAI_API_KEY')
        GITHUB_TOKEN   = credentials('GITHUB_TOKEN')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Verify Files') {
            steps {
                // List files in the workspace to confirm review.py is present
                sh 'ls -la'
            }
        }
        
        stage('Prepare Environment') {
            steps {
                sh '''
                    echo "Verifying Docker availability..."
                    which docker
                    docker --version
                    
                    echo "PATH in Jenkins environment is: $PATH"
                '''
            }
        }
        
        stage('Run Code Review in Docker') {
            steps {
                // Use triple-quoted string so we can easily quote the mount path
                sh """
                    echo "Pulling Python 3.9 Docker image..."
                    docker pull python:3.9
                    
                    echo "Running Docker container to execute review script..."
                    docker run --rm \\
                        -v "\$WORKSPACE:/workspace" \\
                        -w /workspace \\
                        -e OPENAI_API_KEY=\$OPENAI_API_KEY \\
                        -e GITHUB_TOKEN=\$GITHUB_TOKEN \\
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

