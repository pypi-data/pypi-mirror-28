#!groovy

pipeline {
  agent any

  environment {
        GIT_NAME = "eea.testegg"
        GIT_ORG = "eea"
        GIT_VERSIONFILE = "eea/testegg/version.txt"
        GIT_HISTORYFILE = "docs/HISTORY.txt"
    }

  stages {
  stage('Pull request checks') {
           when {
                not {
                    environment name: 'CHANGE_ID', value: ''
                }
		          	 environment name: 'CHANGE_TARGET', value: 'master'
            }
     steps {
	      node(label: 'docker-1.13') {
             script {   
						  if ( env.CHANGE_BRANCH != "develop" &&  !( env.CHANGE_BRANCH.startsWith("hotfix")) ) {                       
		                  error "Pipeline aborted due to PR not made from develop or hotfix branch"
			               }      
			    		try {
			           sh '''docker run -i --name="$BUILD_TAG-gitflow-pr" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" -e GIT_ORG="$GIT_ORG" -e GIT_VERSIONFILE="$GIT_VERSIONFILE" -e GIT_HISTORYFILE="$GIT_HISTORYFILE" -e GIT_NAME="$GIT_NAME" eeacms/gitflow'''
		          	} finally {
			         sh '''docker rm -v $BUILD_TAG-gitflow-pr'''
			        }
		           }
		          }
          }	 
   }
	  
  stage('Master branch release and tag') {
      when {
                allOf {
                    environment name: 'CHANGE_ID', value: ''
                    branch 'master'
                }
            }
     steps {
            node(label: 'docker-1.13') {
		          withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'eea-jenkins',
                   usernameVariable: 'EGGREPO_USERNAME', passwordVariable: 'EGGREPO_PASSWORD'],string(credentialsId: 'eea-jenkins-token', variable: 'GITHUB_TOKEN'), [$class: 'UsernamePasswordMultiBinding', credentialsId: 'pypi-jenkins',
                   usernameVariable: 'PYPI_USERNAME', passwordVariable: 'PYPI_PASSWORD']]) {
                      script{
				                  try {
				                    sh '''docker run -i --name="$BUILD_TAG-gitflow-master" -e GIT_BRANCH="$BRANCH_NAME" -e EGGREPO_USERNAME="$EGGREPO_USERNAME" -e EGGREPO_PASSWORD="$EGGREPO_PASSWORD" -e GIT_NAME="$GIT_NAME" -e GIT_ORG="$GIT_ORG" -e GIT_TOKEN="$GITHUB_TOKEN" -e PYPI_USERNAME="$PYPI_USERNAME"  -e PYPI_PASSWORD="$PYPI_PASSWORD" eeacms/gitflow'''
		                  		} finally {
				                   sh '''docker rm -v $BUILD_TAG-gitflow-master'''
				                  }	    
		                      }
		               }
	              }
      }
   }
	  
  }  
  
}
