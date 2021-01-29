import groovy.json.JsonSlurperClassic
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

    def dockerImage = "docker.custenborder.com/jcustenborder/jenkins-packer-ansible-python:0.0.1"

    stage('generate') {
        withDockerRegistry(credentialsId: 'custenborder_docker', url: 'https://docker.custenborder.com') {
            docker.image(dockerImage).inside() {
                sh "pip install -r requirements.txt"
                sh "python generator.py"
            }
        }
    }

    stage('push') {
        def workSpaceRoot = new File(pwd())
        def buildRoot = new File(workSpaceRoot, "build")
        def repositoriesFile = new File(buildRoot, "repositories.json")
        def repoRoot = new File(workSpaceRoot, "repos")

        sh "repositoriesFile = ${repositoriesFile}"
        sh "find ${workSpaceRoot}"
        sh "mkdir ${repoRoot}"

        def repositories = new JsonSlurperClassic().parse(repositoriesFile)

        repositories.each {
            def name = it['name']
            def imageDirectory = new File(repoRoot, name)
            sh "mkdir ${imageDirectory}"
            def path = it['path']
            def branchBuild = new File(workSpaceRoot, path)
            def branch = it['branch']
            def branchDirectory = new File(imageDirectory, branch)
            sh "mkdir ${branchDirectory}"
            def repositoryUrl = it['repository_url']
            sh "copy -rv ${branchBuild}/ ${branchDirectory}/"
        }




//        sh "mkdir build"
//        dir('build') {
//            git branch: 'master', changelog: false, credentialsId: '50a4ec3a-9caf-43d1-bfab-6465b47292da', poll: false, url: 'git@github.com:jcustenborder/kafka-connect-all.git'
//            sh 'git config user.email "jenkins@custenborder.com"'
//            sh 'git config user.name "Jenkins"'
//        }


    }

//    stage('push') {
//        dir('build') {
//            sh "echo `git add --all . && git commit -m 'Build ${BUILD_NUMBER}' .`"
//            sshagent(credentials: ['50a4ec3a-9caf-43d1-bfab-6465b47292da']) {
//                sh "git push 'git@github.com:jcustenborder/kafka-connect-all.git' master"
//            }
//        }
//    }
}
