import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
})

export default {
  getAll() {
    return api.get('/campaigns')
  },
  create(data) {
    return api.post('/campaigns', data)
  },
  toggleStatus(id) {
    return api.patch(`/campaigns/${id}/toggle`)
  }
}