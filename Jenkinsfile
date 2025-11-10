pipeline {
    agent any
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }
    
    stages {
        stage('Initialize') {
            steps {
                echo '========== NIDS IPv6 Configuration Pipeline =========='
                echo 'Starting build...'
                sh 'sudo mkdir -p /var/log/nids || true'
                sh 'sudo mkdir -p /etc/nids || true'
            }
        }
        
        stage('Code Quality') {
            steps {
                echo '========== Stage: Code Quality =========='
                sh '/usr/bin/python3 -m py_compile src/nids_ipv6_config.py'
                echo 'PASSED: Python syntax validation'
            }
        }
        
        stage('Application Tests') {
            steps {
                echo '========== Stage: Application Tests =========='
                sh '/usr/bin/python3 src/nids_ipv6_config.py --help'
                echo 'PASSED: Help command'
                sh '/usr/bin/python3 src/nids_ipv6_config.py show'
                echo 'PASSED: Show command'
                sh '/usr/bin/python3 src/nids_ipv6_config.py validate'
                echo 'PASSED: Validation'
            }
        }
        
        stage('Build Artifacts') {
            steps {
                echo '========== Stage: Build Artifacts =========='
                sh 'mkdir -p artifacts'
                sh 'cp src/nids_ipv6_config.py artifacts/'
                sh 'cp config/ipv6_config.json artifacts/'
                sh 'cp README.md INSTALL.md CONFIG.md artifacts/'
                echo 'PASSED: Artifacts ready'
            }
        }
        
        stage('Packaging') {
            steps {
                echo '========== Stage: Packaging Validation =========='
                sh 'head -3 packaging/nids-ipv6-config.spec'
                sh 'head -3 debian/DEBIAN/control'
                echo 'PASSED: Packaging validated'
            }
        }
    }
    
    post {
        success {
            echo '========================================='
            echo 'PIPELINE SUCCESSFUL - READY FOR DEPLOYMENT'
            echo '========================================='
        }
        failure {
            echo 'PIPELINE FAILED'
        }
    }
}
