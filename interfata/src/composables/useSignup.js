import { ref } from 'vue'
import axios from 'axios'
const error = ref(null)
const isPending = ref(false)

async function createUserWithUsernameAndPassword(username, password, displayName, dblp_profile, scholar_profile) {
  const url = 'http://localhost:5000/user';
  try {
    const response = await axios.post(url, {
      username,
      password,
      name: displayName,
      dblp_profile,
      scholar_profile
    })
    return response.data
  } catch (error) {
    console.error('Error during sign-up:', error)
    throw error
  }
}

const signup = async (username, password, displayName, dblpProfile, scholarProfile) => {
  error.value = null
  isPending.value = true

  try {
    const res = await createUserWithUsernameAndPassword(username, password, displayName, dblpProfile, scholarProfile)
    if (!res) {
      throw new Error('Could not complete signup')
    }
    // todo: change
    // await res.user.updateProfile({ displayName })
    error.value = null
    isPending.value = false
    return res
  } catch (err) {
    error.value =  err.message
    if(err.response.data?.errors){
      error.value = err.response.data?.errors
    }
    if(err.message === "Request failed with status code 409"){
      error.value = `${username} has been used before. Please try another username.`
    }
    isPending.value = false
  }
}

const useSignup = () => {
  return { error, signup }
}

export default useSignup
