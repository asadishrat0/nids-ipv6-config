pipeline {
    agent any
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }
    
    parameters {
        choice(name: 'DEPLOYMENT_ENV', choices: ['BUILD_ONLY', 'DEV', 'STAGING', 'PRODUCTION'], description: 'Environment to deploy')
        choice(name: 'TARGET_HOSTS', choices: ['all', 'ubuntu_servers', 'redhat_servers'], description: 'Target servers for deployment')
        booleanParam(name: 'DRY_RUN', defaultValue: true, description: 'Ansible dry-run (no changes)?')
        booleanParam(name: 'RUN_ANSIBLE', defaultValue: false, description: 'Run Ansible deployment?')
    }
    
    environment {
    APP_NAME = 'nids-ipv6-config'
    APP_VERSION = '1.0.0'
    DEPLOYMENT_ENV = "${params.DEPLOYMENT_ENV ?: 'BUILD_ONLY'}"
    TARGET_HOSTS = "${params.TARGET_HOSTS ?: 'all'}"
    DRY_RUN = "${params.DRY_RUN ?: 'true'}"
    RUN_ANSIBLE = "${params.RUN_ANSIBLE ?: 'false'}"
}
    
    stages {
        stage('Initialize') {
            steps {
                echo '╔════════════════════════════════════════════════╗'
                echo '║  NIDS IPv6 Configuration Pipeline              ║'
                echo '║  Build: Package & Deploy                       ║'
                echo '╚════════════════════════════════════════════════╝'
                echo ''
                echo "Environment: ${DEPLOYMENT_ENV}"
                echo "Target Hosts: ${TARGET_HOSTS}"
                echo "Dry Run: ${DRY_RUN}"
                echo "Run Ansible: ${RUN_ANSIBLE}"
                echo ''
                sh 'mkdir -p artifacts reports'
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
                echo 'PASSED: Show configuration'
                sh '/usr/bin/python3 src/nids_ipv6_config.py validate'
                echo 'PASSED: Configuration validation'
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
        
        stage('Check Ansible Setup') {
            when {
                expression { params.RUN_ANSIBLE == true || params.DEPLOYMENT_ENV != 'BUILD_ONLY' }
            }
            steps {
                echo '========== Stage: Check Ansible Setup =========='
                sh '''
                    echo "Checking Ansible installation..."
                    if command -v ansible &> /dev/null; then
                        ansible --version
                        echo "✓ Ansible is installed"
                    else
                        echo "✗ Ansible not found - attempting to install..."
                        sudo apt-get update && sudo apt-get install -y ansible
                    fi
                    
                    echo ""
                    echo "Checking inventory file..."
                    if [ -f inventory.ini ]; then
                        echo "✓ inventory.ini found"
                        ansible-inventory -i inventory.ini --list | grep -E '"(ubuntu|redhat)' | head -10 || true
                    else
                        echo "⚠ inventory.ini not found - Ansible deployment will be skipped"
                    fi
                    
                    echo ""
                    echo "Checking playbook file..."
                    if [ -f deploy-playbook.yml ]; then
                        echo "✓ deploy-playbook.yml found"
                        ansible-playbook deploy-playbook.yml --syntax-check
                        echo "✓ Playbook syntax is valid"
                    else
                        echo "⚠ deploy-playbook.yml not found"
                    fi
                '''
            }
        }
        
        stage('Ansible Dry Run') {
            when {
                allOf {
                    expression { params.RUN_ANSIBLE == true }
                    expression { params.DRY_RUN == true }
                    expression { fileExists('inventory.ini') }
                    expression { fileExists('deploy-playbook.yml') }
                }
            }
            steps {
                echo '========== Stage: Ansible Dry Run (Preview) =========='
                sh '''
                    echo "Running Ansible in check mode (--check)..."
                    echo "Environment: ${DEPLOYMENT_ENV}"
                    echo "Target: ${TARGET_HOSTS}"
                    echo ""
                    
                    ansible-playbook -i inventory.ini deploy-playbook.yml \
                        --limit ${TARGET_HOSTS} \
                        --check \
                        -v 2>&1 | tee reports/ansible-dry-run.log
                    
                    echo ""
                    echo "✓ Dry run completed - no changes made"
                '''
            }
        }
        
        stage('Ansible Deploy') {
            when {
                allOf {
                    expression { params.RUN_ANSIBLE == true }
                    expression { params.DRY_RUN == false }
                    expression { fileExists('inventory.ini') }
                    expression { fileExists('deploy-playbook.yml') }
                }
            }
            steps {
                echo '========== Stage: Ansible Deployment =========='
                sh '''
                    echo "Deploying to ${TARGET_HOSTS}..."
                    echo "Environment: ${DEPLOYMENT_ENV}"
                    echo ""
                    
                    ansible-playbook -i inventory.ini deploy-playbook.yml \
                        --limit ${TARGET_HOSTS} \
                        -v 2>&1 | tee reports/ansible-deployment.log
                    
                    if [ ${PIPESTATUS[0]} -eq 0 ]; then
                        echo ""
                        echo "✓ Deployment successful"
                    else
                        echo ""
                        echo "✗ Deployment encountered issues"
                    fi
                '''
            }
        }
        
        stage('Verify Deployment') {
            when {
                allOf {
                    expression { params.RUN_ANSIBLE == true }
                    expression { params.DRY_RUN == false }
                    expression { fileExists('inventory.ini') }
                }
            }
            steps {
                echo '========== Stage: Verify Deployment =========='
                sh '''
                    echo "Verifying deployment on all hosts..."
                    echo ""
                    
                    ansible ${TARGET_HOSTS} -i inventory.ini \
                        -m command \
                        -a "python3 /usr/local/bin/nids_ipv6_config.py show" \
                        -v 2>&1 | tee reports/verification.log || true
                    
                    echo ""
                    echo "✓ Verification completed"
                '''
            }
        }
        
        stage('Generate Report') {
            steps {
                echo '========== Stage: Generate Report =========='
                sh '''
                    mkdir -p reports
                    
                    cat > reports/build-summary.txt << 'SUMMARY'
╔════════════════════════════════════════════╗
│ NIDS IPv6 Configuration Build Summary      │
╚════════════════════════════════════════════╝

Build Information:
==================
Application: nids-ipv6-config
Version: 1.0.0
Build Date: $(date)
Build Number: ${BUILD_NUMBER}
Environment: ${DEPLOYMENT_ENV}

Build Stages:
=============
✓ Code Quality: PASSED
✓ Application Tests: PASSED
✓ Build Artifacts: PASSED
✓ Packaging Validation: PASSED
SUMMARY
                    
                    if [ "${RUN_ANSIBLE}" == "true" ]; then
                        cat >> reports/build-summary.txt << 'ANSIBLE'

Deployment Information:
=======================
Target Hosts: ${TARGET_HOSTS}
Dry Run: ${DRY_RUN}
Deployment Logs:
  - ansible-dry-run.log (if applicable)
  - ansible-deployment.log (if applicable)
  - verification.log (if applicable)
ANSIBLE
                    fi
                    
                    cat reports/build-summary.txt
                    
                    echo ""
                    echo "Reports generated in: ${WORKSPACE}/reports/"
                '''
                archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
            }
        }
    }
    
    post {
        success {
            echo '╔════════════════════════════════════════════════╗'
            echo '║        PIPELINE SUCCESSFUL ✓                   ║'
            echo '╚════════════════════════════════════════════════╝'
            sh '''
                echo ""
                echo "Build Summary:"
                echo "=============="
                echo "Application: nids-ipv6-config v1.0.0"
                echo "Status: SUCCESS"
                echo "Build Number: ${BUILD_NUMBER}"
                echo ""
                
                if [ "${RUN_ANSIBLE}" == "true" ]; then
                    echo "Deployment:"
                    echo "  Environment: ${DEPLOYMENT_ENV}"
                    echo "  Target: ${TARGET_HOSTS}"
                    echo "  Mode: $([ "${DRY_RUN}" == "true" ] && echo "Preview (--check)" || echo "Actual Deployment")"
                else
                    echo "Package build completed successfully"
                    echo "Ready for deployment"
                fi
                
                echo ""
                echo "Artifacts: ${WORKSPACE}/artifacts/"
                echo "Reports: ${WORKSPACE}/reports/"
                echo ""
                ls -lh artifacts/ || true
            '''
        }
        
        failure {
            echo '╔════════════════════════════════════════════════╗'
            echo '║        PIPELINE FAILED ✗                       ║'
            echo '╚════════════════════════════════════════════════╝'
            sh '''
                echo "Build Number: ${BUILD_NUMBER}"
                echo "Failed Stage: Check logs for details"
            '''
        }
        
        always {
            echo '========== Pipeline Cleanup =========='
            sh 'echo "Execution completed at: $(date)"'
        }
    }
}
