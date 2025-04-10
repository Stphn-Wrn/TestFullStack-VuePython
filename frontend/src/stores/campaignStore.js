// src/stores/campaignStore.js
import { defineStore } from 'pinia';
import apiClient from '@/api/client';

export const useCampaignStore = defineStore('campaign', {
  state: () => ({
    campaigns: [],
    isLoading: false,
    error: null,
  }),

  actions: {
    async fetchCampaigns() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.get('/campaigns/all');
        this.campaigns = response.data.data;
      } catch (error) {
        this.error = 'Failed to fetch campaigns.';
      } finally {
        this.isLoading = false;
      }
    },
    async createCampaign(campaignData) {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.post('/campaigns/', campaignData);
        console.log('Created campaign:', response.data);
        this.campaigns.push(response.data.data);
      } catch (error) {
        console.error('Create campaign failed:', error);
        if (error.response) {
          console.error(
            'Server responded with:',
            error.response.status,
            error.response.data,
          );
        }
        this.error = 'Failed to create campaign.';
      } finally {
        this.isLoading = false;
      }
    },

    async updateCampaign(campaignId, campaignData) {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.patch(
          `/campaigns/${campaignId}`,
          campaignData,
        );

        if (response.data.message === 'No fields to update') {
          return { updated: false, message: response.data.message };
        }

        const index = this.campaigns.findIndex(
          (campaign) => campaign.id === campaignId,
        );
        if (index !== -1) {
          this.campaigns[index] = response.data.data;
        }

        return { updated: true, message: 'Campaign updated successfully' };
      } catch (error) {
        this.error = 'Failed to update campaign.';
        return { updated: false, error: this.error };
      } finally {
        this.isLoading = false;
      }
    },

    async deleteCampaign(campaignId) {
      this.isLoading = true;
      this.error = null;
      try {
        await apiClient.delete(`/campaigns/${campaignId}`);
        this.campaigns = this.campaigns.filter(
          (campaign) => campaign.id !== campaignId,
        ); // Retirer la campagne supprimée de la liste
      } catch (error) {
        this.error = 'Failed to delete campaign.';
      } finally {
        this.isLoading = false;
      }
    },
  },

  getters: {
    // 1. Vérifier si l'utilisateur a des campagnes
    hasCampaigns: (state) => state.campaigns.length > 0,
  },
});
