import { ref } from 'vue'
import { removeToken } from './tokenManagement'
const error = ref(null)
const isPending = ref(false)


const logout = async () => {
  error.value = null
  isPending.value = true
  try {
    removeToken();
    isPending.value = false
  } catch (err) {
    console.error(err.message)
    error.value = err.message
    isPending.value = false
  }
}

const useLogout = () => {
  return { error, logout, isPending }
}

export default useLogout
