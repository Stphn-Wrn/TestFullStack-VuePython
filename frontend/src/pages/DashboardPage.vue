<template>
  <v-container>
    <v-app-bar color="primary" dense>
      <v-toolbar-title>Dashboard</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn variant="outlined" @click="openCampaignDialog">Create a campaign</v-btn>
    </v-app-bar>

    <v-row>
      <v-col cols="12" md="4" v-for="(campaign, index) in campaigns" :key="index">
        <v-card>
          <v-card-title>{{ campaign.name }}</v-card-title>
          <v-card-subtitle>{{ campaign.description }}</v-card-subtitle>
          <v-card-text>
            <p><strong>Start date:</strong> {{ campaign.startDate }}</p>
            <p><strong>End date:</strong> {{ campaign.endDate }}</p>
            <p><strong>Budget:</strong> {{ campaign.budget }}€</p>
            <p><strong>Status:</strong> <v-chip :color="campaign.status === 'Active' ? 'green' : 'red'">{{ campaign.status }}</v-chip></p>
          </v-card-text>
          <v-card-actions>
            <v-btn color="blue" @click="editCampaign(index)">Edit</v-btn>
            <v-btn color="red" @click="deleteCampaign(index)">Delete</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>{{ isEditing ? 'Edit campaign' : 'Create a campaign' }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="campaignData.name" label="Campaign name"></v-text-field>
          <v-textarea v-model="campaignData.description" label="Description"></v-textarea>
          <v-text-field v-model="campaignData.startDate" label="Start date" type="date"></v-text-field>
          <v-text-field v-model="campaignData.endDate" label="End date" type="date"></v-text-field>
          <v-text-field v-model="campaignData.budget" label="Budget" type="number"></v-text-field>
          <v-select v-model="campaignData.status" label="Status" :items="['Active', 'Inactive']"></v-select>
        </v-card-text>
        <v-card-actions>
          <v-btn color="grey" @click="dialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="saveCampaign">{{ isEditing ? 'Update' : 'Create' }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';

const campaigns = ref([
  { name: 'Campaign 1', description: 'Description 1', startDate: '2025-04-01', endDate: '2025-04-10', budget: 5000, status: 'Active' },
  { name: 'Campaign 2', description: 'Description 2', startDate: '2025-05-01', endDate: '2025-05-15', budget: 8000, status: 'Inactive' }
]);

const dialog = ref(false);
const isEditing = ref(false);
const campaignData = ref({ name: '', description: '', startDate: '', endDate: '', budget: '', status: 'Active' });
const editingIndex = ref(null);

const openCampaignDialog = () => {
  campaignData.value = { name: '', description: '', startDate: '', endDate: '', budget: '', status: 'Active' };
  isEditing.value = false;
  dialog.value = true;
};

const editCampaign = (index) => {
  campaignData.value = { ...campaigns.value[index] };
  editingIndex.value = index;
  isEditing.value = true;
  dialog.value = true;
};

const saveCampaign = () => {
  if (isEditing.value) {
    campaigns.value[editingIndex.value] = { ...campaignData.value };
  } else {
    campaigns.value.push({ ...campaignData.value });
  }
  dialog.value = false;
};

const deleteCampaign = (index) => {
  campaigns.value.splice(index, 1);
};
</script>

<style>
.v-container {
  padding-top: 20px;
  height:auto;
}
.secondary {
  
}
.v-card {
  transition: 0.3s;
}
.v-card:hover {
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
}
.v-row {
  margin-top: 64px;
}
.dashboard-content {
  padding-top: 64px;
  height: auto;
  display: flex;
  flex-direction: column;
}

.v-main {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}
</style>