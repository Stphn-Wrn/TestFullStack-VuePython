import { defineStore } from 'pinia'
import api from '@/api/campaigns'

export const useCampaignStore = defineStore('campaigns', {
  state: () => ({
    campaigns: [],
    loading: false
  }),
  actions: {
    async fetchCampaigns() {
      this.loading = true
      const { data } = await api.getAll()
      this.campaigns = data
      this.loading = false
    },
    async toggleCampaignStatus(id) {
      await api.toggleStatus(id)
      await this.fetchCampaigns()
    }
  }
})