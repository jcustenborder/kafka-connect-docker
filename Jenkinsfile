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

        def repositories = readJSON file: "build/repositories.json"
        sshagent(credentials: ['50a4ec3a-9caf-43d1-bfab-6465b47292da']) {
            repositories.each {
                def name = it['name']
                def imageDirectory = new File(repoRoot, name)
                def path = it['path']
                def branchBuild = new File(workSpaceRoot, path)
                def branch = it['branch']
                def branchDirectory = new File(imageDirectory, branch)
                def repositoryUrl = it['repository_url']
                sh "mkdir -p ${branchDirectory}"

                sh "echo processing ${name} - ${branch}"
                dir("${branchDirectory}") {
                    git branch: branch, changelog: false, credentialsId: '50a4ec3a-9caf-43d1-bfab-6465b47292da', poll: false, url: repositoryUrl
                    sh 'git config user.email "jenkins@custenborder.com"'
                    sh 'git config user.name "Jenkins"'
                    sh "cp -rv ${branchBuild}/* ."
                    sh "echo `git add --all . && git commit -m 'Build ${BUILD_NUMBER}' .`"
                    sh "git push '${repositoryUrl}' '${branch}'"
                }
            }
        }
    }
}
