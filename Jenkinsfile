node {
  checkout scm
  switch(env.BRANCH_NAME) {
    case "develop":
      build job: 'staging', parameters: [[$class: 'StringParameterValue', name: 'BRANCH_NAME', value: "${env.BRANCH_NAME}"]]
    break
    
    default:
    break
  }
}