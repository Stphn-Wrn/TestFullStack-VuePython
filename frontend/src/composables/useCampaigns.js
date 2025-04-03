import { ref } from 'vue'
import { useCampaignStore } from '@/stores/campaignStore'

export default function useCampaigns() {
  const store = useCampaignStore()
  const error = ref(null)
  
  const fetchCampaigns = async () => {
    try {
      await store.fetchCampaigns()
    } catch (err) {
      error.value = err.response?.data?.message || 'Erreur serveur'
    }
  }

  const toggleStatus = async (id) => {
    try {
      await store.toggleCampaignStatus(id)
    } catch (err) {
      error.value = 'Échec du changement de statut'
    }
  }

  return { 
    campaigns: store.campaigns,
    loading: store.loading,
    error,
    fetchCampaigns,
    toggleStatus
  }
}