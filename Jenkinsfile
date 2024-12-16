pipeline {
    agent {
        label 'ubuntu-latest'
    }
    environment {
        OPENAI_API_KEY = credentials('OPENAI_API_KEY') // Store API Key securely in Jenkins credentials
        GITHUB_TOKEN = credentials('GITHUB_TOKEN')     // Store GitHub token securely in Jenkins credentials
    }
    stages {
        stage('Checkout repository') {
            steps {
                // Use a plugin or script to check out the repository
                checkout scm
            }
        }
        stage('Set up Python environment') {
            steps {
                sh '''
                # Install or ensure Python 3.9 is available
                sudo apt-get update
                sudo apt-get install -y python3.9 python3.9-venv python3-pip

                # Create a virtual environment
                python3.9 -m venv venv
                source venv/bin/activate

                # Upgrade pip and install dependencies
                pip install --upgrade pip
                pip install openai PyGithub GitPython
                '''
            }
        }
        stage('Run Code Review') {
            steps {
                sh '''
                # Activate the virtual environment
                source venv/bin/activate

                # Run the code review script
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

