properties([
        buildDiscarder(logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '', numToKeepStr: '10'))
])

//triggers {
//    upstream(upstreamProjects: "jcustenborder/connect-utils/job/master", threshold: hudson.model.Result.SUCCESS)
//}

node {
    stage('checkout') {
        deleteDir()
        checkout scm
    }

    def dockerImage = "docker.custenborder.com/jcustenborder/jenkins-packer-ansible-python/manifests/0.0.1"

    stage('generate') {
        withDockerRegistry(credentialsId: 'custenborder_docker', url: 'https://docker.custenborder.com') {
            docker.image(dockerImage).inside() {
                sh "pip install -r requirements.txt"
                sh "python generator.py"
            }
        }
    }

    stage('push') {
        dir('build') {
            git branch: 'master', changelog: false, credentialsId: '50a4ec3a-9caf-43d1-bfab-6465b47292da', poll: false, url: 'git@github.com:jcustenborder/kafka-connect-all.git'
            sh 'git config user.email "jenkins@custenborder.com"'
            sh 'git config user.name "Jenkins"'
            sh "echo `git add --all . && git commit -m 'Build ${BUILD_NUMBER}' .`"
            sshagent(credentials: ['50a4ec3a-9caf-43d1-bfab-6465b47292da']) {
                sh "git push 'git@github.com:jcustenborder/kafka-connect-all.git' master"
            }
        }
    }
}
