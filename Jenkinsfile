pipeline {
    agent any

    environment {
        PATH = "/usr/local/bin:/usr/bin:/bin"
        OPENAI_API_KEY = credentials('OPENAI_API_KEY')
        GITHUB_TOKEN = credentials('GITHUB_TOKEN')
        GITHUB_REPO = "NeuralSentinel/SafetyArithmetic_BKUP"
    }

    stages {
        stage('Setup') {
            steps {
                script {
                    if (env.CHANGE_ID != null) {
                        // This is a pull request
                        echo "Building for PR: ${env.CHANGE_ID}"
                    }
                }
            }
        }
        
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Code Review in Docker') {
            when {
                expression { env.CHANGE_ID != null }
            }
            steps {
                sh """
                    docker run --rm \
                        -v "\$WORKSPACE:/workspace" \
                        -w /workspace \
                        -e OPENAI_API_KEY=\$OPENAI_API_KEY \
                        -e GITHUB_TOKEN=\$GITHUB_TOKEN \
                        -e GITHUB_REPO=\$GITHUB_REPO \
                        python:3.9 /bin/bash -c "
                            python -m pip install --upgrade pip
                            pip install openai PyGithub GitPython
                            python review_pr.py
                        "
                """
            }
        }

        stage('Other Tasks') {
            steps {
                echo "Running other tasks"
            }
        }
    }

    post {
        always {
            echo "Pipeline execution complete."
        }
        failure {
            echo "Pipeline failed."
        }
    }
}


// pipeline {
//     agent any

//     environment {
//         PATH = "/usr/local/bin:/usr/bin:/bin"
//         OPENAI_API_KEY = credentials('OPENAI_API_KEY')
//         GITHUB_TOKEN   = credentials('GITHUB_TOKEN')
//         GITHUB_REPO    = "NeuralSentinel/SafetyArithmetic_BKUP"
//     }

//     stages {
//         stage('Checkout') {
//             steps {
//                 checkout scm
//             }
//         }

//         stage('Run Code Review in Docker') {
//             steps {
//                 sh """
//                     docker run --rm \
//                         -v "\$WORKSPACE:/workspace" \
//                         -w /workspace \
//                         -e OPENAI_API_KEY=\$OPENAI_API_KEY \
//                         -e GITHUB_TOKEN=\$GITHUB_TOKEN \
//                         -e GITHUB_REPO=\$GITHUB_REPO \
//                         python:3.9 /bin/bash -c "
//                             python -m pip install --upgrade pip
//                             pip install openai PyGithub GitPython
//                             python review_pr.py
//                         "
//                 """
//             }
//         }
//     }

//     post {
//         always {
//             echo "Pipeline execution complete."
//         }
//         failure {
//             echo "Pipeline failed."
//         }
//     }
// }


// pipeline {
//     agent any

//     environment {
//         PATH = "/usr/local/bin:/usr/bin:/bin"
//         OPENAI_API_KEY = credentials('OPENAI_API_KEY')
//         GITHUB_TOKEN   = credentials('GITHUB_TOKEN')
//         GITHUB_REPO    = "NeuralSentinel/SafetyArithmetic_BKUP"
//     }

//     stages {
//         stage('Checkout') {
//             steps {
//                 checkout scm
//             }
//         }

//         stage('Run Code Review in Docker') {
//             steps {
//                 sh """
//                     docker run --rm \
//                         -v "\$WORKSPACE:/workspace" \
//                         -w /workspace \
//                         -e OPENAI_API_KEY=\$OPENAI_API_KEY \
//                         -e GITHUB_TOKEN=\$GITHUB_TOKEN \
//                         -e GITHUB_REPO=\$GITHUB_REPO \
//                         python:3.9 /bin/bash -c "
//                             python -m pip install --upgrade pip
//                             pip install openai PyGithub GitPython
//                             python review_pr.py
//                         "
//                 """
//             }
//         }
//     }

//     post {
//         always {
//             echo "Pipeline execution complete."
//         }
//         failure {
//             echo "Pipeline failed."
//         }
//     }
// }







//tes

// pipeline {
//     agent any

//     environment {
//         // Explicit PATH setup (if needed)
//         PATH = "/usr/local/bin:/usr/bin:/bin"

//         // Jenkins credentials
//         OPENAI_API_KEY = credentials('OPENAI_API_KEY')
//         GITHUB_TOKEN   = credentials('GITHUB_TOKEN')

//         // Additional environment vars (edit as needed)
//         GITHUB_REPO = "NeuralSentinel/SafetyArithmetic_BKUP"  // e.g. "octocat/Hello-World"
//         CHANGE_ID   = "123"               // PR number
//     }

//     stages {
//         stage('Checkout') {
//             steps {
//                 // Pull the Jenkinsfile's own repo code which includes review.py
//                 checkout scm
//             }
//         }

//         stage('List Files') {
//             steps {
//                 sh 'ls -la'
//             }
//         }

//         stage('Prepare Environment') {
//             steps {
//                 sh '''
//                     echo "Verifying Docker is installed..."
//                     which docker || echo "Docker not found!"
//                     docker --version || true

//                     echo "PATH in Jenkins environment is: $PATH"
//                 '''
//             }
//         }

//         stage('Run Code Review in Docker') {
//             steps {
//                 sh """
//                     echo "Pulling Python 3.9 Docker image..."
//                     docker pull python:3.9

//                     echo "Running Docker container to execute review script..."
//                     docker run --rm \\
//                         -v "\$WORKSPACE:/workspace" \\
//                         -w /workspace \\
//                         -e OPENAI_API_KEY=\$OPENAI_API_KEY \\
//                         -e GITHUB_TOKEN=\$GITHUB_TOKEN \\
//                         -e GITHUB_REPO=\$GITHUB_REPO \\
//                         -e CHANGE_ID=\$CHANGE_ID \\
//                         python:3.9 /bin/bash -c "
//                             python -m pip install --upgrade pip
//                             pip install openai PyGithub GitPython
//                             python review_pr.py
//                         "
//                 """
//             }
//         }
//     }
// }



// pipeline {
//     agent any
//     environment {
//         PATH            = "/usr/local/bin:/usr/bin:/bin"
//         OPENAI_API_KEY  = credentials('OPENAI_API_KEY')
//         GITHUB_TOKEN    = credentials('GITHUB_TOKEN')
//     }
//     stages {
//         stage('Checkout') {
//             steps {
//                 checkout scm
//             }
//         }
//         stage('List Files') {
//             steps {
//                 // Confirm review.py is at the root of this workspace
//                 sh 'ls -la'
//             }
//         }
//         stage('Run Code Review in Docker') {
//             steps {
//                 sh """
//                     docker pull python:3.9
//                     docker run --rm \\
//                         -v "\$WORKSPACE:/workspace" \\
//                         -w /workspace \\
//                         -e OPENAI_API_KEY=\$OPENAI_API_KEY \\
//                         -e GITHUB_TOKEN=\$GITHUB_TOKEN \\
//                         python:3.9 /bin/bash -c "
//                             python -m pip install --upgrade pip
//                             pip install openai PyGithub GitPython
//                             python review_pr.py
//                         "
//                 """
//             }
//         }
//     }
// }













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

